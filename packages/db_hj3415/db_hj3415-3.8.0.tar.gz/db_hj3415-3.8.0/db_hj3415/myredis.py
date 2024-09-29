"""
redis 서버를 이용해서 mongodb의 데이터를 캐시한다.
데이터의 캐시 만료는 데이터를 업데이트 시키는 모듈인 scraper_hj3415에서 담당하고
여기서 재가공해서 만들어지는 데이터는 만료기간을 설정한다.
장고에서 필요한 데이터를 보내는 기능이 주임.
"""

import redis
from db_hj3415 import mymongo
import json
from utils_hj3415 import utils
from typing import Tuple, Callable, Dict, Any, Optional
import datetime
from typing import List, Dict
from db_hj3415 import cli as db_cli


def connect_to_redis(addr: str) -> redis.Redis:
    conn_str = f"Connect to Redis ..."
    print(conn_str, f"Server Addr : {addr}")
    return redis.Redis(host=addr, port=6379, db=0)


class Base:
    setting_manager = db_cli.DbSettingsManager()
    redis_client = connect_to_redis(setting_manager.get_address('redis'))

    # 기본 Redis 캐시 만료 시간 (12시간)
    DEFAULT_CACHE_EXPIRATION_SEC = 3600 * 12

    def __init__(self):
        if Base.redis_client is None:
            raise ValueError("myredis.Base.redis_client has not been initialized!")

    @classmethod
    def delete(cls, redis_name: str):
        """
        redis_name 에 해당하는 키/값을 삭제하며 원래 없으면 아무일 없음
        :param redis_name:
        :return:
        """
        # print(Redis.list_redis_names())
        cls.redis_client.delete(redis_name)
        # print(Redis.list_redis_names())

    @classmethod
    def delete_all_with_pattern(cls, pattern: str) -> bool:
        """
        pattern에 해당하는 모든 키를 찾아서 삭제한다.
        :param pattern: ex) 005930.c101* - 005930.c101로 시작되는 모든키 삭제
        :return:
        """
        # print(Redis.list_redis_names())
        # SCAN 명령어를 사용하여 패턴에 맞는 키를 찾고 삭제
        cursor = '0'
        while cursor != 0:
            cursor, keys = cls.redis_client.scan(cursor=cursor, match=pattern, count=1000)
            if keys:
                cls.redis_client.delete(*keys)

        # print(Redis.list_redis_names())
        return True

    @classmethod
    def list_redis_names(cls) -> list:
        """
        전체 레디스 아이템을 리스트로 반환한다.
        :return:
        """
        # byte를 utf-8로 디코드하고 정렬함.
        return sorted([item.decode('utf-8') for item in cls.redis_client.keys('*')])

    def get_cached_data(self, redis_name: str) -> Dict:
        """Redis에서 캐시된 데이터를 가져옵니다."""
        cached_data = self.redis_client.get(redis_name)
        if cached_data is None:
            return None
        return json.loads(cached_data.decode('utf-8'))

    def set_cached_data(self, redis_name: str, data: Any, expiration_sec: int = DEFAULT_CACHE_EXPIRATION_SEC) -> None:
        """Redis에 데이터를 캐싱하고 만료 시간을 설정합니다."""
        self.redis_client.setex(redis_name, expiration_sec, json.dumps(data))
        print(f"Redis 캐시에 저장 (만료시간: {expiration_sec}초) - {redis_name}")

    def fetch_and_cache_data(self, redis_name: str, refresh: bool, fetch_function: Callable, *args) -> Dict:
        """캐시에서 데이터를 가져오거나, 없으면 fetch_function을 호출하여 데이터를 계산 후 캐싱합니다."""
        if not refresh:
            cached_data = self.get_cached_data(redis_name)
            if cached_data:
                ttl_hours = round(self.redis_client.ttl(redis_name) / 3600, 1)
                print(f"Redis 캐시에서 데이터 가져오기 (남은시간: {ttl_hours} 시간) - {redis_name}")
                return cached_data

        # 캐시된 데이터가 없거나 refresh=True인 경우
        data = fetch_function(*args)

        if data:
            self.set_cached_data(redis_name, data)
        return data


