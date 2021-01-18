from django.contrib import admin
from . models import Profile,Book
# Register your models here.
from django.contrib.admin import AdminSite

class BookAdmin(admin.ModelAdmin):
    list_display = ['book_id','book_name','book_author','avalaible','category']

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("books",)
    list_display = ['__str__','reg_no']
admin.site.register(Book,BookAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.AdminSite.site_header = "SGGS Library Admin"