import settings
import os
import numpy as np
import pandas as pd
import random
from pprint import pprint

# Importo variables preseteadas

cripto = settings.cripto
fuente = settings.fuente
n = settings.escenarios
dt = settings.intervalo_tiempo
bots = settings.bots
inicio = settings.fecha_inicio
metodo = settings.metodo
desplazamiento = settings.desplazamiento

def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots):
    '''
    Recibe parametros de simulacion definidos en setting.py
    Genera escenarios de simulación y corre los ejecutores en cada uno
    Devuelve resultados en respectivos CSV
    '''
    # Creacion de escenarios
    df = pd.read_csv(fuente)
    df = df.loc[::-1].reset_index(drop=True)
    sub_df = df.copy()
    registros = n * dt * 24 * 60 if metodo == "cascada" else dt * 24 * 60
    sub_df.drop(df.tail(registros).index, inplace = True)
    ultimo = len(sub_df.index)-2
    escenarios = []
    comienzo = random.randint(1, ultimo) if inicio == False or metodo == "spot" else df.index[df["date"] == inicio][0]
    
    for i in range(n):
        if metodo == "spot":
            final = comienzo + registros
        elif metodo == "cascada":
            final = comienzo + registros/(n-i)
        elif metodo == "desplazamiento":
            comienzo += desplazamiento * 24 * 60 if i > 0 else 0
            final = comienzo + registros          
        fecha_comienzo = df["date"][comienzo]
        fecha_final = df["date"][final]
        escenarios.append([fecha_comienzo, fecha_final])

    pprint(escenarios)

    # Ejecución de los bots
    for i in escenarios:
        for j in bots:
            #ejecutor.ejecutar(i,j,cripto)
            print(f'ejecutor en escenario {escenarios.index(i)}, bot{j}')

    return print("Simulacion finalizada exitosamente =)")


simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots)


'''

def simular(cripto, fuente, n, dt, inicio, desplazamiento, metodo, *bots):

    if metodo == "spot":
        # Creacion de escenarios
        df = pd.read_csv(fuente)
        df = df.loc[::-1].reset_index(drop=True)
        registros = dt * 24 * 60
        sub_df = df.copy()
        sub_df.drop(df.tail(registros).index, inplace = True)
        ultimo = len(sub_df.index)-2
        escenarios = []
        #escenarios2 = []
        
        for i in range(n):
            comienzo = random.randint(1, ultimo)
            final = comienzo + registros
            fecha_comienzo = df["date"][comienzo]
            fecha_final = df["date"][final]
            escenarios.append([fecha_comienzo, fecha_final])
            #escenarios2.append([comienzo, final])

        pprint(escenarios)
        #print(escenarios2)

        # Ejecución de los bots
        for i in escenarios:
            for j in bots:
                #ejecutor.ejecutar(i,j,cripto)
                print(f'ejecutor en escenario {escenarios.index(i)}, bot{j}')

    if metodo == "cascada":
        # Creacion de escenarios
        df = pd.read_csv(fuente)
        df = df.loc[::-1].reset_index(drop=True)
        registros = n * dt * 24 * 60
        sub_df = df.copy()
        sub_df.drop(df.tail(registros).index, inplace = True)
        ultimo = len(sub_df.index)-2
        escenarios = []
        comienzo = random.randint(1, ultimo) if inicio == False else df.index[df["date"] == inicio][0]

        for i in range(n):
            final = comienzo + registros/(n-i)
            fecha_comienzo = df["date"][comienzo]
            fecha_final = df["date"][final]
            escenarios.append([fecha_comienzo, fecha_final])

        pprint(escenarios)

        # Ejecución de los bots
        for i in escenarios:
            for j in bots:
                #ejecutor.ejecutar(i,j,cripto)
                print(f'ejecutor en escenario {escenarios.index(i)}, bot{j}')

    if metodo == "desplazamiento":
        # Creacion de escenarios
        df = pd.read_csv(fuente)
        df = df.loc[::-1].reset_index(drop=True)
        registros = dt * 24 * 60
        sub_df = df.copy()
        sub_df.drop(df.tail(registros).index, inplace = True)
        ultimo = len(sub_df.index)-2
        escenarios = []
        desplazamiento = desplazamiento * 24 * 60
        comienzo = random.randint(1, ultimo) if inicio == False else df.index[df["date"] == inicio][0]

        for i in range(n):
            comienzo += desplazamiento
            final = comienzo + registros
            fecha_comienzo = df["date"][comienzo]
            fecha_final = df["date"][final]
            escenarios.append([fecha_comienzo, fecha_final])

        pprint(escenarios)

        # Ejecución de los bots
        for i in escenarios:
            for j in bots:
                #ejecutor.ejecutar(i,j,cripto)
                print(f'ejecutor en escenario {escenarios.index(i)}, bot{j}')


    return print("Simulacion finalizada exitosamente =)")

'''