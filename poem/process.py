# -*- coding: UTF-8 -*-

from asyncio.windows_events import NULL
from unittest import result
from xmlrpc.client import Boolean
import pymysql
import os
import re
import pandas as pd
import numpy as np


path_data = './data/'
length_poem = 54000


def preprocess():
    sqlfile = open(path_data+'poem.sql', 'r', encoding='utf8')
    # global df_all
    # global df_dynasty_id
    # global df_dynasty_name
    # global df_poet_name
    # global df_poem_name
    # global df_desc
    sqltxt = sqlfile.readline()

    dict_dynasty_name = {0: "醌"}  # 古诗词不存在的字，占位用的，可以用null，但是我想选个字（
    # dict_dynasty_id = {0:0}
    dict_poet_name = {0: "醌"}
    dict_poem_name = {0: "醌"}
    dict_contents = {0: "醌"}
    dict_desc = {0: "醌"}
    dict_all = {0: "醌"}

    while len(sqltxt) != 0:
        sqltxt = "".join(sqltxt)
        m = re.split(r"\(|,|'", sqltxt)
        #print(len(m))
        # for (i,content) in enumerate(m):
        #     print(i)
        #     print(content)

        id = int(m[13]) - 159171
        # dict_dynasty_id[id] = m[14]
        dict_dynasty_name[id] = m[16]
        dict_poet_name[id] = m[19]
        dict_poem_name[id] = m[25]
        dict_contents[id] = m[31]
        dict_desc[id] = m[33]
        dict_all[id] = m[16] + m[19] + m[25] + m[31]

        # 13 id
        # 14 dynasty_id
        # 16 dynasty
        # 19 poet_name
        # 25 poem_name
        # 31 contents
        # 33 poet_desc

        sqltxt = sqlfile.readline()

    sqlfile.close()

    df_all = pd.DataFrame({'id': list(dict_poem_name.keys()),
                           # 'dynasty_id':list(dict_dynasty_id.values()),
                           'dynasty_name': list(dict_dynasty_name.values()),
                           'poet_name': list(dict_poet_name.values()),
                           'poem_name': list(dict_poem_name.values()),
                           'contents': list(dict_contents.values()),
                           'desc': list(dict_desc.values())})

    # df_dynasty_id = pd.DataFrame({'id':list(dict_dynasty_id.keys()),
    #                     'value':list(dict_dynasty_id.values())})
    # df_dynasty_name = pd.DataFrame({'id':list(dict_dynasty_name.keys()),
    #                     'value':list(dict_dynasty_name.values())})
    # df_poet_name = pd.DataFrame({'id':list(dict_poet_name.keys()),
    #                     'value':list(dict_poet_name.values())})
    # df_poem_name = pd.DataFrame({'id':list(dict_poem_name.keys()),
    #                     'value':list(dict_poem_name.values())})
    # df_contents = pd.DataFrame({'id':list(dict_contents.keys()),
    #                     'value':list(dict_contents.values())})
    # df_desc = pd.DataFrame({'id':list(dict_desc.keys()),
    #                     'value':list(dict_desc.values())})

    return dict_poem_name, dict_contents, dict_all, df_all


def word_count(dict):
    dict_word = {"道": 0}
    num_dict_word = 1

    for (key, context) in dict.items():

        context = context.replace('N', '')
        context = context.replace('U', '')
        context = context.replace('n', '')
        context = context.replace('\\', '')
        context = context.replace('，', '')
        context = context.replace('。', '')
        context = context.replace('!', '')
        context = context.replace('?', '')
        # context = context.replace('。','')
        # print("content")
        # print(context)

        for j in context:
            # print(j in dict_word.keys())
            if j in dict_word.keys():
                continue
            else:
                dict_word[j] = num_dict_word
                num_dict_word = num_dict_word + 1

    # print(num_dict_word)
    return num_dict_word, dict_word

# query = ''

# con = 'y'
# while con != 'n':
#     query = input('查询\n')
#     if query in dict_word.keys():
#         print(dict_word[query])
#     else:
#         print("未查询到！")
#     con = input('是否继续查询？输入n停止\n')


#

