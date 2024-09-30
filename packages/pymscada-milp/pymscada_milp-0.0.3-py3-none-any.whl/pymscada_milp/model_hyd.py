"""An hydraulic LP modelling object."""
import bisect
from enum import Enum
import logging
import time
from pathlib import Path
import shutil
from yaml import dump
from pymscada_milp import LpModel
from pymscada_milp import interp, interp_step, tod_to_xs_ys, bid_period, day_seconds


class State(Enum):
    OFF = 0
    FIXED = 1
    FREE = 2


class TimeSeries():
    """Time series data structure for model."""

    time = 0

    def __init__(self, time_series: float|list[list[int, int|float]] = None
                 ) -> None:
        self._value = None
        self.series: dict[int, list[int|float]] = {}
        if time_series is not None:
            if type(time_series) == float:
                self.set([[0, time_series]])
            else:
                self.set(time_series)

    @property
    def value(self) -> float:
        if self._value is None:
            raise ValueError(f'{self.name} TimeSeries value is None.')
        return self._value

    @value.setter
    def value(self, new_value: float) -> None:
        self._value = new_value
        self.series[TimeSeries.time] = new_value

    def get(self, time: int) -> float:
        if not self.series:
            raise ValueError(f'{self.name} TimeSeries has no values.')
        series_times = sorted(self.series.keys())
        index = bisect.bisect_right(series_times, time) - 1
        if index < 0:
            return self.series[series_times[0]]
        return self.series[series_times[index]]

    def set(self, time_series: list[list[int, int|float]]) -> None:
        """Set a list of [time_us, value] pairs."""
        self.series.update(time_series)

    def times(self):
        return sorted(self.series.keys())

    def values(self):
        values = []
        for t in sorted(self.series.keys()):
            values.append(self.series[t])
        return values


