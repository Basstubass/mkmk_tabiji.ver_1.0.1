# https://qiita.com/Spooky_Maskman/items/9f4c487ed884d803641b

# モジュールのインポート
import pandas as pd
import urllib
import urllib.error
import urllib.request

# Google API モジュール
from pygeocoder import Geocoder
import googlemaps

googleapikey = 'AIzaSyBHmiWAqFiEytkNFn6jxHAqhxcIx_pO8sc'
output_path = '出力先のフォルダのパス'
pixel = '640x480'
scale = '18'

# リストの初期化
location = []

# リストに場所や地名を追加する
location = ["国会議事堂", "วัดพระแก้ว", "New York City", "Государственный Эрмитаж", "مكة المكرمة"]

# リストの表示
location

# geocodeで取得できる情報の一覧の例（国会議事堂の場合）
gmaps = googlemaps.Client(key=googleapikey)
address = u'国会議事堂'
result = gmaps.geocode(address)
result

