# -*- coding: utf-8 -*-
"""Sendgrid Class file for Retreat App."""
# import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import ClickTracking
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import From
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import MimeType
from sendgrid.helpers.mail import Subject
from sendgrid.helpers.mail import To
from sendgrid.helpers.mail import TrackingSettings


class Sendgrid:
    """Sendgrid Class for Retreat App."""

    def __init__(self, api_key):
        """Initialize Sendgrid Class."""
        self.client = SendGridAPIClient(api_key=api_key)

    def send_email(self, to, subject, html_content):
        """Send an email to a user."""
        # create an email message with sendgrid
        message = Mail()
        message.from_email = From("noreply@broadinstitute.org")
        message.to = [To(email=to)]
        message.subject = Subject(subject)
        message.content = Content(MimeType.html, html_content)

        # disable click tracking
        tracking_settings = TrackingSettings()
        tracking_settings.click_tracking = ClickTracking(False, False)
        message.tracking_settings = tracking_settings

        # send email
        try:
            response = self.client.send(message)
        except Exception as sendgrid_error:
            print(f"ERROR: Failed sending Sendgrid email: {sendgrid_error}")
            return None
        return response
