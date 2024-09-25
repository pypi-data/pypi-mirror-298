import socket
import threading
import random
import string
from google.protobuf.message import DecodeError
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
from abc import abstractmethod

from e2t.oms import BYMA_Messages_pb2 as pb


class E2T_OMS_BYMA:

    @abstractmethod
    def status(self, clOrdID, orderID, quantity, price, live, cumQty, leavesQty, avgPx, lastPx):
        pass

    @abstractmethod
    def reject(self, idRef, reason):
        pass

    @abstractmethod
    def trade(self, orderId, execId, time, lastQty, lastPx, avgPx, cumQty):
        pass

    def connect(self, HOST, PORT):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}...")
            self.send_token_req("666", 'clientID')
        except socket.error as e:
            print(f"Error connecting to {HOST}:{PORT}: {e}")
            return

        def handle_client():
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        print("Connection closed by server")
                        break
                    message = pb.Message()
                    size, new_pos = _DecodeVarint32(data, 0)
                    message.ParseFromString(data[new_pos:new_pos + size])

                    if message.messageType == pb.MessageType.ORDER_STATUS:
                        self.status(
                            message.orderStatus.clOrdID,
                            message.orderStatus.orderID,
                            message.orderStatus.quantity,
                            message.orderStatus.price,
                            message.orderStatus.live,
                            message.orderStatus.cumQty,
                            message.orderStatus.leavesQty,
                            message.orderStatus.avgPx,
                            message.orderStatus.lastPx
                        )
                    elif message.messageType == pb.MessageType.TRADE_ORDER:
                        self.trade(
                            message.tradeOrder.orderID,
                            message.tradeOrder.execID,
                            message.tradeOrder.time,
                            message.tradeOrder.lastQty,
                            message.tradeOrder.lastPx,
                            message.tradeOrder.avgPx,
                            message.tradeOrder.cumQty
                        )
                    elif message.messageType == pb.MessageType.REJECT:
                        self.reject(
                            message.reject.idRef,
                            message.reject.reason
                        )
                    elif message.messageType == pb.MessageType.TOKEN_RESPONSE:
                        self.token = message.tokenResponse.token
                    else:
                        print(f"Unknown message type: {message.messageType}")
                except DecodeError as e:
                    print(f"Error decoding message: {e}")
                    continue
                except Exception as e:
                    print(f"Error handling message: {e}")

        threading.Thread(target=handle_client, daemon=True).start()

    def send_order(self, order_buffer):
        try:
            if self.client:
                size = len(order_buffer)
                self.client.sendall(_VarintBytes(size) + order_buffer)
            else:
                print("Error: Client not available")
        except socket.error as e:
            print(f"Error sending order: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def send_token_req(self, clientID, busID):
        try:
            token_request = pb.TokenRequest(
                clientID=str(clientID),
                busID=busID
            )
            message = pb.Message(
                messageType=pb.MessageType.TOKEN_REQUEST,
                tokenRequest=token_request
            )
            buffer = message.SerializeToString()
            self.send_order(buffer)
        except Exception as e:
            print(f"Error creating token request: {e}")

    def send_limit_order(self, clOrdID, side, securityID, quantity, price, timeInForce, expireTime, settlType, account,
                         display):
        try:
            limit_order = pb.LimitOrder(
                token=self.token,
                clOrdID=clOrdID,
                side=side,
                securityID=securityID,
                quantity=quantity,
                price=price,
                timeInForce=timeInForce,
                expireTime=expireTime,
                settlType=settlType,
                account=account,
                display=display
            )
            message = pb.Message(
                messageType=pb.MessageType.LIMIT_ORDER,
                limitOrder=limit_order
            )
            buffer = message.SerializeToString()
            self.send_order(buffer)
        except Exception as e:
            print(f"Error creating limit order: {e}")

    def send_limit_replace(self, clOrdID, origClOrdID, quantity, price, expireTime, account, display):
        try:
            limit_replace = pb.LimitReplace(
                token=self.token,
                clOrdID=clOrdID,
                origClOrdID=origClOrdID,
                quantity=quantity,
                price=price,
                expireTime=expireTime,
                account=account,
                display=display
            )
            message = pb.Message(
                messageType=pb.MessageType.LIMIT_REPLACE,
                limitReplace=limit_replace
            )
            buffer = message.SerializeToString()
            self.send_order(buffer)
        except Exception as e:
            print(f"Error creating limit replace: {e}")

    def send_limit_cancel(self, clOrdID, origClOrdID):
        try:
            limit_cancel = pb.LimitCancel(
                token=self.token,
                clOrdID=clOrdID,
                origClOrdID=origClOrdID
            )
            message = pb.Message(
                messageType=pb.MessageType.LIMIT_CANCEL,
                limitCancel=limit_cancel
            )
            buffer = message.SerializeToString()
            self.send_order(buffer)
        except Exception as e:
            print(f"Error creating limit cancel: {e}")
