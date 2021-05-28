from sample import Functions
import pandas as pd 
import datetime
import time
import requests
import sys
fun=Functions()
fun.readZerodhaAccessToken()
ftg = []
live_trading=False
history_data={}
live_data={}
scrips = [s.strip() for s in open('fno.txt')]
p={}
putsandcall_id=-1001249836767
mytrades_id=-1001400620608

bot_token="1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg"

instruments = ['NSE:{}'.format(s) for s in scrips]
# print(instruments)
for instrument, ohlc in fun.ohlc(instruments).items():
	# print(instrument,ohlc)
	gap = round((ohlc['ohlc']['open'] - ohlc['ohlc']['close']) / ohlc['ohlc']['close'],3)
	# print(instrument,gap)
	if abs(gap) > 0.02:
		ftg.append((instrument, gap))
# print(ftg)
ftg.sort(key=lambda x: abs(x[1]), reverse=True)
# ftg=pd.DataFrame(ftg).iloc[:,0].head(5)
print(ftg)

welcome_message="https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id={}&parse_mode=Markdown&text=Good morning,Have a profitable Day :)".format(mytrades_id)
requests.get(welcome_message)


#getting data for live and history 
while True:
	try:
		if str(datetime.datetime.now().strftime('%X')) > str(datetime.time(9,16)):
			for instrument,gap in ftg:
				for k,v in fun.ohlc(instrument).items():
					live_data[k]={'high':v['ohlc']['high'],'low':v['ohlc']['low'],'ltp':v['last_price']}
					for key,value in live_data.items():
						try:
							history_data[key]
						except:
							history_data[key]={'high':value['high'],
												'low':value['low'],
												'ltp':value['ltp'],
												'Entry':False,
												'Exit':False,
												'position':'',
												'Entryprice':None,
												'Exitprice':None,
												'quantity':None,
												'stoploss':None,
												'target':None,
												'pnl':None
												}

					# print(history_data)
					#placing buy order in gapdown stocks at high with low as stoploss

					
					# print(history_data)
					if gap<-0.02:
						try:
							p[instrument]
						except:
							p[instrument]={'instrument':instrument,
							'entry':history_data[key]['high'],
							'target':round(history_data[key]['high']+1.5*(history_data[key]['high']-history_data[key]['low']),2),
							'stoploss':round(history_data[key]['low'],2)}
							send_buy_stocks=f"Buy {p[instrument]['instrument']} Entry {p[instrument]['entry']} Target {p[instrument]['target']} stoploss {p[instrument]['stoploss']} "
							url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001249836767&text= {}'.format(send_buy_stocks)
							requests.get(url)
							# print(p)
						# print(instrument,gap)
						# print(p)
						

						if value['ltp'] == history_data[key]['ltp'] and not history_data[key]['Entry']:
							qty=int(1000/(history_data[key]['high']-history_data[key]['low']))

							if live_trading:
								try:
									fun.buyorder(instrument=instrument[4:],quantity=qty)
								except Exception as e:
									print(f"error placing buy order as {e}")
								
							buyorder=f"buy order placed for {instrument[4:]} at {value['ltp']}"
							print(buyorder)
							url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608&text= {}'.format(buyorder)
							requests.get(url)
							stoploss= round(history_data[key]['low'],2)
							target= round(history_data[key]['high']+1.5*(history_data[key]['high']-history_data[key]['low']),2)
							history_data[key]['Entry']=True
							history_data[key]['Entryprice']=value['ltp']
							history_data[key]['position']='BUY'
							history_data[key]['stoploss']=stoploss
							history_data[key]['target']=target
							history_data[key]['quantity']=qty
							# print(live_data[instrument])
							# print(history_data[key]) 
							# try:
								

								
							# except:
							# 	history_data[key]['Entry']=True
							# 	history_data[key]['Exit']=True
						# print(history_data[key])
					#placing sell order for gapup stocks 
					if gap>0.02:
						try:
							p[instrument]
						except:
							p[instrument]={'instrument':instrument,
							'entry':history_data[key]['low'],
							'target':round(history_data[key]['low']-1.5*(history_data[key]['high']-history_data[key]['low']),2),
							'stoploss':round(history_data[key]['high'],2)}
							send_sell_stocks=f"Sell {p[instrument]['instrument']} Entry {p[instrument]['entry']} Target {p[instrument]['target']} stoploss {p[instrument]['stoploss']} "
							url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001249836767&text= {}'.format(send_sell_stocks)
							requests.get(url)
							# print(p)
						if value['ltp'] == history_data[key]['ltp'] and not history_data[key]['Entry']:
							qty=int(1000/(history_data[key]['high']-history_data[key]['low']))
							# print(qty)
							if live_trading:
								try:
									fun.sellorder(instrument=instrument[4:],quantity=qty)

								except Exception as e:
									print(f"error placing sell order as {e}")
							sellorder=f"sell order placed for {instrument[4:]} at {value['ltp']}"
							print(sellorder)
							url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608&text= {}'.format(sellorder)
							requests.get(url)

							stoploss= round(history_data[key]['high'],2)
							target=round( history_data[key]['low']-1.5*(history_data[key]['high']-history_data[key]['low']),2)
							history_data[key]['Entry']=True
							history_data[key]['Entryprice']=live_data[k]['ltp']
							history_data[key]['position']='SELL'
							history_data[key]['stoploss']=stoploss
							history_data[key]['target']=target
							history_data[key]['quantity']=qty 
							# print(history_data)
							# try:
								

							# except:
							# 	history_data[key]['Entry']=True
							# 	history_data[key]['Exit']=True

					if history_data[key]['Entry'] and not history_data[key]['Exit']:

						# exit order for buyy
						if history_data[key]['position']=='BUY':
							if str(datetime.datetime.now().strftime('%X'))>str(datetime.time(15,5)) or value['ltp']> history_data[key]['target'] or value['ltp'] <history_data[key]['stoploss']:
								if live_trading:
									try:
										fun.sellorder(instrument=instrument[4:],quantity=history_data[instrument]['quantity'])

									except Exception as e:
										print(f"error placing buy exit order as {e}")
								# print(live_data[instrument])

								history_data[key]['Exit']=True
								history_data[key]['Exitprice']=value['ltp']
								history_data[key]['pnl']=history_data[key]['quantity']*(history_data[key]['Exitprice']-history_data[key]['Entryprice'])
								exitorder=f"exit order placed for {instrument[4:]} at {value['ltp']} and pnl is {history_data[key]['pnl']}"
								print(exitorder)
								url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608&text= {}'.format(exitorder)
								requests.get(url)



						#exit order for sell 
						if history_data[key]['position']=='SELL':
							if str(datetime.datetime.now().strftime('%X')) > str(datetime.time(15,5)) or value['ltp'] < history_data[key]['target'] or value['ltp'] > history_data[key]['stoploss']:
								# print("entering sell order")
								if live_trading:
									try:
										fun.buyorder(instrument=instrument[4:],quantity=history_data[instrument]['quantity'])
									except Exception as e:
										print(f"error placing exit sell order as {e}")
								history_data[key]['Exit']=True
								history_data[key]['Exitprice']=value['ltp']
								history_data[key]['pnl']=history_data[key]['quantity']*(history_data[key]['Entryprice']-history_data[key]['Exitprice'])
								exitorder=f"exit order placed for {instrument[4:]} at {value['ltp']} and pnl is {history_data[key]['pnl']}"
								print(exitorder)
								url='https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608&text= {}'.format(exitorder)
								requests.get(url)
								# print(f"exit order placed for {instrument[4:]} at {value['ltp']} and pnl is : {history_data[key]['pnl']}")
								
								# print(history_data)

					if str(datetime.datetime.now().strftime('%X')) > str(datetime.time(23,34,5)):
						with open('fdata.csv','a') as n:
							print(f"{datetime.datetime.now().replace(microsecond=0)}",file=n)
						q=pd.DataFrame(history_data).T
						q.to_csv('fdata.csv',mode='a')
						sys.exit()
						break
		elif str(datetime.datetime.now().strftime('%X')) < str(datetime.time(9,16)):
			print("wait for start")
			time.sleep(1)
	
	except Exception as e:
		print(f"retrying as .. {e}")



'''
send_sell="https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608\
&parse_mode=Markdown&text={}".format(send_sell_stocks)
requests.get(send_sell)
send_buy="https://api.telegram.org/bot1816110669:AAEQ2udfam2TTpADQ1ejoqeugLERRJS9sUg/sendMessage?chat_id=-1001400620608\
&parse_mode=Markdown&text={}".format(send_buy_stocks)
requests.get(send_buy)
'''