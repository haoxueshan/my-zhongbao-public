import json
import time
import datetime
from bs4 import BeautifulSoup
from orderLs import getOrders
from zhongBao_unit.sqlserver import SQLserver
import os

CONFIG_FILE = "config.json"

def load_config():
    """加载 JSON 配置文件"""
    if not os.path.exists(CONFIG_FILE):
        print("Error: 配置文件不存在，将使用默认值")
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# orderDict = {'orderId': '', 'poiName': '', 'checkIn': '', 'checkOut': '', 'roomName': '', 'breakfast': '',
#              'roomCount': '', 'guest_name': '', 'guest_num': '', 'floorPrice': '', 'status': '', 'payTime': '',
#              'operator': '', 'channel': ''}

def save_pageData(startDate, endDate, page):
    sqldb = SQLserver()
    orderDataLs = getOrders(startDate, endDate, page)
    htmlData = orderDataLs[1]
    soup = BeautifulSoup(htmlData, 'html.parser')
    table = soup.find('table', {'class': 'book_table'})
    # print(table)
    tbody = table.find('tbody')
    # print(tbody)
    trs = tbody.find_all('tr', id=lambda x: x and x.startswith("exid"))
    for tr in trs:
        tds = tr.find_all('td')
        orderId = tds[0].find('a').text.strip()
        poinInfos = tds[1].find('p')
        hodelInfo = reOlder(poinInfos)
        hodelInfo['orderId'] = orderId

        olderStatus = tds[2].find('span', {'title': '订单状态'}).text.strip()
        hodelInfo['status'] = olderStatus

        olderPrice = tds[3].find('p').text.replace('￥', '').strip()
        hodelInfo['floorPrice'] = olderPrice
        # 提取操作人信息
        operator_info = tds[3].find('span')
        if operator_info:
            operator = operator_info.text.strip().split('@')[0]
        else:
            operator = None
        hodelInfo['operator'] = operator
        hodelInfo['channel'] = '众包'
        hodelInfo['guest_num'] = '1'

        select_id = sqldb.select_fetchone(f"select * from review where orderId='{orderId}'")
        print(orderId)
        if select_id != None:

            if select_id['status'].encode('latin1').decode('gbk') != hodelInfo['status'] or \
                    select_id['operator'] == None or select_id['floorPrice'] != hodelInfo['floorPrice']:
                olderUp = "update review set  status='{}',operator='{}' ,floorPrice='{}' WHERE orderId ='{}'"
                olderUp = olderUp.format(hodelInfo['status'], hodelInfo['operator'], hodelInfo['floorPrice'], orderId)
                sqldb.m_update(olderUp)
                print('更新数据：' + orderId)
            continue
        else:
            print('添加数据：' + orderId)
            inesrt_re = "insert into review(orderId, cityName, poiName, checkIn, checkOut, roomName, breakfast,roomCount," \
                        " guest_name, guest_num,floorPrice,status,payTime,operator,channel)" \
                        " values (%s, %s, %s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
            sqldb.m_insert(inesrt_re, [(hodelInfo['orderId'], hodelInfo['cityName'], hodelInfo['poiName'],
                                        hodelInfo['checkIn'], hodelInfo['checkOut'], hodelInfo['roomName'],
                                        hodelInfo['breakfast'], hodelInfo['roomCount'],
                                        hodelInfo['guest_name'], hodelInfo['guest_num'], hodelInfo['floorPrice'],
                                        hodelInfo['status'], hodelInfo['payTime'], hodelInfo['operator'],
                                        hodelInfo['channel'])])


def pageCount(startDate, endDate):
    orderDataLs = getOrders(startDate, endDate,0)
    htmlData = orderDataLs[1]
    soup = BeautifulSoup(htmlData, 'html.parser')
    div = soup.find('div', {'class': 'book_c'})
    tables = div.find_all('table')
    soup = tables[10]
    page_info_td = soup.find_all('td')[1]  # 第二个<td>标签包含总页数信息
    
    

    # 提取总页数信息
    page_info_text = page_info_td.get_text()
<<<<<<< HEAD
=======
    print(page_info_text)

