from pyqqq.utils.api_client import raise_for_status, send_request
from pyqqq.utils.local_cache import DiskCacheManager
from pyqqq.utils.market_schedule import get_last_trading_day, get_market_schedule
from typing import Optional, Union
import datetime as dtm
import pandas as pd
import pyqqq.config as c

domesticCache = DiskCacheManager('domestic_cache')


def get_alert_stocks(alert_type: str, date: dtm.date = None) -> Optional[pd.DataFrame]:
    """
    시장 경보 종목을 조회합니다.

    2024년 3월 25일 데이터 부터 조회 가능합니다.

    Args:
        alert_type (str): 경보종류. caution:투자주의종목 warning:투자경고종목 risk:투자위험종목
        date (dtm.date, optional): 조회할 날짜. 기본값은 None (가장 최근 데이터)

    Returns:
        pd.DataFrame|None: 경보 종목 리스트. 해당일에 저장된 데이터가 없으면 None, 저장되었지만 지정 종목이 없으면 빈 DataFrame이 반환됩니다.

        - code (str, index): 종목코드
        - name (str): 종목명
        - current_price (int): 현재가
        - change (int): 전일대비가격
        - change_rate (float): 전일대비등락율
        - volume (int): 거래량
        - bid_price (int): 매수호가
        - ask_price (int): 매도호가
        - per (float): PER

    Examples:
        >>> df = get_alert_stocks('caution')
        >>> print(df.head())
                    name  current_price  change  change_rate   volume  bid_price  ask_price    per
        code
        402340   SK스퀘어          77600    2400        -3.00   303590      77000      76900  -8.49
        053950    경남제약           1570       1         0.06  4857452       1569       1568  -4.91
        012320  경동인베스트         113100   11800        11.65   994188     118800     118700  22.05
        002720    국제약품           6820     310        -4.35  5559738       6900       6890 -17.14
        219420  링크제니시스           9100     160         1.79  1720993       9120       9100  83.49
    """
    url = f"{c.PYQQQ_API_URL}/domestic-stock/alert-stocks/{alert_type}"
    params = {}
    if date:
        params["date"] = date

    r = send_request("GET", url, params=params)
    if r.status_code == 404:
        return None
    else:
        raise_for_status(r)

        df = pd.DataFrame(r.json())
        if not df.empty:
            df.set_index("code", inplace=True)
        return df


def get_management_stocks(date: dtm.date = None) -> Optional[pd.DataFrame]:
    """
    관리종목을 조회합니다.

    2024년 3월 25일 데이터 부터 조회 가능합니다.

    Args:
        date (dtm.date, optional): 조회할 날짜(지정일이 아닌 데이터 수집일). 기본값은 None (가장 최근 데이터)

    Returns:
        pd.DataFrame|None: 관리종목 리스트. 해당일에 저장된 데이터가 없으면 None, 저장되었지만 지정 종목이 없으면 빈 DataFrame이 반환됩니다.

        - code (str, index): 종목코드
        - name (str): 종목명
        - current_price (int): 현재가
        - change (int): 전일대비가격
        - change_rate (float): 전일대비등락율
        - volume (int): 거래량
        - designation_date (str): 지정일
        - designation_reason (str): 지정사유

    Examples:
        >>> df = get_management_stocks()
        >>> print(df.head())
                   name  current_price  change  change_rate  volume designation_date designation_reason
        code
        001140       국보           2110       0         0.00       0       2024.03.22          감사의견 의견거절
        006380      카프로            732       0         0.00       0       2024.03.22          감사의견 의견거절
        093230     이아이디           1392       0         0.00       0       2024.03.22          감사의견 의견거절
        363280   티와이홀딩스           3205     150        -4.47  393547       2024.03.22  감사범위제한으로인한 감사의견한정
        36328K  티와이홀딩스우           4940     560       -10.18   26011       2024.03.22  감사범위제한으로인한 감사의견한정
    """
    url = f"{c.PYQQQ_API_URL}/domestic-stock/management-stocks"
    params = {}
    if date:
        params["date"] = date

    r = send_request("GET", url, params=params)
    if r.status_code == 404:
        return None
    else:
        raise_for_status(r)

        df = pd.DataFrame(r.json())
        if not df.empty:
            df.set_index("code", inplace=True)
        return df