class DartToday(Base):
    redis_name = 'dart_today'

    def save(self, data: List[Dict]):
        # 이전 내용을 삭제하고...
        self.delete(self.redis_name)
        # 데이터를 Redis에 캐싱
        self.redis_client.set(self.redis_name, json.dumps(data))
        # 60분후 키가 자동으로 제거됨
        Base.redis_client.expire(self.redis_name, 3600)

    def get(self) -> List[Dict]:
        try:
            print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(self.redis_name)}초) - DartToday().get()")
            cached_data = self.redis_client.get(self.redis_name).decode('utf-8')
        except AttributeError:
            return []
        else:
            # rcept_no를 기준으로 정렬한다.
            data_list = json.loads(cached_data)
            sorted_list = sorted(data_list, key=lambda x: x['rcept_no'])
            return sorted_list


class Corps(Base):
    COLLECTIONS = mymongo.Corps.COLLECTIONS

    def __init__(self, code: str = '', page: str = ''):
        self.code_page = code + '.' + page
        self.coprs_code = code
        self.coprs_page = page
        # redis에서 name으로 사용하는 변수의 기본으로 문미에 문자열을 추가로 첨가해서 사용하는 역할을 함.
        super().__init__()

    @property
    def coprs_code(self) -> str:
        return self._coprs_code

    @coprs_code.setter
    def coprs_code(self, code: str):
        assert utils.is_6digit(code), f'Invalid value : {code}'
        self.code_page = code + self.code_page[6:]
        # print('code_page 변경 :', self.code_page)
        self._coprs_code = code

    @property
    def coprs_page(self) -> str:
        return self._coprs_page

    @coprs_page.setter
    def coprs_page(self, page: str):
        assert page in self.COLLECTIONS, f'Invalid value : {page}({self.COLLECTIONS})'
        self.code_page = self.code_page[:7] + page
        # print('code_page 변경 :', self.code_page)
        self._coprs_page = page

    @classmethod
    def get_name(cls, code: str) -> str | None:
        """
        redis_name = 코드명_name
        :param code:
        :return:
        """
        redis_name = code+'_name'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            name = mymongo.Corps.get_name(code)
            # import pprint
            # pprint.pprint(data)
            if name:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, name)
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - get_name()")
            return name
        else:
            print("Redis 캐시에서 데이터 가져오기 - get_name()")
            return cached_data

    @classmethod
    def list_all_codes(cls) -> list:
        """
        redis_name = 'all_codes'
        :return:
        """
        redis_name = 'all_codes'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            codes = []
            for db_name in mymongo.Corps.list_db_names():
                if utils.is_6digit(db_name):
                    codes.append(db_name)
            data = sorted(codes)

            if data:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - krx 리프레시할때 제거되도록 개선..
                # Base.redis_client.expire(redis_name, 3600)
            # print("list_all_codes() - Mongo에서 데이터 가져오기")
            return data
        else:
            # print("list_all_codes() - Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)

    @classmethod
    def list_all_codes_names(cls) -> dict:
        """
        redis_name = 'all_codes_names'
        :return:
        """
        redis_name = 'all_codes_names'

        try:
            cached_data = cls.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            corps = {}
            for code in cls.list_all_codes():
                corps[code] = mymongo.Corps.get_name(code)
            data = corps

            if data:
                # 데이터를 Redis에 캐싱
                cls.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - krx 리프레시할때 제거되도록 개선..
                # Base.redis_client.expire(redis_name, 3600)
            print("list_all_codes_names() - Mongo에서 데이터 가져오기")
            return data
        else:
            print("list_all_codes_names() - Redis 캐시에서 데이터 가져오기")
            return json.loads(cached_data)

    def _list_rows(self, func: mymongo.Corps, redis_name: str) -> list:
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = func.list_rows()
            # import pprint
            # pprint.pprint(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - ", func)
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - ", func)
            return json.loads(cached_data)


