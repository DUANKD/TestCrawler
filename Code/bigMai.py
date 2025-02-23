import requests
import json
import time
import datetime
from urllib.parse import urlencode

class DaMaiTicket:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.damai.cn/',
            'Host': 'www.damai.cn'
        }
        self.cookies = {}  # 需要手动获取登录后的cookies
        
    def set_cookies(self, cookie_string):
        """设置cookies"""
        cookie_dict = {}
        for item in cookie_string.split(';'):
            if '=' in item:
                key, value = item.strip().split('=', 1)
                cookie_dict[key] = value
        self.cookies = cookie_dict
        self.session.cookies.update(cookie_dict)

    def get_performance_info(self, item_id):
        """获取演出信息"""
        # url = f'https://detail.damai.cn/item.htm?id={item_id}'
        url = f'https://search.damai.cn/external/gl.html?type=1&projects={item_id}'
        try:
            # 添加 XSRF-TOKEN
            self.session.cookies.set('XSRF-TOKEN', '24565e79-3e04-45e8-9ed4-a41247daded7')
            headers = self.headers.copy()  # Create a copy of headers
            headers['X-XSRF-TOKEN'] = '24565e79-3e04-45e8-9ed4-a41247daded7'
            headers['Accept'] = 'application/json, text/plain, */*'
            response = self.session.get(url, headers=headers)  # Fix: Use headers as keyword argument
            performance_info = response.json()
            print("演出信息：", json.dumps(performance_info, ensure_ascii=False, indent=2))
            return performance_info
        except Exception as e:
            print(f"获取演出信息失败: {str(e)}")
            return None

    def check_ticket_status(self, item_id):
        """检查票务状态"""
        url = f'https://detail.damai.cn/subpage?itemId={item_id}'
        try:
            response = self.session.get(url, headers=self.headers)
            data = response.json()
            return data
        except Exception as e:
            print(f"检查票务状态失败: {str(e)}")
            return None

    def submit_order(self, item_id, sku_id):
        """提交订单"""
        url = 'https://buy.damai.cn/multi/trans/createOrder'
        data = {
            'itemId': item_id,
            'skuId': sku_id,
            'quantity': 1,  # 购买数量
        }
        try:
            response = self.session.post(url, headers=self.headers, json=data)
            return response.json()
        except Exception as e:
            print(f"提交订单失败: {str(e)}")
            return None

    def auto_buy(self, item_id, target_price=None):
        """自动抢票"""
        while True:
            # 获取演出信息
            performance_info = self.get_performance_info(item_id)
            if not performance_info:
                continue

            # 检查票务状态
            status = self.check_ticket_status(item_id)
            if not status:
                continue

            # 这里需要根据实际返回数据结构进行解析
            # 判断是否有票并且价格合适
            # if self._check_availability(status, target_price):
            #     # 获取到合适的票，尝试下单
            #     order_result = self.submit_order(item_id, status['skuId'])
            #     if order_result and order_result.get('success'):
            #         print("抢票成功！")
            #         break

            print("等待下一次尝试...")
            time.sleep(0.5)  # 避免请求过于频繁

    def _check_availability(self, status, target_price):
        """检查是否有合适的票"""
        # 需要根据实际返回数据结构实现具体逻辑
        return False

def main():
    # 创建抢票实例
    ticket_bot = DaMaiTicket()
    
    # 设置登录cookies（需要手动获取）
    # cookies = input("请输入cookies字符串：")
    cookies = 'gAsFbx5lqCGpdITvsxw9AVtkS6rLJ0uMXAEehdc-CAiXUKrYjqXsnkLkMVuwKxMRE='
    ticket_bot.set_cookies(cookies)
    
    # 设置目标演出ID
    # item_id = input("请输入演出ID：")
    item_id = 874727420209
    
    # 设置目标价格（可选）
    target_price = input("请输入期望价格（直接回车则不限制价格）：")
    if target_price:
        target_price = float(target_price)
    
    # 开始抢票
    print("开始抢票...")
    ticket_bot.auto_buy(item_id, target_price)

if __name__ == "__main__":
    main()