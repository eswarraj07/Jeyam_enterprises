# Jeyam Enterprises Website Deployment Guide

This guide provides instructions for deploying the Jeyam Enterprises website to a production environment and configuring DNS.

## Preparation

1. Make sure you have all the required files:
   - Django project code
   - requirements.txt
   - Procfile
   - runtime.txt
   - .env file (create this from .env.example)

2. Create a `.env` file with your production settings:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual production values.

## Deployment Options

### Option 1: Deploying to Heroku

1. Install the Heroku CLI and log in:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create jeyam-enterprises
   ```

3. Add a PostgreSQL database:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Configure environment variables:
   ```
   heroku config:set DJANGO_SECRET_KEY=your-secret-key
   heroku config:set DJANGO_DEBUG=False
   heroku config:set ALLOWED_HOSTS=jeyam-enterprises.herokuapp.com,yourdomain.com
   ```
   
   Set email configuration:
   ```
   heroku config:set EMAIL_HOST=smtp.example.com
   heroku config:set EMAIL_PORT=587
   heroku config:set EMAIL_USE_TLS=True
   heroku config:set EMAIL_HOST_USER=your-email@example.com
   heroku config:set EMAIL_HOST_PASSWORD=your-email-password
   heroku config:set DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   heroku config:set CONTACT_EMAIL=info@yourdomain.com
   ```

5. Deploy your code:
   ```
   git add .
   git commit -m "Prepare for deployment"
   git push heroku main
   ```

6. Run migrations:
   ```
   heroku run python manage.py migrate
   ```

7. Create a superuser:
   ```
   heroku run python manage.py createsuperuser
   ```

8. Collect static files:
   ```
   heroku run python manage.py collectstatic --noinput
   ```

### Option 2: Deploying to a VPS (e.g., DigitalOcean, AWS EC2, etc.)

1. Set up a server with Ubuntu/Debian:
   - Create a new droplet/instance
   - SSH into your server

2. Install required packages:
   ```
   sudo apt update
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
   ```

3. Create a PostgreSQL database:
   ```
   sudo -u postgres psql
   CREATE DATABASE jeyam_db;
   CREATE USER jeyam_user WITH PASSWORD 'your_password';
   ALTER ROLE jeyam_user SET client_encoding TO 'utf8';
   ALTER ROLE jeyam_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE jeyam_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE jeyam_db TO jeyam_user;
   \q
   ```

4. Clone your repository:
   ```
   git clone https://github.com/yourusername/jeyam_enterprises.git
   cd jeyam_enterprises
   ```

5. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. Create and configure your .env file:
   ```
   cp .env.example .env
   nano .env
   ```

7. Run migrations and collect static files:
   ```
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

8. Set up Gunicorn:
   Create a systemd service file:
   ```
   sudo nano /etc/systemd/system/gunicorn.service
   ```
   
   Add the following content:
   ```
   [Unit]
   Description=gunicorn daemon
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/jeyam_enterprises
   ExecStart=/home/ubuntu/jeyam_enterprises/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/jeyam_enterprises/jeyam_enterprises.sock jeyam_enterprises.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

9. Start and enable Gunicorn:
   ```
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   ```

10. Configure Nginx:
    ```
    sudo nano /etc/nginx/sites-available/jeyam_enterprises
    ```
    
    Add the following content:
    ```
    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        
        location /static/ {
            root /home/ubuntu/jeyam_enterprises;
        }
        
        location /media/ {
            root /home/ubuntu/jeyam_enterprises;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/jeyam_enterprises/jeyam_enterprises.sock;
        }
    }
    ```

11. Enable the site and restart Nginx:
    ```
    sudo ln -s /etc/nginx/sites-available/jeyam_enterprises /etc/nginx/sites-enabled
    sudo systemctl restart nginx
    ```

12. Set up SSL with Let's Encrypt:
    ```
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

## DNS Configuration

To configure DNS for your domain name:

1. Purchase a domain name from a domain registrar (e.g., GoDaddy, Namecheap, Google Domains).

2. Configure DNS records to point to your hosting provider:

   ### For Heroku:
   
   Add the following DNS records at your domain registrar:
   
   - Type: CNAME
   - Name: www
   - Value: jeyam-enterprises.herokuapp.com
   
   For the root domain (apex domain):
   
   - Type: ALIAS or ANAME (if supported by your registrar)
   - Name: @
   - Value: jeyam-enterprises.herokuapp.com
   
   If ALIAS/ANAME is not supported, use:
   
   - Type: A
   - Name: @
   - Value: 75.101.163.44 (Heroku's IP address)
   
   ### For VPS:
   
   Add the following DNS records:
   
   - Type: A
   - Name: @
   - Value: [Your server's IP address]
   
   - Type: A
   - Name: www
   - Value: [Your server's IP address]

3. Configure your domain in Heroku (if using Heroku):
   ```
   heroku domains:add yourdomain.com
   heroku domains:add www.yourdomain.com
   ```

4. Wait for DNS propagation (can take up to 48 hours, but usually much faster).

## Post-Deployment Tasks

1. Test your website thoroughly after deployment.

2. Set up regular database backups.

3. Configure monitoring for your application.

4. Set up a content delivery network (CDN) for better performance (optional).

## Troubleshooting

- Check application logs:
  - Heroku: `heroku logs --tail`
  - VPS: Check `/var/log/nginx/error.log` and your application logs

- Verify DNS configuration:
  - Use tools like `dig` or `nslookup` to check DNS records
  - Example: `dig yourdomain.com`

- SSL issues:
  - Ensure certificates are properly installed and renewed
  - Check SSL configuration in Nginx or your web server

For additional help, refer to the documentation of your hosting provider or contact their support.