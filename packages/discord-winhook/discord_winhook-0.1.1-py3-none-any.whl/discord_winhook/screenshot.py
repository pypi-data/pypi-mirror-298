
import io
import typing
from discord_winhook.base import Hook
import pygetwindow as gw
import pyautogui as pag
from discord_webhook import DiscordWebhook

class SSHook(Hook):
    def __init__(self, url: str, *windows : typing.Union[gw.Win32Window, str, typing.Callable], limit : int = -1):
        super().__init__(url)
        self.__windows = [gw.getWindowsWithTitle(w)[0] if isinstance(w, str) else w for w in windows]
        self.__limit = limit

        self.__results = None
        
    @property
    def results(self):
        return self.__results
    
    def run(self):
        eligibles = {}
        for w in self.__windows:
            if w._hWnd in eligibles:
                continue
            
            if self.__limit!= -1 and len(eligibles) >= self.__limit:
                break

            if isinstance(w, gw.Win32Window):
                eligibles[w._hWnd] = w
        
            if callable(w):
                elist = [e for e in gw.getAllWindows() if w(e)]
                eligibles.update({e._hWnd: e for e in elist})

        self.__results = []

        whook = DiscordWebhook(url=self.url)
        for e in eligibles.values():
            e : gw.Win32Window
            img = pag.screenshot(region=(e.left, e.top, e.width, e.height))
            self.__results.append((e, img))

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

        
            whook.add_file(file=img_byte_arr, filename=f"{e.title}.png")
        self._Hook__send(whook)
        return whook
    
    @property
    def info(self):
        meta = [x.title if isinstance(x, gw.Win32Window) else x.__name__ for x in self.__windows]
        return f"<SCREENSHOT_HOOK {meta}>"