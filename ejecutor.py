import os
import numpy as np
import pandas as pd
import random
from pprint import pprint
from timeit import default_timer as timer
import shutil
import exchange
#import analizador
import criterios

## -------------- PARAMETROS QUE LLEGARIAN DESDE SIMULADOR.PY: ---------------
bot = "bot1"
cripto = "BTC"
monto_inicial = 1000

## Armo Dataframe del archivo fuente
df = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/historial-BTC.csv")
df = df.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe

## Armo manualmente el periodo de estudio
df = df.loc[1:60] # Acoto a una hora
#df = df.loc[1:1440] # Acoto a un dia
#df = df.loc[1:10080] # Acoto a una semana
#df = df.loc[1:43200] # Acoto a un mes
#df = df.loc[1:525960] # Acoto a un año            
#df = df['date'].to_frame().head(10) # Algunos registros para prueba

periodo = df['date'].to_numpy().tolist()
inicio = periodo[0]
fin = periodo[-1]


# QUITAR - ES DE PRUEBA (SIMULA EL ANALIZADOR)
def analizador(indicadores, criteriosBot):
    lista = ["comprar", "vender", "holdear"]
    return lista[random.randint(0, 1)]

## ----------------------------------------------------------------------------

def ejecutar(periodo, bot, cripto, monto_inicial):
    
    ## Genero Dataframe desde el CSV de indicadores
    df_indicadores = pd.read_csv("C:/Users/SUSTENTATOR SA/Desktop/Documentos/Programacion/Curso Python UNSAM/Proyecto final - Bot trading/Repo Github/TradeingBot/indicadores - original.csv")
    df = df_indicadores.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe

    ## Aca transformo el csv para igualar formato de fecha del archivo historial y el de indicadores de Jacks
    df['date'] = pd.to_datetime(df.date)
    df['date'] = df['date'].dt.strftime('%d/%m/%Y %H:%M') 

    # Filtro entre las 2 fechas del periodo a ciclar, para no trabajar con un dataframe enorme
    df = df[df['date'].between(inicio, fin)]  
    df = df.set_index('date')
    
    ## Sumo nuevas columnas a ese Dataframe
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    
    ## Creo una billetera para la cripto en cuestion, e ingreso el monto inicial
    cex = exchange.Exchange("billetera", cripto)
    cex.crearBilletera() 
    fecha_inicial = periodo[0]   
    cex.ingresar("USDT", monto_inicial, fecha_inicial)
        
    ## Obtengo el diccionario con los criterios del bot
    criterioBot = criterios.bots[bot]
        
    ## Ciclo fecha por fecha
    for i in periodo:
        ## METER ACA LOGICA DE ENTRADA (SI CORRESPONDE) --> Primera compra de BTC estrategica
        
        ## Llamo a la funcion analizador pasandole una fila del df y un diccionario con los criterios del bot
        df_fila = df.loc[[i]]                            
        criterio = analizador(i, bot)
        #criterio = analizador.analizador(df_fila, criterioBot)
        print("criterio: ", criterio)
        df.at[i, 'criterio'] = criterio
        
        ## Con el valor del criterio y la disponibilidad en billetera: compro, vendo o holdeo
        
        if criterio != "holdear":
            tenencia_usdt = cex.tenencia("USDT")
            #print("usdt: ", tenencia_usdt)
            tenencia_cripto = cex.tenencia(cripto)
            #print("btc: ", tenencia_cripto)
            precio = df['close'][i]
            
            if criterio == "comprar" and tenencia_usdt > 0:
                monto_usdt = tenencia_usdt # Construir logica de fraccionado
                cex.comprar(cripto, monto_usdt, precio, i)
                df.at[i, 'transaccion'] = "compra"
                df.at[i, 'monto'] = monto_usdt
                
            if criterio == "vender" and tenencia_cripto > 0:
                "Entré"
                monto_cripto = tenencia_cripto # Construir logica de fraccionado
                cex.vender(cripto, monto_cripto, precio, i)
                df.at[i, 'transaccion'] = "venta"  
                df.at[i, 'monto'] = monto_cripto
                      
        else:
            df.at[i, 'transaccion'] = "NA"
    
    ## Guardo Dataframe en un csv
    nombre_historia = f'historia-{bot}.csv'
    df.to_csv(nombre_historia)
    
    ## Creo carpeta de la ejecucion y llevo todos los CSVs allí    
    carpeta = f'ejecucion-{bot}'
    os.mkdir(carpeta)
    
    raiz = os.path.dirname(os.path.realpath(__file__))       
    historia = f'historia-{bot}.csv' # corregir esta parte, no deberia estar hardcodeado
    transacciones = f'Transacciones-{cripto}.csv'
    billetera = f'billetera.csv'
    
    csvs = [historia, transacciones, billetera]
    for csv in csvs:
        shutil.move(os.path.join(raiz,csv), os.path.join(raiz,carpeta,csv))
    
    # Al principio de todo deberia estar la logica que borre la carpeta ejecucion-bot 
    # (Para permitirle ejecutar el archivo sin borrar antes a mano la carpeta)
    
    return print("¡ Ejecucion finalizada !")
    
if __name__=="__main__":
    start = timer()
    ejecutar(periodo, bot, cripto, monto_inicial)
    stop = timer()
    time = stop-start
    print("Tiempo en recorrer: ", time)