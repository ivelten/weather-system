import artc
import iot
import time

control = artc.ARTC()
bmp280  = iot.BMP280Monitor()

while True:

    # Obtém a temperatura, pressão e umidade
    temperature = round(bmp280.get_temperature(), 2)
    pressure = round(bmp280.get_pressure(), 2)
    humidity = round(75.0, 2) # TODO: ajustar para medir apropriadamente quando o sensor de umidade chegar

    # Exibe as medições na tela
    print ("Temperature:     {:.2f} *C".format(temperature))
    print ("Pressure:        {:.2f} hPa".format(pressure))
    print ("Humidity:        {:.2f} %".format(humidity))

    # Computa a simulação para definir a intensidade do aquecedor e refrigerador
    control.compute_simulation(temperature, pressure, humidity)

    # Exibe os resultados na tela
    print ("Chiller Potency: {:.0f} %".format(control.chiller_potency))
    print ("Heater Potency:  {:.0f} %".format(control.heater_potency), end = '\n\n')

    # TODO: procurar um aquecedor e refrigerador para testar os resultados
    time.sleep(30)