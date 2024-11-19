<<<<<<< HEAD
from django.utils.text import slugify

=======
import logging
from django.utils.text import slugify
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
import string
import random


<<<<<<< HEAD
def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return res


def generate_slug(text):
    new_slug = slugify(text)
    from home.models import BlogModel

    if BlogModel.objects.filter(slug=new_slug).first():
=======
def generate_random_string(N: int) -> str:
    """Generate a random string of uppercase letters and digits."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


def generate_slug(text: str) -> str:
    """Generate a unique slug for a given text."""
    new_slug = slugify(text)
    from home.models import Article

    if Article.objects.filter(slug=new_slug).first():
>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
        return generate_slug(text + generate_random_string(5))
    return new_slug


<<<<<<< HEAD
from django.conf import settings
from django.core.mail import send_mail


def send_mail_to_user(token, email):
    subject = f"Your account needs to be verified"
    message = f"Hi paste the link to verify account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
=======
# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def send_mail_to_user(email: str, token: str) -> bool:
    """Send a verification email to the user using an HTML template."""
    subject = "Your Account Needs to be Verified"
    verification_link = f"http://127.0.0.1:8000/verify/{token}"
    
    # Render the HTML template with context
    html_message = render_to_string('verify_account.html', {'verification_link': verification_link})
    plain_message = strip_tags(html_message)  # Create a plain text version of the email
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]  # Use the provided email

    try:
        logger.debug("Initiating email connection.")
        
        # Create the email message
        email_message = EmailMultiAlternatives(subject, plain_message, email_from, recipient_list)
        email_message.attach_alternative(html_message, "text/html")  # Attach the HTML version

        logger.debug("Email message created, attempting to send.")
        email_message.send()  # Send the email
        
        logger.info(f"Email successfully sent to {email}.")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        return False
    


def send_mail_to_admin(subject: str, message: str) -> bool:
    """Send an email to the admin with a message."""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]  # Use the admin email
    
    try:
        logger.debug("Initiating email connection.")
        
        # Create the email message
        email_message = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        
        logger.debug("Email message created, attempting to send.")
        email_message.send()  # Send the email
        
        logger.info(f"Email successfully sent to {recipient_list}.")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {e}")
        return False
    



def set_language(request):
    """Set the language preference for the user."""
    lang = request.GET.get('lang')
    request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER'))
>>>>>>> a8d18b23b80ec99c1d3244ee281b19dc054e7ea5