@domesticCache.memoize()
def get_tickers(date: Optional[dtm.date] = None, market: Optional[str] = None):
    """
    주어진 날짜와 시장에 따른 주식 종목 코드와 관련 정보를 조회합니다.

    이 함수는 지정된 날짜(기본값은 오늘)와 선택적 시장('KOSPI', 'KOSDAQ')에 대한 주식 종목 코드와 추가 정보를 API를 통해 요청합니다.
    반환된 정보는 pandas DataFrame 형태로 제공되며, 데이터가 없는 경우 빈 DataFrame을 반환합니다. DataFrame은 'code'를 인덱스로 사용합니다.

    2018년 1월 1일 데이터 부터 조회 가능합니다.

    Args:
        date (Optional[dtm.date]): 조회할 날짜. 기본값은 현재 날짜입니다.
        market (Optional[str]): 조회할 시장. 'KOSPI' 또는 'KOSDAQ' 중 선택할 수 있습니다.

    Returns:
        pd.DataFrame: 주식 종목 코드와 관련 정보를 포함하는 DataFrame. 'code' 컬럼은 인덱스로 설정됩니다.

        - market (str): 시장 이름 (KOSPI 또는 KOSDAQ)
        - name (str): 종목 이름
        - type (str): 종목 유형 (EQUITY, ETF, ETN)
        - reference_price (int): 기준가
        - upper_limit (int or None): 상한가
        - lower_limit (int or None): 하한가
        - previous_close (int): 전일 종가
        - listing_date (str or None): 상장일

    Raises:
        AssertionError: 잘못된 시장 이름이 입력된 경우 오류를 발생시킵니다.
        HTTPError: API 요청이 실패했을 때 발생.

    Examples:
        >>> tickers = get_tickers()
        >>> print(tickers)
                market     name    type  reference_price  upper_limit  lower_limit  previous_close listing_date delisting_date
        code
        000020   KOSPI     동화약품  EQUITY             7820        10160         5480            7820     19760324
        000040   KOSPI    KR모터스  EQUITY              571          742          400             571     19760525
        000050   KOSPI       경방  EQUITY             6050         7860         4240            6050     19560303
        000070   KOSPI    삼양홀딩스  EQUITY            71100        92400        49800           71100     19681227
        000075   KOSPI   삼양홀딩스우  EQUITY            54200        70400        38000           54200     19920221
    """
    if market:
        assert market in [
            "KOSPI",
            "KOSDAQ",
        ], "market은 'KOSPI' 또는 'KOSDAQ'이어야 합니다."

    if date is None:
        date = dtm.date.today()
        schedule = get_market_schedule(date)
        if schedule.full_day_closed:
            date = get_last_trading_day(date)

    return _get_tickers(date, market)


def _get_tickers_check_not_expected_res(res):
    """
    get_tickers 함수에서 캐싱할 값인지 체크하는 함수
    """
    return (res is None) or res.empty


@domesticCache.memoize(not_expected_res=_get_tickers_check_not_expected_res)
def _get_tickers(date: dtm.date, market: str = None):
    """
    get_tickers 함수의 실제 구현부.
    기존 함수에선 date가 None이어도 정상적으로 돌아서 메모이제이션 하기 좋지않았음.
    """
    url = f"{c.PYQQQ_API_URL}/domestic-stock/tickers/{date.strftime('%Y%m%d')}"
    params = {}
    if market:
        params["market"] = market

    r = send_request("GET", url, params=params)
    raise_for_status(r)

    data = r.json()
    rows = data["rows"]
    cols = data["cols"]

    if len(rows) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=cols)
    df.set_index("code", inplace=True)
    return df


# 8시간 캐시하면 언제 돌려도 9시 개장 전엔 당일 데이터를 받을 수 있음
@domesticCache.memoize(expire=8 * 60 * 60, not_expected_res=_get_tickers_check_not_expected_res)
def get_ticker_info(code: str) -> Optional[pd.DataFrame]:
    """
    종목의 기본정보를 조회합니다.

    Args:
        code (str): 조회할 종목의 코드

    Returns:
        pd.DataFrame|None: 기본정보 리스트. 데이터가 없으면 None

        - code (str, index): 종목코드
        - isin (str): 국제 증권 식별 번호
        - name (str): 이름
        - market (str): 거래소
        - type (str): 종목유형. EQUITY(일반상품), ETF, ETN
        - listing_date (str): 상장일

    Examples:
        >>> df = get_ticker_info("032040")
        >>> print(df)
                isin	name	market	type	full_name	listing_date	delisting_date
        code
        032040	KR7032040008	씨앤에스자산관리	KOSDAQ	EQUITY	주식회사 씨앤에스자산관리	19970123	20181011

    """
    return _ticker_request("code", code)


