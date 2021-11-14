import settings
import os
import numpy as np
import pandas as pd
import random
from pprint import pprint
from itertools import tee
from timeit import default_timer as timer

# Importo variables preseteadas

cripto = settings.cripto
fuente = settings.fuente
n = settings.escenarios
dt = settings.intervalo_tiempo
bots = settings.bots
inicio = settings.fecha_inicio
metodo = settings.metodo
desplazamiento = settings.desplazamiento

## PRUEBA - BORRAR
def ejecutar(escenario, bot, cripto):
    print(f"------Simulacion1 con: {bot}---------")
    contador = 0
    for i in escenario:
        if contador <5:
            contador += 1
            print(i["date"])

def ejecutar2(escenario, bot, cripto):
    print(f"------Simulacion2 con: {bot}---------")
    contador = 0
    for index, row in escenario.iterrows():
        if contador <5:
            contador += 1
            print(row["date"])

def ejecutar2(escenario, bot, cripto):
    print(f"------Simulacion2 con: {bot}---------")
    contador = 0
    for index, row in escenario.iterrows():
        if contador <5:
            contador += 1
            print(row["date"])

def ejecutar3(escenario, bot, cripto):
    print(f"------Simulacion2 con: {bot}---------")
    contador = 0
    for i in escenario.itertuples():
        if contador <5:
            contador += 1
            print(i[1])

def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    ## Creo un dataframe del archivo fuente y lo acoto segun metodo de simulacion
    df = pd.read_csv(fuente)
    df = df.loc[::-1].reset_index(drop=True)
    sub_df = df.copy()
    registros = n * dt * 24 * 60 if metodo == "cascada" else dt * 24 * 60
    sub_df.drop(df.tail(registros).index, inplace = True)
    ultimo = len(sub_df.index)-2
    comienzo = random.randint(1, ultimo) if inicio == False or metodo == "spot" else df.index[df["date"] == inicio][0]
    escenarios_df = []
    rango_fechas = []

    ## Creo dataframes de los distintos escenarios
    for i in range(n):
        if metodo == "spot":
            final = comienzo + registros
        elif metodo == "cascada":
            final = comienzo + registros/(n-i)
        elif metodo == "desplazamiento":
            comienzo += desplazamiento * 24 * 60 if i > 0 else 0
            final = comienzo + registros    
        
        escenario_df = df.loc[comienzo:final]
        escenarios_df.append(escenario_df)

        # Comprobacion de rango de fechas
        fecha_comienzo = df["date"][comienzo]
        fecha_final = df["date"][final]
        #print(i+1, fecha_comienzo, fecha_final)
    
    #print(escenarios_df[-1])

    ## Creacion de iterables

    def generarIterador(df):
        for i in range(len(df)):
            yield df.iloc[i]

    # iterable de iterables
    ''' 
    #escenarios_it = []
    escenarios_it = map(generarIterador, escenarios_df)
    #print(escenarios_it)
    for i in escenarios_it:
        print(i)
    '''

    # Lista de iterables
    '''
    escenarios_it = []
    for i in escenarios_df:
        escenarios_it.append(generarIterador(i))

    pprint(escenarios_it)
    '''

    ## Ejecución de los bots
    
    start = timer()
    for i in escenarios_df:
        for j in bots:
            escenario = generarIterador(i)
            ejecutar(escenario,j,cripto)
            #print(f'ejecutor en escenario {escenarios_it.index(i)}, {j}')
    
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando iteradores: ", time)
    
    '''
    start = timer()
    for i in escenarios_df:
        for j in bots:
            ejecutar2(i,j,cripto)
            #print(f'ejecutor en escenario {escenarios_it.index(i)}, {j}')
    
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y iterrows: ", time)
    '''
    '''
    start = timer()
    for i in escenarios_df:
        for j in bots:
            ejecutar3(i,j,cripto)
            #print(f'ejecutor en escenario {escenarios_it.index(i)}, {j}')
    
    
    stop = timer()
    time = stop-start
    print("Tiempo estimado generando dataframe y itertuples: ", time)
    '''

    return print("Simulacion finalizada exitosamente =)")
simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots)
