import pymysql
import dbconfig
import datetime

class DBHelper:

    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost', port = dbconfig.port, user = dbconfig.db_user,
                               passwd = dbconfig.db_password, db = database)

    def get_all_inputs(self):
        connection  = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_all_crimes(self):
        connection  = self.connect()
        try:
            query = "SELECT category, date, latitude, longitude, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                named_crimes = []
                for crime in cursor:
                    named_crime ={
                        'latitude':crime[2],
                        'longitude':crime[3],
                        'category':crime[0],
                        'description':crime[4],
                        'date': datetime.datetime.strftime(crime[1],'%Y-%m-%d')
                    }
                    named_crimes.append(named_crime)
                return named_crimes

        finally:
            connection.close()

    def add_input(self, data):
        connection  = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection  = self.connect()
        try:
            query = "DELETE from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()

    def add_crime(self, category, date, longitude, latitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, longitude, latitude, description) VALUES (%s, %s, %s, %s, %s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, longitude, latitude, description))
                connection.commit()
        finally:
            connection.close()