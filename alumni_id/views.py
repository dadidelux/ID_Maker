from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import IDBackground, AlumniProfile
from .forms import IDBackgroundForm, AlumniProfileForm
from .utils import generate_id_card

@login_required
def home(request):
    return render(request, 'alumni_id/home.html')

@login_required
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

@login_required
def background_list(request):
    backgrounds = IDBackground.objects.filter(is_active=True)
    return render(request, 'alumni_id/background_list.html', {'backgrounds': backgrounds})

@login_required
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

@login_required
def alumni_list(request):
    alumni = AlumniProfile.objects.all()
    return render(request, 'alumni_id/alumni_list.html', {'alumni': alumni})

@login_required
def view_id_card(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    
    # Check if the request wants to download the image
    if request.GET.get('download') == 'true':
        # Generate the ID card
        id_card_image = generate_id_card(alumni)
        
        # Create the response
        response = HttpResponse(id_card_image.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="{alumni.school_id}_id_card.png"'
        return response
    
    # Regular view - show the ID card in the template
    return render(request, 'alumni_id/view_id_card.html', {
        'alumni': alumni
    })
