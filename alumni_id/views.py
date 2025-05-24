from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import IDBackground, AlumniProfile, College, Program
from .forms import IDBackgroundForm, AlumniProfileForm
from .utils import generate_id_card
from django.db import models

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
    search_query = request.GET.get('search', '')
    year_filter = request.GET.get('year', '')
    college_filter = request.GET.get('college', '')
    program_filter = request.GET.get('program', '')
    
    alumni = AlumniProfile.objects.all()
    
    # Apply filters
    if search_query:
        alumni = alumni.filter(
            models.Q(school_id__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(company__icontains=search_query)
        )
    
    if year_filter:
        alumni = alumni.filter(year_graduated=year_filter)
    
    if college_filter:
        alumni = alumni.filter(college_id=college_filter)
    
    if program_filter:
        alumni = alumni.filter(program_id=program_filter)
    
    # Get unique years for the filter dropdown
    years = AlumniProfile.objects.values_list('year_graduated', flat=True).distinct().order_by('-year_graduated')
    colleges = College.objects.all().order_by('name')
    programs = Program.objects.all().order_by('college__name', 'name')
    
    return render(request, 'alumni_id/alumni_list.html', {
        'alumni': alumni,
        'search_query': search_query,
        'years': years,
        'colleges': colleges,
        'programs': programs,
        'selected_year': year_filter,
        'selected_college': college_filter,
        'selected_program': program_filter,
    })

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

@login_required
def edit_alumni(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    
    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alumni profile updated successfully!')
            return redirect('alumni_list')
    else:
        form = AlumniProfileForm(instance=alumni)
    
    return render(request, 'alumni_id/edit_alumni.html', {
        'form': form,
        'alumni': alumni
    })

@login_required
def delete_alumni(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    
    if request.method == 'POST':
        # Get the confirmation ID from the form
        confirmation_id = request.POST.get('confirmation_id')
        
        # Check if the entered ID matches the alumni's school ID
        if confirmation_id == alumni.school_id:
            alumni.delete()
            messages.success(request, 'Alumni record deleted successfully!')
            return redirect('alumni_list')
        else:
            messages.error(request, 'The entered ID does not match. Deletion cancelled.')
            return redirect('alumni_list')
    
    return render(request, 'alumni_id/delete_alumni.html', {
        'alumni': alumni
    })
