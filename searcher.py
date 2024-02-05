import sys
import pickle
import time
import tkinter as tk
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

options = webdriver.FirefoxOptions()
options.add_argument("-headless")

app = tk.Tk()
app.title('Ferramenta de Busca - β1')
app.geometry("800x500")
app.iconbitmap("FaviconAlt3.ico")

Googling = False

IQ = tk.Entry(app, width=100, borderwidth=15, relief=tk.FLAT, bg="lightgrey")
IQ.pack()
IQ.insert(0, "O que você está procurando?")

AuthorCopy = tk.Label(app, text="Lys Kaldwin 2024 © Todos os direitos reservados.")
AuthorCopy.pack()

L1 = tk.Listbox(app)

def InitialQuestion():
    L1.delete(0, tk.END)

    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    browser.get("https://www.google.com")
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))

    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    time.sleep(5)

    browser.find_element(By.NAME, "q").send_keys(IQ.get())
    time.sleep(5)
    browser.find_element(By.NAME, "q").send_keys(Keys.ENTER)
    results_list = browser.find_elements(By.XPATH, '//div[@class="g"]//a')
    i = 0

    def OpenURL(event):
        weblink = L1.get(tk.ACTIVE)
        webbrowser.open(weblink)

    for item in results_list:
        Attribute = [item.get_attribute('href') for item in browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')]

        for items in Attribute:
            L1.insert(i, items)
            i += 1

        if i == 100:
            browser.find_element(By.ID, "pnnext").click()
            results_list = browser.find_elements(By.XPATH, '//div[@class="g"]//a')

            for item in results_list:
                Attribute = [item.get_attribute('href') for item in browser.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a')]

                for items in Attribute:
                    L1.insert(i, items)
                    i += 1

                if i == 100:
                    results_list = browser.find_elements(By.XPATH, '//div[@class="g"]//a')
                    break
            break

    browser.quit()

    L1.bind("<Double-Button-1>", OpenURL)
    L1.pack(expand=True, fill=tk.BOTH)


Button = tk.Button(app, text="Enviar", padx=40, pady=2, command=InitialQuestion, bg='lightgreen')
Button.pack()

app.mainloop()
