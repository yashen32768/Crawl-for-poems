保留一份不接网页的最终版本后端代码
（加上了朝代判别，如果觉得不完整可以再加）

def judge_dynasty(query):
    ans = query
    if query == '秦' or query == '秦朝' :
        ans = '先秦'
    elif query == '汉朝' or query == '汉':
        ans = '汉代'
    elif query == '南朝' or query == '北朝':
        ans = '南北朝'
    elif query == '隋朝' or query == '隋':
        ans = '隋代'
    elif query == '唐朝' or query == '唐':
        ans = '唐代'
    elif query == '宋朝' or query == '宋' or query == '北宋' or query == '南宋':
        ans = '宋代'
    elif query == '元朝' or query == '元':    
        ans = '元代'
    elif query == '明朝' or query == '明':    
        ans = '明代'
    elif query == '清朝' or query == '清':    
        ans = '清代'
    elif query == '近代' or query == '现代':    
        ans = '近现代' 
    elif query == '晋朝' or query == '晋' or query == '西晋' or query == '东晋' or query == '魏' or query == '魏国' or query == '蜀' or query == '蜀国' or query == '吴' or query == '吴国':    
        ans = '近现代' 

    return ans
