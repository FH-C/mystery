import time
from datetime import datetime, timedelta

d = datetime.today().date() - timedelta(days=2)
print(str(d))
dt = int(time.mktime(time.strptime(str(d), '%Y-%m-%d')))

print(dt)