class C101(Corps):
    def __init__(self, code: str):
        super().__init__(code, 'c101')
        self.mymongo_c101 = mymongo.C101(code)

    @property
    def code(self) -> str:
        return self.coprs_code

    @code.setter
    def code(self, code: str):
        self.coprs_code = code
        self.mymongo_c101.code = code

    def get_recent(self) -> dict:
        # code_page 앞 11글자가 코드와 c101 페이지임.
        redis_name = self.code_page + '_recent'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c101.get_recent(merge_intro=True)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c101 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - C101().get_recent()")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - C101().get_recent()")
            return json.loads(cached_data)

    def get_trend(self, title: str) -> dict:
        """
        title에 해당하는 데이터베이스에 저장된 모든 값을 {날짜: 값} 형식의 딕셔너리로 반환한다.

        title should be in ['BPS', 'EPS', 'PBR', 'PER', '주가', '배당수익률', '베타52주', '거래량']

        리턴값 - 주가
        {'2023.04.05': '63900',
         '2023.04.06': '62300',
         '2023.04.07': '65000',
         '2023.04.10': '65700',
         '2023.04.11': '65900',
         '2023.04.12': '66000',
         '2023.04.13': '66100',
         '2023.04.14': '65100',
         '2023.04.17': '65300'}
        """
        # code_page 앞 11글자가 코드와 c101 페이지임.
        redis_name = self.code_page + '_trend'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c101.get_trend(title)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c101 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - C101().get_trend()")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - C101().get_trend()")
            return json.loads(cached_data)


class C1034(Corps):
    def __init__(self, code: str, page: str):
        super().__init__(code, page)
        # 자식 클래스에서 C103이나 C104를 생성해서 할당함
        self.mymongo_c1034: mymongo.C1034 | None = None

    @property
    def code(self) -> str:
        return self.coprs_code

    @code.setter
    def code(self, code: str):
        assert self.mymongo_c1034 is not None, "self.mymongo_c1034가 None 입니다."
        self.coprs_code = code
        self.mymongo_c1034.code = code

    @property
    def page(self) -> str:
        return self.coprs_page

    @page.setter
    def page(self, page: str):
        assert self.mymongo_c1034 is not None, "self.mymongo_c1034가 None 입니다."
        self.coprs_page = page
        self.mymongo_c1034.page = page

    def list_rows(self):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c1034, redis_name)

    def list_row_titles(self) -> list:
        return self.mymongo_c1034.list_row_titles()

    def latest_value_pop2(self, title: str) -> Tuple[str, float]:
        redis_name = self.code_page + '_latest_value_pop2_' + title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c1034.latest_value(title)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - latest_value_pop2")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - latest_value_pop2")
            return json.loads(cached_data)

    def find_with_yoy(self, row_title: str) -> Tuple[int, dict]:
        redis_name = self.code_page + '_find_with_yoy_' + row_title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c1034.find(row_title, remove_yoy=False)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - find_with_yoy")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - find_with_yoy")
            return json.loads(cached_data)

    def find_without_yoy(self, row_title: str) -> Tuple[int, dict]:
        redis_name = self.code_page + '_find_without_yoy_' + row_title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c1034.find(row_title, remove_yoy=True)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - find_without_yoy")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - find_without_yoy")
            return json.loads(cached_data)

    def sum_recent_4q(self, title: str) -> Tuple[str, float]:
        redis_name = self.code_page + '_sum_recent_4q_' + title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c1034.sum_recent_4q(title)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - sum_recent_4q")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - sum_recent_4q")
            return json.loads(cached_data)

    def find_yoy(self, title: str) -> float:
        """
        타이틀에 해당하는 전년/분기대비 값을 반환한다.\n

        Args:
            title (str): 찾고자 하는 타이틀

        Returns:
            float: 전년/분기대비 증감율

        Note:
            중복되는 title 은 첫번째것 사용\n
        """
        redis_name = self.code_page + '_find_yoy_' + title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c1034.find_yoy(title)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - find_yoy")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - find_yoy")
            return json.loads(cached_data)



class C103(C1034):
    PAGES = mymongo.C103.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c103손익계산서q', 'c103재무상태표q', 'c103현금흐름표q', 'c103손익계산서y', 'c103재무상태표y', 'c103현금흐름표y'
        """
        super().__init__(code, page)
        self.mymongo_c1034 = mymongo.C103(code, page)


class C104(C1034):
    PAGES = mymongo.C104.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c104y', 'c104q
        """
        super().__init__(code, page)
        self.mymongo_c1034 = mymongo.C104(code, page)


