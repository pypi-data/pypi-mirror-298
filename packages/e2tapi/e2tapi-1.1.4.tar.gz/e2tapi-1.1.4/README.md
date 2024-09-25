# API de Python para Market Data y Order Routing

## Descripción

Esta API de Python permite:

- Obtener información de Market Data de IBKR y BYMA.
- Enviar, remplazar y/o cancelar órdenes al mercado para IBKR y BYMA.

La API está diseñada para ser rápida, eficiente y fácil de usar, utilizando Google Protocol Buffers para la
comunicación.


## Instalación

Instalar las dependencias:

```bash
pip install e2tapi
```

## Uso

## Market Data

### BYMA

En el siguiente ejemplo, un código simple se conecta a E2T a través de su API e2tapi. El código envía una solicitud de datos de mercado y muestra la información recibida en pantalla:

```bash
from e2t.mktdata.E2T_MDG_BYMA import E2T_MDG_BYMA
import sys

class MyMktDataByma(E2T_MDG_BYMA):
    def __init__(self):
        super().__init__()

    def snapshot(self, message):
        print(message)

    def bid(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def offer(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def last(self, securityID, type, date, time, lastPx, lastQty, buyer, seller):
        print(securityID, type, date, time, lastPx, lastQty, buyer, seller)

    def open(self, securityID, type, value):
        print(securityID, type, value)

    def close(self, securityID, type, value):
        print(securityID, type, value)

    def high(self, securityID, type, value):
        print(securityID, type, value)

    def low(self, securityID, type, value):
        print(securityID, type, value)

    def imbalance(self, securityID, type, value):
        print(securityID, type, value)

    def volume(self, securityID, type, value):
        print(securityID, type, value)

    def amount(self, securityID, type, value):
        print(securityID, type, value)

    def staticRefPx(self, securityID, type, value):
        print(securityID, type, value)

    def prevClose(self, securityID, type, value):
        print(securityID, type, value)

    def turnover(self, securityID, type, value):
        print(securityID, type, value)

    def totalTrades(self, securityID, type, value):
        print(securityID, type, value)

    def lowLmtPx(self, securityID, type, value):
        print(securityID, type, value)

    def highLmtPx(self, securityID, type, value):
        print(securityID, type, value)

    def bid2(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def offer2(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def bid3(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def offer3(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def bid4(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def offer4(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def bid5(self, securityID, type, px, qty):
        print(securityID, type, px, qty)

    def offer5(self, securityID, type, px, qty):
        print(securityID, type, px, qty)


def main():
    mktDataByma = MyMktDataByma()
    mktDataByma.connect("127.0.0.1", 2206)
    # Solicitar Market Data
    '''
    mktDataByma.send_mktdata_req( securityID, bid, offer, last, open, close, high, low, imbalance, volume, amount, staticRefPx, prevClose, turnover, totalTrades, LimitPx, bid2, offer2, bid3, offer3, bid4, offer4, bid5, offer5)
    '''
    securityID = 'AAPL-0003-C-CT-ARS'  # Cambiar esto al símbolo deseado
    mktDataByma.send_mktdata_req(securityID, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Saliendo ...')
        sys.exit(0)


if __name__ == "__main__":
    main()
```                              

### IBKR

En el siguiente ejemplo, un código simple se conecta a E2T a través de su API e2tapi. El código envía una solicitud de datos de mercado y muestra la información recibida en pantalla:
```bash
from e2t.mktdata.E2T_MDG_IBKR import E2T_MDG_IBKR
import sys


class MyMktDataIbkr(E2T_MDG_IBKR):
    def __init__(self):
        super().__init__()

    def snapshot(self, message):
        print(message)

    def bid(self, symbol, type, value):
        print(symbol, type, value)

    def bidQty(self, symbol, type, value):
        print(symbol, type, value)

    def offer(self, symbol, type, value):
        print(symbol, type, value)

    def offerQty(self, symbol, type, value):
        print(symbol, type, value)

    def last(self, symbol, type, value):
        print(symbol, type, value)

    def lastQty(self, symbol, type, value):
        print(symbol, type, value)

    def open(self, symbol, type, value):
        print(symbol, type, value)

    def close(self, symbol, type, value):
        print(symbol, type, value)

    def high(self, symbol, type, value):
        print(symbol, type, value)

    def low(self, symbol, type, value):
        print(symbol, type, value)

    def volume(self, symbol, type, value):
        print(symbol, type, value)


def main():
    # Conectar al servidor y enviar una solicitud de market data
    mktdata = MyMktDataIbkr()
    mktdata.connect('127.0.0.1', 8888)

    # Solicitar Market Data
    '''
    mktdata.send_mktdata_req(symbol, bid, offer, last, open, close, high, low, volume)
    '''
    symbol = 'AAPL'  #Cambiar esto al símbolo deseado
    mktdata.send_mktdata_req(symbol, True, True, True, True, True, True, True, True)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Saliendo ...')
        sys.exit(0)


if __name__ == "__main__":
    main()

```

## Order Routing

### BYMA

En el siguiente ejemplo, un código simple se conecta a E2T a través de su API e2tapi. Inicialmente, envía una orden, recibe el Reporte de Ejecución, luego la reemplaza y finalmente, después de un segundo, la cancela:

