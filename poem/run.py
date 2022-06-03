# -*- coding: UTF-8 -*-

from asyncio.windows_events import NULL
from turtle import xcor
from matplotlib.style import context
import pymysql
import os
import re
import pandas as pd
import numpy as np
from process import *

dict_dynasty_name, dict_poet_name, dict_poem_name, dict_contents, dict_desc, dict_all, df_all, df_dynasty_id, df_dynasty_name, df_poet_name, df_poem_name, df_contents, df_desc = preprocess()



num_dict_word, dict_word = word_count(dict_all)


# # i = 0
# # for (key,context) in dict_word.items():
# #     print(key)
# #     i = i  +1 
# #     if i > 10:
# #         break


matrix_binary_all = make_matrix_binary(num_dict_word, dict_word, dict_all)
matrix_binary_dynasty = make_matrix_binary(num_dict_word, dict_word, dict_dynasty_name)
matrix_binary_poem = make_matrix_binary(num_dict_word, dict_word, dict_poem_name)
matrix_binary_poet = make_matrix_binary(num_dict_word, dict_word, dict_poet_name)
matrix_binary_contents = make_matrix_binary(num_dict_word, dict_word, dict_contents)



# ans = binary_search_and(matrix_binary[2], matrix_binary[3])

# # vec0 = [[0,1],[1,1]]
# # ans = binary_search_and(vec0[0],vec0[1])
# # print(ans)

# out_list =  vec_to_outlist(ans)

# outlist_to_out(out_list,df_all)


# query = input("查询！\n")
# ans = binary_search_in(query, dict_word, matrix_binary_all)

# out_list =  vec_to_outlist(ans)
# outlist_to_out(out_list,df_all)



query_binary(dict_word, matrix_binary_all, df_all)