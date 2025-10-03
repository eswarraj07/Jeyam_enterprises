# Jeyam Enterprises Website

A professional website for Jeyam Enterprises built with Django, showcasing company information, services, team members, and contact functionality.

## Features

- Responsive design using Bootstrap 5
- Company information and about us page
- Services showcase
- Team members profiles
- Contact form with email notification
- Admin panel for content management

## Technology Stack

- Django 3.2
- Python 3.9
- Bootstrap 5
- PostgreSQL (production) / SQLite (development)
- Gunicorn (WSGI server)
- WhiteNoise (static files)

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/jeyam_enterprises.git
   cd jeyam_enterprises
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the website at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/

## Project Structure

- `company/` - Main Django app containing models, views, and forms
- `jeyam_enterprises/` - Project settings and configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `media/` - User-uploaded files

## Content Management

After setting up the project, use the Django admin panel to:

1. Add company information
2. Create services
3. Add team members
4. Manage testimonials
5. View contact form submissions

## Deployment

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.