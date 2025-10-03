from django.db import models
from django.utils import timezone

class CompanyInfo(models.Model):
    """Model for storing company information"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company/logos/', blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Social media links
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Company Information"

class Service(models.Model):
    """Model for company services"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", blank=True)
    image = models.ImageField(upload_to='company/services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']

class TeamMember(models.Model):
    """Model for team members"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='company/team/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        ordering = ['order']

class Testimonial(models.Model):
    """Model for customer testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    photo = models.ImageField(upload_to='company/testimonials/', blank=True, null=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-date_sent']
