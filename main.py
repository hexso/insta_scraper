from instagram_scraper import InstagramScraper
from instagram_scraper_controller import InstagramScraperController
from datetime import datetime
from utility_function import EasyLogger

def make_dat_for_json(datas):
    if type(datas['picture_list']) == list:
        datas['picture_list'] = ','.join(datas['picture_list'])
    if type(datas['hashtag']) == list:
        datas['hashtag'] = ''.join(datas['hashtag'])
    return datas

if __name__ == '__main__':
    with open('privacy.txt','r') as f:
        id = f.readline()
        password = f.readline()
        feed_post_url = f.readline()
        image_post_url = f.readline()
    insta_scrap = InstagramScraper()
    ctl = InstagramScraperController()
    insta_scrap.login(id, password)

    with open('hash_tag.txt', 'r',encoding='UTF8') as f:
        tag_list = f.readlines()
        tag_list = list(map(lambda s: s.strip(), tag_list))

    for tag in tag_list:
        search_tag = tag
        now_time = datetime.now()
        insta_scrap.search_by_tag(search_tag)
        error_cnt = 0

        cnt = 0
        #해당 해쉬태그에서 feed 정보를 수집한다.
        while 1:
            feed_list = insta_scrap.get_feed_list()
            for feed in feed_list:
                feed_info = insta_scrap.get_info_from_feed(feed)
                feed_info = make_dat_for_json(feed_info)
                res = ctl.http_send_data(feed_post_url, feed_info) #피드로부터 얻은 정보를 서버에 전송한다.
                if res != 0:
                    error_cnt+=1
                picture_list = feed_info['picture_list'].split(',')
                for picture in picture_list:
                    res = ctl.http_send_image(image_post_url,picture)
            print('{}개의 피드를 수집하였습니다.'.format(len(feed_list)))
            cnt += len(feed_list)
            #오늘날짜만 긁어온다.
            feed_time = feed_info['date_time'][:10]
            feed_time = datetime.strptime(feed_time,'%Y-%m-%d')
            time_gap = now_time-feed_time
            if time_gap.days > 1:
                EasyLogger.log_info('오늘 날짜에 해당되는 {} 태그를 모두 {}개 찾았습니다.'.format(search_tag, cnt))
                break

            if error_cnt > 10:
                print('통신에러 발생')
                exit
