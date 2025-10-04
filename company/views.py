from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CompanyInfo, Service, TeamMember, Testimonial
from .forms import ContactForm

def home(request):
    """View for the home page"""
    # Get data for the home page
    services = []
    testimonials = []
    
    try:
        services = Service.objects.all()[:3]  # Display only 3 services on home page
    except Exception as e:
        print(f"Error fetching services for home page: {e}")
    
    try:
        testimonials = Testimonial.objects.all()[:3]  # Display only 3 testimonials
    except Exception as e:
        print(f"Error fetching testimonials for home page: {e}")
    
    context = {
        'services': services,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    """View for the about page"""
    # Get company information and team members
    company_info = None
    try:
        company_info = CompanyInfo.objects.first()
    except Exception as e:
        print(f"Error fetching company info: {e}")
    
    team_members = []
    try:
        team_members = TeamMember.objects.all()
    except Exception as e:
        print(f"Error fetching team members: {e}")
    
    context = {
        'company_info': company_info,
        'team_members': team_members,
    }
    return render(request, 'about.html', context)

def services(request):
    """View for the services page"""
    # Get all services
    services = []
    try:
        services = Service.objects.all()
    except Exception as e:
        print(f"Error fetching services: {e}")
    
    context = {
        'services': services,
    }
    return render(request, 'services.html', context)

def team(request):
    """View for the team page"""
    # Get all team members
    team_members = []
    try:
        team_members = TeamMember.objects.all()
        
        # Separate leadership team (first 3 members) from other team members
        leadership_team = team_members[:3]
        other_team_members = team_members[3:]
    except Exception as e:
        print(f"Error fetching team members: {e}")
        leadership_team = []
        other_team_members = []
    
    context = {
        'leadership_team': leadership_team,
        'team_members': other_team_members,
    }
    return render(request, 'team.html', context)

def contact(request):
    """View for the contact page with form handling"""
    # Get company information for contact details
    company_info = None
    try:
        company_info = CompanyInfo.objects.first()
    except Exception as e:
        print(f"Error fetching company info: {e}")
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
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
            except Exception as e:
                print(f"Error saving contact form: {e}")
                messages.error(request, "There was an error sending your message. Please try again later.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'company_info': company_info,
    }
    return render(request, 'contact.html', context)
