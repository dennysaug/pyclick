from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
# from selenium import webdriver

def resolveCaptcha(browser):
    mainWindow = browser.window_handles[0]  # pega "focus" da janela principal
    print '[*] Trocando para nova janela'
    browser.switch_to_window(browser.window_handles[1])
    time.sleep(95)

    frame = browser.find_element_by_tag_name('frame')
    browser.switch_to_frame(frame)
    try:
        timer = browser.find_element_by_id('timer').text
        numCaptcha = timer.split(' ')[1]
        if numCaptcha:
            buttons = browser.find_element_by_id('buttons')
            lists = buttons.find_elements_by_tag_name('a')
            for li in lists:
                try:
                    element = WebDriverWait(li, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "img"))
                    )

                    if element:
                        img = li.find_element_by_tag_name('img').get_attribute('src')
                        numImg = img.split('clickimages/')[1]
                        if numImg[0] == numCaptcha:
                            print '[*] Captcha resolvido com sucesso'
                            li.click()
                            time.sleep(5)
                            break
                    else:
                        '[*] Imagem do captcha nao encontrada'

                except NoSuchElementException:
                    print '[*] Captcha nao resolvido'

    except NoSuchElementException:
        print '[*] Captcha nao disponivel'

    finally:
        time.sleep(5)
        while len(browser.window_handles) > 1:
            browser.switch_to_window(browser.window_handles[-1])
            browser.close()

        browser.switch_to_window(mainWindow)



############################################ INICIO ##############################################
def init(browser, dados):
    print '\n[*] TWO DOLLAR CLICK [*]'
    browser.get('http://www.twodollarclick.com/index.php?view=login&sid2=TkM0M&siduid=2810211&')

    login = "document.getElementsByName('form_user')[0].value = '%s'" % dados['login']
    senha = "document.getElementsByName('form_pwd')[0].value = '%s'" % dados['senha']

    browser.execute_script(login)
    browser.execute_script(senha)
    print '[*] Efetuando login'
    browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/form/div/div/div[1]/div[3]/a').click()
    time.sleep(10)

def run(browser):
    browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/ul/li[2]/a').click()
    try:
        print '[*] Capturando os anuncios'
        anuncios = browser.find_elements_by_class_name('ptcbox-w1')
        for anuncio in anuncios:
            anuncio.click()
            resolveCaptcha(browser)

    except NoSuchElementException:
        print '[*] Ads nao disponivel no momento'

    finally:
        print '[*] Fim Two Dollar Click [*]'

