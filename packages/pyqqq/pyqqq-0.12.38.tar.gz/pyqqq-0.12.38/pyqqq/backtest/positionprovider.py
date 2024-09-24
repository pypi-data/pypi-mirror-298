import os
import datetime as dtm
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

import requests
import pyqqq
from pyqqq.utils.market_schedule import get_last_trading_day
from pyqqq.datatypes import StockPosition
from pyqqq.brokerage.helper import KISConnection, EBestConnection
from pyqqq.brokerage.kis.simple import KISStockPosition
from pyqqq.brokerage.ebest.simple import EBestStockPosition
from pyqqq.utils.logger import get_logger


class BasePositionProvider(ABC):
    """백테스트 시에 보유 포지션 정보를 제공하는 추상 클래스"""

    @abstractmethod
    def get_positions(self, date: Optional[dtm.date] = None) -> List[StockPosition]:
        pass


class KISPositionProvider(BasePositionProvider):
    """한투 브로커를 사용하여 보유 포지션 정보를 제공"""

    def __init__(self):
        self.qqq = KISConnection()

    def get_positions(self, date: Optional[dtm.date] = None) -> List[KISStockPosition]:
        return self.qqq.broker_simple.get_positions()


class EBestPositionProvider(BasePositionProvider):
    """이베스트 브로커를 사용하여 보유 포지션 정보를 제공"""

    def __init__(self):
        self.qqq = EBestConnection()

    def get_positions(self, date: Optional[dtm.date] = None) -> List[EBestStockPosition]:
        return self.qqq.broker_simple.get_positions()


class ManualPositionProvider(BasePositionProvider):
    """
    백테스팅용 포지션 정보를 직접 업데이트 하는 클래스
    """
    def __init__(
        self,
        positions: List[StockPosition]
    ):
        self.positions = positions or []

    def update_positions(self, positions: List[StockPosition]):
        self.positions = positions

    def get_positions(self, date: Optional[dtm.date] = None) -> List[StockPosition]:
        return self.positions or []


class BackPositionProvider(BasePositionProvider):
    """
    DB에 저장된 포지션 정보를 가져오는 클래스
    """
    logger = get_logger("BackPositionProvider")
    logger.setLevel(logging.DEBUG)

    def __init__(
        self,
        brokerage: str = 'kis',
        api_key: str = None,
        account_no: str = None,
    ):
        self.brokerage = brokerage
        self.api_key = api_key or pyqqq.get_api_key()
        self.account_no = account_no or (os.getenv('KIS_CANO') + os.getenv('KIS_ACNT_PRDT_CD'))

    def get_positions(self, date: dtm.date) -> List[StockPosition]:
        target_date = get_last_trading_day(date)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "date": target_date.strftime("%Y%m%d"),
            "brokerage": self.brokerage,
            "account_no": self.account_no,
        }
        r = requests.get("https://pyqqq.net/api/analytics/positions", headers=headers, params=params)
        if r.status_code == 404:
            self.logger.debug(f"404 request error: {r.text}")
            return []

        r.raise_for_status()

        data = r.json()
        positions = []
        for p in data['positions']:
            pos = StockPosition(
                asset_code=p["asset_code"],
                asset_name=p["asset_name"],
                quantity=p["quantity"],
                sell_possible_quantity=p["sell_possible_quantity"],
                average_purchase_price=Decimal(p["average_purchase_price"]),
                current_price=p["current_price"],
                current_value=p["current_value"],
                current_pnl=Decimal(p["current_pnl"]),
                current_pnl_value=p["current_pnl_value"],
            )
            positions.append(pos)

        return positions
