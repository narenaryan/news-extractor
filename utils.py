import logging
import hashlib
import json

import psycopg2
import psycopg2.extras

from meta import Topics, Countries


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel('DEBUG')


def remove_duplicates():
    """ This function removes duplicate news by checking duplicate digests of data.
    It uses a set to filter out digests.
    """
    with psycopg2.connect("") as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

            for country in Countries:
                for topic in Topics:
                    unqiue_digests = set()
                    cur.execute(f"""
                    SELECT id, digest FROM {country.value}.{topic.name};
                    """)

                    for row in cur.fetchall():
                        digest = row.get('digest')
                        if digest in unqiue_digests:
                            cur.execute(f"""DELETE FROM {country.value}.{topic.name} WHERE id=%s;
                            """, (row.get('id'),))
                        else:
                            unqiue_digests.add(digest)


def recalculate_digests():
    """This function calculates hash for data and updates database.
    It uses python's hashlib SHA 256 to generate hex digest.
    """
    with psycopg2.connect("") as conn:
        with conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:

            for country in Countries:
                for topic in Topics:

                    cur.execute(f"""
                    SELECT id, news FROM {country.value}.{topic.name};
                    """)

                    for row in cur.fetchall():
                        byte_string = bytes(json.dumps(row['news'], sort_keys=True), encoding="utf-8")
                        digest = hashlib.sha256(byte_string).hexdigest()
                        cur.execute(f"""UPDATE {country.value}.{topic.name} SET digest = %s 
                        WHERE id=%s;""", (digest, row.get('id')))

                        LOGGER.info("Updating Country: %s, Topic: %s, ID: %s with digest: %s",
                            country.value,
                            topic.name,
                            row.get('id'),
                            digest
                        )


remove_duplicates()
