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
set_Lv4_sub={"街道","镇","乡"}
ret=[]
def GetLv5(now_addr):#street
    print("Lv5" + now_addr)
    if(level==1):
        ret[5]=now_addr
        return

def GetLv4(now_addr,now_dict):#street
    print("Lv4" + now_addr)
    if len(now_dict)==1:
        for i in now_dict:
            print(now_dict[i])
            now_dict=now_dict[i]['c']
            break
        GetLv5(now_addr, now_dict)
        return
    for street_dict in now_dict:
        now_path=now_dict[street_dict]
        try_street = now_path['n']
        p = -1
        while p < len(now_addr):
            p = p + 1
            # print(addr[lst:p])
            if (now_addr[0:p].find(try_street) >= 0):
                street = try_street
                print("!!!"+now_addr[p:p+2])
                if now_addr[p] in set_Lv4_sub:
                    street=street+now_addr[p]
                    p+=1
                if now_addr[p:p+2] in set_Lv4_sub:
                    street=street+now_addr[p:p+2]
                    p+=2
                print(street)
                ret[4]=street
                GetLv5(now_addr[p:])
                return
    GetLv5(now_addr)
    return

def GetLv3(now_addr,now_dict):#country
    print("Lv3" + now_addr)
    if len(now_dict)==1:
        for i in now_dict:
            print(now_dict[i])
            now_dict=now_dict[i]['c']
            break
        GetLv4(now_addr, now_dict)
        return

    for country_dict in now_dict:
        now_path=now_dict[country_dict]
        try_country = now_path['n']
        p = -1
        while p < len(now_addr):
            p = p + 1
            # print(addr[lst:p])
            if (now_addr[0:p].find(try_country) >= 0):
                country = try_country

                # print("!!!"+now_addr[p])
                if now_addr[p] in set_Lv3_sub:
                    country=country+now_addr[p]
                    p+=1
                print(country)
                ret[3]=country
                GetLv4(now_addr[p:],now_path['c'])
                return
    GetLv4(now_addr, now_dict)
    return

def GetLv2(now_addr,now_dict):#city
    if len(now_dict)==1:
        for i in now_dict:
            print(now_dict[i])
            now_dict=now_dict[i]['c']
            break
        GetLv3(now_addr, now_dict)
        return
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
                ret[2]=(city)
                print(city)
                GetLv3(now_addr[p:],now_path['c'])
                return

    GetLv3(now_addr, now_dict)
    return

def GetLv1(now_addr,now_dict):#province
    print("Lv1" + now_addr)
    if len(now_dict)==1:
        for i in now_dict:
            print(now_dict[i])
            now_dict=now_dict[i]['c']
            break
        GetLv1(now_addr, now_dict)
        return


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


                    ret[1]=(province)
                    print(province)
                    GetLv2(now_addr[p:], now_path['c'])
                else:
                    ret[1] = (province)
                    ret[2]=(province+"市")#市=直辖市
                    print(province)
                    GetLv2(now_addr[p:], now_path['c'])


                    # ret[1]=(province)#省=直辖
                    # ret[2]=(province+"市")#市=直辖市
                    # print(province+"市")
                    # GetLv3(now_addr[p:], now_path['c'])

                return
    GetLv2(now_addr, now_dict)
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
    ret.clear()
    for i in range(10):
        ret.append("")
    level=int(info[0])
    tmp=info[2:]
    name=tmp.split(",")[0]
    addr=tmp.split(",")[1]
    addr = addr.replace(".", "")
    print(name+","+addr)
    if level==1:
        res_list=Split5(addr)
        print(ret)

