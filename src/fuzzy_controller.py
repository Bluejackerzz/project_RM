import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def create_fuzzy_system():
    volume = ctrl.Antecedent(np.arange(0, 51, 1), 'volume')
    time = ctrl.Consequent(np.arange(10, 61, 1), 'time')

    volume['low'] = fuzz.trimf(volume.universe, [0, 0, 20])
    volume['medium'] = fuzz.trimf(volume.universe, [10, 25, 40])
    volume['high'] = fuzz.trimf(volume.universe, [30, 50, 50])

    time['short'] = fuzz.trimf(time.universe, [10, 10, 30])
    time['medium'] = fuzz.trimf(time.universe, [20, 35, 50])
    time['long'] = fuzz.trimf(time.universe, [40, 60, 60])

    rule1 = ctrl.Rule(volume['low'], time['short'])
    rule2 = ctrl.Rule(volume['medium'], time['medium'])
    rule3 = ctrl.Rule(volume['high'], time['long'])

    system = ctrl.ControlSystem([rule1, rule2, rule3])
    simulation = ctrl.ControlSystemSimulation(system)
    return simulation

def get_green_times(lane_totals):
    fuzzy = create_fuzzy_system()
    green_times = {}
    for lane, count in lane_totals.items():
        fuzzy.input['volume'] = count
        fuzzy.compute()
        green_times[lane] = fuzzy.output['time']
    return green_times

