import pandas as pd
from pymongo import MongoClient

from echoss_fileformat import FileUtil, get_logger, set_logger_level

logger = get_logger("echoss_query")


class MongoQuery:
    def __init__(self, conn_info: str or dict):
        """
        Args:
            region_env(str) : Config File Regsion
            ex) conn_info = {
                                'mongo':
                                    {
                                        'host'  : int(ip),
                                        'port'  : int(port)),
                                        'db'    : str(db_name)
                                    }
                            }
        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("[Mongo] support type 'str' and 'dict'")
        required_keys = ['db']
        if (len(conn_info) > 0) and ('mongo' in conn_info) and all(key in conn_info['mongo'] for key in required_keys):
            if 'host' in conn_info['mongo'] and 'port' in conn_info['mongo']:
                self.client = MongoClient(
                    host=conn_info['mongo']['host'],
                    port=conn_info['mongo']['port']
                )
                self.db_name = conn_info['mongo']['db']
                self.db = self.client[self.db_name]
            elif 'uri' in conn_info['mongo']:
                self.client = MongoClient(
                    host=conn_info['mongo']['uri'],
                    directConnection=True
                )
                self.db_name = conn_info['mongo']['db']
                self.db = self.client[self.db_name]
            else:
                logger.debug(f"[Mongo] config info client connection keys (host, prot) or (url) not exist")
        else:
            logger.debug(f"[Mongo] config info not exist")

    def __str__(self):
        return f"MongoDB(client={self.client}, db_name={self.db_name})"

    @staticmethod
    def _parsing(query: str):
        if len(query) != 1:
            default, modify = query
            return default, modify
        else:
            query = query[0]
            return query

    def ping(self):
        """
        Args:
            Any

        Returns:
            str : DB Status
        """
        stat = self.client.admin.command('ping').keys()
        if 'ok' in str(stat):
            logger.debug(f"[Mongo] database connection success")
        else:
            raise ConnectionError('database connection fail')

    def databases(self):
        """
        Args:
            Any

        Returns:
            string : Database list
        """
        result = self.client.list_database_names()
        return pd.DataFrame(result, columns=['Database'])

    def collections(self, database: str) -> pd.DataFrame:
        """
        Args:
            database(str) : database name

        Returns:
            pd.DataFrame() : collection dataframe
        """
        db = self.client[database]
        result = db.list_collection_names()
        return pd.DataFrame(result, columns=['Table'])

    def select(self, collection: str, *query: str or dict) -> pd.DataFrame:
        """
        Args:
            collection(str) :
            *query(str or dict) : Mongo select query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query)

        query = eval(f"self.db.{collection}.find({query})")

        return pd.DataFrame(list(query))

    def insert(self, collection: str, *query: str or dict) -> None:
        """
        Args:
            collection(str) : target collection
            *query(str or dict) : Mongo insert query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query)
        eval(f"self.db.{collection}.insert_one({query})")

    def update(self, collection: str, *query: str or dict) -> None:
        """
        Args:
            collection(str) : target collection
            *query(str or dict) : Mongo update query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        default, modify = self._parsing(query)
        eval(f"self.db.{collection}.update_one({default}, {modify})")

    def delete(self, collection: str, *query: str or dict) -> None:
        """
        Args:
            collection(str) : target collection
            *query(str or dict) : Mongo delete query string

        Returns:
            pd.DataFrame() : DataFrame of query result
        """
        query = self._parsing(query)
        if query == {}:
            raise ValueError("can't delete all collection")
        else:
            return eval(f"self.db.{collection}.delete_one({query})")

    def new_index(self, collection: str, document: str) -> int:
        """
        Args:
            collection(str) : target collection
            document(str) : target document
        Returns:
            int() : maximum value
        """
        max_rows = list(eval(f"self.db.{collection}.find().sort([('{document}',-1)]).limit(1)"))
        if len(max_rows) > 0:
            max_value = max_rows[0][document]
            index = max_value + 1
        else:
            index = 1

        return index

