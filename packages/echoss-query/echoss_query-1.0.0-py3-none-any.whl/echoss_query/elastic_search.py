import pandas as pd
from opensearchpy import OpenSearch
from echoss_fileformat import FileUtil, get_logger, set_logger_level

logger = get_logger("echoss_query")


class ElasticSearch:
    query_match_all = {"query": {"match_all": {}}}
    empty_dataframe = pd.DataFrame()
    query_cache = False

    def __init__(self, conn_info: str or dict):
        """
        Args:
            conn_info : configration dictionary (index is option)
            ex) conn_info = {
                                'elastic':
                                    {
                                        'user'  : str(user),
                                        'passwd': str(passwd),
                                        'host'  : str(host),
                                        'port' : int(port),
                                        'index' : str(index_name)
                                    }
                            }

        """
        if isinstance(conn_info, str):
            conn_info = FileUtil.dict_load(conn_info)
        elif not isinstance(conn_info, dict):
            raise TypeError("ElasticSearch support type 'str' and 'dict'")
        required_keys = ['user', 'passwd', 'host', 'port']
        if (len(conn_info) > 0) and ('elastic' in conn_info) and all(k in conn_info['elastic'] for k in required_keys):
            self.user = conn_info['elastic']['user']
            self.passwd = conn_info['elastic']['passwd']
            self.host = conn_info['elastic']['host']
            self.port = conn_info['elastic']['port']
            if 'index' in conn_info['elastic']:
                self.index_name = conn_info['elastic']['index']
            else:
                self.index_name = None

            self.hosts = [{
                'host': self.host,
                'port': self.port
            }]

            self.auth = (self.user, self.passwd)
            # re-use connection
            self._connect_es()
        else:
            logger.debug(f"[Elastic] config info not exist")

    def __str__(self):
        return f"ElasticSearch(hosts={self.hosts}, index={self.index_name})"

    def _connect_es(self):
        """
        ElasticSearch Cloud에 접속하는 함수
        """
        try:
            self.conn = OpenSearch(
                hosts=self.hosts,
                http_compress=True,
                http_auth=self.auth,
                use_ssl=True,
                verify_certs=True,
                ssl_assert_hostname=False,
                ssl_show_warn=False
            )
            if self.conn is None or self.ping() is False:
                raise ValueError(f"open elasticsearch is failed or health ping failed.")
        except Exception as e:
            raise ValueError("Connection failed by config. Please check config data")

    def ping(self) -> bool:
        """
        Elastic Search에 Ping
        """
        if self.conn:
            return self.conn.ping()
        else:
            return False

    def info(self) -> dict:
        """
        Elastic Search Information
        """
        return self.conn.info()

    def exists(self, id: str or int, index=None) -> bool:
        """
        Args:
            index(str) : 확인 대상 index \n
            id(str) : 확인 대상 id \n
        Returns:
            boolean
        """
        if index is None:
            index = self.index_name
        return self.conn.exists(index, id)

    def to_dataframe(self, result_list):
        if isinstance(result_list, dict):
            if 'hits' in result_list and 'hits' in result_list['hits']:
                result_list = result_list['hits']['hits']
        if result_list is not None and isinstance(result_list, list) and len(result_list)>0:
            if '_source' in result_list[0]:
                documents = [doc['_source'] for doc in result_list]
                df = pd.DataFrame(documents)
                return df
        return self.empty_dataframe

    def search_list(self, body: dict = None, index=None) -> list:
        """
        Args:
            index(str) : 대상 index
            body(dict) : search body
        Returns:
            result(list) : search result of response['hits']['hits']
        """
        if index is None:
            index = self.index_name
        if body is None:
            body = self.query_match_all
        response = self.conn.search(
            index=index,
            body=body
        )
        if len(response) > 0 and 'hits' in response and 'hits' in response['hits']:
            return response['hits']['hits']
        return []

    def search(self, body: dict = None, index=None) -> list:
        """
        Args:
            index(str) : 대상 index
            body(dict) : search body
        Returns:
            result(list) : search result
        """
        if index is None:
            index = self.index_name
        if body is None:
            body = self.query_match_all
        response = self.conn.search(
            index=index,
            body=body
        )
        return response

    def search_field(self, field: str, value: str, index=None) -> list:
        """
        해당 index, field, value 값과 비슷한 값들을 검색해주는 함수 \n
        Args:
            index(str) : 대상 index
            field(str) : 검색 대상 field \n
            value(str) : 검색 대상 value \n
        Returns:
            result(list) : 검색 결과 리스트
        """
        if index is None:
            index = self.index_name
        response = self.conn.search(
            index=index,
            body={
                'query': {
                    'match': {field: value}
                }
            }
        )
        return response['hits']['hits']

    def get(self, id: str or int, index=None) -> dict:
        """
        index에서 id와 일치하는 데이터를 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        if index is None:
            index = self.index_name
        return self.conn.get(index=index, id=id)

    def get_source(self, id: str or int, index=None) -> dict:
        """
        index에서 id와 일치하는 데이터의 소스만 불러오는 함수 \n
        Args:
            id(str) : 가져올 대상 id \n
        Returns:
            result(dict) : 결과 데이터

        """
        if index is None:
            index = self.index_name
        return self.conn.get_source(index, id)

    def create(self, id: str or int, body: dict, index=None):
        """
        index에 해당 id로 새로운 document를 생성하는 함수 \n
        (기존에 있는 index에 데이터를 추가할 때 사용) \n
        Args:
            id(str) : 생성할 id \n
            body(dict) : new data
            index(str) : index name or self.index_name will be used
        Returns:
            result(str) : 생성 결과
        """
        if index is None:
            index = self.index_name
        return self.conn.create(index=index, id=id, body=body)

    def index(self, index: str, body: dict, id: str or int = None) -> str:
        """
        index를 생성하고 해당 id로 새로운 document를 생성하는 함수 \n
        (index를 추가하고 그 내부 document까지 추가하는 방식) \n
        Args:
            index(str) : 생성할 index name \n
            body(dict) : 입력할 json 내용
            id(str) : 생성할 id \n
        Returns:
            result(str) : 생성 결과
        """
        return self.conn.index(index, body, id=id)

    def update(self, id: str or int, body: dict, index=None) -> str:
        """
        기존 데이터를 id를 기준으로 body 값으로 수정하는 함수 \n
        Args:
            id(str) : 수정할 대상 id \n
            body(dict) : data dict to update
            index(str) : 생성할 index name \n
        Returns:
            result(str) : 처리 결과
        """
        if index is None:
            index = self.index_name
        doc_body = {
            'doc' : body
        }
        return self.conn.update(index, id, doc_body)

    def delete(self, id: str or int, index=None) -> str:
        """
        삭제하고 싶은 데이터를 id 기준으로 삭제하는 함수 \n
        Args:
            id(str) : 삭제 대상 id \n
            index(str) : 생성할 index name \n
        Returns:
            result(str) : 처리 결과
        """
        if index is None:
            index = self.index_name
        return self.conn.delete(index, id)

    def delete_index(self, index):
        """
        인덱스를 삭제하는 명령어 신중하게 사용해야한다.\n
        Args:
            index(str) : 삭제할 index
        Returns:
            result(str) : 처리 결과
        """
        return self.conn.indices.delete(index)
