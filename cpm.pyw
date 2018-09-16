#!/usr/bin/python

import sys
import os
if sys.platform == 'win32':
    import win32clipboard as w 
    import win32con
    import pywintypes
    import winsound
else:
    import clipboard
import traceback
#import tracert  
import sendgrowl
import socket
import configset
from debug import debug

__version__ = "2.0"
__test__ = "0.3"
__author__ = "licface"
__url__ = "licface@yahoo.com"
__target__ = "all"
__build__ = "2.7"
__filename__ = os.path.basename(sys.argv[0])
__usage__ = """\n\n
	 Please insert a Word want to be Copy ! \n
	 Default data is this path = "data_argv" """

CLIP_APP = r'c:\TOOLS\EXE\cpath.exe'
# if not os.path.isfile(CLIP_APP):
#     CLIP_APP = 'cpath.exe'

def play(sound_file):
    winsound.PlaySound(sound_file, winsound.SND_ALIAS)

def make_icon():
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'cpm_img.txt')):
        return r'f:\ICONS\FatCow_Icons32x32\clipboard_empty.png'
    f = open(os.path.join(os.path.dirname(__file__), 'cpm_img.txt'), 'rb')
    g = open(os.path.join(os.path.dirname(__file__), 'clipboard.png'), 'wb')
    g.write(f.read().decode('base64'))
    g.close()
    f.close()
    return os.path.join(os.path.dirname(__file__), g.name)    

def sendnotify(dcopy, title="CPM - Copy Clipboard", msg="now clipboard fill with = "):
    try:
        mclass = sendgrowl.growl()
        icon = make_icon()
        event = 'CPM - Copy Clipboard'
        text =  msg + "\"" + str(dcopy) +  "\""
        appname = 'cpm'
        mclass.publish(appname, event, title, text, iconpath=icon)
    except:
        traceback.format_exc()
        pass

def getText():
    try:
        import clipboard
        return clipboard.paste()
    except:
        #traceback.format_exc()
        w.OpenClipboard() 
        d=w.GetClipboardData(win32con.CF_TEXT) 
        w.CloseClipboard() 
        return d 

def setText(aType,aString):
    if os.path.isfile(CLIP_APP):
        os.system(CLIP_APP + " " + aString)
    else:
        try:
            import clipboard
            clipboard.copy(aString)
        except:
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(aType,aString)
            sound_file = r'f:\SOUNDS\OTHER\sent.wav'
            if not os.path.isfile(sound_file):
                sound_file = 'sent.wav'
            play(sound_file)
            w.CloseClipboard()

def sent_to_clipserver(clip, host='127.0.0.1', port=11111):
    conf = configset.configset()
    conf.configname = os.path.join(os.path.dirname(__file__), 'cpm.ini')
    conf.path = os.path.dirname(__file__)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if os.getenv('CLIPSERVER_HOST'):
        host = os.getenv('CLIPSERVER_HOST')
        debug(getenv='', CLIPSERVER_HOST=host)
    if os.getenv('CLIPSERVER_PORT'):
        port = int(os.getenv('CLIPSERVER_PORT'))
        debug(getenv='', CLIPSERVER_PORT=port)
    if os.getenv('CLIPSERVER') == '0':
        debug(getenv='', CLIPSERVER=os.getenv('CLIPSERVER'))
        return False
    if conf.read_config('CLIPSERVER', 'host'):
        host = conf.read_config('CLIPSERVER', 'host')
        debug(read_config='', host=host)
    if conf.read_config('CLIPSERVER', 'port'):
        port = int(conf.read_config('CLIPSERVER', 'port'))
        debug(read_config='', port=port)
    if conf.read_config('CLIPSERVER', 'used'):
        debug(read_config='', used=conf.read_config('CLIPSERVER', 'used'))
        if conf.read_config('CLIPSERVER', 'used') == 0:
            if os.path.basename(sys.executable).lower() == 'python.exe':
                print "NO sent to clipserver"
            return False
        elif conf.read_config('CLIPSERVER', 'used') == 'False':
            if os.path.basename(sys.executable).lower() == 'python.exe':
                print "NO sent to clipserver"
            return False
    if os.path.basename(sys.executable).lower() == 'python.exe':
        print "sent to clipserver"
        debug("sent_to_clipserver")
    debug(host=host)
    debug(port=port)
    client_address = (host, port)
    sock.sendto(clip, client_address)
    sock.close()
    return True

