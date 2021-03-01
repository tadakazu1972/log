#!/usr/bin/env python
# coding: utf-8

import glob

#フォルダ内の.xlsxファイルを取得
files = glob.glob("*.xlsx")
print(files)

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

for file in files:
    
    #Excelファイル読み込み
    df = pd.read_excel(file)
    
    #クレンジング
    #行ずれをおこしている行は削除する
    #プロキシ情報にblockが入っているデータは行ずれおこしていておかしいので削除
    df = df[df['プロキシ情報'] != "block"]
    
    #YYYY-MM-DD HH:MM:SSのdatetime列をつくる
    df['(日)'] = df['(日)'].astype(str)
    df['(時刻)'] = df['(時刻)'].astype(str)
    
    #当月の最初の日と最後の日を格納
    start_str = df['(日)'].iat[0]  #o行目
    end_str   = df['(日)'].iat[-1] #最終行
    
    #数値に変換
    start = int(start_str)
    end   = int(end_str)
    
    #datetime列を追加
    #月、西暦は文字列操作でファイル名から抽出
    yearmonth = file.replace('osakashi_if_', '')
    yearmonth = yearmonth.replace('.xlsx', '')
    #月を末尾2文字目1文字目から生成
    month = yearmonth[-2:]
    #西暦を末尾2文字を削除
    year = yearmonth[:-2]
    
    df["datetime"] = year + " " + df["ログ出力時刻:(月)"].astype(str).str.cat([df["(日)"], df["(時刻)"]], sep=" ")
    
    #object型をdatetime型に変換
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    for day in range(start, end):
        
        #datetime型で範囲指定　9時～18時の間
        df2 = df[(df['datetime'] >= dt.datetime(int(year),int(month),day,9,0)) & (df['datetime'] <= dt.datetime(int(year),int(month),day,18))]
        
        fig = plt.figure(figsize=(20,5)) # (width, height)
        plt.scatter(df2['datetime'], df2['HTTP応答コード'])
        
        #ファイル書き出し
        filename = "log_graph_" + yearmonth + str(day) + ".png"
        fig.savefig(filename)
