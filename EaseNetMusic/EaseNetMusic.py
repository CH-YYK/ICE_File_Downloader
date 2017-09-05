from selenium import webdriver
from bs4 import BeautifulSoup
import requests, os

class Albumcover:
	'''
	This is a modified script from the project("https://mp.weixin.qq.com/s/N5K8_l8Ip31UGEUR5URdTA").

	In this modified script: Safari is used instead of phantomJS,
							 Some existing bug is amended (Like the html parser)

	Intead of traditionally used package (requests), the "webdriver" in "selenium" is used for the HTML in "iframe" tag.

	After obtaining this hidden sheet of html, we use "BeautifulSoup" to parse them and then output data.
	'''

    def __init__(self):
        self.init_url = "http://music.163.com/#/artist/album?id=101988&limit=120&offset=0"
        self.folder_path = "/Users/yangyikang/Desktop/MyPy/Img"

    def save_img(self,url,file_name):
        print("Request for the images...")
        img = self.request(url)
        print("Saving Image...")

        with open(file_name, "wb") as f:
            f.write(img.content)

    def request(self, url):
        r = requests.get(url)
        return r

    def mkdir(self, path):
        path = path.strip()
        isExist = os.path.exists(path)

        if not isExist:
            print("Make a directory named"+path)
            os.makedirs(path)
            print("Success")
        else:
            print("Directory already existed")

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")
        driver = webdriver.Safari()
        driver.get(self.init_url)
        ref = driver.find_elements_by_tag_name('iframe')[0]
        driver.switch_to.frame(ref)
        html = driver.page_source
        driver.quit() 
        ## remember to quit the session at the end, 
        ## or some conflict would happen.

        self.mkdir(self.folder_path)
        print("redirect to new folder")
        os.chdir(self.folder_path)

        file_names = self.get_files(self.folder_path)
        all_li = BeautifulSoup(html, 'html.parser').find(id='m-song-module').find_all("li")

        for li in all_li:
            album_img = li.find('img')['src']  # tag: img, attr: src
            album_name = li.find(class_='dec')['title']
            album_date = li.find(name='span', class_='s-fc3').text.strip()
            album_img_url = album_img[:(album_img.index("?"))]

            photo_name = album_date + "-" + album_name.replace('/', '|') + ".jpg"
            print(album_img_url, photo_name)

            if photo_name in file_names:
                print("photo already exist")
            else:
                self.save_img(album_img_url, photo_name)


if __name__ == '__main__':
    albumcover = Albumcover()
    albumcover.spider()
