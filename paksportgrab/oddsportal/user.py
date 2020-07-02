from paklib import ioutils
from pakselenium import Browser

from .config import names
from .config.selector import userPage


class User(object):
    browser: Browser
    username: str
    password: str

    def __init__(self, browser: Browser):
        self.browser = browser

    def setLoginData(self, username: str, password: str):
        self.username = username
        self.password = password

    def isLoggedIn(self):
        def untilBtn():
            return self.browser.is_on_page(userPage.loginBtn) or self.browser.is_on_page(userPage.logoutBtn)

        if names.baseUrl not in self.browser.current_url:
            self.browser.go(names.baseUrl, until=untilBtn)

        if self.browser.is_on_page(userPage.logoutBtn):
            return True
        return False

    def login(self):
        def untilBtn():
            return self.browser.is_on_page(userPage.loginBtn) or self.browser.is_on_page(userPage.logoutBtn)

        cookiePath = ioutils.correctFileName([names.cookiePath, 'oddsportal_cookies.pkl'])
        if self.isLoggedIn():
            return

        cookies = ioutils.loadPickle(cookiePath)
        if cookies:
            self.browser.set_cookies(cookies)
            self.browser.refresh(until=untilBtn)
            if self.isLoggedIn():
                return

        self.browser.click(userPage.loginBtn, element_text='Login', until=userPage.usernameForm)
        self.browser.fill_text(userPage.usernameForm, self.username)
        self.browser.fill_text(userPage.passwordForm, self.password)
        self.browser.click(userPage.loginFormBtn, element_text='Login', until=userPage.logoutBtn, sleep=1.0)

        assert self.isLoggedIn()

        cookies = self.browser.get_cookies()
        ioutils.savePickle(cookiePath, cookies)

    def logout(self):
        self.browser.go(names.baseUrl)
        if not self.isLoggedIn():
            return
        self.browser.click(userPage.logoutBtn, element_text='Logout')
        assert not self.isLoggedIn()
