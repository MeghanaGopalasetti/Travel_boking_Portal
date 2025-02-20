from django.contrib import admin
from .models import Flight , Hotel,TravelPackage,UserProfile

# Register your models here.
admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(TravelPackage)
admin.site.register(UserProfile)
