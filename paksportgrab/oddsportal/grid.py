from pakselenium import Browser


class Grid(object):
    browser: Browser
    msgSelector: str

    @property
    def msg(self) -> str:
        if self.browser.isOnPage(self.msgSelector):
            msg = self.browser.findElement(self.msgSelector)
            return msg.text
        else:
            return ''

    def isEmpty(self) -> bool:
        msg = self.msg
        if msg:
            if msg == 'No data available':
                return True
            elif 'try again' in self.msg:
                return False
            else:
                print('{} : {}'.format(msg, self.browser.currentUrl))

        return False

    def isReload(self) -> bool:
        if 'try again' in self.msg:
            return True
        return False
