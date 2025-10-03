from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CompanyInfo, Service, TeamMember, Testimonial
from .forms import ContactForm

def home(request):
    """View for the home page"""
    # Get data for the home page
    services = Service.objects.all()[:3]  # Display only 3 services on home page
    testimonials = Testimonial.objects.all()[:3]  # Display only 3 testimonials
    
    context = {
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    """View for the about page"""
    # Get company information and team members
    try:
        company_info = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company_info = None
    
    team_members = TeamMember.objects.all()
    
    context = {
        'company_info': company_info,
        'team_members': team_members,
    }
    return render(request, 'about.html', context)

def services(request):
    """View for the services page"""
    # Get all services
    services = Service.objects.all()
    
    context = {
        'services': services,
    }
    return render(request, 'services.html', context)

def team(request):
    """View for the team page"""
    # Get all team members
    team_members = TeamMember.objects.all()
    
    # Separate leadership team (first 3 members) from other team members
    leadership_team = team_members[:3]
    other_team_members = team_members[3:]
    
    context = {
        'leadership_team': leadership_team,
        'team_members': other_team_members,
    }
    return render(request, 'team.html', context)

def contact(request):
    """View for the contact page with form handling"""
    # Get company information for contact details
    try:
        company_info = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company_info = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            contact_message = form.save()
            
            # Send email notification (if email settings are configured)
            try:
                subject = f"New Contact Message: {contact_message.subject}"
                message = f"""
                Name: {contact_message.name}
                Email: {contact_message.email}
                Phone: {contact_message.phone}
                
                Message:
                {contact_message.message}
                """
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.CONTACT_EMAIL] if hasattr(settings, 'CONTACT_EMAIL') else [settings.DEFAULT_FROM_EMAIL]
                
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Log the error but don't show it to the user
                print(f"Email sending failed: {e}")
            
            # Show success message and redirect
            messages.success(request, "Your message has been sent successfully. We'll get back to you soon!")
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'company_info': company_info,
    }
    return render(request, 'contact.html', context)
