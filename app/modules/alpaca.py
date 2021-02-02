import os
from alpaca_trade_api.entity import Bar, Order
from alpaca_trade_api.rest import APIError
import requests
import alpaca_trade_api as tradeapi

class AlpacaLib:
    def __init__(self,endpoint,keyid,secret) -> None:
        self.alpaca = tradeapi.REST(key_id=keyid,secret_key=secret,base_url=endpoint)
        self.endpoint = endpoint
        self.keyid = keyid
        self.secret = secret
    
    def __create_header(self) -> dict:
        header ={
            "APCA-API-KEY-ID": self.keyid,
            "APCA-API-SECRET-KEY": self.secret
        }
        return header

    def is_market_open(self) -> bool:
        isOpen = self.alpaca.get_clock().is_open
        if isOpen is True:
            return True
        else:
            return False
        
    def get_stock_bar(self,symbols:list,timeframe:str) -> dict:
        if timeframe not in ['minute','1Min','5Min','15Min','1D']:
            raise Exception("Unexpected Timeframe")
        return self.alpaca.get_barset(symbols,timeframe=timeframe)
    
    def get_stock_price(self,symbol:str) -> float:
        apidata = self.alpaca.get_last_trade(symbol=symbol)
        return apidata.price

    def buy_position(self,symbol:str,amount_to_buy:int):
        position = self.alpaca.submit_order(
            symbol=symbol,
            qty=amount_to_buy,
            side="buy",
            type="market",
            time_in_force="ioc"
        )
        return position

    def sell_position(self,symbol:str,qty:int) -> None:
        header = self.__create_header()
        query = {"qty": int(qty)}
        r = requests.delete(
            url=f"{self.endpoint}/v2/positions/{symbol}",
            params=query,
            headers=header
        )
        return r.json()

    def get_position_by_symbol(self,symbol:str):
        try:
            return self.alpaca.get_position(symbol=symbol)
        except APIError as e:
            if e.status_code == 404:
                return None
            else:
                return "ERROR"
        
    def get_list_of_orders(self,status:str) -> Order:
        if status not in ["open","closed","all"]:
            return None
        try:
            return self.alpaca.list_orders(status=status)
        except APIError as e:
            return None

    def get_order_by_order_id(self,orderid:str) -> Order:
        try:
            return self.alpaca.get_order_by_client_order_id(client_order_id=orderid)
        except APIError as e:
            return None
    
    def get_account_cash(self) -> float:
        try:
            account = self.alpaca.get_account()
            return float(account.cash)
        except Exception as e:
            return e

    

        