def main(TEXT, dir_only=False, file_only=False, linux_style=False, linux_style2=False, win_style2=False, url_style = False, change_drive_letter = None, no_clipserver=False):
    if isinstance(TEXT, list) and len(TEXT) > 0:
        if TEXT[0] == "+":
            TEXT.insert(0, os.getcwd())
        for i in TEXT:
            if i == '+':
                TEXT.remove(i)
            elif i == ".":
                index = TEXT.index(i)
                TEXT.remove(i)
                TEXT.insert(index, os.getcwd())
        TEXT = "\\".join(TEXT)
    if TEXT == ["."] or TEXT == ".":
        TEXT = os.getcwd()
    try:
        if len(TEXT) > 0:
            if linux_style:
                TEXT = TEXT.replace("\\", "/")
                TEXT = TEXT.replace(" ", "\\ ")
            elif linux_style2:
                TEXT = TEXT.replace("\\", "/") + "/"
                TEXT = TEXT.replace(" ", "\\ ")
            elif win_style2:
                TEXT = TEXT.replace("\\", "\\\\")
            else:
                # print "LEN(TEXT) =",len(TEXT)
                if len(TEXT) > 1:
                    if TEXT[0] == "." and TEXT[1] == "\\" and len(TEXT) == 2:
                        TEXT = os.getcwd().replace("/", "\\")
                    elif TEXT[0] == "." and TEXT[1] == "/" and len(TEXT) == 2:
                        TEXT = os.getcwd().replace("\\", "/")
                        TEXT = TEXT.replace(" ", "\\ ")
                    elif TEXT[0] == "." and TEXT[1] == "/" and len(TEXT) == 3:
                        if TEXT[2] == "/":
                            TEXT = os.getcwd().replace("\\", "/") + "/"
                        elif TEXT[2] == "\\":
                            TEXT = os.getcwd().replace("/", "\\")
                        TEXT = TEXT.replace(" ", "\\ ")
                    elif TEXT[0] == "." and TEXT[2] == "\\" and len(TEXT) == 3:
                        TEXT = os.getcwd().replace("/", "\\")
                    elif TEXT[0] == "." and TEXT[2] == "/" and len(TEXT) == 3:
                        TEXT = os.getcwd().replace("\\", "/")
                        TEXT = TEXT.replace(" ", "\\ ")
                    elif TEXT[0] == "." and TEXT[3] == "\\" and len(TEXT) == 4:
                        TEXT = os.getcwd().replace("/", "\\")
                    elif TEXT[0] == "." and TEXT[3] == "/" and len(TEXT) == 4:
                        TEXT = os.getcwd().replace("\\", "/")
                        TEXT = TEXT.replace(" ", "\\ ")
                    elif TEXT[0] == "." and TEXT[4] == "\\" and len(TEXT) == 5:
                        TEXT = os.getcwd().replace("/", "\\")
                    elif TEXT[0] == "." and len(TEXT) == 5:
                        if TEXT[4] == "\\":
                            TEXT = os.getcwd().replace("\\", "/") + "/"

            if file_only:
                TEXT = os.path.basename(TEXT)
            elif dir_only:
                TEXT = os.path.dirname(TEXT)
            if change_drive_letter:
                if not change_drive_letter[-1] == ":":
                    change_drive_letter = change_drive_letter + ":"
                if os.path.splitdrive(TEXT)[0]:
                    if not linux_style or not linux_style2:
                        TEXT = change_drive_letter + '\\' + os.path.splitdrive(TEXT)[1]
                    if url_style:
                        TEXT = TEXT.replace(':\\\\', ':\\')
            if url_style:
                TEXT = TEXT.replace('\\', '/')
                TEXT = 'file:///' + TEXT            
                    
            if not sys.platform == 'win32':
                clipboard.copy(TEXT)
                if not no_clipserver:
                    sent_to_clipserver(TEXT)
                sendnotify(TEXT)
            else:
                data_clip_set = setText(w.CF_TEXT, TEXT)
                data_clip = getText()
                if not no_clipserver:
                    sent_to_clipserver(TEXT)
                sendnotify(data_clip)           
        else:
            if file_only:
                TEXT = os.path.basename(TEXT)
            elif dir_only:
                TEXT = os.path.dirname(TEXT)
            
            if not sys.platform == 'win32':
                clipboard.copy(TEXT)
                if not no_clipserver:
                    sent_to_clipserver(TEXT)
                sendnotify(TEXT)
            else:
                data_clip_set = setText(w.CF_TEXT, TEXT)
                data_clip = getText()
                if not no_clipserver:
                    sent_to_clipserver(TEXT)
                sendnotify(data_clip)
        if os.path.basename(sys.executable).lower() == 'python.exe':
            print "\n\n"
            print "\t Please insert a Word want to be Copy ! \n"
            print "\t Default data is this path = ", TEXT

    except IndexError as e:
        traceback.format_exc(msg="Please input Correct Clipboard !")
        print "\n\n"
        print "\t ERROR : ", e
        sendnotify("ERROR: " + str(e), title="ERROR (cpm)", msg="")

    except pywintypes.error as e:
        print "\n\n"
        print "\t ERROR : ", e
        sendnotify("ERROR: " + str(e), title="ERROR (cpm)", msg="")

