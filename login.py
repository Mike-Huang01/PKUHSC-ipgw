import sys
import os
import re
import json
import time
import httplib2
import getpass
from base64 import b64encode, b64decode

def login(data):
    global log
    resp, content = h.request("http://srun.bjmu.edu.cn/cgi-bin/do_login", "POST",
                              data,
                              headers = {'Content-Type': 'application/x-www-form-urlencoded'})
    content = content.decode('gb2312')
    re_lgok = r'^[0-9]+'
    if content == 'ip_exist_error':
        log.write(time.ctime() + ' ' + content + '\n')
        return content
    elif re.match(re_lgok, content):
        log.write(time.ctime() + ' ' + content + '\n')
        return content
    else:
        log.write(time.ctime() + ' ' + content + '\n')
        return 'others'

def logout(data):
    global log
    resp, content = h.request("http://srun.bjmu.edu.cn/cgi-bin/force_logout", "POST",
                              data,
                              headers = {'Content-Type': 'application/x-www-form'})
    content = content.decode('gb2312')
    if content == 'logout_ok':
        log.write(time.ctime() + ' ' + content + '\n')
        return 'logout_ok'
    else:
        log.write(time.ctime() + ' ' + content + '\n')
        return content

def lgout(data):
    resp, content = h.request("http://srun.bjmu.edu.cn/cgi-bin/do_logout", "POST",
                              data,
                              headers = {'Content-Type': 'application/x-www-form'})
    content = content.decode('gb2312')
    if content == 'logout_ok':
        log.write(time.ctime() + ' ' + content + '\n')
        return 'logout_ok'
    else:
        log.write(time.ctime() + ' ' + content + '\n')
        return content
     
base = os.path.dirname(os.path.abspath(__file__))
logf = os.path.join(base, 'login_log.txt')
configf = os.path.join(base, 'config.json')
log = open(logf, 'w+')

h = httplib2.Http()
try:
    resp, content = h.request("http://srun.bjmu.edu.cn")
    if resp['status'] != '200':
        log.write(time.ctime() + ' ' + content + '\n')
    else:
        tags = ['username','password','drop','type','n']
        if 'config.json' in os.listdir(base):
            with open(configf,'r') as config:
                config_dict = json.load(config)
            config_dict['password'] = b64decode(config_dict['password'].encode()).decode()
            datastring = '&'.join([tag + '=' + config_dict[tag] for tag in tags])
        else:
              config_dict = {'drop' : '1','type': '1', 'n': '100'}
              username = input("school id: ")
              passw = getpass.getpass()
              config_dict['password'] ='{TEXT}' + passw
              config_dict['username'] = username
              datastring = '&'.join([tag + '=' + config_dict[tag] for tag in tags])

        # deplete {TEXT}
        start = datastring.index('{')
        end = start + 6
        temp = datastring[0:start] + datastring[end:]
        datastring2 = temp[:-2]
        
        while True:
            if sys.argv[1] == 'login':
                if config_dict.get('uid'):
                    lgout('uid=' + config_dict['uid'])
                else:
                    logout(datastring2)
                content = login(datastring)
                if(re.match(r'^[0-9]+', content)):
                    if not config_dict.get('uid'):
                        config_dict['uid'] = content
                        with open(configf, 'w+') as config:
                            config_dict['password'] = b64encode(config_dict['password'].encode()).decode()
                            json.dump(config_dict, config)
                    break
                elif(content == 'ip_exist_error'):
                    time.sleep(5)
                    continue
                else:
                    break

            elif sys.argv[1] =='logout':
                content = logout(datastring2)
                if(content == 'logout_ok') :
                    break
                else:
                    break
            elif sys.argv[1] == 'lgout':
                if config_dict.get('uid'):
                    content = lgout('uid=' + config_dict['uid'])
                break
except httplib2.ServerNotFoundError as e:
    log.write(time.ctime() + ' ' + str(e) + ': no connection?\n')
        
finally:
    log.close()
