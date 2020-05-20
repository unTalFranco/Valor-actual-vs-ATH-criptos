import datetime
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

claveApi = 'API KEY COINMARKETCAP'  #Acá tenes que introducir la api key obtenida en coinmarketcap.

estadistica = {}
datosFinales = {}
def compararPrecio(codigo): #compara ATH con precio de apertura y saca el porcentaje correspondiente.
    try:
        ath = maximo(codigo)
        precioHoy = apertura(codigo)    
        porcentaje= "{0:.2f}".format(float(precioHoy/ath*100))
        estadistica[codigo]=porcentaje
        print("El precio de " + codigo + " se encuentra en el: " + str(porcentaje) + "% con respecto a su ATH.")
        datosFinales[codigo] = float(porcentaje)
    except:
        print("La api no encontro data sobre " + codigo)

def maximo(codigo): #Trae info de yahoo finance con las cotizaciones historicas y luego busca el ATH.
    ayer = str(getYesterday())
    df = pdr.get_data_yahoo(codigo, start = '2017/01/03', end = ayer)
    ath1 = df['High'].max()
    return ath1

def apertura(codigo): #Obtiene de yahoo finance el precio de apertura del dia. 
    crypto = yf.Ticker(codigo)
    diccionario = dict(crypto.info)
    return diccionario['open']

def getYesterday():           #obtiene la fecha de ayer.
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday 
    return yesterday

def inicializador(cantidad):    #inicia el algoritmo. Se le pasa por argumento la cantidad de criptos a analizar
    cmDatosRank = cmRank()
    lista = crearLista(cmDatosRank,cantidad)
    for item in lista:
        compararPrecio(item)
    print(datosFinales)

def crearLista(respuesta,cantidad):   #Transforma la respuesta de CMC en una lista,con los codigos de las cripto segun el ranking. Y ejecuta el algoritmo por cada item
    data = list(respuesta['data'])
    n=0
    listaSimbolos = []
    while n <= int(cantidad):
        item = data[n]
        listaSimbolos.append(item['symbol']+"-USD")
        n+=1
    return listaSimbolos        
        
        
def cmRank(): #Solicita a la api de CMC un JSON con la info de las criptos.
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
      'sort':"cmc_rank"
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': claveApi,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
   
  #inicializador(20) Se utiliza esta funcion para arrancar el algoritmo, hay que pasarle por argumento la cantidad de criptos a analizar.
