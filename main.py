"""
██████╗ ██╗  ██╗██╗███████╗██╗   ██╗
██╔══██╗██║  ██║██║██╔════╝╚██╗ ██╔╝
██████╔╝███████║██║███████╗ ╚████╔╝ 
██╔══██╗╚════██║██║╚════██║  ╚██╔╝
██║  ██║     ██║██║███████║   ██║
╚═╝  ╚═╝     ╚═╝╚═╝╚══════╝   ╚═╝ developed by r4isy#0001 / github.com/r4isy
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from winsound import Beep
import xlsxwriter
import time
import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
options = Options()

if(config.get('Settings', 'workonHide') == "True"):
    options.add_argument('--headless')
art = """
██████╗ ██╗  ██╗██╗███████╗██╗   ██╗
██╔══██╗██║  ██║██║██╔════╝╚██╗ ██╔╝
██████╔╝███████║██║███████╗ ╚████╔╝ 
██╔══██╗╚════██║██║╚════██║  ╚██╔╝
██║  ██║     ██║██║███████║   ██║
╚═╝  ╚═╝     ╚═╝╚═╝╚══════╝   ╚═╝
"""

print(art)

kenu = False

def process(urL, workbook, worksheet, row):
    global driver
    global wait
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    url = urL

    # Driver'ı başlat
    

    driver.get(url)

    # Web sayfasının tamamen yüklenmesini bekle
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#titleSection")))
    adresbutton = driver.find_elements(By.XPATH, './/a[@class="nav-a nav-a-2 a-popover-trigger a-declarative nav-progressive-attribute"]')
    adresbutton[0].click()
    time.sleep(1)

    if "amazon.com" in driver.current_url:
        wait.until(EC.presence_of_element_located((By.XPATH, './/input[@class="GLUX_Full_Width a-declarative"]')))
        textbox = driver.find_element(By.XPATH, './/input[@class="GLUX_Full_Width a-declarative"]')
        textbox.send_keys("10001")
        submit = driver.find_element(By.XPATH, './/div[@role="button"]')
        submit.click()
        time.sleep(1)
        submit2 = driver.find_element(By.XPATH, './/input[@aria-labelledby="GLUXConfirmClose-announce"]')
        driver.execute_script("arguments[0].click();", submit2)
        kenu = True    
        time.sleep(1)

    elif "amazon.ca" in driver.current_url:
        wait.until(EC.presence_of_element_located((By.XPATH, './/input[@id="GLUXZipUpdateInput_0"]')))
        textbox = driver.find_element(By.XPATH, './/input[@id="GLUXZipUpdateInput_0"]')
        textbox.send_keys("A1A")
        textbox2 = driver.find_element(By.XPATH, './/input[@id="GLUXZipUpdateInput_1"]')
        textbox2.send_keys("1A1")
        submit = driver.find_element(By.XPATH, './/input[@aria-labelledby="GLUXZipUpdate-announce"]')
        submit.click()
        kenu = False
        time.sleep(4)

    realprice = check()

    # Tarayıcıyı kapatma
    print(realprice)
    driver.quit()
    worksheet.write(row, 0, url)
    worksheet.write(row, 1, realprice)

def keno():
        print("Direkt alınamaz")
        time.sleep(2)
        global whole_price
        global fraction_price
        global price
        global rprice
        whole_price = driver.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = driver.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        price = price.replace("$", "")
        if(price != "."):
            rprice = price
        else:
            rprice = "Fiyat bilgisi alınamadı."
        return rprice

def check():
    try:
        time.sleep(3)
        hopbidi = driver.find_element(By.XPATH, './/span[@id="buybox-see-all-buying-choices"]')
        hopbidi.click()
        realprice = keno()

    except:
        print("Direkt alınabilir")
        whole_price = driver.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
        fraction_price = driver.find_elements(By.XPATH,'.//span[@class="a-price-fraction"]')
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        price = price.replace("$", "")
        if(price != "."):
            realprice = price
        else:
            realprice = "Fiyat bilgisi alınamadı."

    return realprice

def run_processes(filename):
    with open(filename) as f:
        num_lines = sum(1 for line in f)
    print("Number of lines:", num_lines)
    
    # Excel dosyasını oluştur ve başlık satırlarını ekle
    x = datetime.datetime.now()
    workbook = xlsxwriter.Workbook( x.strftime("%d") + "." +  x.strftime("%m") + "." +  x.strftime("%y") +'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Link")
    worksheet.write(0, 1, "Fiyat")
    row = 1
    
    with open(filename) as f:
        for i in range(num_lines):
            line = f.readline().strip()
            process(line, workbook, worksheet, row)
            row += 1
            
    # Excel dosyasını kaydet ve kapat
    workbook.close()

run_processes("links.txt")
Beep(1635,500)
Beep(1635,500)