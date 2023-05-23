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
def f_obtenerdatos(tipo_i,fiat_i,crypto_i):
    
    xpath_anunciante = "//div[@class='css-ovjtyv']//div[@class='css-1rhb69f']/a"
    xpath_ordenes = "//div[@class='css-ovjtyv']//div[@class='css-1a0u4z7']"
    xpath_completado = "//div[@class='css-ovjtyv']//div[@class='css-19crpgd']"
    xpath_precio = "//div[@class='css-ovjtyv']//div[@class='css-1m1f8hn']"
    xpath_disponible = "//div[@class='css-ovjtyv']//div[@class='css-3v2ep2']//div[@class='css-vurnku']"
    xpath_limites = "//div[@class='css-ovjtyv']//div[@class='css-16w8hmr']//div[@class='css-4cffwv']"
    xpath_pago = "//div[@class='css-tlcbro']"
    
    list_xpath = [xpath_anunciante,
                  xpath_ordenes,
                  xpath_completado,
                  xpath_precio,
                  xpath_disponible,
                  xpath_limites,
                  xpath_pago]
    
    datos = driver.find_elements(By.XPATH, xpath_anunciante)
    i_total = len(datos)

    list_i = []
    for i in range(0,i_total):
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
col_inicio = 'A'

max_datos_hoja = 10 #numero de filas de datos mostrados en binance, por hoja
max_iteracion_hoja_tfc = 2 #tfcm: combinación de tipo-fiat-crypto-metodo de pago

list_tipo = ['compra','venta'] 
#list_tipo = ['compra'] #temporal hasta desarrollar la def f_cambiartipo

range_fiat = sheet1.range('A2:A10')
list_fiat = range_fiat.options(ndim=1).value
list_fiat = list(filter(None, list_fiat))

range_mpago = sheet1.range('B2:B10')
list_mpago = range_mpago.options(ndim=1).value
list_mpago = list(filter(None,list_mpago))

range_crypto = sheet1.range('C2:C10')
list_crypto = range_crypto.options(ndim=1).value
list_crypto = list(filter(None,list_crypto))
list_crypto = ['USDT'] #temporal hasta desarrollar la def f_cambiarcrypto

timesleep = 6

#endregion

#region INICIALIZAR CHROMEDRIVER
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://p2p.binance.com/es/trade/all-payments/USDT?fiat=BOB' 
driver.get(url)
#driver.implicitly_wait(10) # seconds
driver.maximize_window()
#endregion

for tipo_i in list_tipo:
    f_cambiartipo(tipo_i)
    time.sleep(timesleep)

    for fiat_i in list_fiat:
        f_cambiarfiat(fiat_i)
        #driver.implicitly_wait(10)
        time.sleep(timesleep)

        for mpago_i in list_mpago:
            f_cambiarmpago(mpago_i)
            time.sleep(timesleep)
        
            for crypto_i in list_crypto:
                #f_cambiarcrypto(crypto_i)
                
                iteracion_hoja = 0
                repeticion = True
                while repeticion == True:
                    list_i = f_obtenerdatos(tipo_i,fiat_i,crypto_i) #hasta 10 filas de datos
                    sheet2.range(col_inicio+str(fila_inicio)).value = list_i

                    fila_inicio = fila_inicio + len(list_i)

                    iteracion_hoja = iteracion_hoja + 1

                    if len(list_i) < max_datos_hoja or iteracion_hoja == max_iteracion_hoja_tfc:
                        repeticion = False
                    else:
                        f_nextpage()
                        #driver.implicitly_wait(10)
                        time.sleep(timesleep)
driver.quit()