import psycopg2
from psycopg2 import pool
from abstract_utilities import is_number,SingletonMeta
from .dbSearchFunctions import TableManager
from abstract_security import get_env_value
def get_dbType(dbType=None):
    return dbType or 'database'
def get_dbName(dbName=None):
    return dbName or 'solcatcher'
def get_env_path(env_path=None):
    return env_path or '/home/solcatcher/.env'
def get_db_env_key(dbType=None,dbName=None,key=None):
    dbType = get_dbType(dbType=dbType)
    dbName = get_dbName(dbName=dbName)
    return f"{dbType.upper()}_{dbName.upper()}_{key.upper()}"
def get_env_key_value(dbType=None,dbName=None,key=None,env_path=None):
    dbType = get_dbType(dbType=dbType)
    dbName = get_dbName(dbName=dbName)
    env_path = get_env_path(env_path=env_path)
    env_key = get_db_env_key(dbType=dbType,dbName=dbName,key=key)
    return get_env_value(key=env_key,path=env_path)
def get_db_vars(env_path=None,dbType=None,dbName=None):
    dbVars = {}
    for key in ['user','password','host','port','dbname']:
        value = get_env_key_value(dbType=dbType,dbName=dbName,key=key,env_path=env_path)
        if is_number(value):
            value = int(value)
        dbVars[key]=value
    return dbVars
class connectionManager(metaclass=SingletonMeta):
    def __init__(self,env_path=None,dbType=None,dbName=None,tables=[]):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            self.env_path = get_env_path(env_path=env_path)
            self.dbName = get_dbName(dbName=dbName)
            self.dbType = get_dbType(dbType=dbType)
            self.dbVars = self.get_db_vars(dbType=self.dbType,dbName=self.dbName,env_path=self.env_path)
            self.user = self.dbVars['user']
            self.password = self.dbVars['password']
            self.host = self.dbVars['host']
            self.port = self.dbVars['port']
            self.dbname = self.dbVars['dbname']
            self.simple_connect = self.simple_connect_db()
            self.table_mgr = TableManager()
            self.tables = tables
            self.table_mgr.add_insert_list(self.connect_db(),self.tables,self.dbName)
    def get_dbName(self,dbName=None):
        return get_dbName(dbName=dbName or self.dbName)
    def get_dbType(self,dbType=None):
        return get_dbType(dbType=dbType or self.dbType)
    def get_env_path(self,env_path=None):
        return get_env_path(env_path=env_path or self.env_path)
    def get_db_vars(self,env_path=None,dbType=None,dbName=None):
        env_path = self.get_env_path(env_path=env_path)
        dbName = self.get_dbName(dbName=dbName)
        dbType = self.get_dbType(dbType=dbType)
        dbVars = get_db_vars(env_path=env_path,dbType=dbType,dbName=dbName)
        return dbVars
    def change_db_vars(self,env_path=None,dbType=None,dbName=None,tables=[]):
        dbType = dbType or 'database'
        self.env_path = self.get_env_path(env_path=env_path)
        self.dbName = self.get_dbName(dbName=dbName)
        self.dbType = self.get_dbType(dbType=dbType)
        self.dbVars = self.get_db_vars(env_path=dbType,dbType=dbType,dbName=dbName)
        self.user = self.dbVars['user']
        self.password = self.dbVars['password']
        self.host = self.dbVars['host']
        self.port = self.dbVars['port']
        self.dbname = self.dbVars['dbname']
        self.simple_connect = self.simple_connect_db()
        self.get_db_connection(self.connect_db())
        self.tables = tables or self.tables
        self.table_mgr.add_insert_list(self.connect_db(),self.tables,self.dbName)
        return self.dbVars
    def connect_db(self):
        """ Establish a connection to the database """
        return psycopg2.connect(user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port,
                                dbname=self.dbname
                                )
    def simple_connect_db(self):
        return  psycopg2.pool.SimpleConnectionPool(1, 10, user=self.user,
                                                      password=self.password,
                                                      host=self.host,
                                                      port=self.port,
                                                      database=self.dbname)
    def put_db_connection(self,conn):
        conn = conn or self.connect_db()
        self.simple_connect.putconn(conn)
    def get_db_connection(self):
        return self.simple_connect.getconn()
    def get_insert(self, tableName):
        return self.table_mgr.get_insert(tableName)
    def fetchFromDb(self,tableName,searchValue):
        return self.table_mgr.fetchFromDb(tableName,searchValue,self.connect_db())
    def insertIntoDb(self,tableName,searchValue,insertValue):
        return self.table_mgr.insert_intoDb(tableName,searchValue,insertValue,self.connect_db())
def get_db_connection():
    return connectionManager().get_db_connection()
def put_db_connection(conn):
    connectionManager().put_db_connection(conn)
def connect_db():
    return connectionManager().connect_db()
def get_insert(tableName):
    return connectionManager().get_insert(tableName)
def fetchFromDb(tableName,searchValue):
    return connectionManager().fetchFromDb(tableName,searchValue)
def insertIntoDb(tableName,searchValue,insertValue):
    return connectionManager().insertIntoDb(tableName,searchValue,insertValue)
