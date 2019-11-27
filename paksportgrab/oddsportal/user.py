from paklib import ioutils
from pakselenium import Browser

from .config.selector import userPage
from .config import names


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
            return self.browser.isOnPage(userPage.loginBtn) or self.browser.isOnPage(userPage.logoutBtn)

        if names.baseUrl not in self.browser.currentUrl:
            self.browser.go(names.baseUrl, until=untilBtn)

        if self.browser.isOnPage(userPage.logoutBtn):
            return True
        return False

    def login(self):
        def untilLoginBtn():
            return self.browser.isOnPage(userPage.loginBtn)

        def untilLogoutBtn():
            return self.browser.isOnPage(userPage.logoutBtn)

        def untilBtn():
            return untilLoginBtn() or untilLogoutBtn()

        cookiePath = ioutils.correctFileName([names.cookiePath, 'oddsportal_cookies.pkl'])
        if self.isLoggedIn():
            return

        cookies = ioutils.loadPickle(cookiePath)
        if cookies:
            self.browser.setCookies(cookies)
            self.browser.refresh(until=untilBtn)
            if self.isLoggedIn():
                return

        pe = self.browser.findElement(userPage.loginBtn)
        assert pe.text == 'Login'
        self.browser.click(pe, until=untilLoginBtn)

        pe = self.browser.findElement(userPage.usernameForm)
        self.browser.clearForm(pe)
        self.browser.fillForm(pe, self.username)
        pe = self.browser.findElement(userPage.passwordForm)
        self.browser.clearForm(pe)
        self.browser.fillForm(pe, self.password)

        pe = self.browser.findElement(userPage.loginFormBtn)
        assert pe.text == 'Login'
        self.browser.click(pe, until=untilLogoutBtn)
        assert self.isLoggedIn()

        cookies = self.browser.getCookies()
        ioutils.savePickle(cookiePath, cookies)

    def logout(self):
        self.browser.go(names.baseUrl)
        if not self.isLoggedIn():
            return
        pe = self.browser.findElement(userPage.logoutBtn)
        assert pe.text == 'Logout'
        self.browser.click(pe)
        assert not self.isLoggedIn()
