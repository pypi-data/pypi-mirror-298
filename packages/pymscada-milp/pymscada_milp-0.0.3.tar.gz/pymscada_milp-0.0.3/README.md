# pymscada-milp

## Base MILP operation

Provides a python module to frame and solve MILP problems.

```python
from pymscada_milp import LpModel

# See https://www.homepages.ed.ac.uk/jwp/newMSOcopy/section5/milp.html
#
# max: 20 x1 + 6 x2 + 8 x3;
# 0.8 x1 + 0.2 x2 + 0.3 x3 <=20;
# 0.4 x1 + 0.3 x2 <= 10;
# 0.2 x1 + 0.1 x3 <= 5;
# int x1, x2, x3;
#
# and crucially, on the earlier page and not copied :(
# x3<=20;

m = LpModel()
m.add_row(-20, 'x1', -6, 'x2', -8, 'x3', 'N')  # Negate as default minimizes
m.add_row(0.8, 'x1', 0.2, 'x2', 0.3, 'x3', 'L', 20)
m.add_row(0.4, 'x1', 0.3, 'x2', 'L', 10)
m.add_row(0.2, 'x1', 0.1, 'x3', 'L', 5)
m.add_limit('x1', 'LI', 0)
m.add_limit('x2', 'LI', 0)
m.add_limit('x3', 'UI', 20)
m.write_mps()
m.solve_mps()
print([f'{x} {m.results[x]}' for x in ['x1', 'x2', 'x3']])
m.remove_result()
```

## Hydraulic Model

The LP model (above) was intended to provide a way to model generators,
gates and reservoirs with a procedural representation. i.e.

```python
from pymscada_milp import HydraulicModel, TimeSeries, State

inflow = TimeSeries(9.0)  # Provides inflow present value and history
outflow = TimeSeries(1.0)
tank = TimeSeries(0.5)
model = {
    'name': 'test',
    'actual_time': 1522494300,
    'time_step': 600,
    'duration': 1200,
    'tempdir': 'tmp',
    'model': {
        'Inflow': {
            'type': 'valve',
            'time_series': inflow,
            'dstnode': 'Tank',
            'state': State.FIXED  # Use State.FREE to solve optimally
        },
        'Tank': {
            'type': 'storage',
            'time_series': tank,
            'LV': [
                [0.00, 0],
                [1.00, 1000000]
            ],
            'costs': [
                [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
                [
                    [10000, 10000],  # expensive low cost
                    [50, 10],  # soft low cost
                    [1, 0],  # slightly favour filling
                    [0, 50],  # soft high cost
                    [5000, 5000]  # expensive high cost
                ]
            ]
        },
        'Outflow': {
            'type': 'valve',
            'time_series': outflow,
            'srcnode': 'Tank',
            'state': State.FIXED
        }
    }
}
m = HydraulicModel(model)
m.solve_lp()
print(inflow.values())  # The solver adds inflow predictions / setpoints.
print(tank.values())
print(outflow.values())
m.remove_result()
```