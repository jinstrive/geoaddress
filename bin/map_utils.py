# -*- coding: utf-8 -*-
import simplejson as json
import urllib
import math



GEOCODE_BASE_URL = 'https://maps.google.com/maps/api/geocode/json'
googlekey = "AIzaSyAKTDQhIe3Q9tc-8aEg3aRUpXM1tCQ5qWo"


def geocode(address):
    """
    Get Json From Google Api
    :param address:
    :return:
    """
    geo_args = {
        'address': address,
        'key': googlekey,
    }
    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    req = urllib.urlopen(url)
    if req.getcode() != 200:
        return None
    response = json.loads(req.read())
    # print response
    if response['status'] != 'OK':
        return None
    results = response['results']
    rets = [(result['geometry']['location'], result['formatted_address']) for result in results]
    return rets


x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626
a = 6378245.0
ee = 0.00669342162296594323


def gcj02tobd09(lng, lat):
    """
    火星坐标系 (GCJ-02) 与百度坐标系 (BD-09) 的转换
    即谷歌、高德 转 百度
    :param lng:
    :param lat:
    :return:
    """
    z = math.sqrt(lng * lng + lat*lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lng, bd_lat


def bd09togcj02(bd_lon, bd_lat):
    """
    百度坐标系 (BD-09) 与 火星坐标系 (GCJ-02)的转换
    即 百度 转 谷歌、高德
    :param bd_lat:
    :param bd_lon:
    :return:
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lng, gg_lat


def gps84togcj02(lng, lat):
    """
    GPS84 切换 成 GCJ02
    :param lng:
    :param lat:
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return mglng, mglat


def gcj02togps84(lng, lat):
    """
    GCJ02 转换为 GPS84
    :param lng:
    :param lat:
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat


def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    是否不在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


if __name__ == '__main__':
    # address = '北京市朝阳区望京街阜安西路11号合生麒麟社2楼'
    # rets = geocode(address)
    # print rets
    lng = 116.48497662233521
    lat = 40.00425930705763
    # ret = gcj02tobd09(lng, lat)
    ret = bd09togcj02(lng, lat)
    print ret







