from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import xlwings as xw
import time

def f_cambiarfiat(fiat_i):
    fiatbox = driver.find_element(By.XPATH, "//div[@id='C2Cfiatfilter_searchbox_fiat']//div[@class=' css-uf3q7d']")
    fiatbox.click()
    fiatinput = driver.find_element(By.XPATH, "//div[@id='C2Cfiatfilter_searchbox_fiat']//input[@class='css-jl5e70']")
    fiatinput.send_keys(fiat_i)
    fiatinput.send_keys(Keys.ENTER)
def f_cambiarmpago(mpago_i):
    mpagobox = driver.find_element(By.XPATH, "//div[@id='C2Cpaymentfilter_searchbox_payment']//div[@class=' css-uf3q7d']")
    mpagobox.click()
    mpagoinput = driver.find_element(By.XPATH, "//div[@id='C2Cpaymentfilter_searchbox_payment']//input[@class='css-jl5e70']")
    mpagoinput.send_keys(mpago_i)
    mpagoinput.send_keys(Keys.ENTER)
#def f_cambiarcrypto(crypto_i):
def f_cambiartipo(tipo):
    if tipo == 'compra':
        xpath_tipo = "//div[@class='css-1xpzmrx']" #compra
    else:
        xpath_tipo = "//div[@class='css-dvbf59']" #venta
    driver_tipo = driver.find_element(By.XPATH, xpath_tipo)
    driver_tipo.click()
def f_nextpage():
    nextpage_button = driver.find_element(By.XPATH, "//button[@id='next-page']")
    nextpage_button.click()
def f_obtenerdatos(tipo_i,fiat_i,crypto_i,datos_total):
    
    xpath_anunciante = "//div[@class='css-1jb7fpj']"
    xpath_ordenes = "//div[@class='css-1a0u4z7']"
    xpath_completado = "//div[@class='css-19crpgd']"
    xpath_precio = "//div[@class='css-1m1f8hn']"
    xpath_disponible = "//div[@class='css-3v2ep2']//div[@class='css-vurnku']"
    xpath_limites = "//div[@class='css-4cffwv']"
    xpath_pago = "//div[@class='css-tlcbro']"
    
    list_xpath = [xpath_anunciante,
                  xpath_ordenes,
                  xpath_completado,
                  xpath_precio,
                  xpath_disponible,
                  xpath_limites,
                  xpath_pago]
    
    datos_total_driven = len(driver.find_elements(By.XPATH, xpath_anunciante))
    if datos_total_driven < datos_total:
        datos_total = datos_total_driven
        
    list_i = []
    for i in range(0,datos_total):
        list_datos = [tipo_i,fiat_i,crypto_i]
        for xpath_i in list_xpath:
            driver_xpath = driver.find_elements(By.XPATH, xpath_i)
            
            if xpath_i == xpath_limites:
                dato_xpath = driver_xpath[i*2].text
                list_datos.append(dato_xpath)
                dato_xpath = driver_xpath[i*2+1].text
                list_datos.append(dato_xpath)
            else:
                dato_xpath = driver_xpath[i].text
                list_datos.append(dato_xpath)
            
            if xpath_i == xpath_pago:
                mpagos = dato_xpath
                list_mpagos=[]
                ultimo = False
                for i in range(0,10): #Guardar hasta 10 metodos de pago
                    if ultimo == True:
                        list_mpagos.append('')
                    else:
                        index_fin = mpagos.find('\n')
                        if index_fin > -1:
                            pago_i = mpagos[0:index_fin]
                            mpagos = mpagos[index_fin+1:len(mpagos)]
                        else:
                            pago_i = mpagos
                            ultimo = True
                        list_mpagos.append(pago_i)

                list_datos = list_datos[0:len(list_datos)-1]
                list_datos = list_datos + list_mpagos                
        list_i.append(list_datos)
    
    return(list_i)

#region DEFINIR VARIABLES

path = 'C:/Users/user/Documents/'
file = '30_p2p.xlsx'
wb = xw.Book(path+file)
sheet1 = wb.sheets['Sheet1']
sheet2 = wb.sheets['Hoja1']
fila_inicio = 2 #fila en la que inicia a copiar en excel
col_inicio = 'A' #columna en la que inicia a copiar en excel

max_datos_hoja = int(sheet1.range('B1').value) #numero de filas de datos mostrados en binance, por hoja
datos_total = int(sheet1.range('B2').value) #numero de filas (anunciantes) a guardar

range_tipo = sheet1.range('B5:B14')
list_tipo = range_tipo.options(ndim=1).value
list_tipo = list(filter(None, list_tipo))

range_fiat = sheet1.range('C5:C14')
list_fiat = range_fiat.options(ndim=1).value
list_fiat = list(filter(None, list_fiat))

range_mpago = sheet1.range('D5:D14')
list_mpago = range_mpago.options(ndim=1).value
list_mpago = list(filter(None,list_mpago))

range_crypto = sheet1.range('E5:E14')
list_crypto = range_crypto.options(ndim=1).value
list_crypto = list(filter(None,list_crypto))
#list_crypto = ['USDT'] #temporal 

timesleep = 5

#endregion

#region INICIALIZAR CHROMEDRIVER
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://p2p.binance.com/es/trade/all-payments/USDT?fiat=BOB' 
driver.get(url)
#driver.implicitly_wait(10) # seconds
driver.maximize_window()
#endregion

sheet2.range('A1').value = ['Tipo','Fiat','Crypto','Anunciante','Ordenes','%Completado','Precio','Disponible','Límite Inf','Límite Sup','Pago1','Pago2','Pago3','Pago4','Pago5','Pago6','Pago7','Pago8','Pago9','Pago10']
for tipo_i in list_tipo:
    f_cambiartipo(tipo_i)
    time.sleep(timesleep)

    for fiat_i in list_fiat:
        f_cambiarfiat(fiat_i)
        time.sleep(timesleep)

        for mpago_i in list_mpago:
            f_cambiarmpago(mpago_i)
            time.sleep(timesleep)
        
            for crypto_i in list_crypto:
                #f_cambiarcrypto(crypto_i)
                
                datos_i = 0
                repeticion = True
                while repeticion == True:
                    list_i = f_obtenerdatos(tipo_i,fiat_i,crypto_i,datos_total) #
                    sheet2.range(col_inicio+str(fila_inicio)).value = list_i

                    fila_inicio = fila_inicio + len(list_i)

                    datos_i = datos_i + len(list_i)

                    if datos_i < datos_total:
                        f_nextpage()
                        #driver.implicitly_wait(10)
                        time.sleep(timesleep)
                    else:
                        repeticion = False                      
                        
driver.quit()