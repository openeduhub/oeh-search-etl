import psycopg2

class Database:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host = 'localhost',
            user = 'search',
            password = 'admin',
            database = 'search'
        )
        self.curr = self.conn.cursor()
    def findItem(self, id, spider):
        self.curr.execute("""SELECT uuid, hash FROM "references" WHERE source = %s AND source_id = %s""", (
            spider.name,
            str(id)
        ))
        data = self.curr.fetchall()
        if(len(data)):
            return data[0]
        else:
            return None
    def findSource(self, spider):
        self.curr.execute("""SELECT * FROM "sources" WHERE id = %s""", (
            spider.name,
        ))
        data = self.curr.fetchall()
        if(len(data)):
            return data[0]
        else:
            return None