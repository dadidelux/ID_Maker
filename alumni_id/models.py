from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class IDBackground(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='id_backgrounds/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class College(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Program(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='programs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.college.code})"

    class Meta:
        ordering = ['college', 'name']

class AlumniProfile(models.Model):
    school_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.PROTECT, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True, blank=True)
    year_graduated = models.IntegerField()
    company = models.CharField(max_length=200, blank=True)
    validity_start = models.DateField()
    validity_end = models.DateField()
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    contact_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    
    photo = models.ImageField(upload_to='alumni_photos/')
    id_background = models.ForeignKey(IDBackground, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.school_id}"

    class Meta:
        ordering = ['-created_at']
