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

ret=[]

def GetLv1(now_addr,now_dict):#province
    for prov_dict in now_dict:
        now_path=json_list[prov_dict]
        try_pronvince = now_path['n']
        # print(try_province)
        lst = 0
        p = 0
        while p < len(now_addr):
            if (addr[lst:p].find(try_pronvince) >= 0):
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
                print(province)
                ret.append(province)
                break
            p = p + 1

def Split5(raw):
    PhoneNumber=GetPhoneNumber(raw)
    raw=DelePhoneNumber(raw)#dele phone
    ret=[]
    # print(raw)
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
    # print(name+","+addr)
    if level==1:
        res_list=Split5(addr)

