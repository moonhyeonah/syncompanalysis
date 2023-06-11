#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np


# In[2]:


# 파일 읽어서(매행의 state정보와, found, candidates_count) pandas 데이터 프레임 만들기
# 'Found'가 아닌 경우 출력하고 스킵
# 'state','found' 순으로 정렬
def read_data():
    resultlist = []
    cnt_NotFound = 0
    file = open('NotFound.txt', 'w')
    #with open('smallbasic_tutorial_analysis_results.txt', 'r') as f:
    #with open('ansi_c_kandr_analysis_results.txt', 'r') as f:
    with open('c-collection-analysis-result.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:    # 파일 읽기가 종료된 경우
                break
            strings = line.split()
            if 'NotFound' in strings:
                cnt_NotFound += 1
                print(line)
                file.write(line)
                continue

            state = int(strings.pop(0))
            candidates = int(strings.pop(-1))
            found = int(strings.pop(-1))            
            strings.pop(-1)
            syntax = " ".join(strings)
            resultlist.append([state,syntax,found,candidates])
    
    file.close()
    print('number of NotFound:', cnt_NotFound)
    print()
    df = pd.DataFrame(resultlist, columns=['state','syntax','found','candidates_count'])
    print(df)
    print(df.sort_values(by=['state','found'], ascending=[True,True]))
    return df


# In[3]:


# 각각의 값(state, found, candidates_count)들이 몇번 나타나는지 확인
def df_info():
    count_state = df['state'].value_counts()
    print('state: unique value & count')
    print(count_state)
    print()
    count_found = df['found'].value_counts()
    print('found: unique value & count')
    print(count_found)
    print()
    count_candidates = df['candidates_count'].value_counts()
    print('candidates_count: unique value & count')
    print(count_candidates)


# In[4]:


# 후보군의 50% 안에서 발견한 확률
def calculate_50persent(df):
    # 후보자내 50% 안에서 발견될 확률을 구하기 위해
    df['50%'] = (df['candidates_count'] / 2)
    # 후보자내 50%를 나타내는 값 반올림
    df['50%'] = df['50%'] + 0.1
    df['50%'] = df['50%'].round()
    # 후보자내 50%와 같거나 작은 범위에서 발견된 데이터 추출
    idx = df[df['found']<=df['50%']].index
    print(len(idx))
    print(df['found'].count())    
    print('후보군의 50% 안에서 발견한 확률(%): ', len(idx)/df['found'].count()*100)


# In[5]:


# 구문 후보 목록 첫페이지(10개) 보다 더 뒤에서 발견한 확률
def calculate_1page(df):
    idx = df[df['found'] > 10].index
    #print(len(idx))
    #print(df['found'].count())
    print('후보군 중 10개 보다 더 뒤에서 발견한 확률(%): ', len(idx)/df['found'].count()*100)
    #print(idx)
    nextpage = df.iloc[idx]
    print(nextpage)
    nextpage.to_csv('nextpage.txt', sep = ' ', index = False)


# In[ ]:





# In[6]:


# 후보군중 몇%내에서 발견됐는지 확인
def found_per_candidate(df):
    df['found_percent'] = df['found'] / df['candidates_count']
    print('[mean of total]:', df['found_percent'].mean())
    df.to_csv('found_per_candidate.csv')
    
    #print(df.groupby('state')['found_percent'].describe())
    found_percent_mean = df.groupby('state')['found_percent'].mean()   
    print('[mean per state]')
    print(found_percent_mean)
    found_percent_mean.to_csv('found_percent_mean.csv')
    
    plt.figure(figsize = (10,5)) 
    plt.scatter(found_percent_mean.index, found_percent_mean)
    plt.xlabel('state')
    plt.ylabel('found_ratio')
    plt.show()


# In[7]:


# 구문을 찾기위한 스크롤 횟수의 평균값 구하기
def num_of_scroll(df):
    df['scroll'] = df['found'] - 1
    print('[필요한 스크롤수의 전제 평균]:', df['scroll'].mean())
    
    num_of_scroll_per_state_mean = df.groupby('state')['scroll'].mean()   
    print('[필요한 스크롤수의 상태별 평균]')
    print(num_of_scroll_per_state_mean)
    num_of_scroll_per_state_mean.to_csv('num_of_scroll_mean.csv')
    
    candidates = df.groupby('state')['candidates_count'].mean()
    candidates = candidates.astype(int)
    
    # x축은 state, y축은 스크롤 횟수, 막대그래프 위의 숫자는 후보군의 갯수
    plt.figure(figsize = (10,5)) 
    num_of_scroll_per_state_mean = df.groupby('state')['scroll'].mean()
    plt.bar(num_of_scroll_per_state_mean.index, num_of_scroll_per_state_mean)
    for i, v in enumerate(num_of_scroll_per_state_mean.index):
        plt.text(v, num_of_scroll_per_state_mean[v], candidates[v],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                 fontsize = 9, 
                 color='blue',
                 horizontalalignment='center',  # horizontalalignment (left, center, right)
                 verticalalignment='bottom')    # verticalalignment (top, center, bottom)

    plt.xlabel('state')
    plt.ylabel('scroll')
    plt.show()


# In[8]:


df = read_data()
df


# In[9]:


df_info()


# In[10]:


calculate_50persent(df)
df


# In[19]:


calculate_1page(df)
df


# In[12]:


found_per_candidate(df)


# In[20]:


num_of_scroll(df)


# In[21]:


df['scroll'].value_counts()


# In[15]:


df['scroll'].value_counts(normalize=True)


# In[16]:


df['found'].value_counts()


# In[17]:


df.groupby('state')['scroll'].describe()


# In[18]:


df['scroll'].describe()


# In[87]:


candidates = df.groupby('state')['candidates_count'].mean()
type(candidates)
candidates = candidates.astype(int)


# In[88]:


# x축은 state, y축은 스크롤 횟수, 막대그래프 위의 숫자는 후보군의 갯수
plt.figure(figsize = (10,5)) 
num_of_scroll_per_state_mean = df.groupby('state')['scroll'].mean()
plt.bar(num_of_scroll_per_state_mean.index, num_of_scroll_per_state_mean)
for i, v in enumerate(num_of_scroll_per_state_mean.index):
    plt.text(v, num_of_scroll_per_state_mean[v], candidates[v],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize = 9, 
             color='blue',
             horizontalalignment='center',  # horizontalalignment (left, center, right)
             verticalalignment='bottom')    # verticalalignment (top, center, bottom)
plt.show()


# In[ ]:





# In[5]:


df.info()


# In[6]:


count_found = df['found'].value_counts()
count_found


# In[7]:


count_found.sum()


# In[8]:


df = df.sort_values(by=['state','found'], ascending=[True,True])
df


# In[9]:


count_state = df['state'].value_counts()
count_state


# In[10]:


count_state.sum()


# In[11]:


df.to_csv('test.csv')


# In[12]:


df['found'].describe()


# In[13]:


df2 = df[df['found'] > 10]
df2


# In[14]:


(2/602)*100


# In[15]:


df2 = df[df['found'] < 3]
df2


# In[16]:


495/602


# In[17]:


df2 = df[df['found'] < 5]
df2


# In[18]:


# 후보자내 50% 안에서 발견될 확률을 구하기 위해
df['50%'] = (df['candidates_count'] / 2)
df


# In[19]:


# 후보자내 50%를 반올림
df['50%'] = df['50%'] + 0.1
df['50%'] = df['50%'].round()
df


# In[20]:


# 후보자내 50%와 같거나 작은 범위에서 발견된 데이터 추출
df3 = df[df['found']<=df['50%']]
df3


# In[21]:


(537/602)*100


# In[22]:


df['found_percent'] = df['found'] / df['candidates_count']
df


# In[23]:


df


# In[24]:


df = df.sort_values(by=['state','found'], ascending=[True,True])
df


# In[25]:


df.groupby('state')['found_percent'].describe()


# In[26]:


found_percent_mean = df.groupby('state')['found_percent'].mean()
found_percent_mean


# In[27]:


plt.figure(figsize = (10,5)) 
#found_percent_mean.T.plot()
plt.scatter(found_percent_mean.index, found_percent_mean)
plt.show()


# In[28]:


df.to_csv('raw.csv')


# In[ ]:





# In[16]:


df.sort_values(by='candidates_count', ascending=True)


# In[18]:


df.sort_values(by='candidates_count', ascending=True).to_csv('sort.csv')


# In[20]:


df99 = df[df.candidates_count == 1]


# In[21]:


df99['state'].value_counts()


# In[ ]:




