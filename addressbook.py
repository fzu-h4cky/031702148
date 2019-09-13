import json
import jsonpath
import re
direct_city={"北京","天津","上海","重庆"}
region_dict={"内蒙古":"内蒙古自治区","广西":"广西壮族自治区","宁夏":"宁夏回族自治区","新疆":"新疆维吾尔自治区","西藏":"西藏自治区"}

def GetPhoneNumber(raw):
    match = re.search(r"[0-9]{11}", raw)
    if match:
        return match.group(0)
    return "ErrorPhoneNumber"

def DelePhoneNumber(raw):
    return re.sub(r"[0-9]{11}","",raw)
set_Lv3_sub={"市","区","县"}
ret=[]
def GetLv3(now_addr,now_dict):#country
    print("Lv3" + now_addr)
    for country_dict in now_dict:
        now_path=now_dict[country_dict]
        try_country = now_path['n']
        p = 0
        while p < len(now_addr):
            # print(addr[lst:p])
            if (now_addr[0:p].find(try_country) >= 0):
                country = try_country
                
                # print(now_addr[p])
                print(country)

                # GetLv3(now_addr[p:],now_path['c'])
                break
            p = p + 1


    return
def GetLv2(now_addr,now_dict):#city
    print("Lv2"+now_addr)
    for city_dict in now_dict:
        now_path=now_dict[city_dict]
        try_city = now_path['n']
        p = -1
        while p < len(now_addr):
            p = p + 1
            if (now_addr[0:p].find(try_city) >= 0):
                city = try_city
                city=city+"市"
                ret.append(city)
                print(city)
                GetLv3(now_addr[p:],now_path['c'])
                break



    return

def GetLv1(now_addr,now_dict):#province
    print("Lv1" + now_addr)
    for prov_dict in now_dict:
        now_path=now_dict[prov_dict]
        try_pronvince = now_path['n']
        # print(try_pronvince)

        p =-1
        while p < len(now_addr):
            p = p + 1
            # print(addr[lst:p])
            if (now_addr[0:p].find(try_pronvince) >= 0):
                province=try_pronvince

                if province not in direct_city:#不是直辖市
                    flag=False
                    for s_name, f_name in region_dict.items():
                        # print(s_name + "," + f_name)
                        if (province == s_name):
                            province = f_name
                            flag=True
                            break
                    if flag==False:
                        province+="省"


                    ret.append(province)
                    print(province)
                    GetLv2(now_addr[p:], now_path['c'])
                else:
                    ret.append(province)#省=直辖
                    ret.append(province+"市")#市=直辖市
                    print(province+"市")
                    GetLv3(now_addr[p:], now_path['c'])

                break

    return

def Split5(raw):
    PhoneNumber=GetPhoneNumber(raw)
    raw=DelePhoneNumber(raw)#dele phone
    ret=[]
    print(raw)
    GetLv1(raw,json_list)
    return ret



json_file=open(r'..\lv4.json', 'rb')
data = json_file.read()
json_list= json.loads(data)
input_info=open('1.txt',"r").read()
info_list=input_info.split()
# print(info_list)
for info in info_list:
    level=int(info[0])
    tmp=info[2:]
    name=tmp.split(",")[0]
    addr=tmp.split(",")[1]
    addr = addr.replace(".", "")
    print(name+","+addr)
    if level==1:
        res_list=Split5(addr)

