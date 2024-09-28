"""
Admin forms for persona_integration.
"""
from django.contrib import admin

from persona_integration.models import UserPersonaAccount, VerificationAttempt


@admin.register(UserPersonaAccount)
class UserPersonaAccountAdmin(admin.ModelAdmin):
    fields = ['created', 'modified', 'external_user_id', 'user']


@admin.register(VerificationAttempt)
class VerificationAttemptAdmin(admin.ModelAdmin):
    fields = ['created', 'event_created_at', 'expiration_date', 'inquiry_id', 'modified', 'status', 'user']
    readonly_fields = ['created', 'event_created_at', 'modified',]
