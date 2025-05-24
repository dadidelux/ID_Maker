from django.contrib import admin
from .models import IDBackground, AlumniProfile, College, Program

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    ordering = ('name',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'college', 'created_at', 'updated_at')
    list_filter = ('college',)
    search_fields = ('code', 'name', 'college__name')
    ordering = ('college', 'name')

@admin.register(IDBackground)
class IDBackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('school_id', 'first_name', 'last_name', 'college', 'program', 'year_graduated')
    list_filter = ('college', 'program', 'year_graduated')
    search_fields = ('school_id', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
