from django.contrib import admin
from .models import Employee, Program, Company, Decree

# Register your models here.

admin.site.register(Employee)
admin.site.register(Program)
admin.site.register(Company)
admin.site.register(Decree)
