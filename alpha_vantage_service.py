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

    def get_stock_news(self, symbol: str, limit=5) -> list:
        """
        Fetch the latest news articles about the given stock symbol.
        Return a list of dictionaries with {title, summary, url}.
        """
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "limit": limit,  # request the number of articles
            "sort": "LATEST",
            "apikey": self.api_key
        }
        resp = requests.get(url, params=params)
        data = resp.json()

        # The structure of this JSON can vary, you need to check what the
        # actual response looks like.
        # For example, data might look like:
        # {
        #   "items": 5,
        #   "feed": [
        #       {
        #         "title": "...",
        #         "url": "...",
        #         "summary": "...",
        #         ... 
        #       },
        #       ...
        #   ]
        # }
        # We'll parse out the "feed" portion.

        articles = []
        if "feed" in data:
            for item in data["feed"][:5]:
                title = item.get("title", "No Title")
                url = item.get("url", "#")
                summary = item.get("summary", "No Summary")
                articles.append({
                    "title": title,
                    "url": url,
                    "summary": summary
                })
        return articles