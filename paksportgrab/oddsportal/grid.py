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

    def is_internet_error(self):
        if self.browser.is_on_page(message.internet_error):
            msg = self.browser.find_element(message.internet_error).text
            if msg == 'Нет подключения к Интернету':
                return True
        return False

    def is_empty(self) -> bool:
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

    def is_reload(self) -> bool:
        if 'try again' in self.msg or self.is_internet_error():
            return True
        return False
