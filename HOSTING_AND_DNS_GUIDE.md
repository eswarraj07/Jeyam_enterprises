# Hosting and DNS Configuration Guide for Jeyam Enterprises Website

This guide provides instructions for deploying the Jeyam Enterprises website to a hosting provider and configuring DNS.

## Deploying to a Hosting Provider

### Option 1: Shared Hosting (cPanel, Plesk, etc.)

1. **Prepare your project**:
   - Run `python manage.py collectstatic` to collect all static files
   - Create a production-ready settings file with `DEBUG = False`

2. **Upload your files**:
   - Upload your Django project files to the hosting server using FTP or the hosting control panel
   - Make sure to set the correct permissions (usually 755 for directories and 644 for files)

3. **Set up a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure the web server**:
   - Set up the web server (Apache or Nginx) to serve your Django application
   - Configure WSGI settings in your hosting control panel

5. **Set up the database**:
   - Create a MySQL or PostgreSQL database
   - Update your settings.py file with the database credentials
   - Run migrations: `python manage.py migrate`

6. **Create a superuser**:
   ```
   python manage.py createsuperuser
   ```

### Option 2: VPS or Cloud Hosting (DigitalOcean, AWS, etc.)

1. **Set up a server**:
   - Create a new VPS or cloud instance
   - Install required packages:
     ```
     sudo apt update
     sudo apt install python3-pip python3-dev libpq-dev postgresql nginx
     ```

2. **Set up PostgreSQL**:
   ```
   sudo -u postgres psql
   CREATE DATABASE jeyam_db;
   CREATE USER jeyam_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE jeyam_db TO jeyam_user;
   \q
   ```

3. **Deploy your Django project**:
   - Clone your repository or upload your files
   - Set up a virtual environment and install dependencies
   - Configure your settings.py for production
   - Run migrations and collect static files

4. **Set up Gunicorn**:
   - Install Gunicorn: `pip install gunicorn`
   - Create a systemd service file for Gunicorn
   - Start and enable the service

5. **Configure Nginx**:
   - Create an Nginx configuration file
   - Set up SSL with Let's Encrypt
   - Restart Nginx

### Option 3: Platform as a Service (Heroku, PythonAnywhere, etc.)

1. **Heroku**:
   - Install the Heroku CLI
   - Create a Procfile and runtime.txt
   - Push your code to Heroku
   - Set up environment variables
   - Add a PostgreSQL database

2. **PythonAnywhere**:
   - Upload your code or clone from a repository
   - Set up a virtual environment
   - Configure WSGI settings
   - Set up a database

## Configuring DNS

DNS (Domain Name System) connects your domain name to your hosting provider.

### Step 1: Purchase a Domain Name

Purchase a domain name from a domain registrar such as:
- Namecheap
- GoDaddy
- Google Domains
- Cloudflare Registrar

### Step 2: Configure DNS Records

The DNS configuration depends on your hosting provider:

#### For Shared Hosting or VPS:

1. **Log in to your domain registrar's dashboard**

2. **Find the DNS management section**

3. **Add the following DNS records**:
   
   For the www subdomain:
   - Type: A
   - Name: www
   - Value: Your server's IP address
   - TTL: 3600
   
   For the root domain:
   - Type: A
   - Name: @ (or leave blank)
   - Value: Your server's IP address
   - TTL: 3600

#### For Heroku:

1. **Add the following DNS records**:
   
   For the www subdomain:
   - Type: CNAME
   - Name: www
   - Value: your-app-name.herokuapp.com
   - TTL: 3600
   
   For the root domain:
   - Type: ALIAS or ANAME (if supported)
   - Name: @ (or leave blank)
   - Value: your-app-name.herokuapp.com
   - TTL: 3600

### Step 3: Wait for DNS Propagation

DNS changes can take time to propagate (anywhere from a few minutes to 48 hours).

### Step 4: Set Up SSL Certificate

For a professional website, it's essential to have HTTPS:

1. **Shared Hosting**: Use the SSL certificate provided by your hosting provider or install a Let's Encrypt certificate.

2. **VPS**: Use Let's Encrypt with Certbot:
   ```
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

3. **Heroku**: SSL is included with paid plans or you can use Cloudflare for free SSL.

## Maintenance Tips

1. **Regular Backups**: Set up automated backups for your database and files.

2. **Security Updates**: Keep your Django installation and all dependencies up to date.

3. **Monitoring**: Set up monitoring to be alerted of any downtime or issues.

4. **Performance Optimization**: Use caching, CDN, and other optimization techniques for better performance.

## Troubleshooting

- **Website not loading**: Check your web server logs and Django error logs.
- **Database connection issues**: Verify your database credentials and connection settings.
- **Static files not loading**: Make sure your static files are properly collected and served.
- **DNS issues**: Use tools like `dig` or online DNS checkers to verify your DNS configuration.