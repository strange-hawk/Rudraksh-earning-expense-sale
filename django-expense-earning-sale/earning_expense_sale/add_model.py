import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "earning_expense_sale.settings")

import django
django.setup()
import string
from django.core.management import call_command

from earning.models import Earning
from sale.models import Sale
from faker import Faker
from expense.models import Expense
import random
import datetime



from earning.models import Earning


start_date = datetime.date(year=2021, month=3, day=15)
end_date = datetime.date(year=2021, month=3, day=31)
f = Faker()

'''
earning
for _ in range(50):
    d = ""
    for _ in range(10):
        d = d + random.choices(['1','2','3','4','5','6','7','8','9','0'])[0]
    Earning.objects.create(name=f.company(), mode=random.choices(['TRANSFER', 'CASH'])[0] , amount=round(random.random()*100000,2), area = f.city(), date=f.date_between(start_date=start_date, end_date=end_date))
'''
'''
sales
for _ in range(50):
    Sale.objects.create(name=f.company(), bill_no=''.join(random.choices(string.ascii_letters + string.digits, k=6)),amount=round(random.random()*100000,2), date=f.date_between(start_date=start_date, end_date=end_date), area=f.city())
'''
'''
for _ in range(50):
    Expense.objects.create(name=f.company(), amount=round(random.random()*100000,2),date=f.date_between(start_date=start_date, end_date=end_date))
''' 
