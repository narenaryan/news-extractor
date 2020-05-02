import os
import enum
import pytz
import json
import uuid
import logging
from datetime import datetime

import requests
import psycopg2
import psycopg2.extras

ZERO = 0
NEWS_API_ENDPOINT = "http://newsapi.org/v2/top-headlines"
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel('DEBUG')


class Topics(enum.Enum):
    top = enum.auto()
    business = enum.auto()
    health = enum.auto()
    entertainment = enum.auto()

def fetch_articles(country, topic_name) -> dict:
    payload = {
        "apiKey": os.environ.get("API_KEY"),
        "country": country
    }
    
    if topic_name != 'top':
        payload['category'] = topic_name

    resp = requests.get(NEWS_API_ENDPOINT, params=payload)

    try:
        result = resp.json()
    except ValueError:
        LOGGER.error("The response for topic: %s is not valid", topic_name)
        result = None

    return result


def handler(event, context):
    # This is to convert python uuid to postgres UUID string
    psycopg2.extras.register_uuid()

    # Target native English speakers
    countries = {
        "au": "australia",
        "ca": "canada",
        "nz": "newzealand",
        "gb": "uk",
        "us": "usa"
    }
    with psycopg2.connect("") as conn:
        with conn.cursor() as cur:
            # Fetch articles for countries
            for country, db_schema in countries.items():
                article_count = ZERO
                # Fetch articles from different topics
                for topic in Topics:
                    result = fetch_articles(country, topic.name)
                    
                    if not result:
                        continue

                    now = datetime.now(pytz.utc) # Timezone aware UTC timestamp
                    cur.execute(f"""
                        INSERT INTO {db_schema}.{topic.name} (id, news, created_at) VALUES (%s, %s, %s);
                        """, (uuid.uuid4(), json.dumps(result), now))

                    if result.get('status') == 'error':
                        raise Exception("The API result from newsapi.org is not successful.", result.get('message'))

                    article_count += result.get('totalResults')
                    LOGGER.info("Total: %d articles stored for topic: %s", result.get('totalResults'), topic.name)                   
            LOGGER.info("Total: %d articles stored for country: %s", article_count, topic.name)

    return {
        'statusCode': 200,
        'body': json.dumps('News fetch operation is successful!')
    }
