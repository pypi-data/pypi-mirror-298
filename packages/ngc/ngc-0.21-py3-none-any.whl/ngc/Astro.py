import json
import urllib

def UTCformat(it,timtRegion=8):
    import dateutil
    from datetime import timedelta
    return (dateutil.parser.parse(it)-timedelta(hours=timtRegion)).strftime("%Y-%m-%d %H:%M:%S")

def get_DSO_AZ(ra,dec,mydatetime=None):
    import ephem
    if not mydatetime:
        mydatetime = ephem.now()
    wpf = ephem.Observer()
    wpf.lat = '39.9'  # 纬度
    wpf.lon = '116.4'  # 经度
    wpf.elevation = 0  # 海拔
    wpf.pressure = 0  # 压强
    wpf.date = mydatetime  # 时间根据需要修改
    # p = ephem.FixedBody(mydate)
    p = ephem.FixedBody()
    p._ra = str(ra)
    p._dec = str(dec)
    p.compute(wpf)
    return (p.az/ 2 / ephem.pi * 360,p.alt/ 2 / ephem.pi * 360)

def get_Location():
    dic=json.loads(urllib.request.urlopen("http://ip-api.com/json").read())
    return (dic['lon'],dic['lat'])
