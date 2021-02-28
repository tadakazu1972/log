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

#################################################
#クレンジング
#行ずれをおこしている行は削除する
#プロキシ情報にblockが入っているデータは行ずれおこしていておかしいので削除
df = df[df['プロキシ情報'] != "block"]

#どんだけ減ったか確認
df.shape

#URLの行だけのデータフレーム作成
df2 = df['URL']

#DataFraneのSeriesをリスト化
text = df2.to_list()

# [CONNECT ] と[:443 HTTP/1.0]をトリミング
text = [s.replace('CONNECT ', '') for s in text]
text = [s.replace(':443 HTTP/1.0', '') for s in text]

#####################################################
#カウント
from collections import Counter
cnt = Counter(text)

print(len(text))
print(cnt)

# 頻度の多い順にソートしつつ、dict型をlist型にする
cnt2 = sorted(cnt.items(), key=lambda x: x[1], reverse=True)
print(cnt2[:10]) #確認
print(len(cnt2)) #確認

#csvファイルとして保存
import numpy as np
np.savetxt(filename+'_count.csv', cnt2, delimiter=',', fmt='% s')
