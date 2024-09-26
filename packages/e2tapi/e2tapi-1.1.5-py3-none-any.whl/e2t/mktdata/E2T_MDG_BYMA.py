import socket
import threading
import random
import string

from google.protobuf.message import DecodeError
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
from abc import abstractmethod

from e2t.mktdata import BYMA_Messages_pb2 as pb


class E2T_MDG_BYMA:

    @abstractmethod
    def snapshot(self, message):
        pass

    @abstractmethod
    def bid(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def offer(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def last(self, securityID, type, date, time, lastPx, lastQty, buyer, seller):
        pass

    @abstractmethod
    def open(self, securityID, type, value):
        pass

    @abstractmethod
    def close(self, securityID, type, value):
        pass

    @abstractmethod
    def high(self, securityID, type, value):
        pass

    @abstractmethod
    def low(self, securityID, type, value):
        pass

    @abstractmethod
    def imbalance(self, securityID, type, value):
        pass

    @abstractmethod
    def volume(self, securityID, type, value):
        pass

    @abstractmethod
    def amount(self, securityID, type, value):
        pass

    @abstractmethod
    def staticRefPx(self, securityID, type, value):
        pass

    @abstractmethod
    def prevClose(self, securityID, type, value):
        pass

    @abstractmethod
    def turnover(self, securityID, type, value):
        pass

    @abstractmethod
    def totalTrades(self, securityID, type, value):
        pass

    @abstractmethod
    def lowLmtPx(self, securityID, type, value):
        pass

    @abstractmethod
    def highLmtPx(self, securityID, type, value):
        pass

    @abstractmethod
    def bid2(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def offer2(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def bid3(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def offer3(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def bid4(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def offer4(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def bid5(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def offer5(self, securityID, type, px, qty):
        pass

    @abstractmethod
    def reject(self, securityID, reason):
        pass

    def connect(self, HOST, PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        print(f"Conectado a {HOST}:{PORT}...")

        def handle_client():
            buffer = b""
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        print("Connection closed by server")
                        break

                    buffer += data

                    while len(buffer) >= 5:
                        try:
                            size, new_pos = _DecodeVarint32(buffer, 0)
                        except IndexError:
                            break

                        if len(buffer) < new_pos + size:
                            break

                        message = pb.Message()
                        message.ParseFromString(buffer[new_pos:new_pos + size])

                        process_message(message)

                        buffer = buffer[new_pos + size:]

                except DecodeError as e:
                    print(f"Error decoding message: {e}")
                    buffer = b""
                    continue
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    continue

        def process_message(message):
            if message.messageType == pb.MessageType.SNAPSHOT:
                self.snapshot(message)
            elif message.messageType == pb.MessageType.BID:
                self.bid(
                    message.bid.securityID,
                    'BID',
                    message.bid.bidPx,
                    message.bid.bidQty
                )
            elif message.messageType == pb.MessageType.OFFER:
                self.offer(
                    message.offer.securityID,
                    'OFFER',
                    message.offer.offerPx,
                    message.offer.offerQty
                )
            elif message.messageType == pb.MessageType.LAST:
                self.last(
                    message.last.securityID,
                    'LAST',
                    message.last.date,
                    message.last.time,
                    message.last.lastPx,
                    message.last.lastQty,
                    message.last.buyer,
                    message.last.seller
                )
            elif message.messageType == pb.MessageType.OPEN:
                self.open(
                    message.open.securityID,
                    'OPEN',
                    message.open.openPx
                )
            elif message.messageType == pb.MessageType.CLOSE:
                self.close(
                    message.close.securityID,
                    'CLOSE',
                    message.close.closePx
                )
            elif message.messageType == pb.MessageType.HIGH:
                self.high(
                    message.high.securityID,
                    'HIGH',
                    message.high.highPx,
                )
            elif message.messageType == pb.MessageType.LOW:
                self.low(
                    message.low.securityID,
                    'LOW',
                    message.low.lowPx
                )
            elif message.messageType == pb.MessageType.IMBALANCE:
                self.imbalance(
                    message.imbalance.securityID,
                    'IMBALANCE',
                    message.imbalance.imbalance
                )
            elif message.messageType == pb.MessageType.VOLUME:
                self.volume(
                    message.volume.securityID,
                    'VOLUME',
                    message.volume.volume
                )
            elif message.messageType == pb.MessageType.AMOUNT:
                self.amount(
                    message.amount.securityID,
                    'AMOUNT',
                    message.amount.amount
                )
            elif message.messageType == pb.MessageType.STATIC_REF_PX:
                self.staticRefPx(
                    message.staticRefPx.securityID,
                    'STATIC_REF_PX',
                    message.staticRefPx.staticRefPx
                )
            elif message.messageType == pb.MessageType.PREV_CLOSE:
                self.prevClose(
                    message.prevClose.securityID,
                    'PREV_CLOSE',
                    message.prevClose.prevClose
                )
            elif message.messageType == pb.MessageType.TURNOVER:
                self.turnover(
                    message.turnover.securityID,
                    'TURNOVER',
                    message.turnover.turnover
                )
            elif message.messageType == pb.MessageType.TOTAL_TRADES:
                self.totalTrades(
                    message.totaltrades.securityID,
                    'TOTAL_TRADES',
                    message.totalTrades.totalTrades
                )
            elif message.messageType == pb.MessageType.LOW_LIMIT_PRICE:
                self.lowLmtPx(
                    message.lowLmtPx.securityID,
                    'LOW_LIMIT_PRICE',
                    message.lowLmtPx.lowLmtPx
                )
            elif message.messageType == pb.MessageType.LIMIT_PRICE:
                self.highLmtPx(
                    message.highLmtPx.securityID,
                    'HIGH_LIMIT_PRICE',
                    message.highLmtPx.highLmtPx
                )
            elif message.messageType == pb.MessageType.BID2:
                self.bid2(
                    message.bid2.securityID,
                    'BID2',
                    message.bid2.bidPx,
                    message.bid2.bidQty
                )
            elif message.messageType == pb.MessageType.OFFER2:
                self.offer2(
                    message.offer2.securityID,
                    'OFFER2',
                    message.offer2.offerPx,
                    message.offer2.offerQty
                )
            elif message.messageType == pb.MessageType.BID3:
                self.bid3(
                    message.bid3.securityID,
                    'BID3',
                    message.bid3.bidPx,
                    message.bid3.bidQty
                )
            elif message.messageType == pb.MessageType.OFFER3:
                self.offer3(
                    message.offer3.securityID,
                    'OFFER3',
                    message.offer3.offerPx,
                    message.offer3.offerQty
                )
            elif message.messageType == pb.MessageType.BID4:
                self.bid4(
                    message.bid4.securityID,
                    'BID4',
                    message.bid4.bidPx,
                    message.bid4.bidQty
                )
            elif message.messageType == pb.MessageType.OFFER4:
                self.offer4(
                    message.offer4.securityID,
                    'OFFER4',
                    message.offer4.offerPx,
                    message.offer4.offerQty
                )
            elif message.messageType == pb.MessageType.BID5:
                self.bid5(
                    message.bid5.securityID,
                    'BID5',
                    message.bid5.bidPx,
                    message.bid5.bidQty
                )
            elif message.messageType == pb.MessageType.OFFER5:
                self.offer5(
                    message.offer5.securityID,
                    'OFFER5',
                    message.offer5.offerPx,
                    message.offer5.offerQty
                )
            elif message.messageType == pb.MessageType.REJECT:
                self.reject(
                    message.Reject.securityID,
                    message.Reject.reason
                )

        threading.Thread(target=handle_client, daemon=True).start()

    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def send_mktdata_req(self, securityID, bid, offer, last, open, close, high, low, imbalance, volume, amount,
                         staticRefPx, prevClose, turnover, totalTrades, LimitPx, bid2, offer2, bid3, offer3, bid4,
                         offer4, bid5, offer5):
        try:
            mkt_req = pb.Request(
                securityID=securityID,
                bid=bid,
                offer=offer,
                last=last,
                open=open,
                close=close,
                high=high,
                low=low,
                imbalance=imbalance,
                volume=volume,
                amount=amount,
                staticRefPx=staticRefPx,
                prevClose=prevClose,
                turnover=turnover,
                totalTrades=totalTrades,
                LimitPx=LimitPx,
                bid2=bid2,
                offer2=offer2,
                bid3=bid3,
                offer3=offer3,
                bid4=bid4,
                offer4=offer4,
                bid5=bid5,
                offer5=offer5
            )

            message = pb.Message(
                messageType=pb.MessageType.REQUEST,
                request=mkt_req
            )
            buffer = message.SerializeToString()
            self.send_mkt_req(buffer)
        except Exception as e:
            print(f"Error creating market data request: {e}")

    def send_mkt_req(self, mkt_req_buffer):
        try:
            if self.client:
                size = len(mkt_req_buffer)
                self.client.sendall(_VarintBytes(size) + mkt_req_buffer)
            else:
                print("Error sending Market Data Request: Not connected to server")
        except socket.error as e:
            print(f"Error sending Market Data Request: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
