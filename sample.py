# from config import Credentials
# from collections import namedtuple
from kiteext import KiteExt
from requests import get
from json import loads
from datetime import datetime, date, timedelta
from pandas import DataFrame

class Functions:
    def __init__(self):
        """Fetch SQL credentials"""
        # db_userid   = Credentials.dbuserid.value
        # db_pass     = Credentials.dbpass.value
        # db_host     = Credentials.host.value
        # db_name     = Credentials.database.value
        
        # self.db_userid = db_userid
        # self.db_pass = db_pass
        # self.db_host = db_host
        # self.db_name = db_name
        
        # """Fetch Aliceblue credentials"""
        # user_name   = Credentials.username.value
        # pass_word   = Credentials.password.value
        # two_fa      = Credentials.twofa.value
        # secret_key  = Credentials.secretkey.value
        
        # self.user_name = user_name
        # self.pass_word = pass_word
        # self.two_fa = two_fa
        # self.secret_key = secret_key

        # """Contracts to download from AliceBlue"""
        # use_contracts = ['NFO', 'NSE', 'CDS', 'MCX']
        # self.use_contracts = use_contracts
        
        # """Accounts mapping"""
        # pseudo_id_5min = Credentials.pseudo_accounts_5min.value
        # self.pseudo_id_5min = pseudo_id_5min

        # """Named Tuple for candle"""
        # Candle = namedtuple('Candle', ['open', 'high', 'low', 'close', 'volume'])
        # self.Candle = Candle
        
        """Zerodha"""
        user = loads(open('userzerodha.json', 'r').read().rstrip())
        self.user = user

    def zerodhaObject(self):
        kite = KiteExt()
        self.kite = kite
        return kite
        
    def loginZerodha(self):
        self.kite.login_with_credentials(userid=self.user['user_id'], password=self.user['password'], twofa=self.user['twofa'])
    
    def readZerodhaAccessToken(self):
        enctoken = open('enctoken.txt', 'r').read().rstrip()
        self.enctoken = enctoken
        self.kite = self.zerodhaObject()
        self.kite.set_headers(enctoken)
        
    def kiteInstruments(self, NSE):
        return DataFrame(self.kite.instruments(exchange=NSE), index=None)
    
    def historical_data(self, token, from_date, end_date, interval, cntinuous = False,  getoival = False):
        return DataFrame(self.kite.historical_data(token, from_date, end_date, interval, continuous = cntinuous,  oi = getoival))
    
    def ltp(self, exchg, symbol):
        zscript = f"{exchg}:{symbol}"
        #print(zscript)
        return self.kite.ltp(zscript)

    def ohlc(self,stock):
        # stock=f'NSE:{stock}'
        return self.kite.ohlc(stock)

    def buyorder(self,instrument,quantity):
        return self.kite.place_order(transaction_type=self.kite.TRANSACTION_TYPE_BUY, 
                                 tradingsymbol=instrument,
                                 quantity=quantity, 
                                 product=self.kite.PRODUCT_MIS, 
                                 order_type=self.kite.ORDER_TYPE_MARKET,
                                 variety=self.kite.VARIETY_AMO,
                                 exchange=self.kite.EXCHANGE_NSE)

    def sellorder(self,instrument,quantity):
        return self.kite.place_order(transaction_type=self.kite.TRANSACTION_TYPE_SELL, 
                                 tradingsymbol=instrument,
                                 quantity=quantity, 
                                 product=self.kite.PRODUCT_MIS, 
                                 order_type=self.kite.ORDER_TYPE_MARKET,
                                 variety=self.kite.VARIETY_AMO,
                                 exchange=self.kite.EXCHANGE_NSE)