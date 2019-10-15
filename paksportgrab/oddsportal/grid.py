from pakselenium import Browser

from .config.selector import message


class Grid(object):
    browser: Browser
    msgSelector: str

    @property
    def msg(self) -> str:
        if self.browser.isOnPage(message.msg):
            return self.browser.findElement(message.msg).text
        else:
            return ''

    def isInternetError(self):
        if self.browser.isOnPage(message.internetError):
            msg = self.browser.findElement(message.internetError).text
            if msg == 'Нет подключения к Интернету':
                return True
        return False

    def isEmpty(self) -> bool:
        msg = self.msg
        if msg:
            if msg == 'No data available':
                return True
            elif 'try again' in self.msg:
                return False
            else:
                print('msg: {} : {}'.format(msg, self.browser.currentUrl))

        return False

    def isReload(self) -> bool:
        if 'try again' in self.msg or self.isInternetError():
            return True
        return False
