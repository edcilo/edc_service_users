from app.environ import env


# If True activation flow is enabled
ACCOUNT_CONFIRM_ON = True

# If True when is registered a new user, send automatically an email activation
SEND_ACCOUNT_CONFIRM_EMAIL = True

# Life time for the token in seconds
ACCOUNT_CONFIRM_TOKEN_LIFETIME = 600

# If True the user account must be confirmed for allow login
ACCOUNT_CONFIRM_REQUIRED = True

# Url to use in email verification
ACCOUNT_CONFIRM_URL = 'https://edcilo.com/confirm'
