from datetime import date, timedelta
from parsel import Selector

import requests

from data.config import RANGE_DAYS_FOR_SEARCH_ADDRESS, DAYS_AHEAD_FOR_SEARCH


def get_data(account: str, days: int = DAYS_AHEAD_FOR_SEARCH) -> list:
    """Получает данные для оповещения"""
    r = request_data(account, (-30, days))
    raw_records = get_raw_records(r.text)
    records = adapt_records(raw_records)
    return records


def request_data(account: str, day_range: tuple) -> requests.Response:
    """Получает данные с сайта"""
    url = 'https://ksoe.com.ua/disconnection/search/'
    date_from = date.today() + timedelta(days=day_range[0])
    date_to = date.today() + timedelta(days=day_range[1])
    data = {
        "DisconnectionForm[isprom]": 0,
        "DisconnectionForm[rem]": 'hges',
        "DisconnectionForm[account]": account,
        "DisconnectionForm[datefrom]": date_from.strftime('%d.%m.%Y'),
        "DisconnectionForm[dateto]": date_to.strftime('%d.%m.%Y')
    }
    r = requests.post(url, data=data)
    r.encoding = 'utf8'
    return r


def get_address(account: str, day_range: tuple = RANGE_DAYS_FOR_SEARCH_ADDRESS) -> str:
    """Получает адрес с сайта"""
    r = request_data(account, day_range)

    for tr in Selector(r.text).css('table.table-otkl tbody tr').extract():
        if not Selector(tr).css('td.date').extract():
            tds = Selector(tr).css('td').extract()
            address = Selector(tds[1]).css('td::text').extract_first()
            return address


def get_raw_records(html: str) -> list:
    """Парсит HTML в записи отключений"""
    raw_records = []
    for tr in Selector(html).css('table.table-otkl tbody tr').extract():
        if Selector(tr).css('td.date').extract():
            shutdown_date = Selector(tr).css('td.date::text').extract_first()
            raw_records.append({'date': shutdown_date})
        else:
            record = raw_records.pop()
            tds = Selector(tr).css('td').extract()
            record['time'] = Selector(tds[3]).css('td::text').extract_first()
            record['comment'] = Selector(tds[5]).css('td::text').extract_first()
            raw_records.append(record)
    return raw_records


def adapt_records(raw_records: list) -> list:
    """Переводим ответ на русский"""
    records = []
    for record in raw_records:
        if record['comment'] == 'Планове':
            record['comment'] = 'Плановое'
        elif record['comment'] == 'Аварійне':
            record['comment'] = 'Аварийное'
        records.append({
            'date': record['date'].split(' ')[-1],
            'time': record['time'].replace('з ', 'c '),
            'comment': record['comment']
        })
    return records
