# -*- coding: utf-8 -*-

from pyCTelebot.config.pyVars import DATABASE_URL, ENV_CONFIG
import psycopg2
import psycopg2.extras
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


def convert(result):
    """ convert SQL output to dict """
    my_res = []
    for r in result:
        my_res.append(dict(r))
    return my_res


class MyDB:
    def __init__(self):
        """ Open connection """
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def query(self, query, args):
        """ Do a query """
        try:
            logger.log(msg='MyDB.query: {0} - args: {1}'.format(query, args),
                       level=logging.DEBUG)
            self.cur.execute(query=query, vars=args)
            logger.log(msg='MyDB.query executed',
                       level=logging.DEBUG)
            res = self.cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.log(msg='MyDB.query: {0} - args: {1} ERROR: {2}'.format(query, args, str(error)),
                       level=logging.ERROR)
            return None
        else:
            return res

    def dml(self, query, args):
        """ do a update, insert, delete,... """
        try:
            logger.log(msg='MyDB.dml: {0} - args: {1}'.format(query, args),
                       level=logging.DEBUG)
            self.cur.execute(query=query, vars=args)
            logger.log(msg='MyDB.dml executed',
                       level=logging.DEBUG)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.log(msg='MyDB.dml: {0} - args: {1} ERROR: {2}'.format(query, args, str(error)),
                       level=logging.ERROR)

    def commit(self):
        """ commit """
        self.conn.commit()

    def rollback(self):
        """ rollback """
        self.conn.rollback()

    def close(self):
        """ close connection """
        self.cur.close()
        self.conn.close()
