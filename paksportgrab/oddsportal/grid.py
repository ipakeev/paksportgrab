from pakselenium import Browser

from .config.selector import message


class Grid(object):
    browser: Browser
    msgSelector: str

    @property
    def msg(self) -> str:
        if self.browser.is_on_page(message.msg):
            return self.browser.find_element(message.msg).text
        else:
            return ''

    def isInternetError(self):
        if self.browser.is_on_page(message.internetError):
            msg = self.browser.find_element(message.internetError).text
            if msg == 'Нет подключения к Интернету':
                return True
        return False

    def isEmpty(self) -> bool:
        msg = self.msg
        if msg:
            if msg == 'No data available':
                return True
            elif msg == 'There are no odds available for this event.':
                return True
            elif 'no upcoming matches' in msg or 'as soon as' in msg:
                return True
            elif 'try again' in self.msg:
                return False
            else:
                print('msg: {} : {}'.format(msg, self.browser.current_url))

        return False

    def isReload(self) -> bool:
        if 'try again' in self.msg or self.isInternetError():
            return True
        return False