def make_matrix_binary(num_dict_word, dict_word, dic):

    length_poem = 54000  # 有这么多首诗
    matrix_binary = np.zeros(
        (num_dict_word + 1, length_poem + 1), dtype=Boolean)
    # dict_binary = {0:np.zeros(length_poem, dtype=int)}

    for (key, context) in dic.items():
        context = context.replace('N', '')
        context = context.replace('U', '')
        context = context.replace('n', '')
        context = context.replace('\\', '')
        context = context.replace('，', '')
        context = context.replace('。', '')
        context = context.replace('!', '')
        context = context.replace('?', '')

        for j in context:
            matrix_binary[dict_word[j]][key] = 1

    return matrix_binary


def binary_search_and(vec0, vec1):
    length = len(vec0)
    ans = []
    for i in range(length):
        ans.append(vec0[i] and vec1[i])

    return ans


def binary_search_or(vec0, vec1):
    length = len(vec0)
    ans = []
    for i in range(length):
        ans.append(vec0[i] or vec1[i])

    return ans


def binary_search_not(vec0):
    length = len(vec0)
    ans = []
    for i in range(length):
        ans.append(not vec0[i])

    return ans


def vec_to_outlist(vec0):
    length = len(vec0)
    ans = []
    for i in range(length):
        if vec0[i] == 1:
            ans.append(i)
    return ans

#按顺序这个东西其实并不太好搞，因为有AND OR NOT，所以这里删掉


def outlist_to_out(ans_list, df_all):
    flag = np.zeros(length_poem + 1, dtype=Boolean)
    num = 0
    if ans_list == NULL:
        print('搜索结果为空！')
    # print(ans_list)
    results = []
    print(ans_list)

    for i in ans_list:
        number = i
        # print(i[0])
        if flag[number] == False:
            num = num + 1
            flag[number] = True
            out = df_all.loc[df_all.id == number]
            # print(out)        
            res = {"dynasty_name": out.dynasty_name.values.tolist(),
                   "poet_name": out.poet_name.values.tolist(), 
                   "poem_name": out.poem_name.values.tolist(),
                   "contents": out.contents.values.tolist()}
            print(res)
            results.append(res)

    print('共搜到诗的数目：')
    print(num)
    return results


def query_seq(query, ans_list, df_all):
    # print('query')
    # print(query)
    ans = []

    if ans_list == NULL:
        return
    for i in ans_list:
        out = df_all.loc[df_all.id == i].values[0]
        if out[3].find(query) >= 0:
            # print(out[2])
            ans.append([i, out[3].find(query), out[7], out[8]])
        if out[4].find(query) >= 0:
            # print(out[3])
            # 加一个权重,从而保证同名诗人和同名诗歌出现时，诗人在前面，后面同理, 顺序是诗人、诗歌、朝代、内容
            ans.append([i, out[4].find(query) + 1, out[7], out[8]])
        if out[2].find(query) >= 0:
            # print(out[4])
            ans.append([i, out[2].find(query) + 2, out[7], out[8]])
        if out[5].find(query) >= 0:
            # print(out[4])
            # print(i)
            # print(out[4].find(query))
            ans.append([i, out[5].find(query) + 3, out[7], out[8]])

    ans.sort(key=lambda x: x[3])
    ans.sort(key=lambda x: x[2], reverse=True)
    ans.sort(key=lambda x: x[1])

    ans_num = []
    for i in ans:
        ans_num.append(ans[0])
    return ans_num


def query_seq_noquery(ans_list, df_all):  # query 太复杂而不好对其排序
    # print('query')
    # print(query)
    ans = []

    if ans_list == NULL:
        return
    for i in ans_list:
        out = df_all.loc[df_all.id == i].values[0] 
        # print(out)
        ans.append([i, out[7], out[8]])

    ans.sort(key=lambda x: x[2])
    ans.sort(key=lambda x: x[1], reverse=True)

    ans_num = []
    for i in ans:
        ans_num.append(ans[0])
    return ans_num


def binary_search_in(context, dict_word, matrix_binary, df_all):
    context = context.replace('N', '')
    context = context.replace('U', '')
    context = context.replace('n', '')
    context = context.replace('\\', '')
    context = context.replace('，', '')
    context = context.replace('。', '')
    context = context.replace('!', '')
    context = context.replace('?', '')
    context = context.replace('nan', '')
    out = np.ones(length_poem + 1, dtype=int)
    for (i, word) in enumerate(context):
        # print(word)
        # if i == 0:
        #     id = dict_word[word]
        #     out = matrix_binary[id]
        #应该能去，要是出bug加回来
        out = binary_search_and(out, matrix_binary[dict_word[word]])
    # print(out)
    for (id, value) in enumerate(out):
        if value == 1:
            context_in_all = df_all.loc[df_all.id == id].values[0]
            # print(len(context_in_all))
            # print(context_in_all)
            exist = context_in_all[2].find(context) + context_in_all[3].find(
                context) + context_in_all[4].find(context) + context_in_all[5].find(context)
            #查询位置+1，似乎是因为读入df的问题
            if exist == -4:
                # print(context)
                # print(context_in_all)
                # assert()
                out[id] = 0
    return out


