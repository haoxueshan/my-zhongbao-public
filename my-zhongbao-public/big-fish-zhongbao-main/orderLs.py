import datetime
import time

import requests


def getOrders(gotime, totime, orderbb, depth=0):
    url = "https://crowds.hotel98.cn/order/maintain_order_e_V2.aspx"

    params = {
        "ss": "ok",
        "gotime": f"{gotime}",
        "totime": f"{totime}",
        "orderby": "0",
        "status": "",
        "newmanagestatus": "",
        "oid": "",
        "uid": "",
        "hname": "",
        "orderPriceLow": "",
        "orderPriceHight": "",
        "orderbb": "1",
        "page":f"{orderbb}",
    }
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9,ko;q=0.8",
        "priority": "u=0, i",
        "referer": "https://crowds.hotel98.cn/order/maintain_order_e_V2.aspx?ss=ok&gotime=2025-08-31+00%3A00&totime=2025-09-02+23%3A59&orderby=0&status=&newmanagestatus=&oid=&uid=&hname=&orderPriceLow=&orderPriceHight=&orderbb=1",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "frame",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }

    cookies = {
        "ASP.NET_SessionId": "ykvypaaiipfuvh0hlravemzn",
        "userinfo": "uid=263&gid=15&username=ztest01&realname=%e4%bc%97%e5%8c%8501&password=cab78e3d8db05a6b7c79f8fb1e8fd769",
        "loginingo": "name=ztest01&pwd=ztest01",
    }
    

    response = requests.request("GET", url, headers=headers, params=params,cookies=cookies)

    ordersData = response.text

    if "没有登录，请登录后操作" in ordersData:
        if depth == 3:
            return False, '没有登录，请登录后操作'
        time.sleep(120)
        return getOrders(gotime, totime, orderbb, depth + 1)


    else:
        return True, ordersData


if __name__ == '__main__':
    startDate = (datetime.datetime.now() - datetime.timedelta(days=10))
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.datetime.now()
    endDate = endDate.strftime("%Y-%m-%d %H:%M")
    print(startDate)
    print(getOrders(startDate, endDate, 0))
