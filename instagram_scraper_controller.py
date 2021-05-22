import requests
from utility_function import EasyLogger
import json
import base64

logger = EasyLogger()
DEBUG = 0
INFO = 1
WARNING = 2

class InstagramScraperController:
    def __init__(self):
        self.PICTURE_DIR = 'picture/'
        pass

    def save_feed_csv(self,data):
        pass

    def save_feed_db(self,data):
        pass

    @logger.util_log(INFO)
    def http_send_data(self, url, data):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.post(url, headers=headers, data=json.dumps(data))
        if res.status_code == 200:
            return 0
        else:
            log = 'Fail to send data to {} server'.format(url)
            logger.log_info(log, WARNING)
            return res.status_code

    @logger.util_log(INFO)
    def http_send_image(self, url, image):
        '''
        :param image_name: 리스트 형식으로 보내기.
        :return:
        '''
        files = open(self.PICTURE_DIR + image, 'rb')
        img_data = base64.encodebytes(files.read()).decode('utf-8')
        upload = {'filename': image, 'data': img_data}
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.post(url, data=json.dumps(upload),headers=headers)
        if res.status_code == 200:
            return 0
        else:
            log = 'Fail to send image {} to {} server'.format(image,url)
            logger.log_info(log, WARNING)
            return res.status_code


if __name__ == '__main__':
    data = {'hashtag' : 'asd', 'content' : 'asda', 'location' : '1111', 'date_time' : '2019-11-12T16:34:30', 'picture_list' : 'fasad.img'}
    pass