def query_exact_poet(context, df_all):
    ans = np.zeros(length_poem + 1, dtype=int)
    list = df_all.id[df_all.poet_name == context]
    for i in list:
        ans[i] = 1
    return ans


def query_exact_dynasty(context, df_all):
    ans = np.zeros(length_poem + 1, dtype=int)
    list = df_all.id[df_all.dynasty_name == context]
    for i in list:
        ans[i] = 1
    return ans


# 说实话很乱，不如一次性输入一串字符串来拆（
# def query_binary_old(dict_word, matrix_binary_dynasty, matrix_binary_poet, matrix_binary_poem, matrix_binary_all, df):
#     query = input("请输入查询, 或者输入NOT\n")

#     if query == 'NOT':
#         query = input("输入NOT后查询\n")
#         # ans = query_binary_seq(dict_word, matrix_binary_dynasty, matrix_binary_poet, matrix_binary_poem, matrix_binary_all, query)
#         ans = binary_search_in(query, dict_word, matrix_binary_all, df)
#         ans = binary_search_not(ans)

#     else:
#         ans = binary_search_in(query, dict_word, matrix_binary_all, df)

#     operation = input("是否继续输入查询：AND , OR. 输入END结束查询输入\n")
#     while operation != 'END':
#         query = input("请输入查询,或者输入NOT\n")
#         if query == 'NOT':
#             query = input("输入NOT后查询")
#             temp = binary_search_in(query, dict_word, matrix_binary_all, df)
#             temp = binary_search_not(temp)
#         else:
#             temp = binary_search_in(query, dict_word, matrix_binary_all, df)
#         if operation == 'AND':
#             ans = binary_search_and(ans, temp)
#         if operation == 'OR':
#             ans = binary_search_or(ans, temp)

#         operation = input("是否继续输入查询：AND , OR. 输入END结束查询输入\n")


#     out_list =  vec_to_outlist(ans)
#     outlist_to_out(out_list, df)

def query_binary(dict_word, matrix_binary_all, df, query):

    if query == NULL:
        print('输入错误！')
    ans = np.ones(length_poem + 1, dtype=int)
    # 查询形如 白居易 AND 琵琶行 AND NOT 李清照 用空格隔开各个查询项
    m = re.split(r" ", query)
    prev = 1  # 0 word 1 AND 2 OR
    prev_not = 0  # 0 False 1 True
    for context in m:
        if context == 'AND':
            prev = 1
        elif context == 'OR':
            prev = 2
        elif context == 'NOT':
            prev_not = 1
        else:
            temp = binary_search_in(context, dict_word, matrix_binary_all, df)

            if prev_not == 1:
                temp = binary_search_not(temp)
                prev_not = 0
            if prev == 1:
                ans = binary_search_and(ans, temp)
            if prev == 2:
                ans = binary_search_or(ans, temp)

            prev = 0

    return ans


def query_zone_input():
    input0 = input('请输入朝代，或者输入0保持空\n')
    if input0 == '':
        input0 = 0
    input1 = input('请输入诗人名字，或者输入0保持空\n')
    if input1 == '':
        input1 = 0
    input2 = input('请输入诗歌标题，或者输入0保持空\n')
    if input2 == '':
        input2 = 0
    input3 = input('请输入诗词内容，或者输入0保持空\n')
    if input3 == '':
        input3 = 0
    return [input0, input1, input2, input3]


#context 里面这个形式:[dynasty,poet_name, poem_name, poem_content]， 如果没有输入0

