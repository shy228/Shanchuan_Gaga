
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
from lxml import etree
import re
import json
from datetime import datetime
import re
import math
import pandas as pd
import investpy
import akshare as ak
import numpy as np
from dateutil.relativedelta import relativedelta
pd.set_option('display.max_columns',None)

# from requests_html import HTMLSession
# session = HTMLSession()
# start_day = input("起始日 yyyy-mm-dd:")
# end_day = input("截至日 yyyy-mm-dd:")

### 输入要查询的基金类型
fund_big_type = str(input("基金类型 开放基金/场内基金/货币基金："))
if fund_big_type == "开放基金":
   fund_small_type = str(input("开放式基金类型 总排名/股票型/混合型/债券型/指数型/QDII/LOF/FOF :"))
elif fund_big_type == "货币基金":
    fund_small_type = str(input("开放式基金类型 总排名/A/B :"))
else:
    fund_small_type =None

### 输入要查询的时间
# date_range = str(input("查询范围 一年/五年/十年/首发至今："))
# if date_range == "一年":
#     end_date = datetime.now()-relativedelta(years=1).strftime("%Y-%m-%d")
# if date_range == "五年":
#     end_date = datetime.now()-relativedelta(years=5).strftime("%Y-%m-%d")
# if date_range == "十年":
#     end_date = datetime.now()-relativedelta(years=10).strftime("%Y-%m-%d")




### 选择headers
def get_headers(header):
    if header=='AJJ':
        header={
        "Accept": "*/*",
        "Cookie": "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1658366176; Hm_lvt_a47da7b82bdb6445aef7aaa2b00470b0=1658366537; Hm_lpvt_a47da7b82bdb6445aef7aaa2b00470b0=1658366537; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1658366878; v=A-GYcY9SJ2hDoIscHwuMqIbk8Kb-jlWOfwP5lEO23ehHqg9Yi95lUA9SCWrQ",
        "Host": "fund.10jqka.com.cn",
        # "Proxy-Connection": "keep-alive",
        "Referer": "https://fund.10jqka.com.cn/008652/pubnote.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
    if header=='TTJJ':
        header= {
        "Accept": "*/*",
        "Cookie": "a383e7455c48eb40ed06b5; EMFUND0=null; EMFUND7=06-15%2016%3A05%3A04@%23%24%u5609%u5B9E%u589E%u957F%u6DF7%u5408@%23%24070002; EMFUND8=06-15%2016%3A19%3A21@%23%24%u534E%u5B9D%u4E2D%u8BC1%u91D1%u878D%u79D1%u6280%u4E3B%u9898ETF%u53D1%u8D77%u5F0F%u8054%u63A5C@%23%24013478; EMFUND9=06-16 14:29:48@#$%u524D%u6D77%u5F00%u6E90%u53EF%u8F6C%u503A%u503A%u5238@%23%24000536; ASP.NET_SessionId=5x1r1qa1cubsnrthczhgdu0g; st_si=10707895079291; st_pvi=01426301037088; st_sp=2022-06-15%2016%3A05%3A07; st_inirUrl=https%3A%2F%2Fwww.google.com%2F; st_sn=1; st_psi=20220706232939210-112200312936-3130797818; st_asi=delete",
        "Host": "fund.eastmoney.com",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://fund.eastmoney.com/data/fundranking.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
    if header=='Rf':
        header = {
            'accept': 'text/plain, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '279',
            'referer': 'https://cn.investing.com/rates-bonds/china-1-year-bond-yield-historical-data',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'PHPSESSID=p31bqia8hao6je1obud54df81s; geoC=CN; adBlockerNewUserDomains=1658378988; udid=54adec806a1241eb0618f8f22c277e0a; __cflb=04dToRbvTbLk4kLGJXyVjsASqHox7JsuBtcPrYcL2Q; __gads=ID=48d667ebae5c5417-22d928664ad500e4:T=1658379020:S=ALNI_MYfjmNZADiWOhP58RE78PUPIxRKAQ; __gpi=UID=000007ebb96a70f1:T=1658379020:RT=1658379020:S=ALNI_MZbVnTCQ5X90P2qcVKkzCGARvZdWg; _ga=GA1.2.437347470.1658379020; _gid=GA1.2.494439917.1658379025; Hm_lvt_a1e3d50107c2a0e021d734fe76f85914=1658379025; _fbp=fb.1.1658379122169.337311241; SideBlockUser=a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A2%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2229235%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A36%3A%22%2Frates-bonds%2Fchina-7-year-bond-yield%22%3B%7Di%3A1%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A5%3A%2229231%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A36%3A%22%2Frates-bonds%2Fchina-1-year-bond-yield%22%3B%7D%7D%7D%7D; adsFreeSalePopUp=3; smd=54adec806a1241eb0618f8f22c277e0a-1658381623; cf_chl_2=85a283832cbff4a; cf_chl_prog=x14; cf_clearance=Z_C_yePeRtJtq8eF_uq4zbuklW6MTVJY7_FVIlsZN8U-1658381685-0-150; nyxDorf=NTIzZDZgMWQzbzs%2FZT83NmM2NWRkYjZlZ25nZDI%2FMz9nYzFiMTcxPmQ0bDRjPzdoMzkyNGY5ZT89P25oMGdkMDViM2U2ajE%2BMzM7YmUz; invpc=6; _gat=1; _gat_allSitesTracker=1; __cf_bm=bEE0hWPsEmufn2qGQOwHEqanno35MKeVAbnkXWWQuAk-1658381691-0-AcFZdNpaw+qEhxlkz4eteachTY9mPilQxtXZ0i6wfQH5OnUEV8JqxKGetm+1xQAx7jKqVRXrzPe7WHkTpYtcqqthtbCW3L6qp6E1HU7dRtw/LOkrdR0UlRs+B1d/3cY6ySXuuKheWdQrHKRuUHF9hQH9vTjEIWioErh/QSq+K9nN; outbrain_cid_fetch=true; Hm_lpvt_a1e3d50107c2a0e021d734fe76f85914=1658381693'
        }
    return header

### 获取网站基金排名网页url
def get_url_ranking(fund_type, search_area):
    if fund_big_type == "开放基金":
        if fund_small_type == "总排名":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.7023344719850388'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "股票型":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.6660371233518754'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "混合型":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=hh&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.9666323519722015'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "债券型":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=zq&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=|&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.27257339539195113'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "指数型":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=zs&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=|&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.4258530484993981'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "QDII":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.8707529387112636'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "LOF":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=lof&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.9302834360505927'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        elif fund_small_type == "FOF":
            url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=fof&rs=&gs=0&sc=lnzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.7958035286407923'.format(datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%Y-%m-%d'))
        else:
            print('Invalid option!')
    elif fund_big_type == "货币基金":
        if fund_small_type == "总排名":
            url_ranking = 'http://api.fund.eastmoney.com/FundRank/GetHbRankList?intCompany=0&MinsgType=&IsSale=1&strSortCol=SYL_Y&orderType=desc&pageIndex=1&pageSize=50&callback=jQuery18301234779423494814_1657443960471&_=1657444020514'
        elif fund_small_type == "A":
            url_ranking = 'http://api.fund.eastmoney.com/FundRank/GetHbRankList?intCompany=0&MinsgType=a&IsSale=1&strSortCol=SYL_Y&orderType=desc&pageIndex=1&pageSize=50&callback=jQuery18301234779423494814_1657443960471&_=1657444324570'
        elif fund_small_type == "B":
            url_ranking = 'http://api.fund.eastmoney.com/FundRank/GetHbRankList?intCompany=0&MinsgType=b&IsSale=1&strSortCol=SYL_Y&orderType=desc&pageIndex=1&pageSize=50&callback=jQuery18301234779423494814_1657443960471&_=1657444358092'
    elif fund_big_type == "场内基金":
        url_ranking = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=fb&ft=ct&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=50&v=0.034827935304446944'
    else:
        print('Invalid option!')
    return url_ranking

