# Navi The Helper: Email Notification Service

## What is it?

Navi The Helper is a lightweight, containerized email notification service built with Python and Flask. It provides a simple HTTP endpoint that allows any application to send email notifications through Gmail's SMTP server.

## Problem it Solves

Many applications need to send notifications, but implementing email functionality can be complex and time-consuming. This service solves several common problems:

1. **Decoupled Notification System**: Instead of building email functionality into each application, you can use this service as a standalone notification system.
2. **Simple Integration**: Any application that can make HTTP requests can send emails through this service.
3. **Reliable Delivery**: Built-in retry logic ensures reliable email delivery.
4. **Easy Deployment**: Containerized with Docker and ready for Google Cloud Run deployment.

## Setup Guide

### Prerequisites
- Docker installed on your machine
- A Gmail account
- Google Cloud account (for Cloud Run deployment)
- Google Cloud CLI installed (for deployment)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jeremiahoclark/navithehelper.git
   cd navithehelper
   ```

2. Create your environment file:
   ```bash
   cp .env.template .env
   ```

3. Configure your `.env` file:
   - Set `GMAIL_ADDRESS` to your Gmail address
   - Set `GMAIL_PASSWORD` to your Gmail app password (See "Gmail Setup" below)
   - Set `RECIPIENT_EMAIL` to your default recipient email

4. Build and run the Docker container:
   ```bash
   docker build -t navithehelper .
   docker run -p 8080:8080 --env-file .env navithehelper
   ```

### Gmail Setup

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password:
   - Go to Google Account settings
   - Navigate to Security
   - Under "2-Step Verification", click on "App passwords"
   - Generate a new app password for "Mail"
   - Use this password in your `.env` file

### Cloud Run Deployment

1. Initialize Google Cloud project:
   ```bash
   gcloud init
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy navithehelper \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="GMAIL_ADDRESS=your-email@gmail.com,GMAIL_PASSWORD=your-app-password,RECIPIENT_EMAIL=default-recipient@gmail.com"
   ```

## Usage

Send an email using curl:
```bash
curl -X POST http://localhost:8080/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test Email",
    "body": "This is a test email",
    "recipient_email": "recipient@example.com"
  }'
```

The `recipient_email` field is optional. If not provided, it will use the default recipient from your environment variables.

## Security Considerations

- Never commit your `.env` file or expose your Gmail app password
- When deploying to production, consider adding authentication to the endpoint
- Use HTTPS for all production requests
- Regularly rotate your Gmail app password

## Contributing

Feel free to open issues or submit pull requests. All contributions are welcome! 