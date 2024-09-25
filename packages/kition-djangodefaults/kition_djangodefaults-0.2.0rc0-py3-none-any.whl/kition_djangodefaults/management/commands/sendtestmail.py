from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):
    email_recipient_arg_name = "recipient"
    help = "Sends a test email to verify the email configuration"

    def add_arguments(self, parser):
        parser.add_argument(self.email_recipient_arg_name, type=str)

    def handle(self, *args, **options):
        recipient = options[self.email_recipient_arg_name]

        try:
            send_mail(
                recipient_list=[recipient],
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject="Email Delivery works 🎉",
                message="This is a test email sent to verify the SMTP configuration.",
            )
            self.stdout.write(self.style.SUCCESS(f"Email sent to {recipient}"))
        except Exception as err:
            self.stdout.write(
                self.style.ERROR(f"Failed to send email to {recipient}: {err}")
            )
