from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
import telebot
import urllib
import requests
my_id = '1298257175'
token = '5355906057:AAG9F31zO-ApNmiH8euwSPg4iDhKYiMpnMY'
bot = telebot.TeleBot(token=token)
from bs4 import BeautifulSoup
def pars(url):
    #определить есть акция или нет(если этот блок есть , то и скидка соответственно тоже есть )
    page = requests.get(url)
    b_page = BeautifulSoup(page.content , 'lxml')
    result =b_page.find('div',{'class':'game_area_purchase_game_wrapper'})
    #только в том случае , если скидка есть
    price = result.find('div',{'class':'discount_final_price'})
    if price == None:
        final  = result.find('div',{'class':'game_purchase_price price'}).get('data-price-final')
        return('скидки нет ',str(int(final)/100)+' USD')
    else:
        return('СКИДКА!!!!',price.text)
class Bot():
    def __init__(self,url,path):
        self.url = url
        self.path = path
        self.login()
    def login(self):
        #///////сделать браузер невидимым и создать настройки
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--disable-dev-shm-usage')
        self.image_list = []
        #///////задать сам драйвер и открыть вкладку
        #если с настройками
        self.driver = webdriver.Chrome(chrome_options=self.options)
        # если без настроек

        #self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        sleep(1)
        if (self.driver.page_source) ==[]:
            print('жду еще')
            sleep(1)
        while True:
            height = self.driver.execute_script('return document.body.scrollHeight')
            start_height = height
            #прокрутка страницы
            #повторение 5 раз чтобы точно проверить
            for i in range(5):
                height = self.driver.execute_script('return document.body.scrollHeight')
                self.driver.execute_script(f'window.scrollTo(0,{height})')
                sleep(1)
                # ///////найти элементы
                output = self.driver.find_elements(By.TAG_NAME, 'img')
                sleep(1)
                output = self.driver.find_elements(By.TAG_NAME, 'img')

                for i in output:
                    try:
                        src = i.get_attribute('src')
                        self.image_list.append(src)
                        print(src)
                    except:
                        print('в скрипт попало что-то инородное ! скип!')

            print('завершено!')
            if start_height == height:
                break
        self.final_list = list(set(self.image_list))
        #ВЫВОД
        #print(self.final_list)
        num = 1
        txt_list = ''
        txt_begin = open(f'{self.path}','r').read()
        #вывод всего
        for i in self.final_list:
            print(i,num)
            num+=1
            txt_list+= i +','
        open(f'{self.path}','w').write(f'{txt_begin+txt_list}')


        bot.send_message(my_id,'Количество:'+str(len(self.final_list)))



def main():
    #path - это файл в который копируются ссылки
    url_xiaoven = 'https://www.pinterest.com/search/pins/?q=xioven&rs=sitelinks_searchbox'
    url_choungun = 'https://www.pinterest.com/search/pins/?rs=ac&len=2&q=xingyun&eq=xing&etslf=14262'
    path_memes = 'https://www.pinterest.com/search/pins/?q=memes&rs=typed'
    path_gen_memes = 'https://www.pinterest.com/search/pins/?rs=ac&len=2&q=memes%20genshin%20impact&eq=memes%20gens&etslf=3047'
    urls = [url_choungun,url_xiaoven]
    urls_meme = [path_memes,path_gen_memes]
    path1 = 'img.txt'
    path2 = 'memes.txt'
    for i in urls:
        my_bot = Bot(i,path1)
    for i in urls_meme:
        my_bot = Bot(i, path2)

if __name__ == "__main__":
    main()