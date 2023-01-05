import serial
from firebase_admin import credentials,db,initialize_app
from geoloc import get_loc,date_time
from functools import cache

@cache
def init():
    cred = credentials.Certificate('Firebase.json')
    initialize_app(cred, {
        'databaseURL' : 'https://meteo-e33d4-default-rtdb.firebaseio.com/'
    })

def data():
    ref = db.reference('/')
    arduino = serial.Serial("/dev/ttyACM0", 9600)
    data = arduino.readline()
    value = str(data[0:len(data)].decode("utf-8"))
    list = value.split("X")
    final_list=[]
    for i in list:
        final_list.append(str(i).replace('\r\n',''))
    file = open("count.txt","r+")
    n=file.read()
    cli_ref = ref.child('Climat').child(n)
    cli_ref.set({
        "Temperature": final_list[1],
        "Humidité": final_list[0],
        "Pluie": final_list[2],
        "Localisation": get_loc(),
        "Date" : date_time()[0],
        "Heure" : date_time()[1]
    })
    file.seek(0)
    m = int(n)
    m += 1
    file.write(str(m))
    file.close()