import requests
from datetime import datetime
import smtplib
import time


my_lat = 46.164059
my_long = 15.869980
my_lat_range = (41,51)
my_long_range = (10,20)

my_location = {
    "lat":my_lat,
    "lng":my_long,
    "formatted":0
}

def iss_overhead():

    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_longitude = iss_data["iss_position"]["longitude"]
    iss_latitude = iss_data["iss_position"]["latitude"]
    #print (iss_latitude + " " + iss_longitude)
    if float(iss_latitude) > my_lat_range[0] and float(iss_latitude) < my_lat_range[1] and float(iss_longitude) > my_long_range[0] and float(iss_longitude) < my_long_range[1]:
        return True
    else:
        return False


def dark_outside():
    sunrise_response = requests.get(url=f"https://api.sunrise-sunset.org/json", params = my_location)
    sunrise_response.raise_for_status()
    sunrise = sunrise_response.json()["results"]["sunrise"]
    sunset = sunrise_response.json()["results"]["sunset"]
    rise = sunrise.split("T")[1].split(":")[0]
    s_set = sunset.split("T")[1].split(":")[0]
    time_now = datetime.now().hour
    
    if int(time_now) > int(s_set) + 1 or int(time_now) < int(rise) + 1:
        return True
    else:
        return False 



my_email = "andro.miljan@yahoo.com"
my_password = "zkhtxylmoeiiijeo"
primatelji = ["andro.miljan@gmail.com"]
message = f'''Subject: ISS je u blizini!\n\n
Zdravo Andro,

Mrak je, pa ono, pogledaj i vidi dal se vidi. PC


Pozdravi!
'''

message2 = f'''Subject: ISS je u blizini!\n\n
Zdravo Andro,

Nije mrak pa se ne vidi al ono, fyi. PC


Pozdravi!
'''




def send_mail(text):
    for adresa in primatelji:
        veza = smtplib.SMTP("smtp.mail.yahoo.com",587)
        veza.starttls()
        veza.login(user=my_email,password=my_password)
        veza.sendmail(my_email,adresa,text)
        veza.quit()


while True:
    if dark_outside() and iss_overhead():
        send_mail(message)
    elif iss_overhead() and dark_outside() == False:
        send_mail(message2)
    else:
        print(datetime.now())
    time.sleep(60)


