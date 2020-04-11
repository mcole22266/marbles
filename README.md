# The Marble Race

## About

This is a website created primarily as a hobby project. The motivation was a Marble Racing _sensation_ created
by Tanner Sheets during the covid-19 crisis. The site allows visitors to see the current standings in any 
Series Cup as an Admin can update race data in numerous ways.

## How To Run

1. Create a `secrets.env` file in the root directory with the following variables:

    - GMAIL_USERNAME - used to send emails to site goers
    - GMAIL_PASSWORD - used to authenticate email
    - ENCRYPTED_SECURITY_CODE - used to authenticate new admin sign-ons
        - Pick a security code and encrypt it first with SHA512.
        - Set this equal to your hashed security code
    - POSTGRES_USER - username for postgres container
    - POSTGRES_PASSWORD - password for postgres container
    - POSTGRES_DB - database name for postgres container
    - SQLALCHEMY_DATABASE_URI - typically postgresql://{postgres_user}:{postgrespass}@db:5432/{postgres_db}
        - NOTE: Items in brackets are manually typed out

2. Be sure to have docker-compose installed on your machine.
3. In the terminal, build and launch the app with `docker-compose up --build`
4. When the build is complete, navigate to `localhost`.

## Developers

- Michael Cole (Repository Owner and Developer)
    - <mcole042891@gmail.com>
