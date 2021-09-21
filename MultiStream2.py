import asyncio
from datetime import datetime
from sys import path
from threading import Thread
import websockets
from typing import Tuple, List, Iterable
import json
import pandas as pd
import re
import os

URLS = [
    "wss://stream.binance.com:9443/ws/xrpusdt@kline_1m",
    "wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
    "wss://stream.binance.com:9443/ws/ltcusdt@kline_1m",
    "wss://stream.binance.com:9443/ws/bchusdt@kline_1m",
    "wss://stream.binance.com:9443/ws/ethusdt@kline_1m",
    ]

async def SuscripcionIndividual(url: str):
    """Se crea una suscripcion individual a cada WebSocket"""
    async with websockets.connect(url) as websocket:
        data = await websocket.recv()
        data = json.loads(data)

        lista = []
        data = await websocket.recv()
        datos = json.loads(data)
        print('\n', datos)

        vela = datos['k']
        tiempo_cierre = vela['T']

        open = vela['o']
        close = vela['c']
        high = vela['h']
        low = vela['l']
        volumen = vela['v']

        temporal = [tiempo_cierre, open, close, high,low, volumen]
        lista.append(temporal)
        info = pd.DataFrame(lista, columns = ["closeTime", "open", "close", "high", "low", "volume"])

        re_match = re.match(r".*?ws/(.*)@.*",url)
        nombre = re_match.group(1)
        path = "velas"
        absolutepath = os.path.abspath(__file__)
        fileDirectory = os.path.dirname(absolutepath)
        newPath = os.path.join(fileDirectory,path)
        info.to_csv(os.path.join(newPath,f"{nombre}.csv"))

async def Suscripciones(URLS: Iterable[str]) -> List[Tuple[str, int]]:
    """Se suscriben todos los tickets de concurrente y se combinan todos
        en una sola corrutina."""
    while True:
        tareas = [asyncio.create_task(SuscripcionIndividual(url)) for url in URLS]

        # Se corren todas las tareas en paralelo
        await asyncio.gather(*tareas)
        #return tareas

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Suscripciones(URLS))
