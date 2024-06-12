# Japan-stock-info.jsonに記載されている銘柄コードの株価をyfinanceで取得し、LINEに通知するプログラムを作成しています。

import json
import yfinance as yf
from linebot import LineBotApi
from linebot.models import TextSendMessage

file1 = open("Japan-stock-info.json", "r")
stock_info = json.load(file1)

file2 = open("info.json", "r")
LINE_info = json.load(file2)

CHANNEL_ACCESS_TOKEN = LINE_info["CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

for stock in stock_info:
    stock_code = stock["code"]
    stock_name = stock["name"]
    ticker = yf.Ticker(stock_code + ".T")
    stock["stock_price"] = ticker.history(period="1d")["Close"][0]
    stock["stock_high"] = ticker.history(period="1d")["High"][0]
    stock["stock_price_yesterday"] = ticker.history(period="5d")["Close"][0]
    stock["stock_price_last_month"] = ticker.history(period="1mo")["Close"][0]

    stock["from_previous_day"] = round((stock["stock_price"] - stock["stock_price_yesterday"]) / stock["stock_price_yesterday"] * 100, 2)
    stock["month_over_month"] = round((stock["stock_price"] - stock["stock_price_last_month"]) / stock["stock_price_last_month"] * 100, 2)

    if stock["from_previous_day"] > 0:
        stock["from_previous_day"] = "+" + str(stock["from_previous_day"])
        
    if stock["month_over_month"] > 0:
        stock["month_over_month"] = "+" + str(stock["month_over_month"])

    message = (
            stock_name + "(" + stock_code + ")\n"
              + "終値 : " + str(stock["stock_price"]) + "円\n"
              + "高値 : " + str(stock["stock_high"]) + "円\n"
              + "前日比 : " + str(stock["from_previous_day"]) + "%\n"
              + "先月末比 : " + str(stock["month_over_month"]) + "%"
    )
    
    line_bot_api.push_message(LINE_info["USER_ID"], TextSendMessage(text=message))
