from fastapi import Depends
import logging,httpx,db
from datetime import date, timedelta,datetime
from enum import Enum
from passlib.context import CryptContext
from models import MedicineReminder
from firebase_admin import credentials, messaging, initialize_app


pwdContext = CryptContext(schemes=["bcrypt"], deprecated ="auto")

fdm = credentials.Certificate("push-messaging.json")
initialize_app(fdm)

logging.basicConfig(level=logging.INFO)

def hash(password:str):
    return pwdContext.hash(password)

def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)



class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

def current_date(day):
    input_day = Day[day.upper()]
    print(input_day)
    today = date.today()
    current_week_date = today - timedelta(days=today.weekday() - input_day.value)
    return current_week_date

def next_date(day):
    input_day = Day[day.upper()]
    today = date.today()
    days_until_next_day = (input_day.value - today.weekday() + 7) % 7
    next_week_date = today + timedelta(days=days_until_next_day)
    return next_week_date

def convert_double_to_time(time):
    hours = int(time)
    minutes = int((time - hours) * 100)

    if hours >= 12:
        if hours > 12:
            hours -= 12
        return time(hours, minutes).replace(hour=12, minute=minutes, second=0)
    else:
        return time(hours, minutes, second=0)

def convert_time_to_double(local_time):
    hours = local_time.hour
    minutes = local_time.minute

    time_in_double = hours + (minutes / 100.0)

    return time_in_double

def convert_string_to_local_time(time_string):
    local_time = datetime.strptime(time_string, "%H:%M").time()
    return local_time


def convert_int_to_day(days):
    day_map = {
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday"
    }

    part = days.split(",")
    day_list = [day_map[i] for i in part if i in day_map]

    return day_list


def convert_string_to_local_time(time_string):
    time_format = "%H:%M" 
    
    try:
        local_time = datetime.strptime(time_string, time_format).time()
        return local_time
    except ValueError:
        return None


async def send_message(medicine: str, time: str,api_key:str):
   
    fcm_message = messaging.Message(
        notification=messaging.Notification(
            title='Push Notification',
            body=f"Time to take {medicine} at {time}"
        ),
        token=api_key
    )
    try:
      
        response = messaging.send(fcm_message)
        print("Notification sent successfully!")
        return {"message": "Notification sent successfully", "response": response}
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
   
    

async def sendSingleMedicineReminder(medicineReminder:MedicineReminder):
    time = convert_string_to_local_time(medicineReminder.time).strftime("%H:%M")
  
    days = convert_int_to_day(medicineReminder.days)
    current_time = datetime.now().strftime("%H:%M")
   

    for day in days:
        current_day = datetime.now().strftime("%A")
        if day.upper()==current_day.upper() and time == current_time:
            try:
                await send_message(medicineReminder.description, medicineReminder.time, medicineReminder.api_key)
            except:

                logging.info("Error sending message")

async def sendMedincineReminders():
    db_current = db.SessionLocal()
    medicineReminders = db_current.query(MedicineReminder).all()
    for medicineReminder in medicineReminders:
        await sendSingleMedicineReminder(medicineReminder)

    

