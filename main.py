import  telebot
from bs4 import BeautifulSoup
import requests
import random as rand

def pars_steam_price(url):
    #определить есть акция или нет(если этот блок есть , то и скидка соответственно тоже есть )
    page = requests.get(url)
    b_page = BeautifulSoup(page.content , 'lxml')
    result =b_page.find('div',{'class':'game_area_purchase_game_wrapper'})
    #только в том случае , если скидка есть
    price = result.find('div',{'class':'discount_final_price'})
    if price == None:
        final  = result.find('div',{'class':'game_purchase_price price'}).get('data-price-final')
        return'скидки нет ',str(int(final)/100)+' USD'
    else:
        return 'СКИДКА!!!!',price.text




class Net_helper():
    def __init__(self):
        self.token = '5432900655:AAE8RIOOMai_xBSm0U4gPb7zf9YHWhDbdEE'
        self.bot = telebot.TeleBot(self.token)
        self.my_id = '1298257175'
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}
        self.collect()
        self.parc()
        self.send()
    def collect(self):
        h_list = open('img.txt','r').read().split(',')
        m_list = open('memes.txt','r').read().split(',')
        del h_list[-1]
        del m_list[-1]
        #создание рандомных списков с изображениями
        self.img_list = []
        self.meme_list = []
        for i in range(3):
            random = rand.choice(h_list)
            print(random)
            self.img_list.append(random)
        for i in range(2):
            random = rand.choice(m_list)
            print(random)
            self.meme_list.append(random)
        print('ссылки на изображения собраны')
    def parc(self):
        #парсинг курса биткоина
        #url ='https://www.rbc.ru/crypto/currency/btcusd'
        #page = requests.get(url,headers=self.headers)
        #b_page = BeautifulSoup(page.text, 'lxml')
        #self.bitcoin = b_page.find('div',{'class':'chart__subtitle js-chart-value'}).text.replace('  ','')
        #print('курс биткоина взят')
        #парсинг погоды в минске
        url ='https://www.google.com/search?q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%BC%D0%B8%D0%BD%D1%81%D0%BA'
        page = requests.get(url, headers=self.headers)
        b_page = BeautifulSoup(page.text, 'lxml')
        self.weather = b_page.find('span', {'class': 'wob_t q8U8x'}).text.replace('  ', '')
        #парсинг изображения орсадков
        url = 'https://www.google.com/search?q=%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0+%D0%BC%D0%B8%D0%BD%D1%81%D0%BA'
        page = requests.get(url, headers=self.headers)
        b_page = BeautifulSoup(page.text, 'lxml')
        self.weather_img = 'https:'+b_page.find('img', {'class': 'wob_tci'}).get('src')
        print(self.weather_img)
        #парсинг стоимости игр
        factorio_url = 'https://store.steampowered.com/app/427520/Factorio/'
        self.price1 = pars_steam_price(factorio_url)

    def send(self):
        self.bot.send_message(self.my_id,'Привет , солнышко. Доброго тебе дня !!!!!!!!')

        for i in self.img_list:
            self.bot.send_photo(self.my_id,f'{i}')
        self.bot.send_message(self.my_id,'А вот и мемчики для тебя)')
        for i in self.meme_list:
            self.bot.send_photo(self.my_id,f'{i}')
        #self.bot.send_message(self.my_id,f'Курс биткоина(USD) - {self.bitcoin}')
        self.bot.send_message(self.my_id,f'Погода в городе минск : {self.weather} C')
        self.bot.send_photo(self.my_id , self.weather_img)
        self.bot.send_message(self.my_id, f'цена на factorio -{self.price1}')



def main():
    helper = Net_helper()
if __name__ == '__main__':
    main()