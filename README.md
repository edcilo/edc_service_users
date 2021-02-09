## Build Image

Customize docker-compose.yml file

Create and customize .env file
```
cp .env.example .env
```

Build docker image
```
docker-compose build
```

## Start a new project

Change `composeexample` for the name of your project

```
docker-compose run users_django django-admin startproject app .
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
        'HOST': 'psql',
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
