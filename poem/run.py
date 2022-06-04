# -*- coding: UTF-8 -*-

from asyncio.windows_events import NULL
from encodings import utf_8
import os
import re
import pandas as pd
import numpy as np
import time
from process import *
# import pickle


path_data = './poems/data/'

def process_data():

    dict_poem_name, dict_contents, dict_all, df_all= preprocess()



    num_dict_word, dict_word = word_count(dict_all)

    df_all = rank_determine(df_all)
    df_all.to_csv(path_or_buf=path_data+'df_all.csv') #这两行执行一次就好
    # # df_all:id, dynasty_name, poet_name, poem_name, contents, desc, weight_poet, weight_poem

    # print(df_all.shape)


    matrix_binary_all = make_matrix_binary(num_dict_word, dict_word, dict_all)
    # matrix_binary_dynasty = make_matrix_binary(num_dict_word, dict_word, dict_dynasty_name)
    matrix_binary_poem = make_matrix_binary(num_dict_word, dict_word, dict_poem_name)
    # matrix_binary_poet = make_matrix_binary(num_dict_word, dict_word, dict_poet_name)
    matrix_binary_contents = make_matrix_binary(num_dict_word, dict_word, dict_contents)

    dict_word_pinyin, dict_pinyin_word = preprocess_pinyin()

    # np.save(path_data+'dict_word.npy', dict_word)
    # np.save(path_data+'matrix_binary_all.npy', matrix_binary_all)
    # np.save(path_data+'matrix_binary_poem.npy', matrix_binary_poem)
    # np.save(path_data+'matrix_binary_contents.npy', matrix_binary_contents)
    # np.save(path_data+'dict_word_pinyin.npy', dict_word_pinyin)
    # np.save(path_data+'dict_pinyin_word.npy', dict_pinyin_word)

    
    # print('处理及存储完成')
    return dict_word, matrix_binary_all, matrix_binary_poem, matrix_binary_contents, dict_word_pinyin, dict_pinyin_word


start_time = time.time()

dict_word, matrix_binary_all, matrix_binary_poem, matrix_binary_contents, dict_word_pinyin, dict_pinyin_word = process_data() #处理一次之后就好

df_all = pd.read_csv(filepath_or_buffer=path_data+'df_all.csv') #rank 需要太多时间，所以单独读一个


end_time = time.time()

print('process time:',end_time - start_time)





#df_all, dict_word, matrix_binary_all, matrix_binary_poem, matrix_binary_contents, dict_word_pinyin, dict_pinyin_word
# df_all = np.load(path_data+'df_all.npy',allow_pickle=True)
# dict_word = np.load(path_data+'dict_word.npy',allow_pickle=True)
# matrix_binary_all = np.load(path_data+'matrix_binary_all.npy',allow_pickle=True)
# matrix_binary_poem = np.load(path_data+'matrix_binary_poem.npy',allow_pickle=True)
# matrix_binary_contents = np.load(path_data+'matrix_binary_contents.npy',allow_pickle=True)
# dict_word_pinyin = np.load(path_data+'dict_word_pinyin.npy',allow_pickle=True)
# dict_pinyin_word = np.load(path_data+'dict_pinyin_word.npy',allow_pickle=True)



flag_continue = True

while flag_continue:

    leixing = input('输入查询类型，0：binary；1：zone; 2 : fuzzy; 3: ranked;\n')

    if leixing == '0':
        query = input("请输入查询\n")
        ans = query_binary(dict_word, matrix_binary_all, df_all, query)

        out_list =  vec_to_outlist(ans)
        outlist_to_out(out_list, df_all)
    if leixing == '1':
        query = query_zone_input()
        ans = query_zone(df_all, dict_word, matrix_binary_poem, matrix_binary_contents,  query)

        out_list =  vec_to_outlist(ans)
        outlist_to_out(out_list,df_all)
    if leixing == '2':
        query = input('请输入模糊搜索\n')
        ans1, ans = query_fuzzy(dict_word_pinyin, dict_pinyin_word, dict_word, matrix_binary_all, df_all, query)

        out_list1 =  vec_to_outlist(ans1)
        out_list1 =  query_seq_noquery(out_list1, df_all)
        out_list2 =  vec_to_outlist(ans)
        out_list2 =  query_seq_noquery(out_list2, df_all)
        out_list = out_list1 + out_list2
        outlist_to_out(out_list, df_all) #最好改成模糊搜索版本的

    if leixing == '3':
        query = input('请输入搜索，我们会对结果进行排序\n')
        ans = query_binary(dict_word, matrix_binary_all, df_all, query)

        out_list = vec_to_outlist(ans)
        out_list = query_seq(query, out_list, df_all)
        outlist_to_out(out_list, df_all)

    if leixing == '4':      #zone 查询之后按照诗人诗数量和诗歌长度排序
        query = query_zone_input()
        ans = query_zone(df_all, dict_word, matrix_binary_poem, matrix_binary_contents,  query)

        out_list =  vec_to_outlist(ans)
        out_list =  query_seq_noquery(out_list, df_all)
        outlist_to_out(out_list, df_all)



    input_continue = input('是否继续查询？输入n停止查询，其他继续查询\n')
    if input_continue == 'n':
        flag_continue = False