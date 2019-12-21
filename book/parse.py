#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from pandas.core.frame import DataFrame
from xpinyin import Pinyin

def remove_punctuation(line, strip_all=True):
    if strip_all:
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub('',line)
    else:
        punctuation = """！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟﹋〾〿‘’‛“”„‟…‧﹏"""
        re_punctuation = "[{}]+".format(punctuation)
        line = re.sub(re_punctuation, "", line)

    return line.strip()

def rreplace(self, old, new, *max):
    count = len(self)
    if max and str(max[0]).isdigit():
        count = max[0]
    return new.join(self.rsplit(old, count))

def fill_reshape(lines, rows, cols):
    size = rows * cols
    lines_temp = [''] * size
    for i in range(len(lines)):
        lines_temp[i] = lines[i]
    df = DataFrame(lines_temp)
    b = df.as_matrix().reshape(cols,rows)
    return DataFrame(b).transpose()
    
def main():
    data = r'阅评书目.xlsx'
    output_data = rreplace(data, '.', '_sorted.', 1)
    df = pd.read_excel(data)
    writer = pd.ExcelWriter(output_data)
    book_list = []
    book_list_filter = {}
    book_list_sorted = []
    rows = df.index.size
    cols = df.columns.size
    for i in range(cols):
        for j in range(rows):
            book_list.append(df.iat[j,i])
    
    for i in range(cols):
        book_list.insert(i*(rows + 1), df.columns[i])
    
    for i in range(len(book_list)):
        if str(book_list[i]).strip().lower() != "nan":
            key = remove_punctuation(str(book_list[i]).strip())
            book_list_filter[key] = str(book_list[i])

    print("Total size before sort: %d" %len(book_list_filter))
    # Sort list from order of pinyin
    pin = Pinyin()
    result = []
    for k, v in book_list_filter.items():
        result.append((pin.get_pinyin(k),k))
    result.sort()
    for i in range(len(result)):
        result[i]=result[i][1]
    
    for i in range(len(result)):
        book_list_sorted.append(book_list_filter[result[i]])

    #Save as excel with original value
    print("Total size after sort: %d" %len(book_list_sorted))
    df_out = fill_reshape(book_list_sorted, rows + 1, cols)
    df_out.to_excel(writer, 'sheet 1', header=False, index = False)
    writer.save()

if __name__ == "__main__":
    main()
