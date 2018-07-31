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
import tracert  
import sendgrowl

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

def sendnotify(dcopy, title="CPM - Copy Clipboard", msg="now clipboard fill with = "):
    try:
        mclass = sendgrowl.growl()
        icon = r'f:\ICONS\FatCow_Icons32x32\clipboard_empty.png'
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

# def linuxpath():
#     data_ex = os.getcwd().replace('\\','/')
#     data_argv = data_ex + "/" + sys.argv[2]
#     data_clip_set = setText(w.CF_TEXT, data_argv)
#     data_clip = getText()
#     sendnotify(data_clip)
#     print "\n"
#     print "\t Sucessfully set clipboard ! \n"
#     print "\t now clipboard fill with = \"" + data_clip

# def linuxpath2():
#     data_ex = os.getcwd().replace('\\','/')
#     data_argv = data_ex + "/" + sys.argv[2] + '/'
#     data_clip_set = setText(w.CF_TEXT, data_argv)
#     data_clip = getText()
#     sendnotify(data_clip)
#     print "\n"
#     print "\t Sucessfully set clipboard ! \n"
#     print "\t now clipboard fill with = \"" + data_clip 

# def winpath(session=None):
#     if session == None:
#         data_ex = sys.argv[1].replace('/','\\')
#         #print "data_ex = ", data_ex
#         data_argv = data_ex + "\\" + sys.argv[2] + '\\'
#         data_clip_set = setText(w.CF_TEXT, data_argv)
#         add_slash = ''
#     elif session == 1:
#         data_ex = os.getcwd().replace('\\','/')
#         data_clip_set = setText(w.CF_TEXT, data_ex)
#         add_slash = '/'
#     elif session == 0:
#         data_ex = os.getcwd().replace('\\','/')
#         data_clip_set = setText(w.CF_TEXT, data_ex)
#         add_slash = ''
#     elif session == 2:
#         data_ex = os.path.join(os.getcwd(),sys.argv[2].replace('/','\\'))
#         #print "data_ex = ", data_ex
#         data_argv = data_ex + '\\'
#         data_clip_set = setText(w.CF_TEXT, data_argv)
#         add_slash = ''
#     else:
#         print __usage__
#     data_clip = getText()
#     sendnotify(data_clip)
#     if os.path.basename(sys.executable).lower() == 'python.exe':
#         print "\n"
#         print "\t Sucessfully set clipboard ! \n"
#         print "\t now clipboard fill with = \"" + str(data_clip) + add_slash

# def winpath2():
#     data_ex = os.getcwd()
#     #data_argv = data_ex + "\\" + sys.argv[2]
#     data_argv = os.path.join(data_ex, os.path.abspath('\\'.join(sys.argv[2:])))
#     data_clip_set = setText(w.CF_TEXT, data_argv)
#     data_clip = getText()
#     sendnotify(str(data_argv))
#     if os.path.basename(sys.executable).lower() == 'python.exe':
#         print "data_argv =", data_argv
#         print "\n"
#         print "\t Sucessfully set clipboard ! \n"
#         print "\t now clipboard fill with = \"" + str(data_argv) + "\""


def main(TEXT, dir_only=False, file_only=False, linux_style=False, linux_style2=False, win_style2=False, url_style = False, change_drive_letter = None):
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
                sendnotify(TEXT)
            else:
                data_clip_set = setText(w.CF_TEXT, TEXT)
                data_clip = getText()
                sendnotify(data_clip)           
        else:
            if file_only:
                    TEXT = os.path.basename(TEXT)
            elif dir_only:
                TEXT = os.path.dirname(TEXT)
            
            if not sys.platform == 'win32':
                clipboard.copy(TEXT)
                sendnotify(TEXT)
            else:
                data_clip_set = setText(w.CF_TEXT, TEXT)
                data_clip = getText()
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
    
    if len(sys.argv) == 1:
        main(".")
    else:
        args = parser.parse_args()
        main(args.STRING, args.directory_only, args.filename_only, args.linux_style, args.linux_style2, args.windows_linux_style, args.url_style, args.change_drive_letter)

if __name__ == '__main__':
    usage()
