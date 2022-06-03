# -*- coding: UTF-8 -*-

from asyncio.windows_events import NULL
from turtle import xcor
from xmlrpc.client import Boolean
from matplotlib.style import context
import pymysql
import os
import re
import pandas as pd
import numpy as np



length_poem = 54000 

def preprocess():
    sqlfile = open('.\poems\data\poem.sql','r',encoding='utf8')
    # global df_all
    # global df_dynasty_id
    # global df_dynasty_name
    # global df_poet_name
    # global df_poem_name
    # global df_desc
    sqltxt = sqlfile.readline()

    dict_dynasty_name = {0:"醌"} #古诗词不存在的字，占位用的，可以用null，但是我想选个字（
    # dict_dynasty_id = {0:0}
    dict_poet_name = {0:"醌"}
    dict_poem_name = {0:"醌"}
    dict_contents = {0:"醌"}
    dict_desc = {0:"醌"}
    dict_all = {0:"醌"}

    while len(sqltxt) != 0 :
        sqltxt = "".join(sqltxt)
        m = re.split(r"\(|,|'",sqltxt)
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
    
    df_all = pd.DataFrame({'id':list(dict_poem_name.keys()),
                        # 'dynasty_id':list(dict_dynasty_id.values()),
                        'dynasty_name':list(dict_dynasty_name.values()),
                        'poet_name':list(dict_poet_name.values()),
                        'poem_name':list(dict_poem_name.values()),
                        'contents':list(dict_contents.values()),
                        'desc':list(dict_desc.values())})

    # df_dynasty_id = pd.DataFrame({'id':list(dict_dynasty_id.keys()),
    #                     'value':list(dict_dynasty_id.values())})
    df_dynasty_name = pd.DataFrame({'id':list(dict_dynasty_name.keys()),
                        'value':list(dict_dynasty_name.values())})
    df_poet_name = pd.DataFrame({'id':list(dict_poet_name.keys()),
                        'value':list(dict_poet_name.values())})
    df_poem_name = pd.DataFrame({'id':list(dict_poem_name.keys()),
                        'value':list(dict_poem_name.values())})
    df_contents = pd.DataFrame({'id':list(dict_contents.keys()),
                        'value':list(dict_contents.values())})
    df_desc = pd.DataFrame({'id':list(dict_desc.keys()),
                        'value':list(dict_desc.values())})

    # search_field = [df_dynasty_name, df_poet_name, df_poem_name, df_contents, df_desc]

    return dict_dynasty_name, dict_poet_name, dict_poem_name, dict_contents, dict_desc, dict_all, df_all, df_dynasty_name, df_poet_name, df_poem_name, df_contents, df_desc


def word_count(dict):
    dict_word = {"道":0}
    num_dict_word = 1

    for (key,context) in dict.items():

        context = context.replace('N','')
        context = context.replace('U','')
        context = context.replace('n','')
        context = context.replace('\\','')
        context = context.replace('，','')
        context = context.replace('。','')
        context = context.replace('!','')
        context = context.replace('?','')
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
            

    print(num_dict_word)
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
    
    length_poem = 54000 #有这么多首诗
    matrix_binary = np.zeros((num_dict_word + 1, length_poem + 1), dtype=int)
    # dict_binary = {0:np.zeros(length_poem, dtype=int)}


    for (key,context) in dic.items():
        context = context.replace('N','')
        context = context.replace('U','')
        context = context.replace('n','')
        context = context.replace('\\','')
        context = context.replace('，','')
        context = context.replace('。','')
        context = context.replace('!','')
        context = context.replace('?','')

        for j in context:
            matrix_binary[dict_word[j]][key] = 1
            
        
    return matrix_binary



def binary_search_and(vec0, vec1):
    length = len(vec0)
    ans = []
    for i in range(length):
        ans.append(  vec0[i] and vec1[i])

    return ans


