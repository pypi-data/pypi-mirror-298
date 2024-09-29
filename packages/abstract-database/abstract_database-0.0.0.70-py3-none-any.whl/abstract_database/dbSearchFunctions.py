import json,asyncio,asyncpg,psycopg2
from abstract_apis import asyncPostRpcRequest, asyncPostRequest
from abstract_utilities import SingletonMeta
from abstract_solcatcher import makeLimitedCall
from abstract_solana import Pubkey
class TableManager(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.insert_list = []
            self.dbNames=[]
    def add_insert_list(self,conn,tables,dbName):
        if dbName not in self.dbNames:
            self.dbNames.append(dbName)
            setup_database(tables,conn)
            self.insert_list+=tables
    def get_insert(self, tableName):
        tableName = tableName.lower()
        insertList = [ls for ls in self.insert_list if ls.get("tableName") == tableName.lower()]
        return insertList[0] if insertList else None

    def fetchFromDb(self,tableName,searchValue,conn):
        cached_response = perform_database_operations('fetch', self.get_insert(tableName), searchValue, conn)
        if cached_response:
            return cached_response

    def insert_intoDb(self,tableName,searchValue,insertValue,conn):
        if isinstance(insertValue,dict):
            insertValue = json.dumps(insertValue)
        return perform_database_operations('insert', self.get_insert(tableName), (searchValue,insertValue),conn )
    def search_multiple_fields(self, query,conn,**kwargs):
        return search_multiple_fields(query,conn)
    def get_first_row_as_dict(self,tableName=None,rowNum=1,conn=None):
        """Fetch the first row of data from the specified table and return as a dictionary."""
        tableName = tableName or get_env_value(key="abstract_ai_table_name", path=self.env_path)
        query = f"SELECT * FROM {tableName} ORDER BY id ASC LIMIT {rowNum};"
        cur = conn.cursor()
        try:
            cur.execute(query)
            first_row = cur.fetchone()
            col_names = [desc[0] for desc in cur.description]
            if first_row:
                return dict(zip(col_names, first_row))
            return None
        except psycopg2.Error as e:
            print(f"Error fetching the first row: {e}")
            return None
        finally:
            cur.close()
            conn.close()
def getInsertType(tableName):
    return TableManager().get_insert(tableName)

async def search_Db(tableName, searchValue,**kwargs):
    insertType = getInsertType(tableName)
    if not insertType:
        print(f"No data structure for {tableName}")
        return

    search_query = getSearchQuery(insertType.get('tableName'), '*', insertType.get('columnSearch'))
    try:
        result = await getQuery(search_query, (searchValue,))
        if result:
            print(f"Found in {tableName}: {result}")
            return result
        else:
            print(f"No data found in {tableName} for {searchValue}")
    except Exception as e:
        print(f"Error searching in {tableName}: {str(e)}")
        
async def insert_Db(tableName, searchValue, insertValue,**kwargs):
    insertType = getInsertType(tableName)
    if not insertType:
        print(f"No insert type found for table: {tableName}")
        return

    # Check if entry exists
    existing_entry = await search_Db(insertType.get('tableName'), searchValue)
    if existing_entry:
        print(f"Entry already exists in {tableName} with value {searchValue}")
        return existing_entry

    if not isinstance(insertValue, tuple):
        insertValue = (searchValue, dump_if_json(insertValue))
    
    insert_query = "INSERT INTO {} ({}) VALUES ({})".format(insertType.get('tableName'), insertType('insertQuery'), getInsertQueryS(insertType('insertQuery')))
    try:
        await getQuery(insert_query, insertValue)
        print(f"Inserted into {tableName}: {searchValue}")
    except Exception as e:
        print(f"Error using {insert_query} inserting {instype} with a value of {query} into {tableName}: {str(e)}")




async def universal_db_function(method,  params, check_identical_params=None, doNotCall=None, url=None, data={}):
    # Ensure the table is ready for operations
    insertType = getInsertType(method)
    if not inputs:
        print(f"Unable to find or create table: {method}")
        return

    # Extract the unique identifier for database operations
    unique_identifier = params[0]

    # Attempt to find an existing entry in the database
    existing_entry = await search_Db(tableName, unique_identifier)

    # Determine if the existing entry should be ignored based on the parameters
    if check_identical_params and existing_entry:
        all_match = all(params[k] == existing_entry.get(k, None) for k in params if k in existing_entry)
        if not all_match:
            existing_entry = None

    # If instructed not to make external calls and an entry exists, return it
    if doNotCall and existing_entry:
        return existing_entry

    # If there's no existing entry or it's ignored based on parameters, make an external call if allowed
    if not existing_entry and not doNotCall:
        response_data = await (asyncPostRequest(url=url, data=data, endpoint=method) if url else makeLimitedCall(method, params))

        # Handle unsuccessful responses or errors
        if not response_data or (isinstance(response_data, dict) and response_data.get('error')):
            print(f"Failed to get a valid response for {unique_identifier} in {tableName}: {response_data}")
            return response_data

        # If the response is successful, insert it into the database
        await insert_Db(insertType.get('tableName'), unique_identifier, (unique_identifier, dump_if_json(response_data)))
        print(f"Inserted {unique_identifier} in {tableName}")
        return response_data

    # Return the existing entry if all checks pass and no external call is made
    return existing_entry

def getSearchQuery(tableName, valueSelect='*', columnName=''):
    return f"SELECT {valueSelect} FROM {tableName} WHERE {columnName} = $1"

def getsearchquery(tableName):
    insertType = getInsertType(tableName)
    return getSearchQuery(insertType.get('tableName'), '*', insertType['columnSearch'])

def getInsertQueryS(insertQuery):
    parts = [part.strip() for part in insertQuery[1:-1].split(',')]
    placeholders = ', '.join(f'${i + 1}' for i in range(len(parts)))
    return placeholders


def setup_database(tables, conn):
    """ Create database tables based on provided configurations """
    cur = conn.cursor()
    try:
        for table in tables:
            cur.execute(table['table'])
        conn.commit()
    except psycopg2.Error as e:
        print("Error setting up database tables:", e)
        conn.rollback()
    finally:
        cur.close()

def fetch_data(search_query, search_value, conn):
    """ Fetch data from the database using the specified query and value """
    cur = conn.cursor()
    try:
        cur.execute(search_query, (search_value,))
        return cur.fetchone()
    finally:
        cur.close()

def insert_data(insert_query, values, conn):
    """ Insert data into the database using the specified query and values """
    cur = conn.cursor()
    try:
        cur.execute(insert_query, values)
        conn.commit()
    except psycopg2.Error as e:
        print("Failed to insert data:", e)
        conn.rollback()
    finally:
        cur.close()
        
def search_multiple_fields(query,conn,**kwargs):
    """Search the database using a query."""
    cur = conn.cursor()
    try:
        cur.execute(query)
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error querying JSONB data: {e}")
    finally:
        cur.close()
        conn.close()
def perform_database_operations(operation_type, table_info, value, conn):
    """ Perform dynamic database operations based on type and table info """
    if operation_type == 'fetch':
        return fetch_data(table_info['searchQuery'], value, conn)
    elif operation_type == 'insert':
        insert_data(table_info['insertQuery'], value, conn)

def fetchFromDb(tableName,searchValue,conn):
    cached_response =perform_database_operations('fetch', getInsertType(tableName.lower()), searchValue, conn)
    if cached_response:
        return cached_response

def insert_intoDb(tableName,searchValue,insertValue,conn):
    if isinstance(insertValue,dict):
        insertValue = json.dumps(insertValue)
    perform_database_operations('insert', getInsertType(tableName), (searchValue,insertValue),conn )
