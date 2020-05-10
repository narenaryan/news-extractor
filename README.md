News Collector
==============
A Python lambda function that extracts and stores news in PostgreSQL Database.

Program structure:
==================
The main program is:
  
  handler.py

Helper functions like, deleting duplicate news, lies in:
  
  utils.py

The program detects existing news by creating a digest. If there is an incoming news, it is checked against digest of last record in database. In this way, one can be sure, data is not duplicated irrespective of schedules.

One can see countries and topics in:

  meta.py

Requirements:
-------------
* Python 3.7
* PostgreSQL > 10.0.0 (Make sure you build psycopg2 dependencies for target Lambda environment)
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


Note: To schedule the data extraction and store, one can use AWS cloudwatch event schedule or, cron job or, a celery task.