class C106(Corps):
    PAGES = mymongo.C106.PAGES

    def __init__(self, code: str, page: str):
        """
        :param code:
        :param page: 'c106y', 'c106q
        """
        super().__init__(code, page)
        self.mymongo_c106 = mymongo.C106(code, page)

    @property
    def code(self) -> str:
        return self.coprs_code

    @code.setter
    def code(self, code: str):
        self.coprs_code = code
        self.mymongo_c106.code = code

    @property
    def page(self) -> str:
        return self.coprs_page

    @page.setter
    def page(self, page: str):
        self.coprs_page = page
        self.mymongo_c106.page = page

    def list_row_titles(self) -> list:
        return self.mymongo_c106.list_row_titles()

    def list_rows(self):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c106, redis_name)

    def find(self, row_title: str) -> dict:
        redis_name = self.code_page + '_find_' + row_title
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c106.find(row_title)
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - find")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - find")
            return json.loads(cached_data)

    def get_rivals(self) -> list:
        redis_name = self.code_page + '_rivals'
        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c106.get_rivals()
            # print(data)
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c103468 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - find")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - find")
            return json.loads(cached_data)



class C108(Corps):
    def __init__(self, code: str):
        """
        :param code:
        """
        self.mymongo_c108 = mymongo.C108(code)
        super().__init__(code, 'c108')

    @property
    def code(self) -> str:
        return self.coprs_code

    @code.setter
    def code(self, code: str):
        self.coprs_code = code
        self.mymongo_c108.code = code

    def list_rows(self):
        redis_name = self.code_page + '_rows'
        return super()._list_rows(self.mymongo_c108, redis_name)

    def get_recent_date(self) -> datetime.datetime | None:
        redis_name = self.code_page + '_recent_date'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            # json은 datetime 형식은 저장할 수 없어서 문자열로 저장한다.
            recent_date = self.mymongo_c108.get_recent_date()
            if recent_date is None:
                str_data = ''
            else:
                str_data = recent_date.isoformat()

            if str_data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(str_data))
                # 60분후 키가 자동으로 제거됨 - c108 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - C108().get_recent_date()")
            return recent_date
        else:
            print("Redis 캐시에서 데이터 가져오기 - C108().get_recent_date()")
            str_data = json.loads(cached_data)
            if str_data == '':
                return None
            else:
                return datetime.datetime.fromisoformat(str_data)

    def get_recent(self) -> List[dict] | None:
        redis_name = self.code_page + '_recent'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_c108.get_recent()
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨 - c108 업데이트할때 제거되도록..
                # Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - C108().get_recent()")
            return data
        else:
            print("Redis 캐시에서 데이터 가져오기 - C108().get_recent()")
            return json.loads(cached_data)


class MI(Base):
    def __init__(self, index: str):
        """mi 데이터베이스 클래스

        Note:
            db - mi\n
            col - 'aud', 'chf', 'gbond3y', 'gold', 'silver', 'kosdaq', 'kospi', 'sp500', 'usdkrw', 'wti', 'avgper', 'yieldgap', 'usdidx' - 총 13개\n
            doc - date, value\n
        """
        self.mymongo_mi = mymongo.MI(index)
        self.mi_index = 'mi' + '.' + index
        self.index = index
        super().__init__()

    @property
    def index(self) -> str:
        return self._index

    @index.setter
    def index(self, index: str):
        assert index in mymongo.MI.COL_TITLE, f'Invalid value : {index}({mymongo.MI.COL_TITLE})'
        self._index = index

    def get_recent(self) -> Tuple[str, float]:
        redis_name = self.mi_index + '_recent'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_mi.get_recent()
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨
                Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - MI().get_recent()")
            return data
        else:
            print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - MI().get_recent()")
            return json.loads(cached_data)

    def get_trend(self) -> dict:
        redis_name = self.mi_index + '_trend'

        try:
            cached_data = self.redis_client.get(redis_name).decode('utf-8')
        except AttributeError:
            # redis에 해당하는 값이 없는 경우
            data = self.mymongo_mi.get_trend()
            if data:
                # 데이터를 Redis에 캐싱
                self.redis_client.set(redis_name, json.dumps(data))
                # 60분후 키가 자동으로 제거됨
                Base.redis_client.expire(redis_name, 3600)
            print("Mongo에서 데이터 가져오기 - MI().get_trend()")
            return data
        else:
            print(f"Redis 캐시에서 데이터 가져오기(남은시간:{Base.redis_client.ttl(redis_name)}초) - MI().get_trend()")
            return json.loads(cached_data)

