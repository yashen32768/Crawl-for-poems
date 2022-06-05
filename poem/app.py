# -*- coding: utf-8 -*-

import os
import re
import time
from asyncio.windows_events import NULL
from encodings import utf_8

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request

from process import *

path_data = './data/'


def process_data():
    dict_poem_name, dict_contents, dict_all, df_all = preprocess()
    num_dict_word, dict_word = word_count(dict_all)
    if not os.path.exists(path_data + 'df_all.csv'):
        df_all = rank_determine(df_all)
        df_all.to_csv(path_or_buf=path_data+'df_all.csv')  # 这两行执行一次就好
    # # df_all:id, dynasty_name, poet_name, poem_name, contents, desc, weight_poet, weight_poem
    # print(df_all.shape)
    matrix_binary_all = make_matrix_binary(num_dict_word, dict_word, dict_all)
    # matrix_binary_dynasty = make_matrix_binary(num_dict_word, dict_word, dict_dynasty_name)
    matrix_binary_poem = make_matrix_binary(
        num_dict_word, dict_word, dict_poem_name)
    # matrix_binary_poet = make_matrix_binary(num_dict_word, dict_word, dict_poet_name)
    matrix_binary_contents = make_matrix_binary(
        num_dict_word, dict_word, dict_contents)
    dict_word_pinyin, dict_pinyin_word = preprocess_pinyin()
    # np.save(path_data+'dict_word.npy', dict_word)
    # np.save(path_data+'matrix_binary_all.npy', matrix_binary_all)
    # np.save(path_data+'matrix_binary_poem.npy', matrix_binary_poem)
    # np.save(path_data+'matrix_binary_contents.npy', matrix_binary_contents)
    # np.save(path_data+'dict_word_pinyin.npy', dict_word_pinyin)
    # np.save(path_data+'dict_pinyin_word.npy', dict_pinyin_word)
    # print('处理及存储完成')
    return dict_word, matrix_binary_all, matrix_binary_poem, matrix_binary_contents, dict_word_pinyin, dict_pinyin_word


# start_time = time.time()
dict_word, matrix_binary_all, matrix_binary_poem, matrix_binary_contents, dict_word_pinyin, dict_pinyin_word = process_data()  # 处理一次之后就好
df_all = pd.read_csv(filepath_or_buffer=path_data +
                     'df_all.csv')  # rank 需要太多时间，所以单独读一个
# end_time = time.time()
# print('process time:', end_time - start_time)


'''
Web App
'''
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results", methods=['POST'])
def results():
    # try:
    query = (request.form['search'])
    method = request.form['method']
    results = []
    print(query, method)

    if method == '0':
        start_time = time.time()
        ans = query_binary(dict_word, matrix_binary_all, df_all, query)
        out_list = vec_to_outlist(ans)
        results = outlist_to_out(out_list, df_all)
        end_time = time.time()
        return render_template("results.html", results=results, query=query, num=len(results), time=end_time-start_time)

    elif method == "1":
        start_time = time.time()
        ans = query_zone(df_all, dict_word, matrix_binary_poem,
                            matrix_binary_contents,  query)
        out_list = vec_to_outlist(ans)
        results = outlist_to_out(out_list, df_all)
        end_time = time.time()
        return render_template("results.html", results=results, query=query, num=len(results), time=end_time-start_time)

    elif method == "2":
        start_time = time.time()
        ans1, ans = query_fuzzy(
            dict_word_pinyin, dict_pinyin_word, dict_word, matrix_binary_all, df_all, query)
        out_list1 = vec_to_outlist(ans1)
        out_list1 = query_seq_noquery(out_list1, df_all)
        out_list2 = vec_to_outlist(ans)
        out_list2 = query_seq_noquery(out_list2, df_all)
        out_list = out_list1 + out_list2
        results = outlist_to_out(out_list, df_all)  # 最好改成模糊搜索版本的
        end_time = time.time()
        return render_template("results.html", results=results, query=query, num=len(results), time=end_time-start_time)

    elif method == "3":
        start_time = time.time()
        ans = query_binary(dict_word, matrix_binary_all, df_all, query)
        out_list = vec_to_outlist(ans)
        out_list = query_seq(query, out_list, df_all)
        results = outlist_to_out(out_list, df_all)
        end_time = time.time()
        return render_template("results.html", results=results, query=query, num=len(results), time=end_time-start_time)

    elif method == "4":
        start_time = time.time()
        query = query_zone_input()
        ans = query_zone(df_all, dict_word, matrix_binary_poem,
                            matrix_binary_contents, query)
        out_list = vec_to_outlist(ans)
        out_list = query_seq_noquery(out_list, df_all)
        results = outlist_to_out(out_list, df_all)
        end_time = time.time()
        return render_template("results.html", results=results, query=query, num=len(results), time=end_time-start_time)
    # except:
    #     return render_template("error.html")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
