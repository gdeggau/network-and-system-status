import psycopg2
from configparser import ConfigParser


class Connection(object):

    def __init__(self, filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)

        dbparams = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                dbparams[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} not found in the {1} file'.format(section, filename))

        try:
            print('Connecting to the PostgreSQL database...')
            self._db = psycopg2.connect(**dbparams)
            print('Successfully connected')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise

    def manipulate(self, sql):
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            cur.close()
            self._db.commit()
            print("Query was executed successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        return True

    def retrieve(self, sql):
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(sql)
            rs = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None
        return rs

    def close(self):
        self._db.close()
