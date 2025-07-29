from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from trading_portfolio.models import UserProfile


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    def get_account_balance(self, obj):
        return obj.profile.account_balance if hasattr(obj, 'profile') else 'no profile'
    get_account_balance.short_description = 'Balance'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

