import environ

env = environ.Env(
    # set casting, default value
    APP_ENV=(str, 'dev'),
    APP_DEBUG=(bool, True),
    APP_SECRET_KEY=(str, None),
    APP_PORT=(int, 80),
    ALLOWED_HOSTS=(list, 'localhost'),
    APP_HOME_REDIRECT_TO=(str, 'http://localhost'),

    APP_DB_HOST=(str, 'localhost'),
    APP_DB_PORT=(int, 5432),
    APP_DB_NAME=(str, None),
    APP_DB_USER=(str, None),
    APP_DB_PASS=(str, None),

    APP_EMAIL_HOST=(str, None),
    APP_EMAIL_PORT=(int, 587),
    APP_EMAIL_USER=(str, None),
    APP_EMAIL_PASS=(str, None),

    APP_LANG=(str, 'en'),
    APP_TIME_ZONE=(str, 'UTC'),

    REDIS_CONNECTION=(str, None),
)
