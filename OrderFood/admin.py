from django.contrib import admin

# Register your models here.
from OrderFood.models import *

admin.site.register(Food)
admin.site.register(FoodType)
admin.site.register(FoodCategory)
admin.site.register(Team)
admin.site.register(Department)
admin.site.register(Restaurant)
admin.site.register(Orderlist)
admin.site.register(Contact)
admin.site.register(Taste)