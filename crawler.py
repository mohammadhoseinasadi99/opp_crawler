import re
import urllib.request
class Website:
    history = {}
    def __init__(self, url):
        self.url = url
        self.__text = None
        self.__email = None
        self.__links = None
        self.history[self.url] = self
        self.is_read = False

    def __repr__(self):
        return "site: <<" + self.url + ">>"

    @property
    def text(self):
        if self.__text is None:
            with urllib.request.urlopen(self.url) as req:
                self.__text = req.read().decode('utf-8')
                self.is_read = True
        return self.__text

    @property
    def email(self):
        if self.__email is None:
            pattern = r'[a-zA-Z\.-]+@[\w\.-]+'
            self.__email = re.findall(pattern, self.text)
        return self.__email

    @property
    def links(self):
        if self.__links is None:
            pattern = r'<a[^>]* href="(https?[^"]*)"'
            links = re.findall(pattern, self.text)
            self.__links = []
            for link in links:
                if link in self.history:
                    site = self.history[link]
                else:
                    site = Website(link)
                self.__links.append(site)

        return self.__links
    @classmethod
    def read(cls):
        result = []
        for w in cls.history.values():
            if w.is_read:
                result.append(w)
        return result
    @classmethod
    def unread(cls):
        result = []
        for w in cls.history.values():
            if not w.is_read:
                result.append(w)
        return result


url = "https://www.python.org"
website = Website(url)
print(website.links)
print("read websites: ", Website.read())
print("unread websites: ", Website.unread())