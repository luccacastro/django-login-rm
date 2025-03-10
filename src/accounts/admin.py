from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from accounts.models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "birth_date")
    search_fields = ("user__email", "school__name")