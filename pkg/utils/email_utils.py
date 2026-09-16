import threading
from flask import current_app, render_template
from flask_mail import Message
from pkg import mail

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            # In a production app you'd log this properly
            print(f"Failed to send email: {e}")

def send_email(subject, recipient, template, **kwargs):
    """
    Sends an email asynchronously using Flask-Mail.
    """
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        recipients=[recipient]
    )
    msg.html = render_template(template, **kwargs)
    
    thread = threading.Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread

def send_welcome_email(user_name, user_email):
    """
    Sends a welcome email to a newly registered user.
    """
    return send_email(
        subject="Welcome to TalentBridge!",
        recipient=user_email,
        template="emails/welcome.html",
        user_name=user_name
    )

def send_order_confirmation(user_email, order_details):
    """
    Sends an order confirmation email.
    """
    return send_email(
        subject="Order Confirmation - TalentBridge",
        recipient=user_email,
        template="emails/order_confirmation.html",
        order_details=order_details
    )

def send_password_reset(user_email, reset_link):
    """
    Sends a password reset link.
    """
    return send_email(
        subject="Password Reset Request - TalentBridge",
        recipient=user_email,
        template="emails/password_reset.html",
        reset_link=reset_link
    )