class HydraulicModel():
    """
    MILP Solver for hydraulic / generation scheduling.

    add_element      for adding hydraulic components to the model
     - valve        either as free or to follow a measured flow
     - river        adds a flow delay line
     - summing      sums flows at a node, must flow into one river
     - storage      reservoirs
     - generator    either as free or to follow fixed output
     - cost         simple cost
     - bid_offer    fixed for a period then free
     - revenue      value of generation WRT time of day
     - profile      lake target WRT time of day
     - outage       mode changes for generators
    """

    def __init__(self, config, timeout=30):
        """MILP Solver."""
        self.name = config['name']
        self.time_step = config['time_step']
        self.duration = config['duration']
        self.actual_time = config['actual_time']
        self.model: dict[str, Constraint] = {}
        tmpdir = Path(config['tempdir'])
        if not tmpdir.exists():
            raise NotADirectoryError(tmpdir.absolute())
        self.path = Path(config['tempdir'], '__mpc')
        self.logpath = None
        if 'logdir' in config:
            self.logpath = Path(config['logdir'])
        self.timeout = timeout
        self.lp = None
        self.costs = []
        self.start_time = None
        self.end_time = None
        self.times = None
        for e in config['model']:
            self._add_element(e, config['model'][e])
        for e in self.model.values():
            e.link(self)

    def set_actual_time(self, actual_time):
        self.actual_time = actual_time

    def remove_result(self):
        """Clean the working directory of result files."""
        self.lp.remove_result()

    def save_state(self):
        """Save working state."""
        snap = {
            "at": {
                "start_time": self.start_time,
                "actual_time": self.actual_time,
                "set_time": self.set_time,
                "end_time": self.end_time
            },
            "model": self.model,
            # "modelhistory": self.history,
            "resultsdict": self.lp.resultsdict,
            "resultsraw": self.lp.results
        }
        fh = open(self.path.parent / f"{self.path.name}.yaml", 'w')
        dump(snap, fh)
        fh.close()

    def capture_result(self):
        """Save the solver files for postmortem analysis."""
        now = time.localtime()
        snaptime = f"{now.tm_year:04d}{now.tm_mon:02d}{now.tm_mday:02d}_" \
            f"{now.tm_hour:02d}{now.tm_min:02d}{now.tm_sec:02d}"
        if self.logpath is None or not self.logpath.exists() or\
                not self.logpath.is_dir():
            return
        for f in [
            self.path.parent / f"{self.path.name}.rows_cols",
            self.path.parent / f"{self.path.name}.debug",
            self.path.parent / f"{self.path.name}.lp",
            self.path.parent / f"{self.path.name}.yaml",
            self.path.parent / f"{self.path.name}.output",
            self.path.parent / f"{self.path.name}.param"
        ]:
            try:
                shutil.copy(f, self.logpath / f"{snaptime}{f.name}")
                # f.rename(self.logpath / f"{snaptime}{f.name}")
                # shutil.move(f, f"log/{snaptime}_{f}")
            except OSError:
                logging.warning(f"could not move {f} to log")

    def _add_element(self, name: str, e: dict):
        """Configure a model node to be a particular type."""
        if e['type'] == 'valve':
            self.model[name] = Valve(name=name, **e)
        elif e['type'] == 'summing':
            self.model[name] = Summing(name=name, **e)
        elif e['type'] == 'storage':
            self.model[name] = Storage(name=name, **e)
        elif e['type'] == 'river':
            self.model[name] = River(name=name, **e)
        elif e['type'] == 'generator':
            self.model[name] = Generator(name=name, **e)
        elif e['type'] == 'cost':
            self.model[name] = Cost(name=name, **e)
        elif e['type'] == 'consent':
            self.model[name] = Consent(name=name, **e)
        elif e['type'] == 'bid_offer':
            self.model[name] = BidOffer(name=name, **e)
        elif e['type'] == 'relation':
            self.model[name] = Relation(name=name, **e)
        elif e['type'] == 'delta_cost':
            self.model[name] = DeltaCost(name=name, **e)
        elif e['type'] == 'change_cost':
            self.model[name] = ChangeCost(name=name, **e)
        elif e['type'] == 'step_cost':
            self.model[name] = StepCost(name=name, **e)
        elif e['type'] == 'revenue':
            self.model[name] = RevenueProfile(name=name, **e)
        elif e['type'] == 'profile':
            self.model[name] = StorageProfile(name=name, **e)
        elif e['type'] == 'limit_profile':
            self.model[name] = LimitProfile(name=name, **e)
        elif e['type'] == 'match':
            self.model[name] = Match(name=name, **e)
        elif e['type'] == 'time_profile':
            self.model[name] = TimeProfile(name=name, **e)
        elif e['type'] == 'add':
            self.model[name] = Add(name=name, **e)
        else:
            logging.critical(f"{name} type {e['type']} does not exist")

    #   @profile()
    def solve_lp(self):
        """
        Make and solve the MILP.

        model must already be defined, this makes the LP for a given
        time period. Default actual_time is the system time.time()
        minimum is time_step=1 (but keep at 600) and duration=1
        """
        # calculate the times
        # start_time
        # +   actual_time
        # +   |set_time
        # +   ||       +            + end_time
        # +   ||       +            +
        self.start_time = self.actual_time - self.actual_time % self.time_step
        if self.duration > 1:
            if self.actual_time == self.start_time:
                self.actual_time += 1  # just shift out of the way
            elif self.actual_time == self.start_time + self.time_step - 1:
                self.actual_time -= 1  # doesn't matter if off by 10-20 seconds
        self.set_time = self.actual_time + 1
        self.end_time = self.start_time + self.duration
        if self.end_time < self.set_time:
            self.end_time = self.set_time
        # collect a set of times for using in modelling
        time_set = set()
        for t in range(self.start_time, self.end_time, self.time_step):
            time_set.add(t)
        time_set.add(self.actual_time)
        time_set.add(self.set_time)
        time_set.add(self.end_time)
        self.times = sorted(time_set)
        # Build the model
        self.lp = LpModel(
            f"{self.name} {self.actual_time}",
            filename=self.path,
            timeout=self.timeout
        )
        for e in self.model:
            self.model[e]._create_lp(self)
        logging.info("MILP add costs")
        if len(self.costs) == 0:
            logging.warning('MILP has no costs - not running')
            return
        self.lp.add_row(self.costs, 'N')
        self.costs = []  # memory leak otherwise, TO DO look for more
        logging.info(f"Actual time:{self.actual_time} MILP write MPS")
        self.lp.write_mps()
        self.lp.solve_mps()
        for e in self.model:
            self.model[e]._post_process(self)
        self.lp.parse_mps()
        self.save_state()

    def add_cost(self, name):
        """
        Add a cost to the MILP.

        tuple of multiplier, cost or just cost.
        """
        if type(name) == tuple:
            if name[0] is None:
                print('oops')
            self.costs.append(name[0])
            self.costs.append(name[1])
        else:
            self.costs.append(name)


