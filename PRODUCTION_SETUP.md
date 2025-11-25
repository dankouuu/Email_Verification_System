# Production Setup Guide: Email Verification System (AWS)

This guide will help you deploy your Django backend and React frontend to AWS for a secure, production-ready email verification system.

---

## 1. Backend (Django on AWS Elastic Beanstalk)

### a) Prepare Django for Production
- Set `DEBUG = False` in your Django settings.
- Set `ALLOWED_HOSTS` to your AWS domain (e.g., `['.elasticbeanstalk.com']`).
- Use a strong, unique `SECRET_KEY` (set as an environment variable).
- Use PostgreSQL (RDS) or another production database (not SQLite).
- Run:
  ```sh
  python3 manage.py collectstatic
  ```

### b) Install AWS CLI & EB CLI
```sh
pip install awsebcli --upgrade
aws configure
```

### c) Initialize Elastic Beanstalk
```sh
cd backend
eb init -p python-3.11 your-app-name
```
- Choose your AWS region.
- Set up SSH if you want.

### d) Create Environment & Deploy
```sh
eb create your-env-name
eb deploy
```

### e) Set Environment Variables in AWS Console
- Go to Elastic Beanstalk > Configuration > Software > Edit Environment Properties.
- Add:
  - `EMAIL_VERIFICATION_JWT_SECRET`
  - `EMAIL_VERIFICATION_JWT_EXPIRY`
  - `MAILGUN_API_KEY`
  - `MAILGUN_DOMAIN`
  - `MAILGUN_FROM_EMAIL`
  - `SECRET_KEY` (Django)
  - Database credentials

### f) (Optional) Set Up RDS for PostgreSQL
- In AWS Console, create an RDS PostgreSQL instance.
- Update your Django `DATABASES` setting to use RDS.

---

## 2. Frontend (React on AWS S3 + CloudFront)

### a) Build the Frontend
```sh
cd frontend
npm run build
```
- This creates a `dist/` folder with static files.

### b) Create S3 Bucket
- In AWS Console, create an S3 bucket (enable static website hosting).
- Upload the contents of `dist/` to the bucket.

### c) (Optional) Set Up CloudFront
- In AWS Console, create a CloudFront distribution pointing to your S3 bucket for global CDN and HTTPS.

### d) Update Verification Link
- In your Django backend, update the verification link to use your CloudFront/S3 domain instead of `localhost:5173`.

---

## 3. Update API URLs in Frontend
- In your React app, update API URLs to point to your deployed backend (Elastic Beanstalk domain).

---

## 4. (Optional) Domain & HTTPS
- Register a domain (Route 53) and point it to your CloudFront and Elastic Beanstalk environments.
- Set up SSL certificates (AWS Certificate Manager).

---

## 5. Monitoring & Maintenance
- Set up CloudWatch for logs and monitoring.
- Regularly update dependencies and monitor for security.

---

## 6. (Optional) Advanced Features
- Use Celery + Redis for async email sending.
- Add reCAPTCHA to prevent spam.
- Set up user authentication if needed.

