from paklib import io
from pakselenium import Browser, catch

from .config import names
from .config.selector import user_page


class User(object):
    browser: Browser
    username: str
    password: str

    def __init__(self, browser: Browser):
        self.browser = browser

    def set_login_data(self, username: str, password: str):
        self.username = username
        self.password = password

    def is_logged_in(self):
        def until_btn():
            return self.browser.is_on_page(user_page.login_btn) or self.browser.is_on_page(user_page.logout_btn)

        @catch.timeoutException(lambda: self.browser.refresh())
        def go():
            self.browser.go(names.base_url, until=until_btn)

        if names.base_url not in self.browser.current_url:
            go()
        if self.browser.is_on_page(user_page.logout_btn):
            return True
        return False

    def login(self):
        def until_btn():
            return self.browser.is_on_page(user_page.login_btn) or self.browser.is_on_page(user_page.logout_btn)

        cookie_path = io.path([names.cookie_path, 'oddsportal_cookies.pkl'])
        if self.is_logged_in():
            return

        cookies = io.load_pickle(cookie_path)
        if cookies:
            self.browser.set_cookies(cookies)
            self.browser.refresh(until=until_btn)
            if self.is_logged_in():
                return

        @catch.timeoutException(lambda: self.browser.refresh())
        def click_login_btn():
            self.browser.click(user_page.login_btn, element_text='Login', until=user_page.username_form)

        @catch.timeoutException(lambda: self.browser.refresh())
        def login_after_fill():
            self.browser.click(user_page.login_form_btn, element_text='Login', until=user_page.logout_btn, sleep=1.0)

        click_login_btn()
        self.browser.fill_text(user_page.username_form, self.username)
        self.browser.fill_text(user_page.password_form, self.password)
        login_after_fill()

        assert self.is_logged_in()

        cookies = self.browser.get_cookies()
        io.save_pickle(cookie_path, cookies)

    def logout(self):

        @catch.timeoutException(lambda: self.browser.refresh())
        def logout():
            self.browser.go(names.base_url)
            if not self.is_logged_in():
                return
            self.browser.click(user_page.logout_btn, element_text='Logout')

        logout()
        assert not self.is_logged_in()