def usage():
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('STRING', action='store', help='String/Text copy to', nargs='*')
    parser.add_argument('-f', '--filename-only', action='store_true', help='Copy basename or filename only')
    parser.add_argument('-d', '--directory-only', action='store_true', help='Copy directory name only')
    parser.add_argument('-l', '--linux-style', action='store_true', help='Copy as linux style')
    parser.add_argument('-L', '--linux-style2', action='store_true', help='Copy as linux style and add "/" in end of file')
    parser.add_argument('-w', '--windows-linux-style', action='store_true', help='Copy as windows style and replace "/" with "//')
    parser.add_argument('-u', '--url-style', action='store_true', help='Copy as Url style')
    parser.add_argument('-c', '--change-drive-letter', action='store', help='Copy as Url style')
    parser.add_argument('-x', '--no-clipserver', action='store_true', help="Don't send to clipserver if available")
    
    if len(sys.argv) == 1:
        main(".")
    if sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == 'help':
        import easygui
        USAGE = """usage: cpm.pyw [-h] [-f] [-d] [-l] [-L] [-w] [-u] [-c CHANGE_DRIVE_LETTER]
               [-x]
               [STRING [STRING ...]]

positional arguments:
  STRING                String/Text copy to

optional arguments:
  -h, --help            show this help message and exit
  -f, --filename-only   Copy basename or filename only
  -d, --directory-only  Copy directory name only
  -l, --linux-style     Copy as linux style
  -L, --linux-style2    Copy as linux style and add "/" in end of file
  -w, --windows-linux-style
                        Copy as windows style and replace "/" with "//
  -u, --url-style       Copy as Url style
  -c CHANGE_DRIVE_LETTER, --change-drive-letter CHANGE_DRIVE_LETTER
                        Copy as Url style
  -x, --no-clipserver   Don't send to clipserver if available
        """
        image = r'f:\ICONS\FatCow_Icons32x32\clipboard_empty.png'
        choices = ["Close"]
        reply = easygui.codebox(msg='CPM Usage', title='CPM Usage', text=USAGE)
    else:
        args = parser.parse_args()
        main(args.STRING, args.directory_only, args.filename_only, args.linux_style, args.linux_style2, args.windows_linux_style, args.url_style, args.change_drive_letter, args.no_clipserver)

if __name__ == '__main__':
    usage()
