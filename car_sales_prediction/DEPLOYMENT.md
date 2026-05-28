# 🌐 Deployment Guide - Car Sales Price Prediction System

## Deploying to Production

This guide explains how to deploy your application to various cloud platforms.

---

## 1️⃣ Deploy to Heroku (Recommended - Free)

### Prerequisites
- Heroku Account (heroku.com)
- Git installed
- Heroku CLI installed

### Step 1: Create Heroku App
```bash
heroku login
heroku create your-app-name
```

### Step 2: Create Procfile
Create file named `Procfile` in project root:
```
web: gunicorn app:app
```

### Step 3: Install Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Step 4: Create Runtime.txt
```
python-3.10.0
```

### Step 5: Create .gitignore
```
*.pkl
*.pyc
__pycache__/
.env
venv/
```

### Step 6: Deploy
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Step 7: Configure Environment Variable
```bash
heroku config:set SECRET_KEY=your-secret-key
```

### Step 8: View App
```bash
heroku open
```

---

## 2️⃣ Deploy to AWS EC2

### Step 1: Launch EC2 Instance
- Choose Ubuntu 20.04 LTS
- t2.micro (free tier)
- Allow HTTP (80) and HTTPS (443)

### Step 2: Connect via SSH
```bash
ssh -i "key.pem" ubuntu@your-instance-ip
```

### Step 3: Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip mysql-server nginx gunicorn
```

### Step 4: Clone Project
```bash
git clone your-repo-url
cd car_sales_prediction
```

### Step 5: Install Python Packages
```bash
pip3 install -r requirements.txt
```

### Step 6: Configure Nginx
Create `/etc/nginx/sites-available/car_sales`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }

    location /static {
        alias /home/ubuntu/car_sales_prediction/static;
    }
}
```

### Step 7: Start Application
```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

---

## 3️⃣ Deploy to DigitalOcean

### Step 1: Create Droplet
- Choose Ubuntu 20.04
- Basic plan ($5/month)

### Step 2: Copy Project Files
```bash
scp -r car_sales_prediction root@your-ip:/var/www/
```

### Step 3: Install & Configure
Same as AWS EC2 steps 3-7

### Step 4: Setup Domain
- Point domain DNS to droplet IP
- Use Let's Encrypt for SSL

---

## 4️⃣ Deploy to PythonAnywhere (Easiest)

### Step 1: Create Account
Visit pythonanywhere.com

### Step 2: Upload Files
- Use web interface to upload files
- Or use Git

### Step 3: Configure Web App
- Add Python 3.9+ app
- Set working directory
- Upload files

### Step 4: Set Database
- Connect your MySQL database
- Update DB credentials in app.py

### Step 5: Run
- Click "Reload Web App"
- Your app runs at pythonanywhere.com

---

## Production Checklist

Before deploying:

### Security
- [ ] Change SECRET_KEY in app.py
- [ ] Set DEBUG = False
- [ ] Use HTTPS
- [ ] Add CSRF protection
- [ ] Validate all inputs
- [ ] Use environment variables for secrets

### Performance
- [ ] Optimize database queries
- [ ] Add database indexes
- [ ] Enable caching
- [ ] Minimize CSS/JS files
- [ ] Use CDN for static files
- [ ] Enable gzip compression

### Database
- [ ] Backup database regularly
- [ ] Use strong passwords
- [ ] Restrict database access
- [ ] Enable SSL connections
- [ ] Monitor database usage

### Monitoring
- [ ] Setup error logging
- [ ] Monitor server resources
- [ ] Track user analytics
- [ ] Setup uptime monitoring
- [ ] Configure alerts

---

## Environment Variables

Create `.env` file (don't commit to git):
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key
DB_USER=root
DB_PASSWORD=ben10
DB_HOST=db.example.com
DB_NAME=car_sales_db
```

Update app.py to read:
```python
import os
from dotenv import load_dotenv

load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
```

---

## Database Migration to Cloud

### Backup Current Database
```bash
mysqldump -u root -pben10 car_sales_db > backup.sql
```

### Restore to Cloud Database
```bash
mysql -h cloud-db-host -u root -pben10 car_sales_db < backup.sql
```

---

## Troubleshooting Deployment

### Application not starting
- Check error logs
- Verify all packages installed
- Check model.pkl exists

### Database connection failed
- Verify credentials
- Check host/port
- Ensure firewall allows access

### Static files not loading
- Check file permissions
- Verify static/ folder exists
- Configure web server correctly

### SSL certificate issues
- Use Let's Encrypt (free)
- Update HTTPS configuration
- Force HTTPS redirect

---

## Cost Considerations

| Platform | Price | Notes |
|----------|-------|-------|
| Heroku | Free-$7/month | Easy, free tier available |
| AWS EC2 | ~$5-20/month | t2.micro free for 1 year |
| DigitalOcean | $5+/month | Simple, affordable |
| PythonAnywhere | Free-$25/month | No setup needed |
| Azure | Pay-as-you-go | Free trial available |
| Google Cloud | Pay-as-you-go | Free tier included |

---

## Scaling Tips

As users grow:

1. **Database**
   - Use managed database (RDS, CloudSQL)
   - Add read replicas
   - Implement caching (Redis)

2. **Server**
   - Use load balancer
   - Multiple app instances
   - Auto-scaling groups

3. **Storage**
   - Use cloud storage (S3, GCS)
   - CDN for static files
   - Database backups

4. **Monitoring**
   - Track performance metrics
   - Setup auto-scaling alerts
   - Monitor database usage

---

## Maintenance Tasks

### Daily
- Monitor error logs
- Check application health
- Review user feedback

### Weekly
- Backup database
- Review performance metrics
- Update security patches

### Monthly
- Analyze user behavior
- Optimize slow queries
- Review costs

### Quarterly
- Retrain ML model
- Update dependencies
- Security audit

---

Good luck with your deployment! 🚀
