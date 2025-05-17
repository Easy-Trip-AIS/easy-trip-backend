from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Додаткові поля', {'fields': ('date_of_birth',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Додаткові поля', {'fields': ('date_of_birth',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# Клас кастомних токенів для аdmin
class MyOutstandingTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'jti', 'created_at', 'expires_at')
    search_fields = ('user__username', 'jti')

class MyBlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'blacklisted_at')
    search_fields = ('token__jti',)

# Знімаємо дефолтні OutstandingToken та BlacklistedToken
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)

# Реєструємо свої, для того щоб відобразити в admin панелі.
admin.site.register(OutstandingToken, MyOutstandingTokenAdmin)
admin.site.register(BlacklistedToken, MyBlacklistedTokenAdmin)