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
            'maxpoints': 200
        }
    }], filename=plotly_user_config['filename'], fileopt='overwrite', auto_open=False)

print "Olcum baslatiliyor..."

stream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
stream.open() #yayin baslatilir

while True:
    GPIO.setmode(GPIO.BOARD)

    TRIG = 7
    ECHO = 12

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.output(TRIG,0)

    GPIO.setup(ECHO,GPIO.IN)

    time.sleep(0.1)

    print "Bu linkten yayinlanan grafige ulasabilirsiniz: ", url
# 10 uS lir bir darbe sinyali gonderilir #
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

# Ve gelen yansimanin gecikmesi olculur #
    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        stop = time.time()

# Ses hizina gore islem yapildiginda cm cinsinden uzaklik asagidaki gibi hesaplanir #
    uzaklik = (stop - start) * 17150

    print str(uzaklik) + " cm"
    
    if uzaklik > 2 and uzaklik < 400:
        # veri plotly ye yazilir
        stream.write({'x': datetime.datetime.now(), 'y': uzaklik})

    GPIO.cleanup()
