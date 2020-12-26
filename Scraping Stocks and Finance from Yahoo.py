#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import json
import csv
import io
from bs4 import BeautifulSoup
import requests


# In[2]:


url_state = 'https://in.finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://in.finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://in.finance.yahoo.com/quote/{}/financials?p={}'


# In[3]:


stock = 'F'


# In[5]:


response = requests.get(url_financials.format(stock,stock))


# In[6]:


response


# In[7]:


response.text


# In[8]:


soup = BeautifulSoup(response.text, 'html.parser')


# In[10]:


pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]


# In[11]:


# beginning
script_data[:500]


# In[12]:


# the end
script_data[-500:]


# In[13]:


start = script_data.find("context")-2


# In[14]:


json_data = json.loads(script_data[start:-12])


# In[15]:


json_data['context'].keys()


# In[16]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()


# In[21]:


annual_ls = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterly_ls = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quarterly_bf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']


# In[22]:


print(annual_ls[0])


# In[23]:


annual_ls[0]['operatingIncome']


# In[25]:


annual_is_stmts = []

# consolidate annual
for s in annual_ls:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_is_stmts.append(statement)


# In[26]:


annual_is_stmts[0]


# In[27]:


annual_cf_stmts = []
quarterly_cf_stmts = []

# annual
for s in annual_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_cf_stmts.append(statement)
            
# quarterly
for s in quarterly_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    quarterly_cf_stmts.append(statement)


# In[28]:


annual_cf_stmts[0]


# In[29]:


# Profile data


# In[31]:


response = requests.get(url_profile.format(stock,stock))
soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find("context")-2

json_data = json.loads(script_data[start:-12])


# In[32]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()


# In[33]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'].keys()


# In[34]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['companyOfficers']


# In[35]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['longBusinessSummary']


# In[36]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['secFilings']['filings']


# In[37]:


# Statistical Data


# In[39]:


response = requests.get(url_state.format(stock,stock))
soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find("context")-2

json_data = json.loads(script_data[start:-12])


# In[40]:


json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']


# In[41]:


## Hisorical Stock Data


# In[42]:


stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/YESBANK.NS?period1=1577342726&period2=1608965126&interval=1d&events=history&includeAdjustedClose=true'


# In[43]:


response = requests.get(stock_url)


# In[44]:


response.text


# In[45]:


stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'
params = {
    'range':'5y',
    'interval':'1d',
    'events':'history',
    'includeAdjustedClose':'true'
}


# In[46]:


response = requests.get(stock_url.format(stock), params=params)


# In[47]:


response.text


# In[51]:


from io import StringIO
file = StringIO(response.text)
reader = csv.reader(file)
data = list(reader)
for row in data[:5]:
    print(row)


# In[52]:


response = requests.get(stock_url.format(stock), params=params)


# In[53]:


file = StringIO(response.text)
reader = csv.reader(file)
data = list(reader)
for row in data[:5]:
    print(row)


# In[ ]:




