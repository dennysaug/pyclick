#firefox 46
from requests.exceptions import ConnectionError

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotVisibleException
from compareimage import  bot
import requests
import time
import random


def resolveCaptcha(browser):
    mainWindow = browser.window_handles[0]  # pega "focus" da janela principal
    print '[*] Trocando para nova janela'
    browser.switch_to_window(browser.window_handles[1])
    # time.sleep(10)

    # if browser.find_element_by_tag_name('body').text == "Error - You've already made all attempts of today.":
    #     print '[*] ' + browser.find_element_by_tag_name('body').text
    #     return False

    try:

        if browser.current_url.find('gpt.php') > 1 or browser.current_url.find('surfing_grid.php') > 1:
            roda = True
            while roda:
                roda = False
                try:
                    frame = browser.find_element_by_name('surfmainframe')
                    if frame.get_attribute('src').find('gpt.php?v=cheat') > 1:
                        print '[*] Resolvendo captcha interno'
                        browser.switch_to_frame(frame)
                        pergunta = browser.find_element_by_tag_name('span').text
                        tts = browser.find_elements_by_tag_name('tt')

                        if pergunta.find('XWYZ') > 1:
                            for tt in tts:
                                if tt.text == pergunta:
                                    tt.find_element_by_tag_name('input').click()


                        elif pergunta == 'Is this PTCstar.com?':
                            for tt in tts:
                                if tt.text == 'YES':
                                    tt.find_element_by_tag_name('input').click()

                        elif pergunta == '2x5':
                            for tt in tts:
                                if tt.text  == '10':
                                    tt.find_element_by_tag_name('input').click()

                        elif pergunta == '17-5':
                            for tt in tts:
                                if tt.text == '12':
                                    tt.find_element_by_tag_name('input').click()

                        elif pergunta == 'GRASS IS':
                            for tt in tts:
                                if tt.text == 'BLACK':
                                    tt.find_element_by_tag_name('input').click()

                        else:
                            print '[*] Pergunta nao localizada'


                        browser.find_element_by_name('submit').click()
                        print '[*] Captcha interno resolvido com sucesso'
                        print '[*] Atualizando a pagina'
                        time.sleep(2)
                        roda = True

                except NoSuchElementException:
                    print '[*] Sem captcha interno'
                    roda = False



            time.sleep(5)
            frame = browser.find_element_by_tag_name('frame')
            browser.switch_to_frame(frame)

            timerOK = True
            while timerOK:
                try:
                    timer = browser.find_element_by_id('timer')
                    linkImagem = timer.find_element_by_tag_name('img').get_attribute('src')
                    print '[*] Lendo imagem do captcha'
                    timerOK = False

                except NoSuchElementException:
                    print '[*] Aguardando carregar as imagens'
                    timerOK = True
                    time.sleep(3)

            time.sleep(2)

            connection = True
            while connection:
                try:
                    print '[*] Baixando img1.png'
                    r = requests.get(linkImagem)
                    connection = False
                except ConnectionError:
                    print '[*] Timeout '
                    time.sleep(3)
                    connection = True

            resolvido = False
            time.sleep(5)
            while not resolvido:
                try:
                    if r.ok:
                        print '[*] Salvando a img1.png'
                        img1 = open('img1.png', 'w')
                        img1.writelines(r.content)
                        img1.close()

                        buttons = browser.find_element_by_id('buttons')
                        lists = buttons.find_elements_by_tag_name('a')
                        alvo = {}
                        for li in lists:
                            try:
                                element = WebDriverWait(li, 5).until(
                                    EC.visibility_of_element_located((By.TAG_NAME, "img"))
                                )

                                if element:
                                    img = li.find_element_by_tag_name('img').get_attribute('src')
                                    connection = True
                                    while connection:
                                        try:
                                            r = requests.get(img)
                                            print '[*] Baixando img2.png'
                                            connection = False
                                        except ConnectionError:
                                            print '[*] Aguardando 5s para tentar baixar novamente'
                                            time.sleep(3)

                                    time.sleep(3)
                                    if r.ok:
                                        print '[*] Tentando resolver o captcha'
                                        img2 = open('img2.png', 'w')
                                        img2.writelines(r.content)
                                        img2.close()
                                        resultado = bot.solve('img1.png', 'img2.png')
                                        print '[*] ' + str(resultado) + ' pixels de diferenca'
                                        alvo[resultado] = li


                                else:
                                    '[*] Imagem do captcha nao encontrada'


                            except NoSuchElementException:
                                print '[*] Captcha ainda nao carregado totalmente'
                                time.sleep(3)
                                print '[*] Nova tentativa sera realizada'

                        index = sorted(alvo)[0]
                        alvo[index].click()
                        print '[*] Captcha resolvido com sucesso\n'
                        resolvido = True
                        time.sleep(2)

                except NoSuchElementException or StaleElementReferenceException or IndexError:
                    print '[*] Nao resolvido. Tentando novamente'


    except NoSuchElementException or StaleElementReferenceException:
        print '[*] Captcha nao disponivel\n'
        return False

    finally:
        # time.sleep(1)
        while len(browser.window_handles) > 1:
            browser.switch_to_window(browser.window_handles[-1])
            browser.close()
        browser.switch_to_window(mainWindow)




