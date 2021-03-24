from app.environ import env


# USERS_ACTIVATION_ON: If True activation flow is enabled
USERS_ACTIVATION_ON = True

# USERS_SEND_ACTIVATION_EMAIL: If True when is registered a new user, send automatically an email activation
USERS_SEND_ACTIVATION_EMAIL = True

# USERS_ACTIVATION_TOKEN_LIFETIME: life time for the token in seconds
USERS_ACTIVATION_TOKEN_LIFETIME = 600

# USER_ACTIVATION_REQUIRED: If True the user account must be activated for login
USERS_ACTIVATION_REQUIRED = False

# USERS_ACTIVATION_URL: Url to use in email verification
USERS_ACTIVATION_URL = 'https://edcilo.com/confirm'