class Constraint():
    """
    Base class for hydraulic nodes.

    Provides a consistent way of addressing source and destination nodes,
    handling flows and providing standard names to make cross-connecting
    limits more likely to succeed.
    """

    __slots__ = ['name', 'type', 'time_series', 'srcnode', 'dstnode',
                 'inflows', 'outflows', 'elements', 'costs', 'min', 'max',
                 'setpoint', 'lowcost', 'highcost', 'ranges', 'runningcost',
                 'history']

    def __init__(self, **kwargs):
        """Constraint init."""
        self.name: str = None
        self.type: str = None
        self.time_series: TimeSeries = None
        self.srcnode = None
        self.dstnode = None
        self.inflows = []
        self.outflows = []
        self.elements = []
        self.costs = None
        self.min = None
        self.max = None
        self.setpoint = None
        self.lowcost = None
        self.highcost = None
        self.ranges = []  # permitted operating ranges
        self.runningcost = None
        self.history: TimeSeries = None
        for k in kwargs:
            if hasattr(self, k):
                setattr(self, k, kwargs[k])
            else:
                logging.critical(f"Node {self.name} has no {k}")

    def link(self, m: HydraulicModel):
        """Make source / destination connections between nodes."""
        if self.srcnode is not None:
            m.model[self.srcnode].outflows.append(self.name)
        if self.dstnode is not None:
            m.model[self.dstnode].inflows.append(self.name)

    def _create_lp(self, m: HydraulicModel):
        logging.error('Must have custom LP building routine')

    def _post_process(self, m: HydraulicModel):
        if self.time_series is None:
            return
        for t in m.times:
            if self._default_name(t) in m.lp.results:
                value = m.lp.results[self._default_name(t)]
                self.time_series.set([[t, value]])

    def _add_limit_costs(self, m: HydraulicModel, t: int):
        if self.costs is not None:
            cost = self._cost_name(t)
            xs = self.costs[0]  # [self._volume(wl) for wl in self.costs[0]]
            ys = self.costs[1]
            m.add_cost(cost)
            m.lp.add_sos2_disc(self._default_name(t), xs, cost, ys)
        if len(self.elements) == 0:
            elements = [self._default_name(t)]
        else:
            elements = [m.model[e]._default_name(t) for e in self.elements]
        if self.min is not None:
            m.lp.add_row(elements, 'G', self.min)
        if self.max is not None:
            m.lp.add_row(elements, 'L', self.max)
        if self.lowcost is not None:
            if self.setpoint is None:
                raise SystemExit(f"{self.name} lowcost must have setpoint")
            cost = self._pos_cost_name(t)
            m.add_cost((self.lowcost, cost))
            m.lp.add_row(elements, cost, 'G', self.setpoint)
        if self.highcost is not None:
            if self.setpoint is None:
                raise SystemExit(f"{self.name} highcost must have setpoint")
            cost = self._neg_cost_name(t)
            m.add_cost((self.highcost, cost))
            m.lp.add_row(elements, -1, cost, 'L', self.setpoint)

    def _add_ranges(self, m: HydraulicModel, t: int):
        # A single range is just a simple min / max
        if len(self.ranges) == 1:
            m.lp.add_row(self._default_name(t), 'G', self.ranges[0][0])
            m.lp.add_row(self._default_name(t), 'L', self.ranges[0][1])
        # Two ranges are semi-continuous
        elif len(self.ranges) == 2:
            if len(self.ranges[0]) == 1:
                m.lp.add_semi(self._default_name(t), self.ranges[1][0],
                              self.ranges[1][1], self._running_bv_name(t))
                if self.runningcost is not None:
                    m.add_cost((self.runningcost, self._running_bv_name(t)))
            else:
                logging.warning(f"NOT IMPLEMENTED range {self.name}")

    def _range_conform(self, value):
        """Make values conform to a range, avoids solves going infeasible."""
        r = self.ranges
        if len(r[0]) == 1:
            if value < r[1][0] / 2:
                return 0.0
            elif value < r[1][0]:
                return r[1][0]
            elif value < r[1][1]:
                return value
            else:  # value must be > ranges[1][1]
                if len(r) == 2:  # no additional range
                    return r[1][1]
                elif len(r) == 3:
                    if value < (r[2][0] - r[1][1]) / 2 + r[1][1]:
                        return r[1][1]
                    elif value < r[2][0]:
                        return r[2][0]
                    elif value < r[2][1]:
                        return value
                    else:  # must be higher
                        return r[2][1]
        elif len(r[0]) == 2:
            if value < r[0][0]:
                return r[0][0]
            elif value < r[0][1]:
                return value
            else:
                if len(r) == 1:  # no additional range
                    return r[0][1]
                elif len(r) == 2:
                    if value < (r[1][0] - r[0][1]) / 2 + r[0][1]:
                        return r[0][1]
                    elif value < r[1][0]:
                        return r[1][0]
                    elif value < r[1][1]:
                        return value
                    else:  # must be higher
                        return r[1][1]

    def _default_name(self, time):
        return f"{self.name}__DEFAULT__{time}"

    def _running_bv_name(self, time):
        return f"{self.name}__Running_BV__{time}"

    def _off_bv_name(self, time):
        return f"{self.name}__Off_BV__{time}"

    def _flow_name(self, time):
        return f"{self.name}__Flow__{time}"

    def _flow_bv_name(self, time):
        return f"{self.name}__Flow_BV__{time}"

    def _inflow_name(self, time):
        return f"{self.name}__Flow_in__{time}"

    def _outflow_name(self, time):
        return f"{self.name}__Flow_out__{time}"

    def _power_name(self, time):
        return f"{self.name}__Power__{time}"

    def _volume_name(self, time):
        return f"{self.name}__Volume__{time}"

    def _level_name(self, time):
        return f"{self.name}__Level__{time}"

    def _cost_name(self, time):
        return f"{self.name}__Cost__{time}"

    def _pos_cost_name(self, time):
        return f"{self.name}__Cost_pos__{time}"

    def _neg_cost_name(self, time):
        return f"{self.name}__Cost_neg__{time}"

    def _pos_limit_name(self, time):
        return f"{self.name}__Limit_pos__{time}"

    def _neg_limit_name(self, time):
        return f"{self.name}__Limit_neg__{time}"

    def _pos_lake_profile_name(self, time):
        return f"{self.name}__Profile_pos__{time}"

    def _neg_lake_profile_name(self, time):
        return f"{self.name}__Profile_neg__{time}"

    def _pos_power_delta_name(self, time):
        return f"{self.name}__PowerDelta_pos__{time}"

    def _neg_power_delta_name(self, time):
        return f"{self.name}__PowerDelta_neg__{time}"

    def _pos_power_chg_name(self, time):
        return f"{self.name}__PowerChg_pos__{time}"

    def _neg_power_chg_name(self, time):
        return f"{self.name}__PowerChg_neg__{time}"

    def _pos_slack_name(self, time):
        return f"{self.name}__SLACK_pos__{time}"

    def _neg_slack_name(self, time):
        return f"{self.name}__SLACK_neg__{time}"


