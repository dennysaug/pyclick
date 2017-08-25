import time
from selenium import webdriver
from buxinc import buxinc
from twodollarclick import twodollarclick
from ptcbank import ptcbank
from freebitcoin import freebitcoin
from scarlet import  scarlet
from ptcstar import  ptcstar



# NAO REMOVA MEUS CREDITOS!
print "[*] BOT PARA MINERAR BY DENNYS AUGUSTUS [*]\n"
# DEU TRABALHO FAZER ESSA BAGACA!

#LENDO ARQUIVO COM SENHAS#
env = open('.env', 'r')
env = env.readlines()
dados = {}

dados['ptcbank'] = {'login': env[2].rstrip('\n').split('=')[1], 'senha': env[3].rstrip('\n').split('=')[1]}
dados['ptcstar'] = {'login': env[5].rstrip('\n').split('=')[1], 'senha': env[6].rstrip('\n').split('=')[1]}
dados['scarlet'] = {'login': env[8].rstrip('\n').split('=')[1], 'senha': env[9].rstrip('\n').split('=')[1]}
dados['buxinc'] = {'login': env[11].rstrip('\n').split('=')[1], 'senha': env[12].rstrip('\n').split('=')[1]}
dados['twodollarclick'] = {'login': env[14].rstrip('\n').split('=')[1], 'senha': env[15].rstrip('\n').split('=')[1]}


browser = webdriver.Firefox(timeout=60)
mainWindow = browser.window_handles[0]

browser.set_window_size(1200,654)

# eveads.net
# http://10centclix.com
# http://greatadz.com

while True:
    i = 0

    # ptcbank.init(browser, dados['ptcbank'])
    # ptcbank.run(browser)

    ptcstar.init(browser, dados['ptcstar'])
    ptcstar.run(browser)

    scarlet.init(browser, dados['scarlet'])
    scarlet.run(browser)

    twodollarclick.init(browser, dados['buxinc'])
    twodollarclick.run(browser)

    buxinc.init(browser, dados['twodollarclick'])
    buxinc.run(browser)

    print 'Aguardando 24hrs pare reiniciar'
    time.sleep(86400)



