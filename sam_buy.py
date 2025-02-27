import json
import requests
from time import sleep


# getCapacityData commitPay 接口的request.body都需要修改为自己的！

# 全局变量定义 无需传参 会在getCapacityData中赋值
startRealTime = ''
endRealTime = ''

# 修改点1： /getCapacityData抓包 填写下面值
longitude = ''
latitude = ''
deviceid = ''
authtoken = ''
# 修改点2： /commitPay 抓包填写下面值
# 把getCapacityData接口的response.body里一些关于库存的true或false修改一下就可以进入到commitPay方法获取trackinfo和data
trackinfo= ''



def getCapacityData():
    global startRealTime
    global endRealTime

    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/delivery/portal/getCapacityData'
    data = {
        # 修改点3：填自己的
        # "perDateList":["2022-03-30","2022-03-31","2022-04-01","2022-04-02","2022-04-03","2022-04-04","2022-04-05"],"storeDeliveryTemplateId":"1099860739333462"
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '156',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'latitude': latitude,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'

    }
    try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        # print(ret.text)
        myRet = json.loads(ret.text)
        print(myRet['data'].get('capcityResponseList')[0])
        status = (myRet['data'].get('capcityResponseList')[0].get('dateISFull'))
        time_list = myRet['data'].get('capcityResponseList')[0].get('list')
        for i in range(0,len(time_list)):
            if not time_list[i].get('timeISFull'):
                startRealTime = time_list[i].get('startRealTime')
                endRealTime = time_list[i].get('endRealTime')
                # print(startRealTime)
                print('【成功】获取配送时间')
                order(startRealTime, endRealTime)
    except Exception as e:
        print('getCapacityData [Error]: ' + str(e))
        return False


def order(startRealTime,endRealTime):

    print('下单：'+startRealTime)

    myUrl = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/commitPay'
    data = {
        
        # 修改点4： 抓包替换为自己的 修改 expectArrivalTime为startRealTime ； expectArrivalEndTime 为endRealTime

        # "goodsList":
        #     [{
        #         "isSelected":'true',"quantity":1,"spuId":"1283175","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11198003","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11834649","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11188478","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"18471933","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11193474","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"17432120","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11183508","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"10566138","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"10561730","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11183507","storeId":"5103"},
        #         {"isSelected":'true',"quantity":1,"spuId":"11193470","storeId":"5103"}],
        # "invoiceInfo":{},"cartDeliveryType":1,"floorId":1,"amount":"12680","purchaserName":"",
        # "settleDeliveryInfo":
        
        # 修改点4中的一项注意修改"expectArrivalTime":startRealTime "expectArrivalEndTime":endRealTime ：
        
        #     {"expectArrivalTime":startRealTime,
        #      "expectArrivalEndTime":endRealTime,
        #      "deliveryType":0},"tradeType":"APP","purchaserId":"","payType":0,"currency":"CNY","channel":"wechat","shortageId":1,"isSelfPickup":0,"orderType":0,
        # "couponList":[{"promotionId":"2133123123","storeId":"5103"}],"uid":"12321","appId":"12312","addressId":"145123532498",
        # "deliveryInfoVO":{"storeDeliveryTemplateId":"10998630739528765462","deliveryModeId":"1009","storeType":"4"},"remark":"",
        # "storeInfo":{"storeId":"51033","storeType":"4","areaBlockId":"13333806"},
        # "shortageDesc":"其他商品继续配送（缺货商品直接退款）","payMethodId":"1486659732"
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Content-Length': '1617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'SamClub/5.0.45 (iPhone; iOS 15.4; Scale/3.00)',
        'device-name': 'iPhone14,3',
        'device-os-version': '15.4',
        'device-id': deviceid,
        'longitude': longitude,
        'latitude': latitude,
        'track-info': trackinfo,
        'device-type': 'ios',
        'auth-token': authtoken,
        'app-version': '5.0.45.1'

    }
   try:
        ret = requests.post(url=myUrl, headers=headers, data=json.dumps(data))
        # {"code":"LIMITED","msg":"服务器正忙,请稍后再试","traceId":"","requestId":"8f4cf2f1a29d4845949bdd38f3e82c19.1035.16492924173893553","clientIp":"","rt":0,"success":false}
        print(ret.text)
        myRet = json.loads(ret.text)
        status = myRet.get('success')
        if status:
            print('【成功】哥，咱家有菜了~')
            import os
            file = r"nb.mp3"
            os.system(file)
            exit()
        else:
            order(startRealTime, endRealTime)

    except Exception as e:
        print('order [Error]: ' + str(e))
        getCapacityData()
        return False



while 1:
    getCapacityData()
    sleep(6)