def binary_search_or(vec0, vec1):
    length = len(vec0)
    ans = []
    for i in range(length):
        ans.append(  vec0[i] or vec1[i])

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


def outlist_to_out(ans_list, df_all):
    flag = np.zeros(length_poem + 1, dtype=Boolean)
    if ans_list == NULL:
        print('搜索结果为空！')
    for i in ans_list:
        if flag[i] == False:
            flag[i] = True
            out = df_all.loc[df_all.id == i]
            print(out)
            # for j in out:
            #     print(j)

def binary_search_in(context, dict_word, matrix_binary):
        context = context.replace('N','')
        context = context.replace('U','')
        context = context.replace('n','')
        context = context.replace('\\','')
        context = context.replace('，','')
        context = context.replace('。','')
        context = context.replace('!','')
        context = context.replace('?','')
        out = []
        for (i, word) in enumerate(context):
            # print(word)
            if i == 0:
                id = dict_word[word]
                out = matrix_binary[id]
            out = binary_search_and(out, matrix_binary[dict_word[word]])
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
def query_binary(dict_word, matrix_binary, df):
    query = input("请输入查询, 或者输入NOT\n")

    if query == 'NOT':
        query = input("输入NOT后查询\n")
        ans = binary_search_in(query, dict_word, matrix_binary)
        ans = binary_search_not(ans)

    else:
        ans = binary_search_in(query, dict_word, matrix_binary)

    operation = input("是否继续输入查询：AND , OR. 输入END结束查询输入\n")
    while operation != 'END':
        query = input("请输入查询,或者输入NOT\n")
        if query == 'NOT':
            query = input("输入NOT后查询")
            temp = binary_search_in(query, dict_word, matrix_binary)
            temp = binary_search_not(temp)
        else:
            temp = binary_search_in(query, dict_word, matrix_binary)
        if operation == 'AND':
            ans = binary_search_and(ans, temp)
        if operation == 'OR':
            ans = binary_search_or(ans, temp)
        
        operation = input("是否继续输入查询：AND , OR. 输入END结束查询输入\n")


    out_list =  vec_to_outlist(ans)
    outlist_to_out(out_list,df)



def query_zone_input():
    input0=input('请输入朝代，或者输入0保持空\n')
    if input0 == '':
        input0 = 0
    input1=input('请输入诗人名字，或者输入0保持空\n')
    if input1 == '':
        input1 = 0
    input2=input('请输入诗歌标题，或者输入0保持空\n')
    if input2 == '':
        input2 = 0
    input3=input('请输入诗词内容，或者输入0保持空\n')
    if input3 == '':
        input3 = 0
    return [input0,input1,input2,input3]
    


#context 里面这个形式:[dynasty,poet_name, poem_name, poem_content]， 如果没有输入NULL

def query_zone(df_all, dict_word, matrix_binary_poem, matrix_binary_contents,  context = [0,0,0,0]):
    print(context)
    if context[0] != 0:
        print('dyan')
        list_dynasty = query_exact_dynasty(context[0], df_all)
    else:
        list_dynasty = np.ones(length_poem + 1, dtype=int)
    if context[1] != 0:
        print('poet')
        list_poet = query_exact_poet(context[1], df_all)
    else:
        list_poet = np.ones(length_poem + 1, dtype=int)
    if context[2] != 0:
        print('poem')
        list_poem = binary_search_in(context[2], dict_word, matrix_binary_poem)
    else:
        list_poem = np.ones(length_poem + 1, dtype=int)
    if context[3] != 0:
        print('s')
        list_context = binary_search_in(context[3], dict_word, matrix_binary_contents)
    else:
        list_context = np.ones(length_poem + 1, dtype=int)
    ans = binary_search_and(list_dynasty, list_poet)
    ans = binary_search_and(ans, list_poem)
    ans = binary_search_and(ans, list_context)
    
    return ans

#输出里面朝代id是空