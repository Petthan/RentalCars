from datetime import datetime, timedelta
from dateutil.parser import parse

def validate_date(date):
    try:
        date = parse(date)
    except ValueError as vex:
        raise ValueError(f"Cant validate date {date}")
    return date

def validate_days(days):
    try:
        days = int(days)
    except ValueError as vex:
        raise ValueError(f"Cant convert days to integer {days}")
    if days < 1:
        raise ValueError("Days cant be lower than 1")
    return timedelta(days=days)

def validate_birthdate(birthdate):
    today = datetime.now()
    try:
        #birthdate = datetime.strptime(birthdate, "%Y/%m/%d")
        birthdate = parse(birthdate)
    except ValueError as vex:
        raise ValueError(f"Cant validate date {birthdate}")
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    print(age)
    if age < 18:
        raise ValueError(f"Not old enough")
    return birthdate

def validate_name(name):
    if not name:
        raise ValueError("Must contain a name")
    return str(name)