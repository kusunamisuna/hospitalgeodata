import csv
import json
import time
import xml.etree.ElementTree as ET
import sys

import requests
from bs4 import BeautifulSoup

URL = 'http://www.geocoding.jp/api/'
TSVPATH = './tsv/'
JSONPATH = './json/'
PREFTABLE = {"1":"Hokkaido","2":"Aomori","3":"Iwate","4":"Miyagi","5":"Akita","6":"Yamagata","7":"Fukushima","8":"Ibaraki","9":"Tochigi","10":"Gumma","11":"Saitama","12":"Chiba","13":"Tokyo","14":"Kanagawa","15":"Niigata","16":"Toyama","17":"Ishikawa","18":"Fukui","19":"Yamanashi","20":"Nagano","21":"Gifu","22":"Shizuoka","23":"Aichi","24":"Mie","25":"Shiga","26":"Kyoto","27":"Osaka","28":"Hyogo","29":"Nara","30":"Wakayama","31":"Tottori","32":"Shimane","33":"Okayama","34":"Hiroshima","35":"Yamaguchi","36":"Tokushima","37":"Kagawa","38":"Ehime","39":"Kochi","40":"Fukuoka","41":"Saga","42":"Nagasaki","43":"Kumamoto","44":"Oita","45":"Miyazaki","46":"Kagoshima","47":"Okinawa"}

def main():

    args = sys.argv
    prefcode = str(args[1])

    rows = getRows(prefcode)

    csvlist = getCSVList(rows)

    writeTSV(prefcode, csvlist)
    writeJSON(prefcode, csvlist)

def coordinate(address):
    """
    addressに住所を指定すると緯度経度を返す。

    """
    payload = {'q': address}
    html = requests.get(URL, params=payload)
    soup = BeautifulSoup(html.content, "html.parser")
    if soup.find('error'):
        print(soup)
        raise ValueError(f"Invalid address submitted. {address}")
    latitude = soup.find('lat').string
    longitude = soup.find('lng').string
    return [latitude, longitude]


def getRows(prefcode):
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get('http://www.hospital.or.jp/shibu_kaiin/?sw=' + str(prefcode) + '&sk=1')

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.findAll("table", {"class": "flat_table"})[0]
    rows = table.findAll("tr")

    return rows


def getCSVList(rows):

    csvlist = []
    # ヘッダ行の追加
    headlist = ['id', 'type', 'name', 'url','beds', 'address', 'tel', 'lat', 'lon']
    csvlist.append(headlist)

    for i, row in enumerate(rows):
        csvRow = []

        if i < 1:
            continue

        csvRow.append(str(i))
        for cell in row.findAll(['td', 'th', 'a']):
            if cell.get('href'):
                csvRow.append(cell.get('href').replace('\n', ''))
            else:
                csvRow.append(cell.get_text())

        latitude, longitude = coordinate(csvRow[5])
        csvRow.append(latitude)
        csvRow.append(longitude)
        csvlist.append(csvRow)
        time.sleep(20)

    print(csvlist)

    return csvlist


def writeTSV(prefcode, csvlist):

    with open(TSVPATH + prefcode + '-hospital-' + PREFTABLE[prefcode] + '_info.tsv', 'w',newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(csvlist)

def writeJSON(prefcode, csvlist):

    with open(TSVPATH + prefcode + '-hospital-' + PREFTABLE[prefcode] + '_info.tsv',  'r',newline='',  encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter="\t")
        data = list(reader)
        fw = open(JSONPATH + prefcode + '-hospital-' + PREFTABLE[prefcode] + '_info.json', 'w', encoding='utf-8')
        json.dump(data, fw, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
