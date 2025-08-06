from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from trading_portfolio.models import UserProfile, Asset, Portfolio, Transaction, PortfolioPosition


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

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'asset_type')
    search_fields = ('symbol', 'name')
    list_filter = ('asset_type',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at')
    search_fields = ('user__username',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'asset', 'transaction_type', 'quantity', 'price', 'timestamp')
    list_filter = ('transaction_type', 'asset__symbol')
    search_fields = ('portfolio__user__username', 'asset__symbol')

@admin.register(PortfolioPosition)
class PortfolioPositionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'asset', 'quantity')
    search_fields = ('portfolio__user__username', 'asset__symbol')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)

