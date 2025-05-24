from django.contrib import admin
from .models import IDBackground, AlumniProfile

@admin.register(IDBackground)
class IDBackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)

@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('school_id', 'first_name', 'last_name', 'year_graduated', 'email')
    list_filter = ('year_graduated', 'created_at')
    search_fields = ('school_id', 'first_name', 'last_name', 'email')
