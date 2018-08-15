import os
import sys
PID = os.getpid()
import socket
from make_colors import make_colors
import clipboard
import traceback
import sendgrowl
from datetime import datetime

def sendnotify(dcopy, title="CLIPSERVER", msg="now clipboard fill with = "):
    try:
        mclass = sendgrowl.growl()
        icon = r'f:\ICONS\FatCow_Icons32x32\clipboard_empty.png'
        event = 'clip_receive'
        text =  msg + "\"" + str(dcopy) +  "\""
        appname = 'clipserver'
        mclass.publish(appname, event, title, text, iconpath=icon)
    except:
        traceback.format_exc()
        pass

def get_time():

    return datetime.strftime(datetime.now(), '%Y:%m:%d %H:%M:%S.%f')

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	host = '0.0.0.0'
	port = 11111
	server_address = (host, port)
	sock.bind(server_address)
	print "Syslog Bind: %s:%s [pid:%s]" % (make_colors(host, 'green'), make_colors(str(port), 'cyan'), make_colors(PID, 'red'))

	while 1:
		data = sock.recv(65565)
		if data:
			if data == 'EXIT':
				sys.exit('server shutdown ....')
			if os.getenv('DEBUG'):
				print make_colors(get_time(), 'lightred') + " RECEIVE:", make_colors(data, 'lightyellow') + " " + make_colors("[%s]", 'white', 'lightmagenta') %(str(PID))
			clipboard.copy(data)
			sendnotify(data)

except SystemExit:
    sys.exit('SYSTEM EXIT !')
except:
    traceback.format_exc()

if __name__ == '__main__':
	print "PID::", PID
