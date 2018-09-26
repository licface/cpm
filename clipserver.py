import os
import sys
PID = os.getpid()
import socket
from make_colors import make_colors
import clipboard
import traceback
import sendgrowl
from datetime import datetime
from configset import configset

CONFIG = configset()
CONFIGNAME = os.path.join(os.path.dirname(__file__), 'clipserver.ini')
CONFIG.configname = CONFIGNAME

def make_icon():
    f = open(os.path.join(os.path.dirname(__file__), 'image_string.txt'), 'rb')
    g = open(os.path.join(os.path.dirname(__file__), 'clipboard_empty.png'), 'wb')
    g.write(f.read().decode('base64'))
    g.close()
    f.close()
    return os.path.join(os.path.dirname(__file__), g.name)

def sendnotify(dcopy, title="CLIPSERVER", msg="now clipboard fill with = "):
    try:
        mclass = sendgrowl.growl()
        icon = r'f:\ICONS\FatCow_Icons32x32\clipboard_empty.png'
        if not os.path.isfile(icon):
            icon = make_icon()
        event = 'clip_receive'
        text =  msg + "\"" + str(dcopy) +  "\""
        appname = 'clipserver'
        mclass.publish(appname, event, title, text, iconpath=icon)
    except:
        traceback.format_exc()
        pass

def get_time():
    return datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S.%f')

def main():
    global CONFIG
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = CONFIG.read_config('SERVER', 'host', value = '0.0.0.0')
        if not host:
            host = '0.0.0.0'
        port = CONFIG.read_config('SERVER', 'port', value = '11111')
        if port:
            port = int(port)
        else:
            port = 11111
        server_address = (host, port)
        sock.bind(server_address)
        print "Syslog Bind: %s:%s [pid:%s]" % (make_colors(host, 'lightgreen'), make_colors(str(port), 'lightcyan'), make_colors(PID, 'lightwhite', 'lightred'))
    
        while 1:
            try:
                data = sock.recv(65565)
            except:
                data = ''
                
            if data:
                if data == 'EXIT':
                    sys.exit('server shutdown ....')
                if os.getenv('DEBUG'):
                    print make_colors(get_time(), 'lightred') + " RECEIVE:", make_colors(data, 'lightyellow') + " " + make_colors("[%s]", 'white', 'lightmagenta') %(str(PID))
                print get_time() + " - " + make_colors("CLIPBOARD INSERT", 'lightyellow')
                clipboard.copy(data)
                sendnotify(data)
    
    except SystemExit:
        sys.exit('SYSTEM EXIT !')
    except:
        traceback.format_exc()

if __name__ == '__main__':
    print "PID::", PID
    main()