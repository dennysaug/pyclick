from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from PIL import Image
from captcha2upload import CaptchaUpload
import time


def init(browser, dados):
    print '\n[*] PTCBANK [*]'

    while browser.current_url != 'https://www.ptcbank.net/members.php':
        browser.get('https://www.ptcbank.net/login.php?r=')
        browser.find_element_by_name('username').send_keys(dados['login'])
        browser.find_element_by_name('password').send_keys(dados['senha'])
        browser.save_screenshot('ptcbank.png')
        img = Image.open('ptcbank.png')
        box = (650, 490, 788, 564)
        area = img.crop(box)
        area.save('ptcbank.png')

        captcha = CaptchaUpload('777c64eaf7b22ead16668198b16266e1')
        resposta = captcha.solve('ptcbank.png')

        browser.find_element_by_name('code').send_keys(resposta)
        time.sleep(8)

        time.sleep(2)
        print '[*] Efetuando login'
        browser.find_element_by_xpath('/html/body/div/div[4]/div/div/div/div/div/fieldset/form/table/tbody/tr[5]/td[2]/font/input').click()



def run(browser):
    mainWindow = browser.window_handles[0]
    browser.get('http://www.ptcbank.net/surfads.php')
    divAnuncios = browser.find_element_by_id('ref')
    divAnuncios = divAnuncios.find_elements_by_id('tables')

    saldo = 0.0

    ######################## ADS $0.20  ############################
    links = divAnuncios[0].find_elements_by_tag_name('a')
    if len(links):
        print '[*] Anuncios de $0.20'
        for link in links:
            try:
                print '[*] Clicando no anuncio'
                link.click()
                browser.switch_to_window(browser.window_handles[1])
                if browser.current_url.find('dfehwert.com') > 0:
                    adLink = browser.find_element_by_tag_name('a')
                    adLink = adLink.get_attribute('href')
                    adLink = 'http' + adLink.split('http')[3]
                    print '[*] Link capturado'
                    browser.get(adLink)
                    iframe = browser.find_element_by_tag_name('iframe')
                    print '[*] Selecionando iframe'
                    browser.switch_to_frame(iframe)
                    time.sleep(10)
                    fecharModal = True

                    while fecharModal:
                        try:
                            browser.find_element_by_id('close2').click()
                            print '[*] Recompensa adquirida com sucesso'
                            saldo = saldo + 0.2
                            fecharModal = False
                        except ElementNotVisibleException:
                            print '[*] Botao close ainda nao disponivel'
                            time.sleep(5)


                else:
                    print '[*] Anuncio nao contabilizado'

            except NoSuchElementException:
                print '[*] Nao foi possivel contabilizar Ads'
                continue

            while len(browser.window_handles) > 1:
                browser.switch_to_window(browser.window_handles[-1])
                browser.close()

            browser.switch_to_window(mainWindow)

    print '[*] Fim Ads $0.20'
    ##############################################################
    ######################## ADS $0.10  ############################
    links = divAnuncios[1].find_elements_by_tag_name('a')
    print '[*] Anuncios de $0.10'
    if len(links):
        for link in links:
            try:
                print '[*] Clicando no anuncio'
                link.click()
                browser.switch_to_window(browser.window_handles[1])
                if browser.current_url.find('dfehwert.com') > 0:
                    adLink = browser.find_element_by_tag_name('a')
                    adLink = adLink.get_attribute('href')
                    adLink = 'http' + adLink.split('http')[2]
                    print '[*] Link capturado'
                    browser.get(adLink)
                    iframe = browser.find_element_by_tag_name('iframe')
                    print '[*] Selecionando iframe'
                    browser.switch_to_frame(iframe)
                    time.sleep(10)
                    fecharModal = True
                    while fecharModal:
                        try:
                            browser.find_element_by_id('close2').click()
                            print '[*] Recompensa adquirida com sucesso'
                            saldo = saldo + 0.1
                            fecharModal = False
                        except ElementNotVisibleException:
                            print '[*] Botao close ainda nao disponivel'
                            time.sleep(5)

                else:
                    print '[*] Anuncio nao contabilizado'

            except NoSuchElementException:
                print '[*] Nao foi possivel contabilizar Ads'
                continue

            while len(browser.window_handles) > 1:
                browser.switch_to_window(browser.window_handles[-1])
                browser.close()

            browser.switch_to_window(mainWindow)


    print '[*] Fim Ads $0.10'
    ################################################################

    ######################## ADS $0.02  ############################
    links = divAnuncios[2].find_elements_by_tag_name('a')
    print '[*] Anuncios de $0.02'
    if len(links):
        for link in links:
            try:
                print '[*] Clicando no anuncio'
                link.click()

                browser.switch_to_window(browser.window_handles[1])
                if browser.current_url.find('dfehwert.com') > 0:
                    adLink = browser.find_element_by_tag_name('a')
                    adLink = adLink.get_attribute('href')
                    adLink = 'http' + adLink.split('http')[2]
                    print '[*] Link capturado'
                    browser.get(adLink)
                    iframe = browser.find_element_by_tag_name('iframe')
                    print '[*] Selecionando iframe'
                    browser.switch_to_frame(iframe)
                    time.sleep(12)
                    fecharModal = True
                    while fecharModal:
                        try:
                            browser.find_element_by_id('close2').click()
                            print '[*] Recompensa adquirida com sucesso'
                            saldo = saldo + 0.02
                            fecharModal = False
                        except ElementNotVisibleException:
                            print '[*] Botao close ainda nao disponivel'
                            time.sleep(5)


                else:
                    print '[*] Anuncio nao contabilizado'

            except NoSuchElementException:
                print '[*] Nao foi possivel contabilizar Ads'
                continue

            while len(browser.window_handles) > 1:
                browser.switch_to_window(browser.window_handles[-1])
                browser.close()

            browser.switch_to_window(mainWindow)

    print '[*] Fim Ads $0.2'
    ##############################################################
    ######################## ADS $0.30  ############################
    links = divAnuncios[3].find_elements_by_tag_name('a')
    print '[*] Anuncios de $0.30'
    if len(links) > 2:
        try:
            links[2].click()
            print '[*] Clicando no anuncio'
            time.sleep(5)
            browser.switch_to_window(browser.window_handles[1])

            print '[*] URL: ' + browser.current_url
            time.sleep(2)
            browser.execute_script('document.myform.submit();')
            time.sleep(3)
            print '[*] Recompensa adquirida com sucesso'
            saldo = saldo + 0.3
            browser.close()
            browser.switch_to_window(mainWindow)

        except NoSuchElementException:
            print '[*] Nao foi possivel contabilizar Ads'

        time.sleep(10)

        try:
            links[3].click()
            print '[*] Clicando no anuncio'
            time.sleep(5)
            browser.switch_to_window(browser.window_handles[1])
            print '[*] URL: ' + browser.current_url
            time.sleep(4)
            browser.execute_script('document.myform.submit();')
            print '[*] Recompensa adquirida com sucesso'
            saldo = saldo + 0.3
            time.sleep(4)
            browser.close()
            browser.switch_to_window(mainWindow)

        except NoSuchElementException:
            print '[*] Nao foi possivel contabilizar Ads'

    print '[*] Fim Ads $0.30'
    ##############################################################

    print '[*] Saldo dia: $' + str(saldo)
    browser.refresh()
    print '[*] PTCBANK [*]'