class Summing(Constraint):
    """
    Enforce equality on nodes at a junction.

    Note that negative flows in history can cause infeasibility
    There *MUST* be one River in the outflows
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.inflows = []
        self.outflows = []
        self.slack = False
        super().__init__(**kwargs)
        pass

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            flows = []
            for flow in self.inflows:
                if m.model[flow].type == 'river':
                    flows.append(m.model[flow]._outflow_name(t))
                else:
                    flows.append(m.model[flow]._flow_name(t))
            for flow in self.outflows:
                if m.model[flow].type == 'river':
                    flows.append(-1.0)
                    flows.append(m.model[flow]._inflow_name(t))
                else:
                    flows.append(-1.0)
                    flows.append(m.model[flow]._flow_name(t))
            # if self.slack:
            #     s1 = self._neg_slack_name(t)
            #     s2 = self._pos_slack_name(t)
            #     m.lp.add_row(flows, s1, -1, s2, 'E', 0.0)
            #     m.add_cost((1e10, s1))
            #     m.add_cost((1e10, s2))
            # else:
            m.lp.add_row(flows, 'E', 0.0)


class Storage(Constraint):
    """
    Accumulates the inflow differences into a volume.

    River outflow is not permitted.
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.inflows = []
        self.outflows = []
        self._vol = 0
        self.LV = None
        super().__init__(**kwargs)
        if self.time_series is None:
            raise f'{self.name} must have a level time_series.'
        self.LV_xs = [x[0] for x in self.LV]
        self.LV_ys = [x[1] for x in self.LV]
        if self.costs is not None:
            self.costs[0] = [self._volume(wl) for wl in self.costs[0]]
        if self.min is not None:
            self.min = self._volume(self.min)
        if self.max is not None:
            self.max = self._volume(self.max)
        if self.setpoint is not None:
            self.setpoint = self._volume(self.setpoint)

    def _default_name(self, time):
        return super()._volume_name(time)

    def _level(self, volume):
        return interp(volume, self.LV_ys, self.LV_xs)

    def _volume(self, level):
        return interp(level, self.LV_xs, self.LV_ys)

    def _create_lp(self, m: HydraulicModel):
        level = self.time_series.get(m.actual_time)
        self._vol = self._volume(level)
        for ti, t in enumerate(m.times):
            if t < m.actual_time:
                continue
            if t == m.actual_time:
                m.lp.add_row(self._volume_name(t), 'E', self._vol)
            else:
                t_prior = m.times[ti - 1]
                dt = t - t_prior
                flows = []
                for flow in self.inflows:
                    inflow = m.model[flow]
                    flows.append(dt)
                    if inflow.type == 'river':
                        flows.append(inflow._outflow_name(t_prior))
                    else:
                        flows.append(inflow._flow_name(t_prior))
                for flow in self.outflows:
                    outflow = m.model[flow]
                    flows.append(-dt)
                    if outflow.type == 'river':
                        flows.append(outflow._inflow_name(t_prior))
                    else:
                        flows.append(outflow._flow_name(t_prior))
                m.lp.add_row(flows, self._volume_name(t_prior),
                             -1, self._volume_name(t), 'E', 0)
                self._add_limit_costs(m, t)

    def _post_process(self, m: HydraulicModel):
        for t in m.times:
            if self._volume_name(t) in m.lp.results:
                volume = m.lp.results[self._volume_name(t)]
                level = self._level(volume)
                m.lp.results[self._level_name(t)] = level
                if self.time_series is None:
                    continue
                self.time_series.set([[t, level]])


