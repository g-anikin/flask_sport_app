import sqlite3


class DatabaseInterface:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()

    def execute(self, query, data):
        self.cur.execute(query, data)
        self.conn.commit()
        return self.cur

    def create_table(self, create_table_script):
        query = open(create_table_script, 'r').read()
        self.cur.execute(query)
        self.conn.commit()
        return self.cur

    def select_from_db(self):
        self.cur.execute('SELECT * from exercises;')
        return self.cur.fetchall()

    def select_for_insert(self):
        self.cur.execute('SELECT name, body_part, about, pic_link from exercises;')
        return self.cur.fetchall()

    def select_parts(self):
        self.cur.execute('SELECT body_part from exercises;')
        return self.cur.fetchall()

    def select_id(self):
        self.cur.execute('SELECT id from exercises;')
        return self.cur.fetchall()

    def select_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def add_exercise(self, name, body_part, about, pic_link):
        return self.execute("INSERT INTO exercises (name, body_part, about, pic_link) VALUES (?, ?, ?, ?)", (name, body_part, about, pic_link))

    def delete_exercise(self, id_number):
        self.cur.execute(f'delete from exercises where id={id_number}')
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    a = DatabaseInterface('exercise.db')
    # a.create_table('create_table.sql')
    # a.add_exercise('name1', 'body_part1', 'about1', 'pic_link1')
    # b = a.select_from_db()
    b = a.select_parts()
    print(b)
    lst = []
    for i in b:
        print(i[0].split(','))
        for j in i[0].split(','):
            lst.append(j)
    lst = set(lst)
    list(lst)
    # a.delete_exercise('10')
    # print(a.select_from_db())
    # print(a.select_query("select name, body_part, about, pic_link from exercises where body_part like '%body_part7%' or body_part like '%body_part8%';"))