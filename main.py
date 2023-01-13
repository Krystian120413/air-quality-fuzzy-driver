import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# zmienne wejściowe

pm10 = ctrl.Antecedent(np.arange(0, 200), 'PM 10')
pm25 = ctrl.Antecedent(np.arange(0, 150), 'PM 2.5')

# zmienna wyjściowa

air_quality = ctrl.Consequent(np.arange(0, 350), 'air-quality')

# funkcje przynależności do zmiennej wejściowej zawartość pyłu PM10 w powietrzu

pm10['GOOD'] = fuzz.trapmf(pm10.universe, [0, 0, 55, 60])
pm10['MODERATE'] = fuzz.trapmf(pm10.universe, [50, 65, 75, 90])
pm10['PASSABLE'] = fuzz.trapmf(pm10.universe, [80, 95, 105, 120])
pm10['BAD'] = fuzz.trapmf(pm10.universe, [110, 125, 200, 200])
pm10.view()

# funkcje przynależności do zmiennej wejściowej zawartość pyłu PM2.5 w powietrz

pm25['GOOD'] = fuzz.trapmf(pm25.universe, [0, 0, 28, 30])
pm25['MODERATE'] = fuzz.trapmf(pm25.universe, [25, 30, 50, 50])
pm25['PASSABLE'] = fuzz.trapmf(pm25.universe, [45, 55, 65, 70])
pm25['BAD'] = fuzz.trapmf(pm25.universe, [55, 75, 150, 150])
pm25.view()

# funkcje przynależności do zmiennej wyjściowej jakość powietrza

air_quality['GOOD'] = fuzz.trapmf(air_quality.universe, [0, 0, 95, 115])
air_quality['MODERATE'] = fuzz.trapmf(air_quality.universe, [90, 105, 145, 165])
air_quality['PASSABLE'] = fuzz.trapmf(air_quality.universe, [140, 155, 195, 215])
air_quality['BAD'] = fuzz.trapmf(air_quality.universe, [180, 200, 350, 350])
air_quality.view()

# reguły

rule0 = ctrl.Rule(pm10['GOOD'] & pm25['GOOD'], air_quality['GOOD'])
rule1 = ctrl.Rule(pm10['GOOD'] & pm25['MODERATE'], air_quality['GOOD'])
rule2 = ctrl.Rule(pm10['GOOD'] & pm25['PASSABLE'], air_quality['MODERATE'])
rule3 = ctrl.Rule(pm10['GOOD'] & pm25['BAD'], air_quality['PASSABLE'])

rule4 = ctrl.Rule(pm10['MODERATE'] & pm25['GOOD'], air_quality['MODERATE'])
rule5 = ctrl.Rule(pm10['MODERATE'] & pm25['MODERATE'], air_quality['MODERATE'])
rule6 = ctrl.Rule(pm10['MODERATE'] & pm25['PASSABLE'], air_quality['MODERATE'])
rule7 = ctrl.Rule(pm10['MODERATE'] & pm25['BAD'], air_quality['PASSABLE'])

rule8 = ctrl.Rule(pm10['PASSABLE'] & pm25['GOOD'], air_quality['MODERATE'])
rule9 = ctrl.Rule(pm10['PASSABLE'] & pm25['MODERATE'], air_quality['MODERATE'])
rule10 = ctrl.Rule(pm10['PASSABLE'] & pm25['PASSABLE'], air_quality['PASSABLE'])
rule11 = ctrl.Rule(pm10['PASSABLE'] & pm25['BAD'], air_quality['BAD'])

rule12 = ctrl.Rule(pm10['BAD'] & pm25['GOOD'], air_quality['PASSABLE'])
rule13 = ctrl.Rule(pm10['BAD'] & pm25['MODERATE'], air_quality['PASSABLE'])
rule14 = ctrl.Rule(pm10['BAD'] & pm25['PASSABLE'], air_quality['BAD'])
rule15 = ctrl.Rule(pm10['BAD'] & pm25['BAD'], air_quality['BAD'])

# sterownik rozmyty

air_quality_ctrl = ctrl.ControlSystem([
    rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15
])

# symulacja działania sterownika

air_quality_sensor_simulation = ctrl.ControlSystemSimulation(air_quality_ctrl)
air_quality_sensor_simulation.input['PM 10'] = 70
air_quality_sensor_simulation.input['PM 2.5'] = 63
air_quality_sensor_simulation.compute()

pm10.view(sim=air_quality_sensor_simulation)
pm25.view(sim=air_quality_sensor_simulation)
air_quality.view(sim=air_quality_sensor_simulation)

print("air-quality:", round(air_quality_sensor_simulation.output['air-quality']))
air_quality_ctrl.view()
plt.show()