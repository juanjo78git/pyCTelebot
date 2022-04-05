# -*- coding: utf-8 -*-

from pyCTelebot.config.auth import DATABASE_URL, ENV_CONFIG
import psycopg2
import logging

# Logs
logger = logging.getLogger(__name__)
# DEBUG / INFO / WARNING / ERROR / CRITICAL
if ENV_CONFIG.get('log') == 'CRITICAL':
    logger.setLevel(logging.CRITICAL)
elif ENV_CONFIG.get('log') == 'ERROR':
    logger.setLevel(logging.ERROR)
elif ENV_CONFIG.get('log') == 'WARNING':
    logger.setLevel(logging.WARNING)
elif ENV_CONFIG.get('log') == 'INFO':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)


class MyDB:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()

    def query(self, query, *args):
        try:
            self.cur.execute(query)
            res = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.log(msg='MyDB.query: {0} - ERROR: {1}'.format(query, str(error)), level=logging.ERROR)
            return None
        else:
            return res

    def close(self):
        self.cur.close()
        self.conn.close()