def query_zone(df_all, dict_word, matrix_binary_poem, matrix_binary_contents,  context=[0, 0, 0, 0]):
    # print(context)
    if context[0] != 0:
        # print('dyan')
        list_dynasty = query_exact_dynasty(context[0], df_all)
    else:
        list_dynasty = np.ones(length_poem + 1, dtype=int)
    if context[1] != 0:
        # print('poet')
        list_poet = query_exact_poet(context[1], df_all)
    else:
        list_poet = np.ones(length_poem + 1, dtype=int)
    if context[2] != 0:
        # print('poem')
        list_poem = binary_search_in(context[2], dict_word, matrix_binary_poem)
    else:
        list_poem = np.ones(length_poem + 1, dtype=int)
    if context[3] != 0:
        # print('s')
        list_context = binary_search_in(
            context[3], dict_word, matrix_binary_contents)
    else:
        list_context = np.ones(length_poem + 1, dtype=int)
    ans = binary_search_and(list_dynasty, list_poet)
    ans = binary_search_and(ans, list_poem)
    ans = binary_search_and(ans, list_context)

    return ans

#输出里面朝代id是空


def query_binary_test(context, df_all):
    print(df_all.loc[df_all.dynasty_name == context])
    print(df_all.loc[df_all.poem_name == context])
    print(df_all.loc[df_all.poet_name == context])
    print(df_all.loc[df_all.contents == context])


def preprocess_pinyin():
    pinyin_file = open(path_data + '\pinyin.txt', 'r', encoding='utf8')
    ptxt = pinyin_file.readline()

    dict_word_pinyin = {'阿': []}
    dict_pinyin_word = {'a': ['阿']}

    while len(ptxt) != 0:
        ptxt = ptxt.strip('\n')
        ptxt = "".join(ptxt)

        m = re.split(r" ", ptxt)
        word = ''
        for (i, context) in enumerate(m):
            if i == 0:
                word = context
            if i != 0:
                if context in dict_word_pinyin.keys():
                    dict_word_pinyin[word].append(context)
                else:
                    dict_word_pinyin[word] = [context]

                if context in dict_pinyin_word.keys():
                    dict_pinyin_word[context].append(word)
                else:
                    dict_pinyin_word[context] = [word]

        ptxt = pinyin_file.readline()

    pinyin_file.close()

    return dict_word_pinyin, dict_pinyin_word

    # for item in dict_word_pinyin.items():
    #     print(item)


def query_fuzzy(dict_word_pinyin, dict_pinyin_word, dict_word, matrix_binary_all, df_all, query_word):

    ans1 = binary_search_in(query_word, dict_word, matrix_binary_all, df_all)

    ans = np.ones(length_poem + 1, dtype=int)
    for word in query_word:
        if word in dict_word_pinyin.keys():
            pinyins = dict_word_pinyin[word]
        else:
            continue  # 就，这个字在拼音表里面根本找不到，直接跳过吧，当作所有项都符合（， 如果存在的话则这个字肯定有读音，后面不需要再判断
        temp = np.zeros(length_poem + 1, dtype=int)
        for pinyin in pinyins:
            word_list = dict_pinyin_word[pinyin]
            temp2 = np.zeros(length_poem + 1, dtype=int)
            for fuzzy_word in word_list:
                if fuzzy_word in dict_word.keys():
                    temp2 = binary_search_or(temp2, binary_search_in(
                        fuzzy_word, dict_word, matrix_binary_all, df_all))
                else:
                    continue  # 同音字在古诗词里面从来没有使用过，直接跳过。（如‘啥’‘铝’等字）
            temp = binary_search_or(temp, temp2)

        ans = binary_search_and(ans, temp)

    #要改一下最好，但是怎么改还在想
    return ans1, ans


def rank_determine(df_all):
    # print("???")
    # length = df_all.shape[0]
    # for i in range(length):
    #     row = df_all.loc[df_all.id == i].value[0]
    list_weight_poet = []  # 诗人的诗越多，权重越重
    list_weight_poem = []  # 诗人的诗越短，权重越重

    for index, row_df in df_all.iterrows():
        if index % 1000 == 0:
            print(index)
        # print(index, row)
        row = row_df.values
        poet_name = row[2]  # 这里不需要+1，因为还没存进去
        noname = '无名氏'

        if poet_name.find(noname) >= 0:
             num_poet = 1
        else:
            num_poet = df_all.id[df_all.poet_name == poet_name].count()
        list_weight_poet.append(num_poet)

        len_poem = len(row[4])
        list_weight_poem.append(len_poem)

    df_all['weight_poet'] = list_weight_poet
    df_all['weight_poem'] = list_weight_poem

    return df_all
