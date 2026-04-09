from datetime import date, timedelta , datetime
#1
today = date.today()
new_date = today - timedelta(days=5)
print(new_date)

#2
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("yesterday:",yesterday)
print("today:",today)
print("tomorrow:",tomorrow)

#3
now = datetime.now()
without_m = now.replace(microsecond=0)
print(without_m)

#4
date1_str = input()
date2_str = input()

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

delta = date1 - date2

seconds = delta.total_seconds()
print(seconds)