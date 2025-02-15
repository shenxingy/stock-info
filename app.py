from flask import Flask, render_template, request, redirect, url_for
from alpha_vantage_service import AlphaVantageService
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)

# 初始化服务类
alpha_vantage = AlphaVantageService()

@app.route("/")
def index():
    # 主页，只显示一个简单的表单让用户输入股票代码
    return render_template("index.html")

@app.route("/stock", methods=["POST"])
def handle_stock_form():
    """
    当表单使用 POST 提交时，由该路由处理；
    然后重定向到 /stock/<symbol>
    """
    symbol = request.form.get("symbol")
    return redirect(url_for("stock_page", symbol=symbol.upper()))

@app.route("/stock/<symbol>")
def stock_page(symbol):
    # 1. 调用 Alpha Vantage 接口获取各种信息
    overview = alpha_vantage.get_company_overview(symbol)
    quote = alpha_vantage.get_global_quote(symbol)
    time_series = alpha_vantage.get_daily_time_series(symbol)
    
    one_year_ago = datetime.now() - timedelta(days=365)

    highs_52 = []
    lows_52 = []
            
    # 2. 判断是否是无效 Symbol（检查 overview 中是否有 "Name" 且不为空）
    if not overview or "Name" not in overview or not overview["Name"]:
        error_msg = f"The stock symbol '{symbol}' is invalid. Please try again."
        # 返回模板，并将关键字段都设为 "N/A" 或空，防止模板中报错
        return render_template(
            "stock.html",
            error_msg=error_msg,
            symbol="N/A",
            company_name="N/A",
            sector="N/A",
            industry="N/A",
            market_cap="N/A",
            pe_ratio="N/A",
            eps="N/A",
            dividend="N/A",
            dividend_yield="N/A",
            exchange="N/A",
            current_price="N/A",
            previous_close="N/A",
            open_price="N/A",
            volume="N/A",
            high_52_week = "N/A",
            low_52_week = "N/A",
            dates=[],
            closes=[]
        )

    # 3. 如果 Symbol 有效，提取所需字段
    for date_str, daily_info in time_series.items():
    # Parse date from string
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj >= one_year_ago:
            # "2. high" or "3. high" or "2. high adjusted"? 
            # Check how your data is named—commonly "2. high"
            daily_high = float(daily_info["2. high"])
            daily_low = float(daily_info["3. low"])
            highs_52.append(daily_high)
            lows_52.append(daily_low)
        
        # Safely compute the 52-week high/low if we have at least one day
        if highs_52 and lows_52:
            high_52_week = max(highs_52)
            low_52_week = min(lows_52)
        else:
            high_52_week = "N/A"
            low_52_week = "N/A"
    
    company_name = overview.get("Name", "N/A")
    sector = overview.get("Sector", "N/A")
    industry = overview.get("Industry", "N/A")
    market_cap = overview.get("MarketCapitalization", "N/A")
    pe_ratio = overview.get("PERatio", "N/A")
    eps = overview.get("EPS", "N/A")
    dividend = overview.get("DividendPerShare", "N/A")
    dividend_yield = overview.get("DividendYield", "N/A")
    exchange = overview.get("Exchange", "N/A")

    current_price = quote.get("05. price", "N/A")
    previous_close = quote.get("08. previous close", "N/A")
    open_price = quote.get("02. open", "N/A")
    volume = quote.get("06. volume", "N/A")
    latest_news = alpha_vantage.get_stock_news(symbol, limit=5)

    # 4. 处理时间序列数据，提取日期和收盘价，以供画图
    dates = []
    closes = []
    for date_str, daily_info in sorted(time_series.items()):
        dates.append(date_str)
        closes.append(float(daily_info["4. close"]))

    # 5. 正常渲染模板
    return render_template(
        "stock.html",
        error_msg=None,  # 无错误信息
        symbol=symbol,
        company_name=company_name,
        sector=sector,
        industry=industry,
        market_cap=market_cap,
        pe_ratio=pe_ratio,
        eps=eps,
        dividend=dividend,
        dividend_yield=dividend_yield,
        exchange=exchange,
        current_price=current_price,
        previous_close=previous_close,
        open_price=open_price,
        volume=volume,
        high_52_week=high_52_week,
        low_52_week=low_52_week,
        news=latest_news,
        dates=dates,
        closes=closes
    )