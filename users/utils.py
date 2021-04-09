from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Email(object):
    def __init__(self, subject, from_addr, to_addr, context, html_template, txt_template):
        self.subject = subject
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.context = context
        self.html_template = html_template
        self.txt_template = txt_template

    def create_message(self):
        email_html_message = render_to_string(self.html_template, self.context)
        email_plaintext_message = render_to_string(self.txt_template, self.context)

        msg = EmailMultiAlternatives(self.subject, email_plaintext_message, self.from_addr, self.to_addr)
        msg.attach_alternative(email_html_message, "text/html")
        return msg

    def send(self):
        msg = self.create_message()
        msg.send()