### 获取网站基金排名网页源码
def get_content():
    url_ranking = get_url_ranking(fund_big_type, fund_small_type)
    header_TTJJ=get_headers('TTJJ')
    response = requests.get(url=url_ranking, headers=header_TTJJ)
    content_ranking = response.text
    # Extracting the total number of funds in the ranking·
    # obj = re.compile(r'allRecords:(?P<total_row>.*?),pageIndex:1,pageNum', re.S)
    # result = obj.finditer(content_ranking)
    # for sales in result:
    #     total_row = float(sales.group("total_row"))
    # # Dividing the total number of the funds by 50 which is the number of funds on one page
    # print('There are ', math.ceil(total_row / 50), 'pages for this fund type.')
    return content_ranking

### 所有的基金代码
def get_fund_code():
    content_ranking = get_content()
    s1 = eval(re.findall(r'\[(.*)\]',content_ranking)[0])
    print(s1)
    fund_code_list = []
    for i in s1:
        code = i.split(',')[0]
        fund_code_list.append(code)
    str(fund_code_list)
    return fund_code_list

### 获取每只基金的历史净值并每个以df格式储存在字典里
def get_price_df_dic():
    fund_code_list = get_fund_code()
    price_dic = {}
    for code in fund_code_list:
        df = ak.fund_open_fund_info_em(fund=code, indicator="单位净值走势").iloc[::-1]
        df['净值日期'] = pd.to_datetime(df['净值日期'])
        # df.set_index('净值日期',inplace=True)
        price_dic[code] = df
    return price_dic

