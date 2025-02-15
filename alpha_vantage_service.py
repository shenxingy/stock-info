import os
import requests

class AlphaVantageService:
    def __init__(self, api_key=None):
        # 可以从环境变量中获取 key，或者从参数传进来
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_company_overview(self, symbol: str) -> dict:
        """
        获取公司概况
        """
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    def get_global_quote(self, symbol: str) -> dict:
        """
        获取实时行情数据
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data.get("Global Quote", {})

    def get_daily_time_series(self, symbol: str) -> dict:
        """
        获取日级别历史数据（用于绘制图表）
        """
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "compact",  # 或者 "full" 获取更长历史数据
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data.get("Time Series (Daily)", {})