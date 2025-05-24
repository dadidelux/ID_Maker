from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import IDBackground, AlumniProfile
from .forms import IDBackgroundForm, AlumniProfileForm

def home(request):
    return render(request, 'alumni_id/home.html')

def upload_background(request):
    if request.method == 'POST':
        form = IDBackgroundForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'ID Background uploaded successfully!')
            return redirect('background_list')
    else:
        form = IDBackgroundForm()
    
    return render(request, 'alumni_id/upload_background.html', {'form': form})

def background_list(request):
    backgrounds = IDBackground.objects.filter(is_active=True)
    return render(request, 'alumni_id/background_list.html', {'backgrounds': backgrounds})

def register_alumni(request):
    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumni profile created successfully!')
            return redirect('alumni_list')
    else:
        form = AlumniProfileForm()
    
    return render(request, 'alumni_id/register_alumni.html', {'form': form})

def alumni_list(request):
    alumni = AlumniProfile.objects.all()
    return render(request, 'alumni_id/alumni_list.html', {'alumni': alumni})

def view_id_card(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    return render(request, 'alumni_id/view_id_card.html', {
        'alumni': alumni
    })
