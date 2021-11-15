import requests
from datetime import datetime
import smtplib
import time

iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
iss_data = iss_response.json()
iss_longitude = iss_data["iss_position"]["longitude"]
iss_latitude = iss_data["iss_position"]["latitude"]


my_lat = 46.164059
my_long = 15.869980
my_lat_range = (41,51)
my_long_range = (10,20)
my_location = {
    "lat":my_lat,
    "lng":my_long,
    "formatted":0
}

sunrise_response = requests.get(url=f"https://api.sunrise-sunset.org/json", params = my_location)
sunrise_response.raise_for_status()
sunrise = sunrise_response.json()["results"]["sunrise"]
sunset = sunrise_response.json()["results"]["sunset"]
rise = sunrise.split("T")[1].split(":")[0]
s_set = sunset.split("T")[1].split(":")[0]

time_now = datetime.now().hour

my_email = "andro.miljan@yahoo.com"
my_password = "zkhtxylmoeiiijeo"
primatelji = ["andro.miljan@gmail.com"]
message = f'''Subject: ISS je u blizini!\n\n
Zdravo Andro,

ISS je upravo na koordinatama {iss_latitude},{iss_longitude}. Noć je, pa ono, škicni i vidi dal se vidi.

Pozdravi!
'''

test_message = f'''Subject: Stanica nije vidljiva\n\n

Nema trenutno ISSa, stanica je na: {iss_latitude},{iss_longitude}

Andro
'''

def send_mail(text):
    for adresa in primatelji:
        veza = smtplib.SMTP("smtp.mail.yahoo.com",587)
        veza.starttls()
        veza.login(user=my_email,password=my_password)
        veza.sendmail(my_email,adresa,text)
        veza.quit()


while True:
    if float(time_now) > float(s_set) + 1 or float(time_now) < float(rise) + 1:
        if iss_latitude in range(my_lat_range[0],my_lat_range[1]) and iss_longitude in range(my_long_range[0],my_long_range[1]):
            send_mail(message)
            time.sleep(600)
        else:
            time.sleep(180)
    else:
        time.sleep(180)
    