############################################ INICIO ##############################################

def init(browser, dados):
    print '\n[*] PTCSTAR [*]'
    browser.get('http://ptcstar.com/index.php?view=login&')
    login = "document.getElementsByName('form_user')[0].value = '%s'" % dados['login']
    senha = "document.getElementsByName('form_pwd')[0].value = '%s'" % dados['senha']

    browser.execute_script(login)
    browser.execute_script(senha)
    print '[*] Efetuando login'
    browser.find_element_by_class_name('login_submit').click()
    time.sleep(10)
    i = 1
    while i < 3:
        print '[*] Cancelado o alert ' + str(i)
        browser.switch_to_alert().dismiss()
        time.sleep(2)
        i += 1

###################################### VIEWS ADS ############################################

def run(browser):
    print '\n[*] PTCSTAR [*]'
    print '[*] Views Ads'

    browser.get('http://ptcstar.com/index.php?view=click&')

    try:
        table = browser.find_element_by_class_name('ads_box')

        if table:
            links = table.find_elements_by_class_name('ads_title')
            for link in links:
                print '[*] Acessando ' + link.find_element_by_tag_name('a').get_attribute('href')
                if link.find_element_by_tag_name('a').get_attribute('href').find('gpt.php?v=') > 1:
                    link.find_element_by_tag_name('a').click()
                    time.sleep(2)
                    resolveCaptcha(browser)

            print '[*] Fim Ads'

    except NoSuchElementException:
        print '[*] Ads indisponivel no momento'

    ######################################### STARGRID #################################################

    starGrid = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/nav/ul/li[2]/ul/li[3]/a').get_attribute('href')
    browser.get(starGrid)
    print '[*] Indo para StarGrid'
    grid = browser.find_element_by_class_name('adgridbase')
    links = grid.find_elements_by_class_name('adgrid')

    print '[*] Iniciando 20 jogadas'

    randon_links = random.sample(links,20)

    for link in randon_links:
        try:
            browser.switch_to_window(browser.window_handles[0])
            if link:
                try:
                    link.click()
                    if len(browser.window_handles) > 1:
                        print '[*] Acessando ' + link.get_attribute('id')
                        time.sleep(4)
                        resolveCaptcha(browser)
                    else:
                        print '[*] Tentivas esgotadas'
                        return
                except StaleElementReferenceException:
                    print '[*] Link nao encontrado'


        except NoSuchElementException:
            print '[*] Link do anuncio nao encontrado'

    print "[*] Fim StarGrid [*]"

    # transformar em base64 para comparar as strings.
    #####################################################################################
    # import time
    # from selenium import webdriver
    # browser = webdriver.Firefox(timeout=60)
    # mainWindow = browser.window_handles[0]
    # browser.set_window_size(1200,654)
    # print '\n[*] PTCSTAR [*]'
    # browser.get('http://ptcstar.com/index.php?view=login&')
    # browser.execute_script("document.getElementsByName('form_user')[0].value = 'dennysaug'")
    # browser.execute_script("document.getElementsByName('form_pwd')[0].value = '051938..'")
    # print '[*] Efetuando login'
    # browser.find_element_by_class_name('login_submit').click()
    # time.sleep(10)
    # browser.switch_to_alert().dismiss()
    # time.sleep(2)
    # browser.switch_to_alert().dismiss()
    # browser.get('http://ptcstar.com/index.php?view=click&')
    # table = browser.find_element_by_class_name('ads_box')
    # links = table.find_elements_by_class_name('ads_title')