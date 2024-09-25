###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 07/12/2019.
###
import os
from openpyweb import Version

from urllib.request import urlopen
import json

class ip:

    def __init__(self):

        self.HTTP_headers = ['SERVER_ADDR',
                            'REMOTE_ADDR',
                            'HTTP_CLIENT_IP'
                            ]
        self.HTTP_proxy_header = ['HTTP_VIA',
                                  'VIA',
                                  'Proxy-Connection',
                                  'HTTP_X_FORWARDED_FOR',
                                  'HTTP_FORWARDED_FOR',
                                  'HTTP_X_FORWARDED',
                                  'HTTP_FORWARDED',
                                  'HTTP_CLIENT_IP',
                                  'HTTP_FORWARDED_FOR_IP',
                                  'X-PROXY-ID',
                                  'MT-PROXY-ID',
                                  'X-TINYPROXY',
                                  'X_FORWARDED_FOR',
                                  'FORWARDED_FOR',
                                  'X_FORWARDED',
                                  'FORWARDED',
                                  'CLIENT-IP',
                                  'CLIENT_IP',
                                  'PROXY-AGENT',
                                  'HTTP_X_CLUSTER_CLIENT_IP',
                                  'FORWARDED_FOR_IP',
                                  'HTTP_PROXY_CONNECTION'
                                  ]
        self.ips = ['127.0.0.0', '127.0.0.1', '127.0.0.2', '192.0.0.0', '192.0.0.1', '192.168.0.0',
               '192.168.0.1', '192.168.0.253', '192.168.0.254', '192.168.0.255', '192.168.1.0',
               '192.168.1.1', '192.168.1.253', '192.168.1.254', '192.168.1.255', '192.168.2.0',
               '192.168.2.1', '192.168.2.253', '192.168.2.254', '192.168.2.255', '10.0.0.0', '10.0.0.1',
               '11.0.0.0', '11.0.0.1', '1.0.0.0', '1.0.1.0', '1.1.1.1', '255.0.0.0', '255.0.0.1',
               '255.255.255.0', '255.255.255.254', '255.255.255.255', '0.0.0.0', '::', '0::', '::1',
               '0:0:0:0:0:0:0:0']


        self._ip = ""
        self.hostname = ""
        self.city = ""
        self.region = ""
        self.country = ""
        self.loc = ""
        self.org = ""
        self.is_vpn = False
        return None

    def ip(self):
        self._ip = os.environ.get("REMOTE_ADDR")
        return self._ip
    
    def get(self):

        for header in self.HTTP_headers:
            if self.os(header) != "":
                self._ip = self.ip()
                self.property(self._ip)
            return self

    def check(self, ip):
        for header in self.HTTP_proxy_header:
            response = True if self.os(header) != "" else False
        return response

    def vpn(self):

        for header in self.HTTP_proxy_header:
            if self.os(header) != "":
                self.ip = self.os(header)
                self.is_vpn = self.check(self, self.ip)
                self.property(self.ip)
            return self


    def property(self, ip):
        try:
            ipU= "http://ipinfo.io/{ip}/json".format(ip=ip)
            url_ip = urlopen(ipU).read()
            response = url_ip.decode('utf-8')
            j_response = json.loads(response)
            if j_response.get("bogon", "") == "":
                self.hostname = j_response.get("hostname", "")
                self.city = j_response.get("city", "")
                self.region = j_response.get("region", "")
                self.country = j_response.get("country", "")
                self.loc = j_response.get("loc", "")
                self.org = j_response.get("org", "")
            return self
        except Exception:
            return False
