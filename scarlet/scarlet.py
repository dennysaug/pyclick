import Image
import base64
import os
import requests

from captcha2upload import CaptchaUpload
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random



def resolveCaptcha(browser, imagesb64):
    mainWindow = browser.window_handles[0]  # pega "focus" da janela principal
    print '[*] Trocando para nova janela'
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(35)

    try:

        browser.save_screenshot('scarlet/scarlet.png')
        scarlet = Image.open('scarlet/scarlet.png', 'r')
        scarlet.crop((371,8,671,58)).convert('RGB').save('scarlet/crop.png')

        posicao = 50
        ordem = 0

        map = browser.find_element_by_id('Map')
        areas = map.find_elements_by_tag_name('area')
        time.sleep(4)

        browser.execute_script("$('area').css('display', 'block');")

        while posicao <= 300:
            nomeImagem = 'testando' +str(ordem)+ '.png'
            print '[*] ' + nomeImagem
            Image.open('scarlet/crop.png','r').crop((posicao-50,0,posicao,50)).convert('RGB').save('scarlet/'+nomeImagem)
            img64 = open('scarlet/' + nomeImagem, 'r')
            img64 = base64.b64encode(img64.read())


            if len([imgb for imgb in imagesb64 if img64 in imgb]):
                endprogress = areas[ordem].get_attribute('onclick')
                browser.execute_script(endprogress);
                print '[*] Imagem de cabeca para baixo localizada e clicada'
                time.sleep(12)
                posicao = 300
            else:
                posicao += 50
                ordem += 1

        try:
            browser.find_element_by_class_name('successbox')
            print '[*] Captcha resolvido com sucesso'

        except NoSuchElementException:
            print '[*] Captcha nao resolvido'



    except NoSuchElementException:
        print '[*] Captcha nao disponivel'

    finally:
        print 'entrou  no finally!'
        time.sleep(10)
        browser.close()
        browser.switch_to_window(mainWindow)




def init(browser, dados):
    print '[*] Abrindo o browser'
    while browser.current_url != 'http://www.scarlet-clicks.info/index.php?view=account':
        browser.get('https://www.scarlet-clicks.info/index.php?view=login')
        browser.find_element_by_name('username').send_keys(dados['login'])
        browser.find_element_by_name('psword').send_keys(dados['senha'])
        browser.save_screenshot('scarlet/captchalogin.png')
        Image.open('scarlet/captchalogin.png').crop((220, 350, 460, 420)).save('scarlet/captchalogin.png')

        captcha = CaptchaUpload('777c64eaf7b22ead16668198b16266e1')
        resposta = captcha.solve('scarlet/captchalogin.png')

        browser.find_element_by_name('captcha').send_keys(resposta)

        print '[*] Efetuando login'
        browser.find_element_by_name('login').click()
        time.sleep(22)



def run(browser):
    print '[*] Views Ads'
    browser.get('http://www.scarlet-clicks.info/index.php?view=ads')
    time.sleep(2)

    imagesb64 = []

    for imgb64 in os.listdir('scarlet/captchas'):
        imgb64 = open('scarlet/captchas/' + imgb64, 'r')
        imagesb64.append(base64.b64encode(imgb64.read()))

    try:
        ads = browser.find_elements_by_css_selector('div.ad-block')
        if len(ads):
            for ad in ads:
                if ad.get_attribute('class').find('disabled') < 1:
                    ad.find_element_by_tag_name('span').click()
                    time.sleep(3)
                    resolveCaptcha(browser, imagesb64)


            print '[*] Fim Ads'


    except NoSuchElementException:
        print '[*] Ads indisponivel no momento'


    ######################################### BUXGRID #################################################
    print '[*] Indo para ScarletGrid'
    browser.get('http://www.scarlet-clicks.info/clixgrid.php')
    grid = browser.find_element_by_class_name('clixgrid_block')
    tds = grid.find_elements_by_tag_name('td')

    print '[*] Iniciando 20 jogadas'


    mainWindow = browser.window_handles[0]  # pega "focus" da janela principal
    randon_block = random.sample(tds,14)

    for block in randon_block:
        try:
            while len(browser.window_handles) <= 1:
                try:
                    print '[*] Acessando ' + block.get_attribute('onclick')
                    block.click()
                    browser.switch_to_window(browser.window_handles[1])
                except IndexError or StaleElementReferenceException:
                    print '[*] Click ainda nao realizado.'
                    time.sleep(3)

            print '[*] Trocando para nova janela'
        except NoSuchElementException:
            print '[*] Link do anuncio nao encontrado'
        finally:
            time.sleep(25)
            browser.close()
            browser.switch_to_window(mainWindow)
            print '[*] Fim'


    print "[*] Fim ScarletGrids\n"
