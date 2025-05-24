# Deployment Guide for ID Maker

## Prerequisites
- Python 3.8+
- PostgreSQL database
- Domain name with SSL certificate
- SMTP server access for emails
- Google OAuth credentials

## Step 1: Environment Setup

1. Create a `.env` file in your project root with the following variables:
```
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=ID_Maker.settings_prod
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings
DB_NAME=id_maker_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Google OAuth settings
GOOGLE_OAUTH2_CLIENT_ID=your-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
```

## Step 2: Database Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE id_maker_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE id_maker_db TO your_db_user;
```

## Step 3: Application Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Collect static files:
```bash
python manage.py collectstatic --no-input
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

## Step 4: Running in Production

1. Test the production settings:
```bash
python manage.py check --deploy
```

2. Run with Gunicorn:
```bash
gunicorn ID_Maker.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-file -
```

## Step 5: Nginx Configuration (Optional)

If using Nginx as a reverse proxy, use this configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project/staticfiles;
    }

    location /media/ {
        root /path/to/your/project/media;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## Security Considerations

1. Always use HTTPS in production
2. Keep your `.env` file secure and never commit it to version control
3. Regularly update dependencies
4. Set up regular database backups
5. Monitor your application logs
6. Use strong passwords for database and admin accounts

## Monitoring and Maintenance

1. Set up error tracking (e.g., Sentry)
2. Configure logging
3. Set up automated backups
4. Monitor server resources
5. Set up uptime monitoring

## Troubleshooting

1. Check logs using:
```bash
tail -f gunicorn-error.log
```

2. Verify static files:
```bash
python manage.py collectstatic --dry-run
```

3. Test email configuration:
```bash
python manage.py sendtestemail admin@example.com
``` 