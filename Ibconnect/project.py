from ibapi.contract import Contract
from ibapi.order import Order
from ibapi import connection, message
from tkinter import *
from tkinter import ttk
import time
from msvcrt import getch

class Application(Frame):
    
    def __init__(self, master):
        """ Initialize the Frame"""
        ttk.Frame.__init__(self, master)
 
        self.port=7496
        self.client_id=82
        self.grid()
        self.create_widgets()
        self.account_code = None
        self.symbol_id, self.symbol =0, 'AAPL'
        self.order_id = 555
        self.unrealized =0
        self.realized=0
        self.unrealized_pnl=0
        self.realized_pnl=0
        self.marked_pnl=0
        self.my_outsideRTH = False

    def create_widgets(self):
        
        #cadre principal
        MyFont = ('Lucida Grande',12)

        self.btnConnect = ttk.Button(self, text = "Connect", command=self.connect_to_tws)
        self.btnConnect.grid(row=0, column=0)
        self.btnDisconnect = ttk.Button(self, text = "Disconnect", command=self.disconnect_it).grid(row=0, column=1, sticky=W)
        
        #notebook
        n=ttk.Notebook(root, width=550, height=350)
        f1= ttk.Frame(n)
        f2= ttk.Frame(n) 
        n.add(f1, text='One')
        n.add(f2, text='Two')
        n.grid(row=3,column=0,padx=5,pady=5,sticky=W)


        #listbox
        self.listbox1= Listbox(f1, font=('Lucida Grande',9 ), width=7)
        self.listbox1.insert(1,'NFLX')
        self.listbox1.insert(2,'APPL')
        self.listbox1.insert(3,'FB')
        self.listbox1.grid(row=0,rowspan=5,column=0,padx=5)


       #Label Symbol 
        self.label4= Label(f1, font=MyFont, text="Symbol").grid(row=0, column=1)
        self.label5= Label(f1, font=MyFont, text="Quantity").grid(row=0, column=2)
        self.label6= Label(f1, font=MyFont, text="Limit Price").grid(row=0, column=3)
        self.label7= Label(f1, font=MyFont, text="Market").grid(row=0, column=4)

        self.cbsymbol= ttk.Combobox(f1, font=MyFont, width=6, textvariable=varSymbol)
        self.cbsymbol.bind ("<Return>", self.cbSymbol_onEnter)
        self.cbsymbol.bind ('<<ComboboxSelected>>', self.cbSymbol_onEnter)
        self.cbsymbol['values'] = ('APPL', 'FB', 'NFLX')
        self.cbsymbol.grid(row=1, column=1, sticky=W)

        self.spinQuantity = Spinbox(f1, font=MyFont, increment=100, from_=0, to=10000,width=7, textvariable=varQuantity).grid(row=1, column=2)
        self.spinLimitPrice = Spinbox(f1, font=MyFont, format='%8.2f', increment=.01, from_=0.0, to=1000.0, width=7, textvariable=varLimitPrice).grid(row=1, column=3)

        self.cbMarket = ttk.Combobox(f1, font=MyFont, width=7, textvariable=varMarket).grid(row=1, column=4,sticky=W)

        self.label8 = Label(f1, font=MyFont, text="OrderType").grid(row=2, column=1, sticky=W)
        
        self.label9 = Label(f1, font=MyFont, text="Visible").grid(row=2, column=2)
        
        self.label10 = Label(f1, font=MyFont, text="Primary Ex.").grid(row=2, column=3)
        
        self.label11 = Label(f1, font=MyFont, text="TIF").grid(row=2, column=4)
        
        self.cbOrderType= ttk.Combobox (f1, font=MyFont, width=6, textvariable=varOrderType)
        self.cbOrderType['values'] = ('LMT','MKT','STP','STP LMT','TRAIL')
        self.cbOrderType.grid(row=3, column=1, sticky=W)
        
        self.tbPrimaryEx = Entry(f1, font= MyFont, width = 8, textvariable=varPrimaryEx).grid(row=3, column = 3, sticky = W)

        self.cbTIF = ttk.Combobox (f1, font=MyFont, width=6, textvariable=varTIF)
        self.cbTIF['values'] = ('DAY','GTC')
        self.cbTIF.grid(row=3, column = 4, sticky = W)

        self.label2= Label(f1, font=MyFont, text="Bid", width=7).grid(row=4, column=2)
    
        self.label3= Label(f1, font=MyFont, text="Ask", width=7).grid(row=4, column=3)

        self.tbBid = Entry(f1, font=MyFont, width=7,textvariable=varBid)
        self.tbBid.bind("<Button-1>", self.tbBid_Click)
        self.tbBid.grid(row=5,column=2, sticky=E)

        self.tbAsk = Entry(f1, font=MyFont, width=7,textvariable=varAsk)
        self.tbAsk.bind("<Button-1>", self.tbAsk_Click)
        self.tbAsk.grid(row=5,column=3)

        self.btnSell = Button(f1, font=('Lucida Grande',10,'bold'), text = "SELL", width=9, bg="red", fg="white", command=self.sell)
        self.btnSell.grid(row=5,column=1, sticky=W)
    
        self.btnBuy = Button(f1, font=('Lucida Grande',10,'bold'), text = "BUY", width=9, bg="green", fg="white", command=self.buy)
        self.btnBuy.grid(row=5,column=4, sticky=E)
    
        self.label1= Label(f1, font=MyFont,width=8, text="Last").grid(row=6,column=1)
    
        self.tbLast = Entry (f1, font = MyFont, width = 8, textvariable= varLast)
        self.tbLast.bind ("<Button-1>", self.tbLast_Click)
        self.tbLast.grid(row=6, column =2, sticky = W)

        self.btnCancelAll = Button(f1, font=('Lucida Grande',10,'bold'), text = "Cancell All", width=8, bg="blue", fg="white", command=self.cancel_all)
        self.btnCancelAll.grid(row=7,column=2)

        self.label22 = Label(f1, font=MyFont, text="Avg Price", width=8)
        self.label22.grid(row=6, column=3)
        
        self.label23 = Label(f1, font=MyFont, text="Position", width=8)
        self.label23.grid(row=7, column=3)

        self.tbAvgPrice = Entry(f1, font=MyFont, width=7,textvariable=varAvgPrice)
        self.tbAvgPrice.grid(row=6,column=4)

        self.tbPosition = Entry(f1, font=MyFont, width=7,textvariable=varPosition)
        self.tbPosition.grid(row=7,column=4)
        
        self.label_unrealized = Label(f1, font=('',10), text = 'Unrealized').grid(row=10,column=2) 
        
        self.label_realized =  Label(f1, font=('',10), text = 'Realized').grid(row=10,column=3)

        self.label_Marked = Label(f1, font=('',10), text = 'Marked').grid(row=10,column=4)

        self.tbUnrealized = Entry(f1, font=('',10), width=11, textvariable=varUnrealized).grid(row=11,column=2)

        self.tbRealized = Entry(f1, font=('',10), width=11, textvariable=varRealized).grid(row=11,column=3)

        self.tbMarked = Entry(f1, font=('',10), width=11, textvariable=varMarked).grid(row=11,column=4)
        
        self.chkOutsideRTH = Checkbutton (f1, font=('',10), text='OutsideRTH', variable=varOutsideRTH)
        self.chkOutsideRTH.grid(row=9, column=6)    
        
    def tbBid_Click(self, event):
        LimitPrice=varBid.get()
        VarLimitPrice.set(LimitPrice)

    def tbAsk_Click(self, event):
        LimitPrice=varAsk.get()
        VarLimitPrice.set(LimitPrice)

    def tbLast_Click(self, event):
        LimitPrice=varLast.get()
        VarLimitPrice.set(LimitPrice)

    def cancel_all(self):
        self.tws_conn.reqGlobalCancel()
    
    def connect_to_tws(self):
        self.tws_conn=connection.Create(port=self.port,clientId=self.client_id)
        self.tws_conn.connect()
        self.register_callback_functions()

    def disconnect_it(self):
        self.tws_conn.disconnect()
    
    def buy(self):
        self.symbol = varSymbol.get()
        self.quantity = varQuantity.get()
        self.order_type = varOrderType.get()
        self.limit_price = varLimitPrice.get()
        self.my_outside = varOutsideRTH.get() # add here
        the_outsideRTH = 0
        if self.my_outside == True:
            the_outsideRTH = 1
        self.place_market_order(self.symbol, self.quantity, self.order_type, True, self.limit_price, the_outsideRTH) # add here

    def sell(self):
        self.symbol = varSymbol.get()
        self.quantity = varQuantity.get()
        self.order_type = varOrderType.get()
        self.limit_price = varLimitPrice.get()
        self.my_outside = varOutsideRTH.get() # add here
        the_outsideRTH = 0
        if self.my_outside == True:
            the_outsideRTH = 1
        self.place_market_order(self.symbol, self.quantity, self.order_type, True, self.limit_price, the_outsideRTH) # add here

    def place_market_order (self,symbol,quantity, order_type,is_buy,limit_price, my_outsideRTH):
        print ( symbol,quantity,order_type,is_buy,limit_price)
        contract= self.create_contract(symbol,'STK','SMART','NASDAQ','USD')
        buysell = 'BUY' if is_buy else 'SELL'
        order= self.create_order(order_type,quantity,buysell,limit_price, my_outsideRTH)
        self.tws_conn.placeOrder(self.order_id,contract,order)
        self.order_id += 1

    def cbSymbol_onEnter(self,event):
        self.tws_conn.reqAccountUpdates(False,self.account_code)
        varSymbol.set(varSymbol.get().upper())
        mytext=varSymbol.get()
        vals=self.cbSymbol.cget('values')
        self.cbSymbol.select_range(0,END) 
        if not vals:
            self.cbSymbol.configure(values= (mytext, ))
        elif mytext not in vals:
            self.cbSymbol.configure(values = vals + (mytext, )) 
        mySymbol = varSymbol.get()
        self.symbol = mySymbol
        self.cancel_market_data()
        self.request_market_data(self.symbol_id,self.symbol)
        self.request_account_updates(self.account_code) 
        varBid.set('0.00') 
        varAsk.set('0.00')
        varPosition.set('0')
        varAvgPrice.set('0.00')
        self.realized_pnl = 0
        self.marked_pnl = 0
        varUnrealized.set('0.00')
        varRealized.set('0.00')
        varMarked.set('0.00')
    
    def request_account_updates(self, account_code):
        self.tws_conn.reqAccountUpdates(True,self.account_code)

    def cancel_market_data(self):
        self.tws_conn.cancelMktData(self.symbol_id)

    def request_market_data(self, symbol_id, symbol): 
        contract= self.create_contract(symbol,'STK','SMART','NASDAQ','USD')
        self.tws_conn.reqMktData(symbol_id, contract,'',False)
    
    def tick_event(self,msg): 
        if msg.fiedl == 1:
            self.bid_price = msg.price 
        elif msg.fiedl == 2:
            self.ask_price == msg.price 
        elif msg.field == 4:
            self.last_prices =msg.price
            self.monitor_position()

    def create_contract(self, symbol,sec_type,exch,prim_exch,curr):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exch
        contract.m_primaryExch = prim_exch
        contract.m_currency = curr
        return contract
    
    def create_order(self, order_type, quantity, action, limit_price, outside_Rth):    
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action
        order.m_lmtPrice = limit_price  
        order.m_outsideRth = outside_Rth                  
        return order

    def register_callback_functions(self):
        self.tws_conn.registerAll(self.server_handler)
        self.tws_conn.register(self.error_handler,'Error')
        self.tws_conn.register(self.tick_event,message.tickPrice,message.tickSize)

    def server_handler(self,msg):
        if msg.typeName == "nextInvalid":
            self.order_id= msg.order_id
        elif msg.typeName == "managedAccounts":
            self.account_code = msg.accountsList
        elif msg.typeName == "UpdatePortfolio" \
                and msg.contract.m_symbol == self.symbol:
            self.unrealized_pnl = msg.unrealizedPNL
            self.realized_pnl = msg.realizedPNL
            self.position = msg.position
            self.average_price = msg.averageCost
        elif msg.typeName == "error" and msg.id != -1:
            return

    def error_handler(self, msg):
        if msg.typeName == 'error' and msg.id !=1:
            print ('Server Error:', msg)
    
    def monitor_position(self):
        print ('Last Price = %s' % (self.last_prices))
        varLast.set(self.last_prices)
        varBid.set(self.bid_price)
        varAsk.set(self.ask_price)
        varAvgPrice.set('%.2f' % self.average_price)
        varPosition.set(self.position)
        myShares = abs(self.position)
        varRealized.set(self.realized_pnl)
        if self.position > 0:
            self.unrealized = '%.2f' % ((self.last_prices - self.average_price)* myShares)
            varUnrealized.set(self.unRealized)
            self.marked_pnl ='%.2f' % (float (self.unrealized)+ float (self.realized_pnl))
            varMarked.set(self.marked_pnl)
        elif self.position < 0: 
            self.unrealized = '%.2f' % ((self.average_price - self.last_prices)* myShares)
            varUnrealized.set(self.unRealized)
            self.marked_pnl ='%.2f' % (float (self.unrealized)+ float (self.realized_pnl))
            varMarked.set(self.marked_pnl)
        else:
            self.marked_pnl = float (self.unrealized_pnl) + float (self.realized_pnl)
            self.marked_pnl = '%.2f' % self.marked_pnl
            self.realized_pnl = '%.2f' % float(self.realized_pnl)
            varUnrealized.set('0.00')
            varRealized.set(self.realized_pnl)
            varMarked.set(self.marked_pnl)


root = Tk()
root.title("Connect to IB TWS with Python")
root.geometry("600x480")
root.attributes("-topmost", True)
varSymbol=StringVar(root, value ='NFLX')
varQuantity=StringVar(root, value ='100')
varLimitPrice=StringVar()
varMarket= StringVar(root, value ='SMART')
varOrderType = StringVar(root, value ='LMT')
varPrimaryEx= StringVar(root, value='NASDAQ')
varTIF=StringVar(root, value ='DAY')
varLast = StringVar()
varBid = StringVar()
varAsk = StringVar()
varAvgPrice = StringVar(root, value='0.00')
varPosition = StringVar(root, value='0')
varUnrealized= StringVar()
varRealized= StringVar()
varMarked=StringVar()
varOutsideRTH= IntVar(root,value=False)

app = Application(root)

root.mainloop()