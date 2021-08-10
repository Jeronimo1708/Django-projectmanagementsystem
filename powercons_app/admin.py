from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminUser, Staffs, Projects, Tasks, Clients, Contracts, Suppliers, Services, Parts, Payments


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)

admin.site.register(AdminUser)
admin.site.register(Staffs)
admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Clients)
admin.site.register(Contracts)
admin.site.register(Suppliers)
admin.site.register(Services)
admin.site.register(Parts)
admin.site.register(Payments)