### 获取Rf并加在df里
def get_Rf_price_df_dic():
    bonds = ak.bond_zh_us_rate()
    bonds['日期'] = pd.to_datetime(bonds['日期'])
    df = bonds.query('日期 > "2002-06-01"')
    Rfs = df.loc[:, ['日期', '中国国债收益率2年']]
    Rfs.rename(columns={'中国国债收益率2年': '无风险收益率'},inplace=True)
    Rfs['无风险收益率'] = Rfs['无风险收益率']/360
    Rfs.set_index('日期')
    price_dic = get_price_df_dic()
    for key in price_dic.keys():
        # Merging the two dataframes
        price_dic[key] = price_dic[key].merge(Rfs, left_on='净值日期', right_on='日期')
        # Setting index for the two columns
        price_dic[key] = price_dic[key].set_index('净值日期', drop=True)
        # Dropping '日期'
        del price_dic[key]['日期']
        # Filling the missing data
        price_dic[key].fillna(method='ffill')
        excess_return = price_dic[key]['日增长率'] - price_dic[key]['无风险收益率']
        price_dic[key]['超额收益']=excess_return
    return price_dic


##### 做数据
### 建立一个新的df储存分析出的数据及评分
def get_analysis_factor_df():
    fund_code_list = get_fund_code()
    analysis_factor_df = pd.DataFrame(index=fund_code_list,columns=['excess_reuturn','std','VaR1%','ES','SR','Max_Drawback','VaR1%_score','ES_score','SR_score'])
    return analysis_factor_df

### excess_reuturn std  alpha  VaR1%   ES  SR   IR 以及后几个的打分
def calculate_analysis_factors():
    analysis_factor_df = get_analysis_factor_df()
    price_dic = get_Rf_price_df_dic()
    for key in price_dic.keys():
        excess_reuturn = np.mean(price_dic[key]['超额收益'])
        std_return = np.std(price_dic[key]['日增长率'])
        VaR_10day = np.percentile(price_dic[key]['日增长率'], 1).pow(10,0.5)   ### 待优化：现在是假设正态分布 才能通过根号天数  之后需要把每十天合成一体 然后再算percentile
        VaR_1day = VaR_10day/pow(10,0.5)
        ES = np.mean(price_dic[key]['日增长率'][price_dic[key]['日增长率'] < VaR_1day])
        SR = excess_reuturn/std_return
        analysis_factor_df.loc[key, 'excess_reuturn'] = excess_reuturn
        analysis_factor_df.loc[key, 'std'] = std_return
        analysis_factor_df.loc[key,'VaR1%']=VaR_10day
        analysis_factor_df.loc[key, 'ES'] = ES
        analysis_factor_df.loc[key, 'SR'] = SR
    return analysis_factor_df

### 分开打分
def seperate_score():
    analysis_factor_df = calculate_analysis_factors()
    price_dic = get_Rf_price_df_dic()
    analysis_factor_df.sort_values(by="VaR1%", inplace=True, ascending=True)
    analysis_factor_df['VaR1%_rank'] = range(len(analysis_factor_df))
    analysis_factor_df.sort_values(by="ES", inplace=True, ascending=False)
    analysis_factor_df['ES_rank'] = range(len(analysis_factor_df))
    analysis_factor_df.sort_values(by="SR", inplace=True, ascending=False)
    analysis_factor_df['SR_rank'] = range(len(analysis_factor_df))
    for key in price_dic.keys():
        VaR1_score = 10 - ((analysis_factor_df.loc[key, 'VaR1%_rank']+1)/len(analysis_factor_df))*10
        if VaR1_score == 0:
            analysis_factor_df.loc[key, 'VaR1%_score'] = 0.1
        else:
            analysis_factor_df.loc[key, 'VaR1%_score'] = VaR1_score
        ES_score = 10 - ((analysis_factor_df.loc[key, 'ES_rank'] + 1) / len(analysis_factor_df)) * 10
        if ES_score == 0:
            analysis_factor_df.loc[key, 'ES_score'] = 0.1
        else:
            analysis_factor_df.loc[key, 'ES_score'] = ES_score
        SR_score = 10 - ((analysis_factor_df.loc[key, 'SR_rank'] + 1) / len(analysis_factor_df))*10
        if SR_score == 0:
            analysis_factor_df.loc[key, 'SR_score'] = 0.1
        else:
            analysis_factor_df.loc[key, 'SR_score'] = SR_score
    analysis_factor_df.drop(columns=['VaR1%_rank', 'ES_rank','SR_rank'],inplace=True)
    return analysis_factor_df


### 最终报告
### 建立一个新的df储存综合评分
def overall_df():
    fund_code_list = get_fund_code()
    overall_df = pd.DataFrame(index=fund_code_list,columns=['综合评分','基金名称','基金经理'])
    return overall_df

### 总体打分
def overall_score():
    analysis_factor_df=seperate_score()
    overall_df1 = overall_df()
    for index in overall_df1.index:
        overall_df1.loc[index,'综合评分']=np.mean([analysis_factor_df.loc[index, 'excess_reuturn'] / np.mean(analysis_factor_df.loc[index, 'VaR1%_score',analysis_factor_df.loc[index, 'ES_score']]),
                    analysis_factor_df.loc[index, 'SR_score']])
    overall_df1.sort_values(by='综合评分', inplace=True, ascending=False)
    print(overall_df1)
    return overall_df1
overall_score()
