class StorageProfile(Constraint):
    """
    Sets a target level for the reservoir.

    For a rising level there is a cost for being below the target but NO cost
    for being above it. This works better than a revenue cost effectively
    bringing the planning to the present time in the solve shortening the
    solve period needed for an effective solution.
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.element = None
        self.timeofday = []
        self.LV = []
        super().__init__(**kwargs)
        self.LV_xs = [x[0] for x in self.LV]
        self.LV_ys = [x[1] for x in self.LV]
        # convert levels to volumes
        for e in self.timeofday:
            e[1] = interp(e[1], self.LV_xs, self.LV_ys)
        # make a copy to make it easy to interpolate levels
        self._tod_xs, self._tod_ys = tod_to_xs_ys(self.timeofday)
        pass

    def _default_name(self, time):
        return super()._volume_name(time)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            sec_into_day = day_seconds(t)
            # Assumes the calling function does not screw up with DST
            lake_target = interp(
                sec_into_day,
                self._tod_xs,
                self._tod_ys
            )
            # lake_target_level = interp(lake_target, self.LV_ys, self.LV_xs)
            # logging.info(f"target at {t} is {lake_target_level:.3f}")
            lake_next = interp(
                sec_into_day + m.time_step,
                self._tod_xs,
                self._tod_ys
            )
            m.lp.add_row(
                m.model[self.element]._volume_name(t),
                self._neg_lake_profile_name(t),
                -1.0, self._pos_lake_profile_name(t),
                'E', lake_target
            )
            if lake_next > lake_target:  # want lake level increasing
                m.add_cost((self.cost, self._neg_lake_profile_name(t)))
                if self.lowcost != 0.0:
                    m.add_cost((self.lowcost, self._pos_lake_profile_name(t)))
            else:  # want lake level decreasing - but less so
                m.add_cost((self.cost, self._pos_lake_profile_name(t)))
                if self.lowcost != 0.0:
                    m.add_cost((self.lowcost, self._neg_lake_profile_name(t)))
        pass

    def _post_process(self, m: HydraulicModel):
        pass


class River(Constraint):
    """
    River is a simple delay line.

    Flow is split into inflow and outflow. outflow is set equal to the old
    inflow value creating links between time periods
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.delay = 0
        self.limitcost = 1000000.0
        super().__init__(**kwargs)
        if self.time_series is None:
            raise f'{self.name} must have a flow time_series.'

    def _default_name(self, time):
        return super()._inflow_name(time)

    def _create_lp(self, m: HydraulicModel):
        # work from the outflow time
        for t in m.times:
            if t < m.actual_time:
                continue
            t_prev = t - self.delay
            if t == m.set_time:
                t_prev = m.actual_time - self.delay
            # a future that depends on the actual_time should be set_time
            # so that a control action can make a difference.
            if t_prev == m.actual_time:
                t_prev = m.set_time
            if t_prev < m.set_time:
                m.lp.add_row(self._outflow_name(t), 'E',
                             self.time_series.get(t_prev))
            else:
                m.lp.add_row(self._outflow_name(t), -1,
                             self._inflow_name(t_prev), 'E', 0.0)
            # if t == m.set_time:
            #     m.lp.add_between(self._inflow_name(t),
            #                      self._inflow_name(t_prev),
            #                      self._inflow_name(t_prev + self.delay))
            self._add_limit_costs(m, t)


