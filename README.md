## Build Image

`docker-compose build`

## Start a new project

Change `composeexample` for the name of your project

```
docker-compose run hits_django django-admin startproject composeexample .
```

## Configure the database in the new project

Open settings.py file, go to the DATABASES configuration and use the next lines:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'edc_psql',
        'PORT': 5432,
    }
}
```

Change your_db_name, your_db_name, your_password for your db credentials defined in .env file

## Run django

Execute the next command:

```
docker-compose up
```

Open your browser with the next url: http://127.0.0.1
