import RPi.GPIO as GPIO
import plotly.plotly as py # plotly kutuphanesi
import json # config.json dosyasini parse etmek icin kullanildi
import time # zamanlayici fonksiyornlari
import datetime # gecerli zamani logla ve grafige gonder

# Json formatinda kullanici bilgileri alinir ve plotly hesabina giris yapilir #
with open('./config.json') as config_file:
    plotly_user_config = json.load(config_file)
    py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

url = py.plot([
    {
        'x': [], 'y': [], 'type': 'scatter',
        'stream': {
            'token': plotly_user_config['plotly_streaming_tokens'][0],
            'maxpoints': 5000
        }
    }], filename=plotly_user_config['filename'], fileopt='overwrite', auto_open=False)

print "Olcum baslatiliyor..."

stream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
stream.open() #yayin baslatilir

while True:
    GPIO.setmode(GPIO.BOARD)

    LDR = 7

    GPIO.setup(LDR,GPIO.IN)

    time.sleep(1)

    print "Bu linkten yayinlanan grafige ulasabilirsiniz: ", url

# Isik olculur #
    durum = GPIO.input(LDR);    
    print durum;
    
    if durum == 0 or durum == 1:
        # veri plotly ye yazilir
        stream.write({'x': datetime.datetime.now(), 'y': durum})

    GPIO.cleanup()
