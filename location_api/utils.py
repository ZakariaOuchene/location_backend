from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_booking_confirmation_email(booking):
    subject = "Confirmation de réservation"
    context = {
        "client_first_name": booking['first_name'],
        "client_last_name": booking['last_name'],
        "car_model": booking['name_car'],
        "date_depart": booking['start_date'],
        "lieux_depart": booking['name_pickup_start'],
        "date_fin": booking['end_date'],
        "lieux_retour": booking['name_pickup_end'],
        "total_prix": booking['total_price'],
    }
    html_message = render_to_string("booking_confirmation_email.html", context)
    send_mail(subject, '', '', [booking['email']], html_message=html_message)