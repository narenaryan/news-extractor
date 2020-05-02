News Collector
==============
A python lambda function that extracts and stores news in Postgres Database.

Requirements:
-------------
* Python 3.7
* PostgreSQL > 10.0.0
* AWS Lambda & Cloudwatch Event Rule (only required for automated schelduing)

Configuration:
--------------
The Python lambda function takes this configuration:

* PGUSER
* PGPORT
* PGDATABASE
* PGPASSWORD
* PGHOST
* API_KEY

Read more about PG variables: https://www.postgresql.org/docs/9.1/libpq-envars.html

API_KEY is the newsapi.org's developer API key. (https://newsapi.org/register)

Description:
------------
One can run the script as a stand-alone program or a lambda function on AWS.

Note: When you run it as a stand-alone program, make sure, you modify script to call handler function.


It basically collects latest news from
these native English speaking countries:

1. Australia
2. Canada
3. New Zealand
4. United Kingdom
5. USA

on these topics:

1. Business
2. Entertainment
3. Health
4. Top headlines

and, saves that JSON information in PostgreSQL database. The database should have following schemas:

1. australia
2. canada
3. newzealand
4. uk
5. usa

Your PostgreSQL database should have these identical tables in each schema representing categories.

1. business
2. entertainment
3. health
4. top


Installing project dependencies:
--------------------------------
make dependecies

Zipping lambda function
-----------------------
make zip


To schedule this data extraction and store, one can use AWS cloudwatch event schedule or, cron job or, a celery task.
