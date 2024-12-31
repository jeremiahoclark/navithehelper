import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

def send_email(subject, body, recipient_email):
    """
    Send an email using Gmail's SMTP server.
    """
    try:
        gmail_address = os.environ['GMAIL_ADDRESS']
        gmail_password = os.environ['GMAIL_PASSWORD']
        
        # Input validation
        if not all([subject, body, recipient_email]):
            raise ValueError("Missing required email fields")
            
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = gmail_address
        msg['To'] = recipient_email
        msg.set_content(body)
        
        # Add retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Connecting to Gmail SMTP server (attempt {attempt + 1})...")
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
                    smtp.login(gmail_address, gmail_password)
                    smtp.send_message(msg)
                logger.info("Email sent successfully.")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({"status": "healthy"}), 200

@app.route('/send-email', methods=['POST'])
def handle_send_email():
    """
    HTTP endpoint to send an email.
    Expects JSON payload with 'subject', 'body', and optionally 'recipient_email'.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload."}), 400
            
        # Extract and validate fields
        subject = data.get('subject', '').strip()
        body = data.get('body', '').strip()
        recipient_email = data.get('recipient_email', os.environ.get('RECIPIENT_EMAIL', '')).strip()
        
        # Validation
        if not subject:
            return jsonify({"error": "Subject cannot be empty"}), 400
        if not body:
            return jsonify({"error": "Body cannot be empty"}), 400
        if not recipient_email:
            return jsonify({"error": "Recipient email is required"}), 400
            
        send_email(subject, body, recipient_email)
        return jsonify({
            "message": "Email sent successfully",
            "recipient": recipient_email
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in /send-email endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)