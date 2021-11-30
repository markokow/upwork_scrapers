# from selenium import webdriver

# driver = webdriver.Firefox()
# driver.get('https://byjus.com/question-answer/solve-int-frac-dx-x-sqrt-x/')
# screenshot = driver.save_screenshot('my_screenshot.png')
# driver.quit()

from datetime import datetime
import pytz

try:
  import lzma
except ImportError:
  from backports import lzma


tz = pytz.timezone('UTC')
naive_time = datetime.now()
tz_time = tz.localize(naive_time)
london_tz = pytz.timezone('Europe/London')
london_time = tz_time.astimezone(london_tz)
actual_time = london_time.time()

base = datetime.strptime('12:00', '%H:%M').time()

# print(naive_time)
# print(tz_time)
# print(actual_time)

london_dt = naive_time.astimezone(pytz.timezone('Europe/London')).time()

print(type(london_dt))

print(london_dt)

print(london_dt.hour)
print(london_dt.minute)
print(london_dt.second)