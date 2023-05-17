import requests
from datetime import datetime
from smtplib import SMTP,SMTPAuthenticationError
from time import sleep

# ------------------------------- CONSTANTS ---------------------------- #
MY_LAT = 51.507351 # Enter your latitude
MY_LONG = -0.127758 # Enter your longitude
SENDER_EMAIL = " " # Enter your Email id here
SENDER_PASSWORD = " " # Enter you password here
RECIEVER_EMAIL = " " # Reciever Email id here
SMTP_CODE = "smtp.gmail.com" # Change to your specific host code

def is_iss_overhead():
    """Returns True is ISS is overhead to our location"""
    global MY_LAT,MY_LONG
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_data = response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

    
def is_night():
    """Checks with given Coords if it is day/night at that location
    and Returns True if it is Night Time."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sun_data = response.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    if time_now.hour() >= sunset and time_now.hour != sunrise:
        return True
    elif time_now.hour >= sunrise and time_now.hour != sunset:
        return False


def send_mail():
    """Sends Email using the SMTP module of python"""
    try:
        with SMTP(SMTP_CODE) as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL,password=SENDER_PASSWORD)
            connection.sendmail(from_addr=SENDER_EMAIL,to_addrs=RECIEVER_EMAIL,msg="Subject:ISS is Passing Over your Head\n\nLook Up,Check your Night Sky NOW!!.")
    except SMTPAuthenticationError:
        print("Authentication Error!\nPlease check if your Email and Password and correct.")
        pass


while is_iss_overhead == True and is_night == True:
    send_mail()
    sleep(60)