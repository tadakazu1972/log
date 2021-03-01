#!/usr/bin/env python
# coding: utf-8

import glob

#フォルダ内の.xlsxファイルを取得
files = glob.glob("*.xlsx")
print(files)

import pandas as pd
from collections import Counter
import numpy as np

for file in files:
    
    #Excelファイル読み込み
    df = pd.read_excel(file)
    
    #クレンジング
    #行ずれをおこしている行は削除する
    #プロキシ情報にblockが入っているデータは行ずれおこしていておかしいので削除
    df = df[df['プロキシ情報'] != "block"]
    
    #URLの行だけのデータフレーム作成
    df2 = df['URL']
    
    #DataFraneのSeriesをリスト化
    text = df2.to_list()
    
    # [CONNECT ] と[:443 HTTP/1.0]をトリミング
    text = [s.replace('CONNECT ', '') for s in text]
    text = [s.replace(':443 HTTP/1.0', '') for s in text]
    
    #カウント
    cnt = Counter(text)

    # 頻度の多い順にソートしつつ、dict型をlist型にする
    cnt2 = sorted(cnt.items(), key=lambda x: x[1], reverse=True)

    #csvファイルとして保存
    filename = file.replace('.xlsx', '')
    np.savetxt(filename + '_count.csv', cnt2, delimiter=',', fmt='% s')
