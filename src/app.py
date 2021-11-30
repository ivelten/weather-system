import artc
import iot
import time

control = artc.ARTC()
bmp280  = iot.BMP280Monitor()
dht11 = iot.DHT11Monitor()

while True:

    # Obtém a temperatura, pressão e umidade
    humidity, temperature1 = dht11.get_humidity_and_temperature()
    temperature2 = round(bmp280.get_temperature(), 2)
    pressure = round(bmp280.get_pressure(), 2)

    # Usa por padrão a temperatura do DHT11, caso não consiga, usa do BMP280
    temperature = round((temperature2 if temperature1 is None else temperature1), 2)

    # Exibe as medições na tela
    print ("Temperature:     {:.2f} *C".format(temperature))
    print ("Pressure:        {:.2f} hPa".format(pressure))
    print ("Humidity:        {:.2f} %".format(humidity))

    # Computa a simulação para definir a intensidade do aquecedor e refrigerador
    control.compute_simulation(temperature, pressure, humidity)

    # Exibe os resultados na tela
    print ("Chiller Potency: {:.0f} %".format(control.chiller_potency))
    print ("Heater Potency:  {:.0f} %".format(control.heater_potency), end = '\n\n')

    # Espera 30 segundos para continuar atualizando as medidas
    time.sleep(30)