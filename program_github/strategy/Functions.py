import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 1000)


def transfer_to_period_data(df, rule_type='15T'):
    """
    将数据转换为其他周期的数据
    :param df:
    :param rule_type:
    :return:
    """ 

    # =====转换为其他分钟数据
    period_df = df.resample(rule=rule_type, on='candle_begin_time', label='left', closed='left').agg(
        {'open': 'first',
         'high': 'max',
         'low': 'min',
         'close': 'last',
         'volume': 'sum',
         })
    period_df.dropna(subset=['open'], inplace=True)  # 去除一天都没有交易的周期
    period_df = period_df[period_df['volume'] > 0]  # 去除成交量为0的交易周期
    period_df.reset_index(inplace=True)
    df = period_df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]

    return df


def transfer_utc_to_gmt8(df):
    """
    将从交易所下载的K线数据的utc时间转换为GMT8的时间，+8小时
    :param df:
    :return:
    """ 

    df['candle_begin_time'] = pd.to_datetime(df['date']) + pd.Timedelta(hours = 8)
    df.sort_values(by = 'candle_begin_time', ascending = True, inplace = True)
    df = df[['candle_begin_time', 'open', 'high', 'low', 'close', 'volume']]
    df.reset_index(inplace = True, drop = True)

    return df