def find_ticker_info(name: str) -> Optional[pd.DataFrame]:
    """
    종목명으로 기본정보를 조회합니다.

    Args:
        name (str): 조회할 종목의 이름

    Returns:
        pd.DataFrame|None: 기본정보 리스트. 데이터가 없으면 None

    Examples:
        >>> df = find_ticker_info("삼성")
        >>> print(df.head())
                isin   name market    type     full_name listing_date delisting_date
        code
        000810  KR7000810002   삼성화재  KOSPI  EQUITY      삼성화재해상보험     19750630
        000815  KR7000811000  삼성화재우  KOSPI  EQUITY  삼성화재해상보험1우선주     19900410
        001360  KR7001360007   삼성제약  KOSPI  EQUITY          삼성제약     19750704
        005930  KR7005930003   삼성전자  KOSPI  EQUITY          삼성전자     19750611
        005935  KR7005931001  삼성전자우  KOSPI  EQUITY      삼성전자1우선주     19890925

    """
    return _ticker_request("name", name)


def _ticker_request(type: str, value: str):
    url = f"{c.PYQQQ_API_URL}/domestic-stock/tickers"
    params = {type: value}

    r = send_request("GET", url, params=params)
    if r.status_code == 404:
        return None
    else:
        raise_for_status(r)

    ticker_list = [r.json()] if type == "code" else r.json()
    df = pd.DataFrame(ticker_list)

    if not df.empty:
        df.set_index("code", inplace=True)
    return df


def get_rising_stocks(market: str, time: Union[dtm.datetime, dtm.date]) -> pd.DataFrame:
    """
    지정된 시장과 시간에 따른 상승 주식 목록을 조회합니다.

    이 함수는 주어진 시장('KOSPI' 또는 'KOSDAQ')과 날짜 및/또는 시간에 대해 상승하는 주식들의 데이터를 API를 통해 요청합니다.
    휴장일인 경우 빈 DataFrame을 반환합니다. 요청한 날짜 및 시간에 대한 데이터가 없는 경우에도 빈 DataFrame을 반환하며,
    요청이 실패하면 예외를 발생시킵니다. 반환된 데이터는 'code'를 인덱스로 사용하는 DataFrame 형태로 제공됩니다.

    시간은 30분 단위로만 제공됩니다. 예를 들어 9시 30분, 10시 00분, 10시 30분 등으로만 조회할 수 있습니다.
    그 외의 시간은 30분 단위로 내림하여 조회합니다. 예를 들어 9시 15분은 9시 00분으로 조회합니다.

    2024년 5월 3일 데이터 부터 조회 가능합니다.

    Args:
        market (str): 조회할 주식 시장의 명칭. 'KOSPI' 또는 'KOSDAQ' 중 하나여야 합니다.
        time (dtm.datetime | dtm.date): 조회할 날짜와 시간. 시간이 제공되지 않은 경우 시장 종료 시간을 사용합니다.

    Returns:
        pd.DataFrame: 주식 데이터를 포함하는 DataFrame. 'code'를 인덱스로 사용합니다.

    Raises:
        AssertionError: 잘못된 시장 명칭이 입력된 경우.
        HTTPError: API 요청이 실패했을 때 발생.

    Examples:
        >>> stocks = get_rising_stocks("KOSPI", dtm.datetime.now())
        >>> print(stocks)
                rank     name  current_price  change  change_rate    volume  bid_price  ask_price  bid_volume  ask_volume    per    roe
        code
        090460     1     비에이치          20700    3060        17.35  14705798      20700      20750      107635      194628   7.87  15.11
        004090     2     한국석유          17150    2050        13.58  12984410      17150      17160       21096        4507  14.66   8.67
        002380     3      KCC         280500   33000        13.33    140193     280000     280500        1259        5112  11.72   4.13
        018880     4    한온시스템           6490     620        10.56   4428320       6480       6490       24297      146398  67.60   2.21
        025620     5  제이준코스메틱           7710     710        10.14   1231670       7700       7710         677        6139  -4.96 -16.66
    """

    assert market in ["KOSPI", "KOSDAQ"], "market은 'KOSPI' 또는 'KOSDAQ'이어야 합니다."

    if isinstance(time, dtm.datetime):
        schedule = get_market_schedule(time.date())
        if schedule.full_day_closed:
            return pd.DataFrame()
    elif isinstance(time, dtm.date):
        schedule = get_market_schedule(time)
        if schedule.full_day_closed:
            return pd.DataFrame()

        time = dtm.datetime.combine(time, schedule.close_time)
    else:
        raise ValueError("time은 datetime 또는 date 객체여야 합니다.")

    url = f"{c.PYQQQ_API_URL}/domestic-stock/rising-stocks/{market}/{time.date()}/{time.strftime('%H%M')}"
    r = send_request("GET", url)
    if r.status_code == 404:
        return pd.DataFrame()
    else:
        raise_for_status(r)

    df = pd.DataFrame(r.json())

    if not df.empty:
        df.set_index("code", inplace=True)

    return df
