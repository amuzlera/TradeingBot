import os

## Cripto con la que vamos a trabajar
cripto = "BTC"

## Fuente de la base de datos principal (Historial de valores para x cripto)
fuente = f'{os.path.dirname(os.path.realpath(__file__))}\historial-{cripto}.csv'

## Cantidad de escenarios en los que vamos a correr la simulación (Cant. de intervalos de tiempo)
escenarios = 5

## Longitud del intervalo de tiempo (En dias)
intervalo_tiempo = 30

## Fecha de inicio preseteada (Pasar String o False)
fecha_inicio = "01/01/2021 00:00"
#fecha_inicio = False

## Tipo de selección de intervalos 
    #   --> Spot: intervalos independientes
    #   --> cascada: intervalos en aumento desde fecha inicio
    #   --> Desplazamiento: Intervalo que se desplaza un delta T por vez
#metodo = "spot"
#metodo = "cascada"
metodo = "desplazamiento"

## Desplazamiento en dias (Siempre activo, solo hace efecto en el metodo desplazamiento)
desplazamiento = 7


## Lista de bots que participan en la simulacion
bots = [
    "bot1",
    "bot2",
    "bot3",
    "bot4",
    "bot5",
]