class Valve(Constraint):
    """
    Valve discharging into free air.
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.state: State = State.OFF
        self.flow: TimeSeries = None
        super().__init__(**kwargs)
        if self.time_series is None:
            raise f'{self.name} must have a flow time_series.'

    def _default_name(self, time):
        return super()._flow_name(time)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            flow = self.time_series.get(t)
            if flow < 0.1:
                flow = 0
            if t <= m.actual_time:
                m.lp.add_row(self._flow_name(t), 'E', flow)
            elif self.state == State.OFF:
                m.lp.add_row(self._flow_name(t), 'E', 0)
            elif self.state == State.FIXED:
                m.lp.add_row(self._flow_name(t), 'E', flow)
            elif self.state == State.FREE:
                self._add_ranges(m, t)
                self._add_limit_costs(m, t)
            else:
                logging.error(f"{self.name} invalid state: {self.state}")


class Generator(Constraint):
    """Ties flow to generation. Generation is slack."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.state = State.FREE
        self.setMW = 0.0
        self.stop = False
        self.startlimit = []
        self.rangelimit = []
        self.PQ = []
        super().__init__(**kwargs)
        if self.time_series is None:
            raise f'{self.name} must have a power time_series.'
        # CPU cost of doing this per call in debug is HIGH
        self.PQ_xs = [x[0] for x in self.PQ]
        self.PQ_ys = [x[1] for x in self.PQ]

    def _default_name(self, time):
        return super()._power_name(time)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            power = self.time_series.get(t)
            self._add_ranges(m, t)
            power = self._range_conform(power)
            if t < m.set_time:
                m.lp.add_row(self._power_name(t), 'E', power)
            elif self.state == State.OFF:
                m.lp.add_row(self._power_name(t), 'E', 0)
            elif self.state == State.FIXED:
                m.lp.add_row(self._power_name(t), 'E', power)
            # Always calculate flow from power
            m.lp.add_sos2(self._power_name(t), [x[0] for x in self.PQ],
                          self._flow_name(t), [x[1] for x in self.PQ])
        if self.state == State.FREE and len(self.startlimit) == 3:
            # need COS leading up to now
            pre_times = [m.start_time - i * m.time_step for i in
                         range(self.startlimit[1] // m.time_step - 1, 0, -1)]
            for t in pre_times:
                power = self._range_conform(self.time_series.get(t))
                m.lp.add_row(self._power_name(t), 'E', power)
                self._add_ranges(m, t)
            cos_lists = [[]]
            lim_lists = {}
            # collect a list of times for COS detection
            # collect a list of time ranges where COS is limited
            for t in pre_times + m.times:
                cos_lists[-1].append(t)
                cos_lists.append([t])
                for lim_t in lim_lists.keys():
                    if t > lim_t and t < lim_t + self.startlimit[1]:
                        lim_lists[lim_t].append(t)
                if t not in lim_lists:
                    lim_lists[t] = [t]
            cos_lists.pop()
            cos_lists.pop(0)
            # apply the COS detection and limiting
            for t1, t2 in cos_lists:
                bv1 = self._running_bv_name(t1)
                bv2 = self._running_bv_name(t2)
                m.lp.add_row(bv1, -1, bv2, f"{bv1}__COS_pos__",
                             -1, f"{bv1}__COS_neg__", 'E', 0.0)
            for times in lim_lists.values():
                cos = []
                for t in times:
                    bv1 = self._running_bv_name(t)
                    cos.append(f"{bv1}__COS_pos__")
                    cos.append(f"{bv1}__COS_neg__")
                c1 = m.lp.get_unique_var('COS', t)
                m.lp.add_row(cos, -1.0, c1, 'L', self.startlimit[0])
                m.add_cost((self.startlimit[2], c1))
        pass


class Cost(Constraint):
    """Simple cost."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = None
        self.measurement = None
        self.timeofday = []
        super().__init__(**kwargs)
        self._tod_xs, self._tod_ys = tod_to_xs_ys(self.timeofday)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            sec_into_day = day_seconds(t)
            ylim = interp_step(sec_into_day, self._tod_xs, self._tod_ys)
            costlist = []
            for e in self.elements:
                costlist.append(m.model[e]._default_name(t))
            m.lp.add_row(
                costlist,
                self._neg_cost_name(t),
                -1, self._pos_cost_name(t),
                'E', ylim  # target
            )
            # add the cost to the objective function
            m.add_cost((self.cost, self._pos_cost_name(t)))
            m.add_cost((self.cost, self._neg_cost_name(t)))
        pass


class Consent(Constraint):
    """Resource consent limit."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = None
        # self.elements = None  # TODO check these are unique
        self.day = 0.0
        self.night = 0.0
        super().__init__(**kwargs)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            # find the target setpoint from the time series
            tod = time.localtime(t)
            min_flow = self.day
            if tod.tm_hour < 7 or tod.tm_hour >= 19:
                min_flow = self.night
            # build the costs to watch
            elements = []
            for e in self.elements:
                if m.model[e].type == 'river':
                    elements.append(m.model[e]._outflow_name(t))
                elif m.model[e].type in ['generator', 'valve']:
                    elements.append(m.model[e]._flow_name(t))
            if self.cost is None:
                m.lp.add_row(elements, 'G', min_flow)
            else:
                m.lp.add_row(elements, self._neg_cost_name(t), 'G', min_flow)
                m.add_cost((self.cost, self._neg_cost_name(t)))
        pass


class BidOffer(Constraint):
    """WITS market offer."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.band = 1.0
        self.states = []
        self.outage = {}
        self.active_bid = 10.0
        self.bid_offer = {}
        self.window = 3720
        super().__init__(**kwargs)
        pass

    def _create_lp(self, m: HydraulicModel):
        lock_time = m.actual_time + self.window
        for t in m.times:
            if t < m.set_time:
                continue
            period = bid_period(t)
            index = self.outage['period'].index(period)
            setpoint = self.outage['setpoint'][index]
            c1 = None
            c2 = None
            c3 = f'Gen__Bid__{period}'
            elements = [m.model[x]._power_name(t) for x in self.elements]
            if self.states[setpoint] == 0:
                m.lp.add_row(elements, 'E', 0)
                m.lp.add_row(c3, 'E', 0)
                continue
            elif self.states[setpoint] == 'OFF':
                m.lp.add_row(c3, 'E', 0)
                continue
            if t == m.set_time:
                c1 = m.lp.get_unique_var('_Bid_lim_lo_TPdispatch', t)
                c2 = m.lp.get_unique_var('_Bid_lim_hi_TPdispatch', t)
                m.lp.add_row(elements, c1, -1.0, c2, 'E', self.active_bid)
            else:
                c1 = m.lp.get_unique_var(f'_Bid_lim_lo_{period}', t)
                c2 = m.lp.get_unique_var(f'_Bid_lim_hi_{period}', t)
                m.lp.add_row(elements, c1, -1.0, c2, -1.0, c3, 'E', 0)
            m.lp.add_row(c1, 'L', self.band)
            m.lp.add_row(c2, 'L', self.band)
            # add a small cost to slightly favour centre of bid
            m.add_cost((0.1, c1))
            m.add_cost((0.1, c2))
            if t <= lock_time:
                index = self.bid_offer['period'].index(period)
                lock_mw = self.bid_offer['setpoint'][index]
                m.lp.add_row(c3, 'E', lock_mw)
            else:  # if outside lock to allow changes
                if self.min is not None:
                    m.lp.add_row(c3, 'G', self.min)
                if self.max is not None:
                    m.lp.add_row(c3, 'L', self.max)


class Match(Constraint):
    """State selection for generator modes in a station."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.states = []
        self.outage = {}
        self.state1 = None
        self.state2 = None
        super().__init__(**kwargs)
        pass

    def _create_lp(self, m: HydraulicModel):
        if self.state1 != State.FREE or self.state2 != State.FREE:
            return
        for t in m.times:
            if t < m.set_time:
                continue
            # if t == m.set_time:
            #     continue
            # else:
            period = bid_period(t)
            index = self.outage['period'].index(period)
            setpoint = self.outage['setpoint'][index]
            for actions in self.states[setpoint]:
                e1, eq, e2 = actions
                if type(e1) == str:
                    e1 = m.model[e1]._power_name(t)
                else:
                    exit(f"{self.name} {self.states[setpoint]} invalid")
                if type(e2) == str:
                    e2 = [-1.0, m.model[e2]._power_name(t)]
                    m.lp.add_row(e1, e2, eq, 0.0)
                else:
                    m.lp.add_row(e1, eq, e2)
            g1 = self.elements[0]
            g1_power = m.model[g1]._power_name(t)
            g1_off = m.model[g1]._off_bv_name(t)
            g1_running = m.model[g1]._running_bv_name(t)
            g2 = self.elements[1]
            g2_power = m.model[g2]._power_name(t)
            g2_off = m.model[g2]._off_bv_name(t)
            g2_running = m.model[g2]._running_bv_name(t)
            m.lp.add_row(g1_running, g1_off, 'E', 1)
            m.lp.add_limit(g1_off, 'BV', None)
            m.lp.add_row(g2_running, g2_off, 'E', 1)
            m.lp.add_limit(g2_off, 'BV', None)
            # G1 < G2 unless G2 is off
            m.lp.add_row(g1_power, -1, g2_power, -100, g2_off, 'L', 0)
            # G2 < G1 unless G1 is off
            m.lp.add_row(g2_power, -1, g1_power, -100, g1_off, 'L', 0)


class Relation(Constraint):
    """Relationships between variables, MAYBE."""

    # TODO needs a LOT of work to clean this hack item up
    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.operator = None
        self.constant = None
        super().__init__(**kwargs)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            if self.operator == 'greater':
                if self.constant is None:
                    m.lp.add_row(
                        m.model[self.elements[0]]._default_name(t),
                        -1, m.model[self.elements[1]]._default_name(t),
                        'G', 0
                    )
                else:
                    m.lp.add_row(
                        m.model[self.elements[0]]._default_name(t),
                        m.model[self.elements[1]]._default_name(t),
                        'G', self.constant
                    )
            if self.operator == 'less':
                if self.constant is None:
                    m.lp.add_row(
                        m.model[self.elements[0]]._default_name(t),
                        -1, m.model[self.elements[1]]._default_name(t),
                        'L', 0
                    )
                else:
                    m.lp.add_row(
                        m.model[self.elements[0]]._default_name(t),
                        m.model[self.elements[1]]._default_name(t),
                        'L', self.constant
                    )
        pass


class DeltaCost(Constraint):
    """Difference between two slack variables."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        super().__init__(**kwargs)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            c1 = m.lp.get_unique_var('Delta', t)
            c2 = m.lp.get_unique_var('Delta', t)
            m.lp.add_row(
                m.model[self.elements[0]]._default_name(t),
                -1, m.model[self.elements[1]]._default_name(t),
                c1, -1.0, c2,
                'E', 0
            )
            m.add_cost((self.cost, c1))
            m.add_cost((self.cost, c2))
        pass


class ChangeCost(Constraint):
    """Cost to move."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.element = None
        super().__init__(**kwargs)

    def _create_lp(self, m: HydraulicModel):
        last_time = 0
        for t in m.times:
            if t < m.set_time:
                last_time = t
                continue
            c1 = m.lp.get_unique_var('Change', t)
            c2 = m.lp.get_unique_var('Change', t)
            m.lp.add_row(
                m.model[self.element]._default_name(t),
                -1, m.model[self.element]._default_name(last_time),
                c1, -1.0, c2,
                'E', 0.0
            )
            m.add_cost((self.cost, c1))
            m.add_cost((self.cost, c2))
            last_time = t
        pass


class StepCost(Constraint):
    """Cost to move larger than a step limit."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.incost = 0.001
        self.outcost = 1.0
        self.band = 5.0
        super().__init__(**kwargs)

    def _create_lp(self, m: HydraulicModel):
        last_time = 0
        for t in m.times:
            # accept bigger steps if they have come from Transpower
            # < m.set_time would block this
            if t <= m.set_time:
                last_time = t
                continue
            c1 = m.lp.get_unique_var('Step', t)
            c2 = m.lp.get_unique_var('Step', t)
            c3 = m.lp.get_unique_var('Step', t)
            c4 = m.lp.get_unique_var('Step', t)
            elements = [
                m.model[x]._default_name(t) for x in self.elements
            ]
            last_elements = [
                m.model[x]._default_name(last_time) for x in self.elements
            ]
            neg_elements = [x for y in last_elements for x in (-1.0, y)]
            m.lp.add_row(
                elements,
                neg_elements,
                c1, -1.0, c2,
                c3, -1.0, c4,
                'E', 0.0
            )
            m.lp.add_row(c1, 'L', self.band)
            m.lp.add_row(c2, 'L', self.band)
            m.add_cost((self.incost, c1))
            m.add_cost((self.incost, c2))
            m.add_cost((self.outcost, c3))
            m.add_cost((self.outcost, c4))
            last_time = t
        pass


class RevenueProfile(Constraint):
    """Cannot recall."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        # self.elements = []  # TODO check these are unique
        self.timeofday = []
        super().__init__(**kwargs)
        self._tod_xs, self._tod_ys = tod_to_xs_ys(self.timeofday)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            # find the value rate with respect to time
            sec_into_day = day_seconds(t)
            ylim = interp_step(sec_into_day, self._tod_xs, self._tod_ys)
            rate = ylim / (3600 / m.time_step)
            costlist = []
            # collect the elements
            for e in self.elements:
                costlist.append(- rate)
                costlist.append(m.model[e]._power_name(t))
            m.lp.add_row(
                costlist,
                self._pos_cost_name(t),
                'E', 0
            )
            m.add_cost((self.cost, self._pos_cost_name(t)))
        pass


class LimitProfile(Constraint):
    """Limit profile sets a target level minimum or maximum."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.cost = 1.0
        self.measurement = None
        self.timeofday = []
        super().__init__(**kwargs)
        self._tod_xs, self._tod_ys = tod_to_xs_ys(self.timeofday)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            sec_into_day = day_seconds(t)
            ylim = interp_step(sec_into_day, self._tod_xs, self._tod_ys)
            elm = []
            for e in self.elements:
                if self.measurement == 'flow':
                    elm.append(m.model[e]._flow_name(t))
                elif self.measurement == 'power':
                    elm.append(m.model[e]._power_name(t))
                else:
                    logging.critical(f"no measurement for {e}")
            if self.min:
                m.lp.add_row(elm, 'G', ylim)
            elif self.max:
                m.lp.add_row(elm, 'L', ylim)
        pass


class TimeProfile(Constraint):
    """
    Set a target based on time of day and interpolated values.

    Set step=True for stepwise interpolation.
    """

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.step = False
        self.timeofday = []
        super().__init__(**kwargs)
        self._tod_xs, self._tod_ys = tod_to_xs_ys(self.timeofday)

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            sec_into_day = day_seconds(t)
            if self.step:
                self.setpoint = interp_step(sec_into_day, self._tod_xs,
                                            self._tod_ys)
            else:
                self.setpoint = interp(sec_into_day, self._tod_xs,
                                       self._tod_ys)
            self._add_limit_costs(m, t)


class Add(Constraint):
    """Add multiple elements into a single element. Add limits."""

    def __init__(self, **kwargs):
        """Inherits from Constraint."""
        self.name = None
        self.defaultname = None
        super().__init__(**kwargs)

    def _default_name(self, time):
        if self.defaultname is None:
            return super()._default_name(time)
        elif self.defaultname == 'power':
            return super()._power_name(time)
        elif self.defaultname == 'flow':
            return super()._flow_name(time)
        else:
            logging.critical(f"{self.name} {self.defaultname} not implemented")

    def _create_lp(self, m: HydraulicModel):
        for t in m.times:
            if t < m.set_time:
                continue
            elements = [
                m.model[x]._default_name(t) for x in self.elements
            ]
            m.lp.add_row(elements, -1.0, self._default_name(t), 'E', 0)
            self._add_limit_costs(m, t)
