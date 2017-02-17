import urllib.parse
import requests
from win32api import *
from win32gui import *
import win32con
import sys, os
import time


class Headlines:

    def __init__(self, main_api, source, sortBy, apiKey):
        self.main_api = main_api

        self.source = source

        self.sortBy = sortBy

        self.apiKey = apiKey

        self.dict = {
            'source': self.source,
            'sortBy': self.sortBy,
            'apiKey': self.apiKey
        }

        self.response = self.get_response_data()

        self.json_data = self.response.json()

        json_status = self.json_data['status']

        if json_status == 'ok':
            self.top_feed = []
            for i in range(0, 5):
                self.top_feed.append(self.json_data['articles'][i]['title'].split('-')[0])

            #print(self.top_feed)
            str_top_feed = ''
            for i in range(0,5):
                str_top_feed += str(i+1)+".)"+" "+ self.top_feed[i] +"\n"

            self.ballontip(str_top_feed, "News")

            #code for scheduling algorithm

            #path = r"C:\Users\stpl\PycharmProjects\googlenewsapp\dist\headlines.exe"

            #if os.path.exists(path):
            #    pass
            #else:
                #os.system("schtasks /Create /TN \"News\" /SC MINUTE /Mo 2 /tr " +"\"" + r"C:\Users\stpl\PycharmProjects\googlenewsapp\dist\headlines.exe" +r"\"")

        else:
            self.ballontip(self.json_data['message'], "News")

    def get_response_data(self):

        url = self.main_api + urllib.parse.urlencode(self.dict)
        response = requests.get(url)

        return response

    def ballontip(self, title, msg):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, \
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                                 0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join(sys.path[0], "balloontip.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, iconPathName, \
                              win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY,(self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20, hicon, "Balloon  tooltip", title, 500, msg))
        # self.show_balloon(title, msg)
        time.sleep(120)
        DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.


def main():

    main_api = 'https://newsapi.org/v1/articles?'

    source = 'the-times-of-india'
    source1= 'espn-cric-info'
    source2 = 'google-news'

    sortBy = 'top'

    apiKey = '42103bd5a57d4eaf85bcb821b675c4d3'

    get_news = Headlines(main_api, source2, sortBy, apiKey)


if __name__ == '__main__':
    main()
