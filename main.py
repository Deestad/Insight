import sys
import pickle
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

edge_options = EdgeOptions()
edge_options.use_chromium = True

edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')


browser = Edge(executable_path=r"C:\Users\ADM\MSEDGEWEBDRIVER\MicrosoftWebDriver.exe", options=edge_options)

browser.get("https://www.google.com")
pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))


while True:
    sitelocal = input("Qual site você deseja acessar?")

    while True:
        try:
            browser.get(sitelocal)
            break
        except:
            print("Por favor, insira um valor com HTTP incluído.")
            sitelocal = input("Qual site você deseja acessar?")

    pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)


    print("Coletando informações...")
    time.sleep(2)
    print("Título:")
    try:
        print(browser.find_element_by_xpath("//meta[@name='title']").get_attribute("content"))
    except:
        print("Título não está presente.")
        pass
    time.sleep(1)
    print("Descrição:")
    try:
        print(browser.find_element_by_xpath("//meta[@name='description']").get_attribute("content"))

    except:
        print("Descrição não está presente.")
        pass

    time.sleep(1)
    print("Palavras-chave:")
    time.sleep(1)
    try:
        print(browser.find_element_by_xpath("//meta[@name='keywords']").get_attribute("content"))
    except:
        print("Palavras Chave não estão presentes.")
        pass
    time.sleep(1)
    print("Autor e Direitos Autorais:")
    time.sleep(1)
    try:
        print(browser.find_element_by_xpath("//meta[@name='title']").get_attribute("content"))
    except:
        print ("Listagem de autor e Copyright não estão presentes.")
        pass
    time.sleep(1)
    print("Meta Robots:")
    time.sleep(1)

    try:
        print(browser.find_element_by_xpath("//meta[@name='robots']").get_attribute("content"))
    except:
        print("Meta Robots não está presente. Site não está oculto.")
        pass
    time.sleep(1)
    print("Fundamentos:")
    time.sleep(1)
    try:
        print(browser.find_element_by_xpath("//*[text()[contains(.,'Wix')]]").get_attribute("content"))
        print("Site possivelmente feito no Wix. Problemas de SEO e funcionalidade são esperados.")
    except:
        pass
    try:
        print(browser.find_element_by_xpath("//meta[@name='generator']").get_attribute("content"))
    except:
        print("Site feito com HTML.")
        pass
    time.sleep(1)

    while True:
        
        resposta = input("Gostaria de verificar algum outro site? Responda com S ou N:")

        if resposta == "S" or "s":
            print("Prosseguindo.")
            for i in range(0,10, 1):
                print(chr(27) + '[2j')
            break
        if resposta == "N" or "n":
            print("Fechando programa.")
            sys.exit()
            break
        if resposta != "S" or "s" or "N" or "n":
            print("Responda com S ou N.")
            pass







