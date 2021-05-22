from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re
import urllib.request
import hashlib
import os

class InstagramScraper:
    def __init__(self):
        self.BIG_WAIT_TIME = 5
        self.SMALL_WAIT_TIME = 2
        self.TINY_WAIT_TIME = 1
        self.PICTURE_DIR = 'picture/'
        if os.path.exists(self.PICTURE_DIR) == False:
            os.mkdir(self.PICTURE_DIR)

    def login(self, id='', password=''):
        self.id = id
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.home_url = 'https://www.instagram.com/'
        self.browser.get(self.home_url)

        sleep(5)
        id_input = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        id_input.send_keys(self.id)
        password_input = self.browser.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input')
        password_input.send_keys(self.password)
        password_input.submit()
        sleep(5)


        if '나중에 하기' in self.browser.page_source:
            page = self.browser.find_elements_by_tag_name("button")
            for i in page:
                if '나중에 하기' in i.text:
                    i.click()
                    sleep(5)
                    break
        if '나중에 하기' in self.browser.page_source:
            page = self.browser.find_elements_by_tag_name("button")
            for i in page:
                if '나중에 하기' in i.text:
                    i.click()
                    sleep(5)
                    break

    def get_feed_list(self, scroll=5):
        '''
        :param scroll: 스크롤 내리는 횟수
        :return: feed 주소
        '''
        feed_list = list()
        for a in range(scroll):
            html = self.browser.page_source
            soup = BeautifulSoup(html,'lxml')
            small_feed_list = soup.select('.v1Nh3.kIKUG._bz0w a')
            for small_feed in small_feed_list:
                url = self.home_url + small_feed['href'][1:] # 앞에 /한개 잘라준다.
                if url not in feed_list:
                    feed_list.append(url)

            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);") # 스크롤 내리기.
            sleep(self.SMALL_WAIT_TIME)
        feed_list = list(set(feed_list))
        return feed_list

    def search_by_tag(self, tag):
        self.browser.get(self.home_url + 'explore/tags/' + tag)

    def get_info_from_feed(self, url):
        '''
        피드주소로부터 정보들을 모두 얻는다.
        :param url: feed 주소.
        :return:
        '''
        cmd = 'window.open({});'.format('\"'+url+'\"')
        self.browser.execute_script(cmd)
        sleep(self.SMALL_WAIT_TIME)

        self.browser.switch_to_window(self.browser.window_handles[-1])
        sleep(1)
        hashtag = self.fetch_hashtag()
        images = self.fetch_image()
        content = self.fetch_contents()
        location = self.fetch_location()
        time = self.fetch_timestamp()
        data = {'hashtag':hashtag, 'picture_list':images, 'content':content, 'location':location, 'date_time':time}
        self.browser.close()
        self.browser.switch_to_window(self.browser.window_handles[-1])
        return data


    def fetch_image(self):
        '''
        피드를 클릭한다음 실행한다.
        :return:
        '''
        img_url_list = []
        picture_name_list = []
        while 1:
            html = self.browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            try:
                for i in soup.select('.eLAPa.RzuR0 img'):
                    img_url_list.append(i['src'])
                self.browser.find_element_by_class_name("coreSpriteRightChevron").click()
            except Exception:
                break

        if len(img_url_list) == 0: #사진이 하나밖에 없을경우 list사이즈가 0이다.
            img_src = soup.select_one('.KL4Bh img')['src']
            img_url_list.append(img_src)

        img_url_list = list(set(img_url_list)) # 중복값 제거
        hash_tag = self.fetch_hashtag()
        image_name = ''.join(hash_tag)[:180]
        for url in img_url_list:
            hash_value = hashlib.blake2b(url.encode('utf-8'), digest_size=4).digest().hex()
            picture_name = image_name + hash_value + '.jpg'
            urllib.request.urlretrieve(url, self.PICTURE_DIR + picture_name)
            picture_name_list.append(picture_name)
        return picture_name_list

    def fetch_hashtag(self):
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select('div.C4VMK > span')[0].text
        tags = re.findall(r'#[\w]+', content)
        return tags

    def fetch_contents(self):
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select('div.C4VMK > span')[0].text
        return content

    def fetch_location(self):
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        try:
            content = soup.select('div.JF9hh > a')[0].text
        except Exception:
            content = 'None'
        return content

    def fetch_timestamp(self):
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        content = soup.select('._1o9PC.Nzb55')[0]['datetime']
        return content


if __name__ == "__main__":
    pass