```bash
import time
from e2t.oms.E2T_OMS_BYMA import E2T_OMS_BYMA


class MyOMSByma(E2T_OMS_BYMA):
    def __init__(self):
        super().__init__()

    def status(self, clOrdID, orderID, quantity, price, live, cumQty, leavesQty, avgPx, lastPx):
        print("\n--- STATUS ---")
        print(f"clOrdID: {clOrdID}")
        print(f"orderID: {orderID}")
        print(f"quantity: {quantity}")
        print(f"price: {price}")
        print(f"live: {live}")
        print(f"cumQty: {cumQty}")
        print(f"leavesQty: {leavesQty}")
        print(f"avgPx: {avgPx}")
        print(f"lastPx: {lastPx}")
        self.clOrdID = clOrdID

    def reject(self, idRef, reason):
        print("\n--- REJECT ---")
        print(f"idRef: {idRef}")
        print(f"reason: {reason}")

    def trade(self, orderId, execId, time, lastQty, lastPx, avgPx, cumQty):
        print("\n--- TRADE ---")
        print(f"orderId: {orderId}")
        print(f"execId: {execId}")
        print(f"time: {time}")
        print(f"lastQty: {lastQty}")
        print(f"lastPx: {lastPx}")
        print(f"avgPx: {avgPx}")
        print(f"cumQty: {cumQty}")


if __name__ == "__main__":
    # Establecer conexión con el OMS

    oms = MyOMSByma()
    oms.connect('127.0.0.1', 2211)

    time.sleep(1)

    # NEW LIMIT ORDER - BUY APPLE 10 @ 100

    '''
    oms.send_limit_order(clOrdId, side, securityID, quantity, price, timeInForce, expireTime, settlType, account,display)
    '''
    oms.send_limit_order('Test123', '1', 'AAPL-0002-C-CT-ARS', 100, 228.45, '0', '', '', '555', 0)

    time.sleep(1)

    # NEW REPLACE ORDER - BUY APPLE 20 @ 150

    '''
    oms.send_limit_replace(clOrdId, origClOrdID, quantity, price, expireTime, account, display)
    '''
    oms.send_limit_replace('Test456', 'Test123', 200, 229.33, '', '555', 0)

    time.sleep(1)

    # NEW CANCEL ORDER - BUY APPLE 20 @ 150

    '''
    oms.send_limit_cancel(clOrdId, origClOrdID)
    '''
    oms.send_limit_cancel('Test789', 'Test456')

    time.sleep(1)
```
### IBKR

En el siguiente ejemplo, un código simple se conecta a E2T a través de su API e2tapi. Inicialmente, envía una orden, recibe el Reporte de Ejecución, luego la reemplaza y finalmente, después de un segundo, la cancela:
```bash
import time
from e2t.oms.E2T_OMS_IBKR import E2T_OMS_IBKR


class MyOMSByma(E2T_OMS_IBKR):
    def __init__(self):
        super().__init__()

    def status(self, requestId, orderId, live, cumQty, leavesQty, avgPx, lastPx):
        print("\n--- STATUS ---")
        print(f"requestId: {requestId}")
        print(f"orderId: {orderId}")
        print(f"live: {live}")
        print(f"cumQty: {cumQty}")
        print(f"leavesQty: {leavesQty}")
        print(f"avgPx: {avgPx}")
        print(f"lastPx: {lastPx}")
        self.order_id = orderId

    def reject(self, idRef, reason):
        print("\n--- REJECT ---")
        print(f"idRef: {idRef}")
        print(f"reason: {reason}")

    def trade(self, orderId, execId, time, lastQty, lastPx, avgPx, cumQty):
        print("\n--- TRADE ---")
        print(f"orderId: {orderId}")
        print(f"execId: {execId}")
        print(f"time: {time}")
        print(f"lastQty: {lastQty}")
        print(f"lastPx: {lastPx}")
        print(f"avgPx: {avgPx}")
        print(f"cumQty: {cumQty}")


if __name__ == "__main__":
    # Establecer conexión con el OMS

    oms = MyOMSByma()
    oms.connect('127.0.0.1', 8888)

    time.sleep(1)

    # NEW LIMIT ORDER - BUY APPLE 10 @ 100

    '''
    oms.send_limit_order(side, symbol, quantity, price)
    '''
    oms.send_limit_order('BUY', 'AAPL', 10, 100)

    time.sleep(1)

    # NEW REPLACE ORDER - BUY APPLE 20 @ 150

    '''
    oms.send_limit_replace(order_id, quantity, price)
    '''
    oms.send_limit_replace(oms.order_id, 20, 150)

    time.sleep(1)

    # NEW CANCEL ORDER - BUY APPLE 20 @ 150

    '''
    oms.send_limit_cancel(order_id)
    '''
    oms.send_limit_cancel(oms.order_id)

    time.sleep(1)
```

## Licencia

Derechos de autor (c) [2024] [Event2trading]

Todos los derechos reservados.

Se concede permiso a cualquier persona que obtenga una copia de este software y de la documentación asociada a utilizar el software sin restricciones, incluido el derecho a utilizar, copiar, modificar y fusionar el software, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del software.

El software se proporciona "tal cual", sin garantía de ningún tipo, expresa o implícita, incluidas, entre otras, las garantías de comerciabilidad, idoneidad para un propósito particular y no infracción. En ningún caso los autores o titulares de derechos de autor serán responsables de ningún reclamo, daño o responsabilidad, ya sea en una acción de contrato, agravio o de otro tipo, que surja de, fuera de o en relación con el software o el uso u otros tratos en el software.
