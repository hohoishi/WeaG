from threading import Thread
import requests
import json

class WeaG:

    def __init__(self):
        self.env = json.load(open('env.json'))
        self.url = self.env['url']
        self.AUTHENTICATION = self.env['token']

    def grab(self, site):
        '''this is a main funtion for grabbing data from CWA's open data api ->
        {O:....}'''
        def _grab(url, site ):
        
            params = {'Authorization':self.AUTHENTICATION,
                            'StationName':site}
            
            r = requests.get(url, params=params)
            if r.json()['records']['Station']:
                s = r.json()['records']['Station'][0]
                info['O'] = r.json()['records']['Station'][0]['ObsTime']['DateTime']
                if 'WeatherElement' in s :

                    info['T'] = float((r.json()['records']['Station'][0]['WeatherElement']['AirTemperature']))
                    info['H'] = float(r.json()['records']['Station'][0]['WeatherElement']['RelativeHumidity'])/100
                elif 'RainfallElement' in s :
                    info['R'] = r.json()['records']['Station'][0]['RainfallElement']['Now']['Precipitation']
        
        info = {}
        ths = [None] * len(self.url)
        for i in range(len(self.url)):
            ths[i] = Thread(target=_grab, args=(self.url[i],site), daemon=True)
            ths[i].start()

        for i in range(len(self.url)):
            ths[i].join()
        return info
    
    def tostr(self , info):
        o = info.get('O')
        o = f'觀測時間 : {o}'if o else ''
        t = info.get('T')
        t = f'溫度 : {t:.1f}度' if t else ''
        h = info.get('H')
        h = f'濕度 : {h:.0%}' if h else ''
        r = info.get('R')
        r = f'雨量 : {r:.1f}mm' if (r != None) else ''

        return f'{o}\n {t}\n {h}\n {r}'
    
if __name__ == '__main__':
    import argparse 

    parser = argparse.ArgumentParser()

    parser.add_argument('site')
    args = parser.parse_args()

    w = WeaG() 
    print(w.grab(args.site))
