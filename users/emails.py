from .utils import Email


class PasswordResetTokenCreatedEmail(Email):
    def __init__(self, context, reset_password_token):
        subject = "Password Reset for {title}".format(title="edcilo.com")
        from_addr = "noreply@edcilo.com"
        to_addr = [reset_password_token.user.email]
        html_template = 'emails/user_reset_password.html'
        txt_template = 'emails/user_reset_password.txt'

        Email.__init__(self, subject, from_addr, to_addr, context, html_template, txt_template)


class AccountConfirmEmail(Email):
    def __init__(self, context, user):
        subject = "Activate your account for {title}".format(title="edcilo.com"),
        from_addr = "noreply@edcilo.com"
        to_addr = [user.email]
        html_template = 'emails/user_activation_token.html'
        txt_template = 'emails/user_activation_token.txt'
        Email.__init__(self, subject, from_addr, to_addr, context, html_template, txt_template)
