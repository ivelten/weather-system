import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control

# Automated Room Temperature Control (ARTC)
class ARTC:
    def __init__(self):

        # Universo das funções de entrada
        temp_universe     = np.arange(0.0, 35.0, 0.5)      # Temperatura, em Celsius
        pressure_universe = np.arange(500.0, 1500.0, 1.0)  # Pressão, em hPa
        humidity_universe = np.arange(0.0, 100.0, 0.5)     # Umidade, em %

        # Antecedentes
        self._temperature = control.Antecedent(temp_universe, 'Temperature')
        self._pressure    = control.Antecedent(pressure_universe, 'Pressure')
        self._humidity    = control.Antecedent(humidity_universe, 'Humidity')

        # Funções para temperatura
        self._temperature['Freezy'] = fuzz.trapmf(self._temperature.universe, [0.0, 0.0, 9.0, 10.0])
        self._temperature['Cold']   = fuzz.trapmf(self._temperature.universe, [9.0, 10.0, 13.5, 15])
        self._temperature['Normal'] = fuzz.trapmf(self._temperature.universe, [13.5, 15.0, 18.5, 20.0])
        self._temperature['Warm']   = fuzz.trapmf(self._temperature.universe, [18.5, 20.0, 23.5, 25])
        self._temperature['Hot']    = fuzz.trapmf(self._temperature.universe, [23.5, 25.0, 35.0, 35.0])

        # Funções para pressão
        self._pressure['Fall']     = fuzz.trapmf(self._pressure.universe, [500.0, 500.0, 680.0, 700.0])
        self._pressure['Low']      = fuzz.trapmf(self._pressure.universe, [680.0, 700.0, 880.0, 900.0])
        self._pressure['Amicable'] = fuzz.trapmf(self._pressure.universe, [880.0, 900.0, 1080.0, 1100.0])
        self._pressure['Elevated'] = fuzz.trapmf(self._pressure.universe, [1080.0, 1100.0, 1280.0, 1300.0])
        self._pressure['High']     = fuzz.trapmf(self._pressure.universe, [1280.0, 1300.0, 1500.0, 1500.0])

        # Funções para umidade
        self._humidity['Dry']         = fuzz.trapmf(self._humidity.universe, [0.0, 0.0, 25.0, 30.0])
        self._humidity['Comfortable'] = fuzz.trapmf(self._humidity.universe, [25.0, 30.0, 55.0, 60.0])
        self._humidity['Wet']         = fuzz.trapmf(self._humidity.universe, [55.0, 60.0, 100.0, 100.0])

        # Universo das funções de saída
        control_universe = np.arange(0.0, 1.0, 0.01)

        # Consequentes
        self._heater  = control.Consequent(control_universe, 'Heater')
        self._chiller = control.Consequent(control_universe, 'Chiller')

        # Funções para o aquecedor
        self._heater['Off']        = fuzz.trimf(self._heater.universe, [0.0, 0.0, 0.0])
        self._heater['Heat']       = fuzz.trapmf(self._heater.universe, [0.0, 0.0, 0.45, 0.55])
        self._heater['Quick-Heat'] = fuzz.trapmf(self._heater.universe, [0.45, 0.55, 1.0, 1.0])

        # Funções para o resfriador
        self._chiller['Off']         = fuzz.trimf(self._chiller.universe, [0.0, 0.0, 0.0])
        self._chiller['Chiller-Fan'] = fuzz.trapmf(self._chiller.universe, [0.0, 0.0, 0.35, 0.45])
        self._chiller['Cool']        = fuzz.trapmf(self._chiller.universe, [0.35, 0.45, 0.65, 0.75])
        self._chiller['Quick-Cool']  = fuzz.trapmf(self._chiller.universe, [0.65, 0.75, 1.0, 1.0])

        # Regras
        r01 = control.Rule(self._temperature['Freezy'] & self._pressure['Fall']     & self._humidity['Dry'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r02 = control.Rule(self._temperature['Freezy'] & self._pressure['Low']      & self._humidity['Dry'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r03 = control.Rule(self._temperature['Freezy'] & self._pressure['Amicable'] & self._humidity['Dry'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r04 = control.Rule(self._temperature['Freezy'] & self._pressure['Elevated'] & self._humidity['Dry'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r05 = control.Rule(self._temperature['Freezy'] & self._pressure['High']     & self._humidity['Dry'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r06 = control.Rule(self._temperature['Freezy'] & self._pressure['Fall']     & self._humidity['Comfortable'], (self._heater['Quick-Heat'],   self._chiller['Off']))
        r07 = control.Rule(self._temperature['Freezy'] & self._pressure['Low']      & self._humidity['Comfortable'], (self._heater['Quick-Heat'],   self._chiller['Off']))
        r08 = control.Rule(self._temperature['Freezy'] & self._pressure['Amicable'] & self._humidity['Comfortable'], (self._heater['Quick-Heat'],   self._chiller['Off']))
        r09 = control.Rule(self._temperature['Freezy'] & self._pressure['Elevated'] & self._humidity['Comfortable'], (self._heater['Quick-Heat'],   self._chiller['Off']))
        r10 = control.Rule(self._temperature['Freezy'] & self._pressure['High']     & self._humidity['Comfortable'], (self._heater['Quick-Heat'],   self._chiller['Off']))
        r11 = control.Rule(self._temperature['Freezy'] & self._pressure['Fall']     & self._humidity['Wet'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r12 = control.Rule(self._temperature['Freezy'] & self._pressure['Low']      & self._humidity['Wet'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r13 = control.Rule(self._temperature['Freezy'] & self._pressure['Amicable'] & self._humidity['Wet'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r14 = control.Rule(self._temperature['Freezy'] & self._pressure['Elevated'] & self._humidity['Wet'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r15 = control.Rule(self._temperature['Freezy'] & self._pressure['High']     & self._humidity['Wet'],         (self._heater['Quick-Heat'],   self._chiller['Off']))
        r16 = control.Rule(self._temperature['Cold']   & self._pressure['Fall']     & self._humidity['Dry'],         (self._chiller['Chiller-Fan'], self._heater['Off']))
        r17 = control.Rule(self._temperature['Cold']   & self._pressure['Low']      & self._humidity['Dry'],         (self._chiller['Chiller-Fan'], self._heater['Off']))
        r18 = control.Rule(self._temperature['Cold']   & self._pressure['Amicable'] & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r19 = control.Rule(self._temperature['Cold']   & self._pressure['Elevated'] & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r20 = control.Rule(self._temperature['Cold']   & self._pressure['High']     & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r21 = control.Rule(self._temperature['Cold']   & self._pressure['Fall']     & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r22 = control.Rule(self._temperature['Cold']   & self._pressure['Low']      & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r23 = control.Rule(self._temperature['Cold']   & self._pressure['Amicable'] & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r24 = control.Rule(self._temperature['Cold']   & self._pressure['Elevated'] & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r25 = control.Rule(self._temperature['Cold']   & self._pressure['High']     & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r26 = control.Rule(self._temperature['Cold']   & self._pressure['Fall']     & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r27 = control.Rule(self._temperature['Cold']   & self._pressure['Low']      & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r28 = control.Rule(self._temperature['Cold']   & self._pressure['Amicable'] & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r29 = control.Rule(self._temperature['Cold']   & self._pressure['Elevated'] & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r30 = control.Rule(self._temperature['Cold']   & self._pressure['High']     & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r31 = control.Rule(self._temperature['Normal'] & self._pressure['Fall']     & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r32 = control.Rule(self._temperature['Normal'] & self._pressure['Low']      & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r33 = control.Rule(self._temperature['Normal'] & self._pressure['Amicable'] & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r34 = control.Rule(self._temperature['Normal'] & self._pressure['Elevated'] & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r35 = control.Rule(self._temperature['Normal'] & self._pressure['High']     & self._humidity['Dry'],         (self._heater['Heat'],         self._chiller['Off']))
        r36 = control.Rule(self._temperature['Normal'] & self._pressure['Fall']     & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r37 = control.Rule(self._temperature['Normal'] & self._pressure['Low']      & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r38 = control.Rule(self._temperature['Normal'] & self._pressure['Amicable'] & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r39 = control.Rule(self._temperature['Normal'] & self._pressure['Elevated'] & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r40 = control.Rule(self._temperature['Normal'] & self._pressure['High']     & self._humidity['Comfortable'], (self._heater['Heat'],         self._chiller['Off']))
        r41 = control.Rule(self._temperature['Normal'] & self._pressure['Fall']     & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r42 = control.Rule(self._temperature['Normal'] & self._pressure['Low']      & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r43 = control.Rule(self._temperature['Normal'] & self._pressure['Amicable'] & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r44 = control.Rule(self._temperature['Normal'] & self._pressure['Elevated'] & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r45 = control.Rule(self._temperature['Normal'] & self._pressure['High']     & self._humidity['Wet'],         (self._heater['Heat'],         self._chiller['Off']))
        r46 = control.Rule(self._temperature['Warm']   & self._pressure['Fall']     & self._humidity['Dry'],         (self._chiller['Cool'],        self._heater['Off']))
        r47 = control.Rule(self._temperature['Warm']   & self._pressure['Low']      & self._humidity['Dry'],         (self._chiller['Cool'],        self._heater['Off']))
        r48 = control.Rule(self._temperature['Warm']   & self._pressure['Amicable'] & self._humidity['Dry'],         (self._chiller['Cool'],        self._heater['Off']))
        r49 = control.Rule(self._temperature['Warm']   & self._pressure['Elevated'] & self._humidity['Dry'],         (self._chiller['Cool'],        self._heater['Off']))
        r50 = control.Rule(self._temperature['Warm']   & self._pressure['High']     & self._humidity['Dry'],         (self._chiller['Cool'],        self._heater['Off']))
        r51 = control.Rule(self._temperature['Warm']   & self._pressure['Fall']     & self._humidity['Comfortable'], (self._chiller['Cool'],        self._heater['Off']))
        r52 = control.Rule(self._temperature['Warm']   & self._pressure['Low']      & self._humidity['Comfortable'], (self._chiller['Cool'],        self._heater['Off']))
        r53 = control.Rule(self._temperature['Warm']   & self._pressure['Amicable'] & self._humidity['Comfortable'], (self._chiller['Cool'],        self._heater['Off']))
        r54 = control.Rule(self._temperature['Warm']   & self._pressure['Elevated'] & self._humidity['Comfortable'], (self._chiller['Cool'],        self._heater['Off']))
        r55 = control.Rule(self._temperature['Warm']   & self._pressure['High']     & self._humidity['Comfortable'], (self._chiller['Cool'],        self._heater['Off']))
        r56 = control.Rule(self._temperature['Warm']   & self._pressure['Fall']     & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r57 = control.Rule(self._temperature['Warm']   & self._pressure['Low']      & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r58 = control.Rule(self._temperature['Warm']   & self._pressure['Amicable'] & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r59 = control.Rule(self._temperature['Warm']   & self._pressure['Elevated'] & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r60 = control.Rule(self._temperature['Warm']   & self._pressure['High']     & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r61 = control.Rule(self._temperature['Hot']    & self._pressure['Fall']     & self._humidity['Dry'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r62 = control.Rule(self._temperature['Hot']    & self._pressure['Low']      & self._humidity['Dry'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r63 = control.Rule(self._temperature['Hot']    & self._pressure['Amicable'] & self._humidity['Dry'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r64 = control.Rule(self._temperature['Hot']    & self._pressure['Elevated'] & self._humidity['Dry'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r65 = control.Rule(self._temperature['Hot']    & self._pressure['High']     & self._humidity['Dry'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r66 = control.Rule(self._temperature['Hot']    & self._pressure['Fall']     & self._humidity['Comfortable'], (self._chiller['Quick-Cool'],  self._heater['Off']))
        r67 = control.Rule(self._temperature['Hot']    & self._pressure['Low']      & self._humidity['Comfortable'], (self._chiller['Quick-Cool'],  self._heater['Off']))
        r68 = control.Rule(self._temperature['Hot']    & self._pressure['Amicable'] & self._humidity['Comfortable'], (self._chiller['Quick-Cool'],  self._heater['Off']))
        r69 = control.Rule(self._temperature['Hot']    & self._pressure['Elevated'] & self._humidity['Comfortable'], (self._chiller['Quick-Cool'],  self._heater['Off']))
        r70 = control.Rule(self._temperature['Hot']    & self._pressure['High']     & self._humidity['Comfortable'], (self._chiller['Quick-Cool'],  self._heater['Off']))
        r71 = control.Rule(self._temperature['Hot']    & self._pressure['Fall']     & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r72 = control.Rule(self._temperature['Hot']    & self._pressure['Low']      & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r73 = control.Rule(self._temperature['Hot']    & self._pressure['Amicable'] & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r74 = control.Rule(self._temperature['Hot']    & self._pressure['Elevated'] & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))
        r75 = control.Rule(self._temperature['Hot']    & self._pressure['High']     & self._humidity['Wet'],         (self._chiller['Quick-Cool'],  self._heater['Off']))

        # Criando o sistema de controle de temperatura
        self._weather_control = control.ControlSystem([
            r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, r11, r12, r13, r14, r15,
            r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30,
            r31, r32, r33, r34, r35, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45,
            r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60,
            r61, r62, r63, r64, r65, r66, r67, r68, r69, r70, r71, r72, r73, r74, r75
        ])

        # Criando a simulação
        self._simulation = control.ControlSystemSimulation(self._weather_control)

    def compute_simulation(self, temperature, pressure, humidity):
        
        # Coloca as entradas para a simulação
        self._simulation.input['Temperature'] = temperature
        self._simulation.input['Pressure'] = pressure
        self._simulation.input['Humidity'] = humidity

        # Computa o resultado da simulação
        self._simulation.compute()

        # Imprime o resultado da simulação
        self.heater_potency = round(self._simulation.output['Heater'], 2) * 100
        self.chiller_potency = round(self._simulation.output['Chiller'], 2) * 100

    def plot_input_mfs(self):

        # Plota os gráficos das funções de entrada
        self._temperature.view()
        self._pressure.view()
        self._humidity.view()

        # Exibe as janelas com os resultados da plotagem
        plt.show()

    def plot_output_mfs(self):

        # Plota os gráficos das funções de saída
        self._heater.view()
        self._chiller.view()

        # Exibe as janelas com os resultados da plotagem
        plt.show()

    def plot_output_simulation(self):

        # Plota os gráficos das funções de saída com o valor da simulação
        self._heater.view(sim = self._simulation)
        self._chiller.view(sim = self._simulation)

        # Exibe as janelas com os resultados da plotagem
        plt.show()