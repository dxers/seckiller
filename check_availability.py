import json
from pyparsing import restOfLine
import requests
from retrying import retry
import timeout_decorator

'''
Phone 14 Pro Max 128GB 深空黑色 MQ833CH/A

iPhone 14 Pro Max 128GB 银色 MQ843CH/A

iPhone 14 Pro Max 128GB 金色 MQ853CH/A

iPhone 14 Pro Max 128GB 暗紫色 MQ863CH/A

iPhone 14 Pro Max 256GB 深空黑色 MQ873CH/A

iPhone 14 Pro Max 256GB 银色 MQ883CH/A

iPhone 14 Pro Max 256GB 金色 MQ893CH/A

iPhone 14 Pro Max 256GB 暗紫色 MQ8A3CH/A

iPhone 14 Pro Max 512GB 深空黑色 MQ8D3CH/A

iPhone 14 Pro Max 512GB 银色 MQ8E3CH/A

iPhone 14 Pro Max 512GB 金色 MQ8F3CH/A

iPhone 14 Pro Max 512GB 暗紫色 MQ8G3CH/A

iPhone 14 Pro Max 1TB 深空黑色 MQ8H3CH/A

iPhone 14 Pro Max 1TB 银色 MQ8J3CH/A

iPhone 14 Pro Max 1TB 金色 MQ8L3CH/A

iPhone 14 Pro Max 1TB 暗紫色 MQ8M3CH/A
'''
@retry(stop_max_attempt_number=3)
@timeout_decorator.timeout(10)
def get_availability():
    stores={"R448":"王府井","R388":"西单大悦城","R320":"三里屯","R479":"华贸购物中心","R645":"朝阳大悦城"}
    iphone_url=r'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/availability.json'
    # A pro/promax
    # G 14
    sku='MQ8A3CH/A'
    headers = {'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en-US;q-0.8,en;q-0.7',
               'referer': 'https://reserve-prime.apple.com/CN/zh_CN/reserve/A/availability?&iUP=N',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.67 Safari/537.36',
               }
    cookie_str = r'dslang=CN-ZH; site=CHN; geo=CN; ccl=WwsyNcK54j2kPzLwbGGJHw==; s_orientation=%5B%5BB%5D%5D; ' \
                 r's_cc=true; check=true; s_campaign=mc-ols-energy_saver-article_ht211094-macos_ui-04022020; dssf=1; ' \
                 r'XID=1e2b043fd33526cd0d7f7b5962bb4cc1; POD=cn~zh; JSESSIONID=8B7AC75267A9983B21AAB8AD19CD5965; '
    cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in cookie_str.split("; ")}

    resp = requests.get(iphone_url, cookies=cookie_dict, headers=headers).content
    result = json.loads(resp)
    # print(result['updated'])
    for store in stores.keys():
        if result['stores'][store][sku]['availability']['unlocked']:
            print("{}有货".format(store))
            return True
    return False