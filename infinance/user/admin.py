from django.contrib import admin
from .models import Dashboard, Cards, Transactions, Reminder

# Register your models here.
admin.site.register(Dashboard)
admin.site.register(Cards)
admin.site.register(Transactions)
admin.site.register(Reminder)
