import os
import enum
import hashlib
import pytz
import json
import uuid
import logging
from datetime import datetime

import requests
import psycopg2
import psycopg2.extras

from meta import Topics, Countries

ZERO = 0
NEWS_API_ENDPOINT = "http://newsapi.org/v2/top-headlines"
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel('DEBUG')


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
    with psycopg2.connect("") as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            # Fetch articles for countries
            for country in Countries:
                article_count = ZERO
                
                # Fetch articles from different topics
                for topic in Topics:
                    result = fetch_articles(country.name.lower(), topic.name)

                    if not result:
                        continue

                    result_string = json.dumps(result, sort_keys=True)
                    byte_string = bytes(result_string, encoding="utf-8")
                    digest = hashlib.sha256(byte_string).hexdigest()

                    cur.execute(f"""SELECT digest FROM {country.value}.{topic.name} ORDER BY created_at DESC LIMIT 1;
                    """)
                    row = cur.fetchone()

                    if digest == row.get('digest'):
                        LOGGER.warning("News already exists in database. Skipping creation.")

                    # Timezone aware UTC timestamp
                    now = datetime.now(pytz.utc)
                    cur.execute(f"""
                        INSERT INTO {country.value}.{topic.name} (id, news, created_at) VALUES (%s, %s, %s);
                        """, (uuid.uuid4(), result_string, now))

                    if result.get('status') == 'error':
                        raise Exception(
                            "The API result from newsapi.org is not successful.", result.get('message'))

                    article_count += result.get('totalResults')
                    LOGGER.info("Total: %d articles stored for topic: %s",
                                result.get('totalResults'), topic.name)
            LOGGER.info("Total: %d articles stored for country: %s",
                        article_count, country)

    return {
        'statusCode': 200,
        'body': json.dumps('News fetch operation is successful!')
    }
