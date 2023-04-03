import sqlite3
import click

def create_table_if_does_not_exist(table_name, create_string, db_path=None, connection=None):
    DB().get_connection()
    # if not db_path and not connection:
    #     raise Exception("one of db_path or connection must be specified")

    # if not connection:
    #     connection = sqlite3.connect(db_path)

class DB(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance
  
    def get_db(self):
        if not hasattr(self, 'db'):
            raise Exception('DB must be set on Sqlite')
        return self.db
    
    def get_connection(self):
        if not hasattr(self, 'connection'):
            click.echo(f"Starting connection to DB: {self.db}")
            self.connection = sqlite3.connect(self.get_db())
        return self.connection
    
    def get_cursor(self):
        if not hasattr(self, 'cursor'):
            self.cursor = self.get_connection().cursor()
        return self.cursor
    
    def execute(self, command):
        return self.get_cursor().execute(command)
    
    def commit(self):
        self.get_connection().commit()
    
    @classmethod
    def set_db(cls, db_path):
        cls.db = f"{db_path}/brkdown.db"

    @classmethod
    def initialize(cls, db_path):
        DB().set_db(db_path)

  
