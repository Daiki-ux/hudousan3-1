import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('hudousan-1-cbd81da179dc.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1uow6KXGYDpfNEklXqKh3NXIfP21GCADelPPIMiBaOoI'

#共有設定したスプレッドシートのワークシート3を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY)
ws2 = worksheet.get_worksheet(1)

#df_bukken = pd.DataFrame(worksheet.get_all_values())
df_bukken = pd.DataFrame(ws2.get_all_values())
df_bukken.columns = list(df_bukken.loc[0, :])
df_bukken.drop(0, inplace=True)
df_bukken.reset_index(inplace=True)
df_bukken.drop('index', axis=1, inplace=True)
df_bukken = df_bukken
df_bukken.head()
df_bukken["面積"] = df_bukken["面積"].replace(",","")
df_bukken["面積"].head()
df_bukken["徒歩"] = df_bukken["徒歩"].astype("float")
df_bukken["価格"] = df_bukken["価格"].astype("float")
df_bukken["想定利回り"] = df_bukken["想定利回り"].astype("float")
df_bukken["年月"] = df_bukken["年月"].astype("float")
df_bukken["面積"] = df_bukken["面積"].astype("float")

import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('不動産価格予測アプリ')

st.sidebar.write("""
# 不動産価格
こちらは不動産価格可視化ツールです。以下のオプションから徒歩時間・建設年を指定できます。
""")

st.sidebar.write("""
## 徒歩時間選択
""")

toho = st.sidebar.slider('徒歩(分)', 1, 30, 10)

st.sidebar.write("""
## 建設年選択
""")
nen = st.sidebar.slider('建設年', 1980, 2020, 1990)

st.write(f"""
### *{nen}年に建設*され、最寄駅から **{toho}分間** の物件の価格予測
#""")


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#matplotlib inline
from sklearn.linear_model import LinearRegression as LR
train = df_bukken
#クロスバリテーション
#内挿と外挿
#線形重回帰
y = train["価格"]
trainX = train[["徒歩","面積"]]
model = LR()
model.fit(trainX,y)

testX = pd.DataFrame([[5,200]],columns=["徒歩","面積"])
model.predict(testX)
testX = pd.DataFrame([[5,200]],columns=["徒歩","面積"])
model.predict(testX)
y = train["価格"]
trainX = train[["徒歩","年月"]]
model = LR()
model.fit(trainX,y)
#testX = pd.DataFrame([[5,1995]],columns=["徒歩","年月"])
testX = pd.DataFrame([[toho,nen]],columns=["徒歩","年月"])
pred = model.predict(testX)

st.write(f"""
### 物件の予測価格　**{format(int(pred), ',')}円** 
#""")