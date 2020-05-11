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

2. If running production, the database is routinely backed up every night at 10:00 pm. These backups are written 
to an S3 bucket as defined in `./postgres/backup.sh`. Create the following to ensure automated backups are done
correctly:
    - Create `./postgres/.aws/credentials`
    - First line: `[default]`
    - Second line: `AWS_ACCESS_KEY_ID=` followed by your AWS access key id
    - Third line: `AWS_SECRET_ACCESS_KEY=` followed by your AWS secret access key
3. Be sure to have docker-compose installed on your machine.
4. In the terminal, build and launch the app with `docker-compose up --build`
    - In production, launch the app with `docker-compose -f docker-compose.prod.yml up --build`
5. When the build is complete, navigate to `localhost`.

## Developers

- Michael Cole (Repository Owner and Developer)
    - <mcole042891@gmail.com>