>>>>>>> 605ebb79ddaf49236da455dd4c063f96f24ff1d6
    # 使用正则表达式提取总页数
    import re

    # 正则表达式模式匹配 "共xx页" 这种格式的信息
    pattern = r'共(\d+)页'
    match = re.search(pattern, page_info_text)

    if match:
        total_pages = int(match.group(1))
        return total_pages
    else:
        return "无法提取总页数信息"


def main():
    # 读取配置文件
    config = load_config()
    use_config = config.get("use_config", False) if config else False
    
    if use_config and config:
        # 使用 JSON 配置
        start_time_str = config.get("start_time", "2024-03-01")
        end_time_str = config.get("end_time", "2024-03-10 23:59")
        max_pages = config.get("max_pages", 30)

        # 转换为 datetime 格式
        start_date = datetime.datetime.strptime(start_time_str.split()[0], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_time_str[:16], "%Y-%m-%d %H:%M")
    else:
        # 采用默认参数（手动设置）
<<<<<<< HEAD
        start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        end_date = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M")
        max_pages = config.get("max_pages", 100)
    pagecountNum = pageCount(start_date, end_date)
    print(f"抓取时间段：{start_date}---{end_date}")
    print("总共页数：%s"%pagecountNum)
    print("抓取页数：%s"%max_pages)
=======
        start_date = datetime.datetime.now() - datetime.timedelta(days=10)
        end_date = datetime.datetime.now()
        max_pages = 100
    pagecountNum = pageCount(start_date, end_date)
    print(pagecountNum)
>>>>>>> 605ebb79ddaf49236da455dd4c063f96f24ff1d6

    for i in range(pagecountNum-1):
        print(f'第{i + 1}页')
        save_pageData(start_date, end_date, i)
        time.sleep(1)
        if i == max_pages:
            break
def reOlder(soup):
    def safe_find_string(soup, keyword):
        return soup.find(string=lambda s: s and keyword in s)

    import re

    def extract_room_info(text):
        match = re.search(r'房型：\s*(.*?)\s*预订：', text, re.S)
        return match.group(1).strip() if match else ''

    room_info_raw = extract_room_info(soup.get_text())

    print("[调试] 房型原始行：", repr(room_info_raw))  # 可选调试打印

    # 拆分字段
    room_info_parts = [p.strip() for p in room_info_raw.split('/') if p.strip()]
    room_type = room_info_parts[0] if len(room_info_parts) > 0 else ''
    breakfast_info = '无早'
    guest_name = ''
    room_count = '1'

    if len(room_info_parts) >= 2:
        if '不含' in room_info_parts[1]:
            breakfast_info = '无早'
        elif '含' in room_info_parts[1]:
            breakfast_info = '含早'
        else:
            breakfast_info = room_info_parts[1]
    if len(room_info_parts) >= 3:
        guest_name = room_info_parts[2]
    if len(room_info_parts) >= 4:
        room_count = room_info_parts[3].split('间')[0]

    # 提取日期
    date_info_text = safe_find_string(soup, '入离：')
    date_info = date_info_text.strip().split('至') if date_info_text else ['', '']
    check_in_date = date_info[0].replace('入离：', '').strip()
    check_out_date = date_info[1].split('(')[0].strip() if len(date_info) > 1 else ''

    # 提取预订时间
    booking_text = safe_find_string(soup, '预订：')
    booking_time = booking_text.strip().replace('预订：', '') if booking_text else ''

    # 提取地区
    location_text = safe_find_string(soup, '地区：')
    location_info = location_text.strip().split('/') if location_text else ['']
    location = location_info[0].replace('地区：', '').strip() if location_info else ''
    location = location.replace('中国,', '').strip()
    if '市' not in location:
        location += '市'

    return {
        "poiName": soup.find('b').text if soup.find('b') else '',
        "checkIn": check_in_date,
        "checkOut": check_out_date,
        "roomName": room_type,
        "guest_name": guest_name,
        "payTime": booking_time,
        "cityName": location,
        "breakfast": breakfast_info,
        "roomCount": room_count
    }


if __name__ == '__main__':
    s = 240
    import traceback
    from zhongBao_unit.emaill import Alarm

    email = Alarm()
    try:
        while True:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            main()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            time.sleep(s)
    except:
        e = traceback.format_exc()
        email.send_mail(e, '众包程序停止')
