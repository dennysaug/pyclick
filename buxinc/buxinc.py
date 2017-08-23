#firefox 46


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# from selenium import webdriver

import time
import random

def resolveCaptcha(browser):
    mainWindow = browser.window_handles[0]  # pega "focus" da janela principal
    print '[*] Trocando para nova janela'
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(30)


    # if browser.find_element_by_tag_name('body').text == 'You have reached your BuxGrid limit for today.':
    #     print '[*] You have reached your BuxGrid limit for today.'
    #     browser.close()
    #     browser.switch_to_window(mainWindow)
    #     print 'ENTROU NO IF'
    #     return False

    try:
        if browser.current_url.find('gpt.php') > 0:

            frame = browser.find_element_by_tag_name('frame')
            browser.switch_to_frame(frame)
            timer = browser.find_element_by_id('timer').text
            numCaptcha = timer.split(' ')[1]
            if numCaptcha:
                buttons = browser.find_element_by_id('buttons')
                lists = buttons.find_elements_by_tag_name('a')
                for li in lists:
                    try:
                        element = WebDriverWait(li, 5).until(
                            EC.visibility_of_element_located((By.TAG_NAME, "img"))
                        )

                        if element:
                            img = li.find_element_by_tag_name('img').get_attribute('src')
                            numImg = img.split('clickimages/')[1]
                            if numImg[0] == numCaptcha:
                                print '[*] Captcha resolvido com sucesso'
                                li.click()
                                break
                        else:
                            '[*] Imagem do captcha nao encontrada'

                    except NoSuchElementException:
                        print '[*] Captcha nao resolvido'


    except NoSuchElementException:
        print '[*] Captcha nao disponivel'
        return False

    finally:
        time.sleep(5)
        while len(browser.window_handles) > 1:
            browser.switch_to_window(browser.window_handles[-1])
            browser.close()
        # print '[*] Aguardando 2s para recomecar's
        browser.switch_to_window(mainWindow)




############################################ INICIO ##############################################

def init(browser, dados):
    print '\n[*] BUXINC [*]'
    browser.get('http://www.buxinc.com/')

    login = "document.getElementsByName('form_user')[0].value = '%s'" % dados['login']
    senha = "document.getElementsByName('form_pwd')[0].value = '%s'" % dados['senha']

    browser.execute_script(login)
    browser.execute_script(senha)

    print '[*] Efetuando login'
    browser.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div/div/div[1]/div[1]/form/div[3]/input').click()

###################################### VIEWS ADS ############################################

def run(browser):
    print '\n[*] BUXINC [*]'
    print '[*] Views Ads'
    browser.switch_to_window(browser.window_handles[0])
    browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]/a').click()

    try:
        table = browser.find_element_by_class_name('ptcList')
        if table:
            links = table.find_elements_by_tag_name('a')
            for link in links:
                if link.get_attribute('href').find('/gpt.php?v=') > 1:
                    link.click()
                    time.sleep(5)
                    resolveCaptcha(browser)

            print '[*] Fim Ads'

    except NoSuchElementException:
        print '[*] Ads indisponivel no momento'

    ######################################### BUXGRID #################################################
    browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[6]/a').click()
    print '[*] Indo para BuxGrid'
    grid = browser.find_element_by_id('bg-grid-w2')
    spans = grid.find_elements_by_tag_name('span')

    print '[*] Iniciando 40 jogadas'

    randon_spans = random.sample(spans,40)

    for span in randon_spans:
        try:
            if span:
                print '[*] Acessando ' + span.get_attribute('rel')
                span.click()
                time.sleep(10)
                if resolveCaptcha(browser) == False:
                    return
        except NoSuchElementException:
            print '[*] Link do anuncio nao encontrado'

    print "[*] Fim BuxGrid [*]"

