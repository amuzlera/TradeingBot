import os
import pandas as pd
from timeit import default_timer as timer
import shutil
import exchange
import analizador
import criterios
import graficar
import indicadores
## -------------- PARAMETROS QUE LLEGARIAN DESDE SIMULADOR.PY: ---------------

'''
## Armo Dataframe del archivo fuente
archivo = 'historial-BTC.csv'
fname = os.path.join(archivo)
df = pd.read_csv(fname)
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
'''
## ----------------------------------------------------------------------------

def ejecutar(bot, cripto, monto_inicial):
    
    ## Obtengo el diccionario con los criterios del bot
    criterioBot = criterios.bots[bot]
    # Obtengo los parametros necesarios para calcular indicadores, a partir 
    # de los criterios del bot
    rsi = criterioBot["RSI"][0]   
    ma = criterioBot["maCross"]
    bBand = criterioBot["bBands"]
    
    ## Genero el CSV donde luego se consultaran los indicadores y valores de mercado
    indicadores.getIndicadores(inicio='2021-01-01 00:00:00', fin='2021-12-31 00:00:00', rsi=rsi, ma=ma, bBand=bBand)
    ## Genero Dataframe desde el CSV de indicadores
    archivo = 'indicadores.csv'
    fname = os.path.join(archivo)
    df_indicadores = pd.read_csv(fname)
    df = df_indicadores.loc[::-1].reset_index(drop=True) # Doy vuelta el dataframe

    ## Aca transformo el csv para igualar formato de fecha del archivo historial y el de indicadores de Jacks
    df['date'] = pd.to_datetime(df.date)
    #df['date'] = df['date'].dt.strftime('%d/%m/%Y %H:%M')   # cambiar a este formato '%Y/%m/%d %H:%M'
                                        

    # Filtro entre las 2 fechas del periodo a ciclar, para no trabajar con un dataframe enorme
    #df = df[df['date'].between(inicio, fin)]  
    #df = df.iloc[1:periodo] # Acoto a una hora
    df = df.set_index('date')
    periodo = df.index
    
    ## Sumo nuevas columnas a ese Dataframe  (Esto podria no estar)
    df["criterio"] = ""
    df["transaccion"] = ""
    df["monto"] = ""
    
    ## Creo una billetera para la cripto en cuestion, e ingreso el monto inicial
    cex = exchange.Exchange("billetera", cripto)
    cex.crearBilletera() 
    fecha_inicial = periodo[0]   
    cex.ingresar("USDT", monto_inicial, fecha_inicial)
        
   
        
    ## Ciclo fecha por fecha
    for i in periodo:
        ## METER ACA LOGICA DE ENTRADA (SI CORRESPONDE) --> Primera compra de BTC estrategica
        
        ## Llamo a la funcion analizador pasandole una fila del df y un diccionario con los criterios del bot
        df_fila = df.loc[[i]]                            
        #criterio = analizador(i, bot)
        criterio = analizador.analizador(df_fila, criterioBot)
        #print("criterio: ", criterio)
        df.at[i, 'criterio'] = criterio
        
        ## Con el valor del criterio y la disponibilidad en billetera: compro, vendo o holdeo
        
        if criterio != "Holdear":
            tenencia_usdt = cex.tenencia("USDT")
            #print("usdt: ", tenencia_usdt)
            tenencia_cripto = cex.tenencia(cripto)
            #print("btc: ", tenencia_cripto)
            precio = df['close'][i]
            
            if criterio == "Comprar" and tenencia_usdt > 0:
                monto_usdt = tenencia_usdt # Construir logica de fraccionado
                cex.comprar(cripto, monto_usdt, precio, i)
                df.at[i, 'transaccion'] = "compra"
                df.at[i, 'monto'] = monto_usdt
                
            if criterio == "Vender" and tenencia_cripto > 0:
                "Entré"
                monto_cripto = tenencia_cripto # Construir logica de fraccionado
                cex.vender(cripto, monto_cripto, precio, i)
                df.at[i, 'transaccion'] = "venta"  
                df.at[i, 'monto'] = monto_cripto
                      
        else:
            df.at[i, 'transaccion'] = "NA"
    
    ## Guardo Dataframe en un csv
    nombre_historia = f'historia-{bot}.csv'
    df = df.iloc[::-1]
    #df.index = pd.to_datetime(df.index)
    #df.index = df.index.strftime('%Y/%m/%d %H:%M')
    # aqui hacer cambio de formato a '%Y/%m/%d %H:%M'
    df.to_csv(nombre_historia)
    
    ## Creo carpeta de la ejecucion y llevo todos los CSVs allí    
    try:    
        carpeta = f'ejecucion-{bot}'
        os.mkdir(carpeta)
    except:
        pass
    raiz = os.path.dirname(os.path.realpath(__file__))       
    historia = f'historia-{bot}.csv' # corregir esta parte, no deberia estar hardcodeado
    transacciones = f'Transacciones-{cripto}.csv'
    billetera = f'billetera.csv'
    
    csvs = [historia, transacciones, billetera]
    for csv in csvs:
        shutil.move(os.path.join(raiz,csv), os.path.join(raiz,carpeta,csv))
    
    # Al principio de todo deberia estar la logica que borre la carpeta ejecucion-bot 
    # (Para permitirle ejecutar el archivo sin borrar antes a mano la carpeta)
    print("¡ Ejecucion finalizada !")
    
    
if __name__=="__main__":
    bot = "bot1"
    cripto = "BTC"
    monto_inicial = 1000
    
    start = timer()
    ejecutar(bot, cripto, monto_inicial)
    stop = timer()
    time = stop-start
    print("Tiempo en recorrer: ", time)
    
    criterioBot = criterios.bots[bot]
    archivo = f'ejecucion-{bot}/historia-{bot}.csv'
    fname = os.path.join(archivo)
    graficar.candlestickGraph(fname, ["RSI", criterioBot["RSI"][1], criterioBot["RSI"][2] ], f'ejecucion-{bot}/billetera.csv', "bBands")
    
    
    
    
    
    
    
    