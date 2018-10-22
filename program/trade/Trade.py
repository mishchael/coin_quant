from datetime import datetime, timedelta
import time
import pandas as pd
from email.mime.text import MIMEText
from smtplib import SMTP
from ccxtParser import bfxParser
import json


# sleep
def next_run_time(time_interval, ahead_time=1):

    if time_interval.endswith('m'):
        now_time = datetime.now()
        time_interval = int(time_interval.strip('m'))

        target_min = (int(now_time.minute / time_interval) + 1) * time_interval
        if target_min < 60:
            target_time = now_time.replace(minute=target_min, second=0, microsecond=0)
        else:
            if now_time.hour == 23:
                target_time = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
                target_time += timedelta(days=1)
            else:
                target_time = now_time.replace(hour=now_time.hour + 1, minute=0, second=0, microsecond=0)

        # sleep直到靠近目标时间之前
        if (target_time - datetime.now()).seconds < ahead_time+1:
            print('距离target_time不足', ahead_time, '秒，下下个周期再运行')
            target_time += timedelta(minutes=time_interval)
        print('下次运行时间', target_time)
        return target_time
    else:
        exit('time_interval doesn\'t end with m')

# 获取bitfinex的k线数据
def get_bfx_candle_data(exchange, symbol, time_interval):

    # 抓取数据
    content = exchange.fetch_ohlcv(symbol, timeframe=time_interval, limit = 1000)

    # 整理数据
    df = pd.DataFrame(content, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

    return df


# 获取okex的k线数据
def get_okex_candle_data(exchange, symbol, time_interval):

    # 抓取数据
    content = exchange.fetch_ohlcv(symbol, timeframe=time_interval, since=0)

    # 整理数据
    df = pd.DataFrame(content, dtype=float)
    df.rename(columns={0: 'MTS', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]

    return df


# 下单
def place_order(exchange, order_type, buy_or_sell, symbol, price, amount):
    """
    下单
    :param exchange: 交易所
    :param order_type: limit, market
    :param buy_or_sell: buy, sell
    :param symbol: 买卖品种
    :param price: 当market订单的时候，price无效
    :param amount: 买卖量
    :return:
    """
    for i in range(5):
        try:
            # 限价单
            if order_type == 'limit':
                # 买
                if buy_or_sell == 'buy':
                    order_info = exchange.create_limit_buy_order(symbol, amount, price)  # 买单
                # 卖
                elif buy_or_sell == 'sell':
                    order_info = exchange.create_limit_sell_order(symbol, amount, price)  # 卖单
            # 市价单
            elif order_type == 'market':
                # 买
                if buy_or_sell == 'buy':
                    order_info = exchange.create_market_buy_order(symbol=symbol, amount=amount)  # 买单
                # 卖
                elif buy_or_sell == 'sell':
                    order_info = exchange.create_market_sell_order(symbol=symbol, amount=amount)  # 卖单
            else:
                pass

            print('下单成功：', order_type, buy_or_sell, symbol, price, amount)
            print('下单信息：', order_info, '\n')
            return order_info

        except Exception as e:
            print('下单报错，1s后重试', e)
            time.sleep(1)

    print('下单报错次数过多，程序终止')
    exit()


# bfx下单
def place_bfx_order(exchange, symbol, order_type, side, amount, price, *args):
    """
    下单
    :param exchange: 交易所
    :param order_type: limit, market
    :param side: buy, sell
    :param symbol: 买卖品种
    :param price: 当market订单的时候，price无效
    :param amount: 买卖量
    :return:
    """
    for i in range(5):
        try:
            # 限价单
            if order_type == 'limit':
                # 买
                if side == 'buy':
                    order_info = exchange.create_limit_buy_order(symbol, amount, price, *args)  # 买单
                # 卖
                elif side == 'sell':
                    order_info = exchange.create_limit_sell_order(symbol, amount, price, *args)  # 卖单
            # 市价单
            elif order_type == 'market':
                # 买
                if side == 'buy':
                    order_info = exchange.create_market_buy_order(symbol=symbol, amount=amount, *args)  # 买单
                # 卖
                elif side == 'sell':
                    order_info = exchange.create_market_sell_order(symbol=symbol, amount=amount, *args)  # 卖单
            else:
                pass

            print('下单成功：', order_type, side, symbol, price, amount)
            print('下单信息：', order_info, '\n')
            return order_info

        except Exception as e:
            print('下单报错，1s后重试', e)
            time.sleep(1)

    print('下单报错次数过多，程序终止')
    exit()


# bfx下margin limit单
def place_bfx_limit_order(exchange, symbol, side, amount, price, *args):
    """
    bfx下margin limit单
    :param exchange: 交易所
    :param order_type: limit, market
    :param side: buy, sell
    :param symbol: 买卖品种
    :param price: 当market订单的时候，price无效
    :param amount: 买卖量
    :return:
    """
    for i in range(5):
        try:
            # 下买单
            if side == 'buy':
                order_info = exchange.create_limit_buy_order(symbol, amount, price, *args)
            elif side == 'sell':
                order_info = exchange.create_limit_sell_order(symbol, amount, price, *args)
            print('下单成功：', side, symbol, amount ,price)
            print('下单信息：', order_info, '\n')
            return order_info

        except Exception as e:
            print('下单报错，1s后重试', e)
            time.sleep(1)

    print('下单报错次数过多，程序终止')
    exit()



# 自动发送邮件
def auto_send_email(to_address, subject, content, from_address='xing_buxing@foxmail.com', if_add_time=True):
    """
    :param to_address:
    :param subject:
    :param content:
    :param from_address:
    :return:
    使用foxmail发送邮件的程序
    """
    try:
        if if_add_time:
            msg = MIMEText(datetime.now().strftime("%m-%d %H:%M:%S") + '\n\n' + content)
        else:
            msg = MIMEText(content)
        msg["Subject"] = subject + ' ' + datetime.now().strftime("%m-%d %H:%M:%S")
        msg["From"] = from_address
        msg["To"] = to_address

        username = from_address
        password = 'your_password'

        server = SMTP('smtp.qq.com', port=587)
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()

        print('邮件发送成功')
    except Exception as err:
        print('邮件发送失败', err)


# 检查margin仓位
def check_bfx_margin_positions(exchange, symbol):
    """
    检查是否持有symbol品种的仓位
    返回该品种的持仓信息
    """
    for x in range(5):
        symbol_position = None
        try:
            response = exchange.private_post_auth_r_positions()
            positions = bfxParser.parse_positions(response)
            if positions:
                symbol_position = positions.get(symbol)
                return symbol_position
        except Exception as e:
            print('查询持仓报错，1s后重试', e)
            time.sleep(1)
        else:
            return symbol_position
        
def close_position(exchange, pos_id):
    pass

def claim_position(exchange, pos_id, amount):
    pass


def check_margin_balance(exchange):

    for i in range(5):
        try:
            margin_balance = exchange.fetch_balance(params = {'type': 'trading'})
            margin_balance = margin_balance.get('free').get('BTC')
            if not margin_balance:
                margin_balance = 0.0
        except Exception as e:
            print('获取margin balance报错，1s后重试', e)
            time.sleep(1)
        else:
            return margin_balance

def check_margin_info(exchange):
    for i in range(5):
        try:
            margin_info = exchange.private_post_auth_r_info_margin_key(params = {'key': 'base'})
            margin_info = margin_info[1][2]
            if not margin_info:
                margin_info = 0.0
        except Exception as e:
            print('获取margin balance报错，1s后重试', e)
            time.sleep(1)
        else:
            return margin_info
        
# 记录上一次交易仓位
def update_last_position(file_path, pos_dict):
    rtn = False
    for i in range(5):
        try:
            file = open(file = file_path, encoding = 'utf-8', mode = 'w')
            content = json.dumps(pos_dict)
            file.write(content)
            file.close()
        except Exception as e:
            print('更新last position报错，1s后重试', e)
            time.sleep(1)
        else:
            print('更新last position成功')
            rtn = True
            break
    return rtn
# 检查上一次交易仓位
def check_last_position(file_path):
    for i in range(5):
        try:
            file = open(file = file_path, encoding = 'utf-8', mode = 'r')
            content = file.read()
            position = json.loads(content)
            file.close()
        except FileNotFoundError as e:
            # 如果文件不存在，初始化仓位信息
            file = open(file = file_path, encoding = 'utf-8', mode = 'w')
            last_position = {}
            # 初始仓位：无仓位
            last_position['side'] = 'close'
            last_position['status'] = 'close'
            last_position['amount'] = 0
            last_position['base_price'] = 0
            last_position['leverage'] = 0
            content = json.dumps(last_position)
            file.write(content)
            file.close()
            return last_position
        except Exception as e:
            print('获取last position报错，1s后重试', e)
            time.sleep(1)
        else:
            return position


    








