from flask import Flask, render_template, request, redirect, url_for
from alpha_vantage_service import AlphaVantageService
from dotenv import load_dotenv
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

    # 2. 整理数据，提取我们需要的字段
    # 这里仅做演示，更多字段自行补充
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
    # 如果要 52-week high/low，需要另想办法（有些字段需要额外接口或由自己在 time_series 数据里遍历计算）

    # 3. 将时间序列数据处理后，可能直接传到模板，或者后端生成图表数据再传
    # 例如，将日期和收盘价整理为一个列表:
    dates = []
    closes = []
    for date_str, daily_info in sorted(time_series.items()):
        dates.append(date_str)
        closes.append(float(daily_info["4. close"]))

    # 4. 渲染模板
    return render_template(
        "stock.html",
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
        dates=dates,
        closes=closes
    )