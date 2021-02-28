#!/usr/bin/env python
# coding: utf-8

import pandas as pd

#Excelファイル読み込み
filename = "XXXXX"
df = pd.read_excel(filename + ".xlsx")

#確認
df.head()
df.columns
df.dtypes
df.shape

######################################################
#クレンジング
#行ずれをおこしている行は削除する
#プロキシ情報にblockが入っているデータは行ずれおこしていておかしいので削除
df = df[df['プロキシ情報'] != "block"]

#どんだけ減ったか確認
df.shape

#YYYY-MM-DD HH:MM:SSのdatetime列をつくる
df['(日)'] = df['(日)'].astype(str)
df['(時刻)'] = df['(時刻)'].astype(str)

#datetime列を追加　西暦2019はファイルによっては手打ちで変更忘れずに！
df["datetime"] = "2019 " + df["ログ出力時刻:(月)"].astype(str).str.cat([df["(日)"], df["(時刻)"]], sep=" ")

#object型をdatetime型に変換
df['datetime'] = pd.to_datetime(df['datetime'])

#######################################################
#グラフ描画
import matplotlib.pyplot as plt
import datetime as dt

#datetime型で範囲指定
df2 = df[(df['datetime'] >= dt.datetime(2019,10,3,9,0)) & (df['datetime'] <= dt.datetime(2019,11,1,19))]

# (width, height)
plt.figure(figsize=(20,5))

#散布図　描画
plt.scatter(df2['datetime'], df2['HTTP応答コード'])
