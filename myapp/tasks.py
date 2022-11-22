from operator import le
from time import sleep
from xml.etree.ElementPath import find
from celery import shared_task
from .models import *
from nsetools import *
from datetime import datetime as dt
from truedata_ws.websocket.TD import TD
import websocket

from celery.schedules import crontab
from celery import Celery
from celery.schedules import crontab
import time
from nsetools import Nse
from myproject.celery import app
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from datetime import datetime, time,timedelta
from celery.exceptions import SoftTimeLimitExceeded
from pytz import timezone
import pendulum
import calendar
from datetime import date
import time as te

def equity():
    try:
        result_items = EquityThree.objects.all()
        print(f"############# \n {result_items}\n############# \n")
        equity_username = 'tdwsp135'
        equity_password = 'saaral@135'

        fnolist = ['AARTIIND', 'ABBOTINDIA', 'ABFRL', 'ACC', 'ADANIPORTS', 'ALKEM', 'AMARAJABAT', 'AMBUJACEM', 'APOLLOHOSP', 'APOLLOTYRE', 'ASIANPAINT', 'ASTRAL', 'ATUL', 'AUBANK', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJFINANCE', 'BALRAMCHIN', 'BANDHANBNK', 'BATAINDIA', 'BEL', 'BERGEPAINT', 'BHARATFORG', 'BHARTIARTL', 'BIOCON', 'BOSCHLTD', 'BPCL', 'BSOFT', 'CANBK', 'CANFINHOME', 'CHAMBLFERT', 'CHOLAFIN', 'CIPLA', 'COALINDIA', 'COFORGE', 'COLPAL', 'CONCOR', 'COROMANDEL', 'CROMPTON', 'CUMMINSIND', 'DABUR', 'DALBHARAT', 'DEEPAKNTR', 'DELTACORP', 'DIVISLAB', 'DIXON', 'DLF', 'DRREDDY', 'ESCORTS', 'GLENMARK', 'GNFC', 'GODREJCP', 'GODREJPROP', 'GRANULES', 'GRASIM', 'GSPL', 'GUJGASLTD', 'HAL', 'HAVELLS', 'HCLTECH', 'HDFC', 'HDFCAMC', 'HDFCBANK', 'HDFCLIFE', 'HINDALCO', 'HINDCOPPER', 'HINDPETRO', 'HINDUNILVR', 'HONAUT', 'IBULHSGFIN', 'ICICIBANK', 'ICICIGI', 'ICICIPRULI', 'IEX', 'IGL', 'INDHOTEL', 'INDIACEM', 'INDIAMART', 'INDIGO', 'INDUSINDBK', 'INDUSTOWER', 'INFY', 'INTELLECT', 'IPCALAB', 'IRCTC', 'ITC', 'JINDALSTEL', 'JKCEMENT', 'JSWSTEEL', 'JUBLFOOD', 'KOTAKBANK', 'LALPATHLAB', 'LAURUSLABS', 'LICHSGFIN', 'LT', 'LTI', 'LTTS', 'LUPIN', 'M&MFIN', 'MARICO', 'MARUTI', 'MCDOWELL-N', 'MCX', 'MFSL', 'MGL', 'MINDTREE', 'MOTHERSON', 'MPHASIS', 'MRF', 'MUTHOOTFIN', 'NATIONALUM', 'NAUKRI', 'NAVINFLUOR', 'NMDC', 'OBEROIRLTY', 'OFSS', 'ONGC', 'PAGEIND', 'PERSISTENT', 'PETRONET', 'PIDILITIND', 'PIIND', 'POLYCAB', 'POWERGRID', 'PVR', 'RAIN', 'RAMCOCEM', 'RELIANCE', 'SBICARD', 'SBILIFE', 'SBIN', 'SHREECEM', 'SIEMENS', 'SRF', 'SRTRANSFIN', 'SUNPHARMA', 'SUNTV', 'SYNGENE', 'TATACHEM', 'TATACOMM', 'TATACONSUM', 'TATAMOTORS', 'TATAPOWER', 'TATASTEEL', 'TECHM', 'TORNTPHARM', 'TORNTPOWER', 'TRENT', 'TVSMOTOR', 'UBL', 'ULTRACEMCO', 'UPL', 'VOLTAS', 'WHIRLPOOL', 'WIPRO', 'ZEEL', 'ZYDUSLIFE']
        
        print(f"length of :{len(fnolist)}")
        # Default production port is 8082 in the library. Other ports may be given t oyou during trial.
        realtime_port = 8082

        print('Starting Real Time Feed.... ')
        print(f'Port > {realtime_port}')

        td_app = TD(equity_username, equity_password, live_port=realtime_port, historical_api=False)
        # print(symbols)
        req_ids = td_app.start_live_data(fnolist)
        live_data_objs = {}

        te.sleep(2)

        liveData = {}
        for req_id in req_ids:
            # print(td_app.live_data[req_id].day_open)
            if (td_app.live_data[req_id].ltp) == None:
                continue
            else:
                liveData[td_app.live_data[req_id].symbol] = [td_app.live_data[req_id].ltp,td_app.live_data[req_id].day_open,td_app.live_data[req_id].day_high,td_app.live_data[req_id].day_low,td_app.live_data[req_id].prev_day_close,dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'),td_app.live_data[req_id].change_perc]

        removeList = ["NIFTY","BANKNIFTY","FINNIFTY"]

        callcrossedset = LiveEquityResult.objects.filter(strike__contains="Call Crossed")
        callonepercentset = LiveEquityResult.objects.filter(strike="Call 1 percent")
        putcrossedset = LiveEquityResult.objects.filter(strike="Put Crossed")
        putonepercentset = LiveEquityResult.objects.filter(strike="Put 1 percent")
        opencallcross = LiveEquityResult.objects.filter(opencrossed="call")
        openputcross = LiveEquityResult.objects.filter(opencrossed="put")

        callcrossedsetDict = {}
        callonepercentsetDict = {}
        putcrossedsetDict = {}
        putonepercentsetDict = {}
        opencallcrossDict = {}
        openputcrossDict = {}

        for i in callcrossedset:
            callcrossedsetDict[i.symbol] = i.time
        for i in callonepercentset:
            callonepercentsetDict[i.symbol] = i.time
        for i in putcrossedset:
            putcrossedsetDict[i.symbol] = i.time
        for i in putonepercentset:
            putonepercentsetDict[i.symbol] = i.time
        for i in opencallcross:
            opencallcrossDict[i.symbol] = i.time
        for i in openputcross:
            openputcrossDict[i.symbol] = i.time

        # Graceful exit
        td_app.stop_live_data(fnolist)
        td_app.disconnect()
        td_app.disconnect()
        three_list = list(EquityThree.objects.all().values_list('symbol', flat=True)) 
        super_three_list = list(SuperLiveSegment.objects.all().values_list('symbol', flat=True)) 
        
        for key,value in liveData.items():
            print(f"Key: {key} \nValue:{value}")
            if key in fnolist:
                # print(key)
                LiveSegment.objects.filter(symbol=key).all().delete()
                if value[6] >= 3 and key not in three_list:
                    three = EquityThree(symbol=key,change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    three.save()
                elif value[6] <= -3 and key not in three_list:
                    three = EquityThree(symbol=key,change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    three.save()

                if float(value[6]) >= 1.5 and key not in super_three_list:
                    gain = SuperLiveSegment(symbol=key,segment="gain",change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    gain.save()

                elif float(value[6]) <= -1.5 and key not in super_three_list:
                    loss = SuperLiveSegment(symbol=key,segment="loss",change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    loss.save()

                if float(value[6]) <= 0:
                    below = LiveSegment(symbol=key,segment="below",change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    below.save()

                elif float(value[6]) >= 0:
                    above = LiveSegment(symbol=key,segment="above",change_perc=value[6],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'),time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'))
                    above.save()


        gainList = list(LiveSegment.objects.filter(segment="gain").values_list('symbol', flat=True))
        lossList = list(LiveSegment.objects.filter(segment="loss").values_list('symbol', flat=True))
        above = list(LiveSegment.objects.filter(segment="above").values_list('symbol', flat=True))
        below = list(LiveSegment.objects.filter(segment="below").values_list('symbol', flat=True))

        print(f"Total length: {len(LiveOITotalAllSymbol.objects.all())}")
        for e in LiveOITotalAllSymbol.objects.all():
            # print(e.symbol)
            # callcross = TestEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="common",opencrossed="common",time=dt.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'),date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))
            # callcross.save()

            # History Check
            historyLen = HistoryOITotal.objects.filter(symbol=e.symbol)
            # total oi earliest
            if len(historyLen) > 0:
                historyStrike = HistoryOITotal.objects.filter(symbol=e.symbol).earliest('time')
                strikegp = LiveOITotal.objects.filter(symbol=e.symbol)
                callstrike = historyStrike.callstrike
                putstrike = historyStrike.putstrike
                # Call 1 percent 
                strike_gap = (float(strikegp[0].strikegap)) * 2
                callone = float(callstrike) - strike_gap
                # Put 1 percent
                putone = float(putstrike) + strike_gap

            else:
                callstrike = e.callstrike
                putstrike = e.putstrike
                callone = e.callone
                putone = e.putone
            
            strikegp = LiveOITotal.objects.filter(symbol=e.symbol)

            if e.symbol in liveData and e.symbol in above:
                try:
                    print(e.symbol)
                    print("the symbol is in above")
                    # print(liveData)

                    # Difference Calculation
                    historyput = HistoryOIChange.objects.filter(symbol=e.symbol)
                    historycall = HistoryOITotal.objects.filter(symbol=e.symbol)
                    strikegp = LiveOITotal.objects.filter(symbol=e.symbol)

                    if len(historyput) > 0:
                        diffputstrike = HistoryOIChange.objects.filter(symbol=e.symbol).earliest('time')
                        diffputstrike = diffputstrike.putstrike
                        print("######### CALL #############")
                        print(f"diff put history {diffputstrike}")
                        history_len = 0
                        if diffputstrike == 0 or diffputstrike == '0':
                            diffputstrike_db = HistoryOIChange.objects.filter(symbol=e.symbol).order_by('time')
                            count = 1
                            while diffputstrike == 0 or diffputstrike == '0':
                                if count < len(diffputstrike_db):
                                    diffputstrike = diffputstrike_db[count].putstrike
                                    count +=1
                                else:
                                    diffputstrike = LiveOIChange.objects.filter(symbol=e.symbol).earliest('time')
                                    diffputstrike = diffputstrike.putstrike
                                    break
                            print(f"diff put history {diffputstrike}")
                    else:
                        is_available = LiveOIChange.objects.filter(symbol=e.symbol)
                        if len(is_available) > 0:
                            diffputstrike = LiveOIChange.objects.filter(symbol=e.symbol).earliest('time')
                            diffputstrike = diffputstrike.putstrike
                            if diffputstrike == 0 or diffputstrike == '0':
                                diffputstrike = LiveOIChange.objects.filter(symbol=e.symbol).order_by('time')
                                diffputstrike = diffputstrike[1].putstrike
                        else:
                            diffputstrike = 0

                    if len(historycall) > 0:
                        diffcallstrike = HistoryOITotal.objects.filter(symbol=e.symbol).earliest('time')
                        diffcallstrike = diffcallstrike.callstrike
                    else:
                        diffcallstrike = LiveOITotal.objects.filter(symbol=e.symbol).earliest('time')
                        diffcallstrike = diffcallstrike.callstrike
                        # diffcallstrike = e.callstrike
                    
                    difference = float(diffputstrike) - float(diffcallstrike)
                    section = int(abs((float(diffputstrike) - float(diffcallstrike))/float(strikegp[0].strikegap)))
                    print(f"call Strike: {callstrike}")

                    if float(liveData[e.symbol][1]) > float(callstrike):
                        print("open checked")
                        if e.symbol in opencallcrossDict:
                            LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                            callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="call",time=opencallcrossDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            callcross.save()
                            continue
                        else:
                            if liveData[e.symbol][6] < 3 and liveData[e.symbol][6] > 0:
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="call",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                callcross.save()
                            else:
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="call",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=False)
                                callcross.save()
                            continue
                    # High Check
                    elif float(liveData[e.symbol][2]) > float(callstrike):
                        print("high checked")
                        if e.symbol in callcrossedsetDict:
                            LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                            callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=callcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            callcross.save()
                            continue
                        else:
                            if liveData[e.symbol][6] < 3 and liveData[e.symbol][6] > 0:
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6], below_three=True)
                                callcross.save()
                            else:
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6], below_three=False)
                                callcross.save()
                            continue

                    elif float(liveData[e.symbol][0]) > float(callstrike):
                        print("ltp checked")
                        if e.symbol in callcrossedsetDict:
                            # print("Yes")
                            # Deleting the older
                            LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                            # updating latest data
                            # print("Yes")
                            callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=callcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            callcross.save()
                            continue
                        else:
                            if liveData[e.symbol][6] < 3 and liveData[e.symbol][6] > 0:
                                # print("Call crossed")
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6], below_three=True)
                                callcross.save()
                            else:
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6], below_three=False)
                                callcross.save()
                            

                    elif float(liveData[e.symbol][0]) >= float(callone) and float(liveData[e.symbol][0]) < float(callstrike):
                        print("100% percent check")
                        if e.symbol in callcrossedsetDict:
                            # print("Already crossed")
                            continue
                        else:
                            if e.symbol in callonepercentsetDict:
                                # print("Already crossed 1 percent")
                                LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                                # updating latest data
                                callcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call 1 percent",opencrossed="Nil",time=callonepercentsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                                callcross.save()
                                continue
                            else:
                                if liveData[e.symbol][6] < 3 and liveData[e.symbol][6] > 0:
                                    # print("Call 1 percent")
                                    callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call 1 percent",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                    callone.save()
                                else:
                                    callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call 1 percent",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6], below_three=False)
                                    callone.save()

                    else:
                        # LiveEquityResult.objects.filter(symbol =e.symbol,strike="Call").delete()
                        # callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        # callone.save()
                        # if e.symbol in callcrossedsetDict:
                        #     LiveEquityResult.objects.filter(symbol=e.symbol,strike="Call").delete()
                        #     LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                        #     callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call Crossed",opencrossed="Nil",time=callcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        #     callone.save()
                        # elif e.symbol in callonepercentsetDict:
                        #     LiveEquityResult.objects.filter(symbol=e.symbol,strike="Call").delete()
                        #     LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                        #     callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call 1 percent",opencrossed="Nil",time=callonepercentsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        #     callone.save()
                        # else:
                        print("default update")
                        LiveEquityResult.objects.filter(symbol=e.symbol).delete()
                        callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Call",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        callone.save()
                except Exception as ex:
                    print(ex)
            # Put
            # print(liveData)
            if e.symbol in liveData and e.symbol in below:
                try:
                    print("the symbol is in above")
                    # Difference Calculation
                    historycall = HistoryOIChange.objects.filter(symbol=e.symbol)
                    historyput = HistoryOITotal.objects.filter(symbol=e.symbol)
                    strikegp = LiveOITotal.objects.filter(symbol=e.symbol)

                    if len(historycall) > 0:
                        diffcallstrike = HistoryOIChange.objects.filter(symbol=e.symbol).earliest('time')
                        diffcallstrike = diffcallstrike.callstrike
                        print("######### PUT #############")
                        print(f"diff call history {diffcallstrike}")
                        history_len = 0
                        if diffcallstrike == 0 or diffcallstrike == '0':
                            diffcallstrike_db = HistoryOIChange.objects.filter(symbol=e.symbol).order_by('time')
                            count = 1
                            while diffcallstrike == 0 or diffcallstrike == '0':
                                if count < len(diffcallstrike_db):
                                    diffcallstrike = diffcallstrike_db[count].putstrike
                                    count +=1
                                else:
                                    diffcallstrike = LiveOIChange.objects.filter(symbol=e.symbol).earliest('time')
                                    diffcallstrike = diffcallstrike.callstrike
                                    break
                    else:
                        is_available = LiveOIChange.objects.filter(symbol=e.symbol)
                        if len(is_available) > 0:
                            diffcallstrike = LiveOIChange.objects.filter(symbol=e.symbol).earliest('time')
                            diffcallstrike = diffcallstrike.callstrike
                            if diffcallstrike == 0 or diffcallstrike == '0':
                                diffcallstrike = LiveOIChange.objects.filter(symbol=e.symbol).order_by('time')
                                diffcallstrike = diffcallstrike[1].callstrike
                        else:
                            diffcallstrike = 0
                        # diffcallstrike = e.callstrike

                    if len(historyput) > 0:
                        diffputstrike = HistoryOITotal.objects.filter(symbol=e.symbol).earliest('time')
                        diffputstrike = diffputstrike.putstrike
                    else:
                        diffputstrike = LiveOITotal.objects.filter(symbol=e.symbol).earliest('time')
                        diffputstrike = diffputstrike.putstrike
                        # diffputstrike = e.putstrike
                    
                    difference = float(diffcallstrike) - float(diffputstrike)
                    section = int(abs((float(diffcallstrike) - float(diffputstrike))/float(strikegp[0].strikegap)))

                    # putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put 1 percent",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference)
                    # putcross.save()

                    if float(liveData[e.symbol][1]) < float(putstrike):
                        print("open check")
                        if e.symbol in openputcrossDict:
                            LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                            putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="put",time=openputcrossDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            putcross.save()
                            continue
                        else:
                            if liveData[e.symbol][6] > -3 and liveData[e.symbol][6] < 0:
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="put",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                putcross.save()
                            else:
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="put",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=False)
                                putcross.save()
                            continue
                    #puthigh Check   
                    elif float(liveData[e.symbol][3]) < float(putstrike):
                        print("high check")
                        if e.symbol in putcrossedsetDict:
                            LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                            putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=putcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            putcross.save()
                            continue
                        else:
                            if liveData[e.symbol][6] > -3 and liveData[e.symbol][6] < 0:
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                putcross.save()
                            else:
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=False)
                                putcross.save()
                            continue

                    elif float(liveData[e.symbol][0]) < float(putstrike):
                        print("ltp check")
                        if e.symbol in putcrossedsetDict:
                            # Deleting the older
                            LiveEquityResult.objects.filter(symbol =e.symbol).delete()
                            # updating latest data
                            putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=putcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                            putcross.save()
                            # print("put crossed updating only the data")
                            continue
                        else:
                            if liveData[e.symbol][6] > -3 and liveData[e.symbol][6] < 0:
                                # print("Put crossed")
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                putcross.save()
                            else:
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=False)
                                putcross.save()

                    elif float(liveData[e.symbol][0]) <= float(putone) and float(liveData[e.symbol][0]) > float(putstrike):
                        print("one percent check")
                        if e.symbol in putcrossedsetDict:
                            # print("Already crossed put")
                            continue
                        else:
                            if e.symbol in putonepercentsetDict:
                                # print("Already crossed 1 percent")
                                LiveEquityResult.objects.filter(symbol =e.symbol).delete()
                                # updating latest data
                                putcross = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put 1 percent",opencrossed="Nil",time=putonepercentsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                                putcross.save()
                                continue
                            else:
                                if liveData[e.symbol][6] > -3 and liveData[e.symbol][6] < 0:
                                    # print("Put 1 percent")
                                    putone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put 1 percent",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=True)
                                    putone.save()
                                else:
                                    putone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put 1 percent",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6],below_three=False)
                                    putone.save()
                    else:
                        # if e.symbol in putcrossedsetDict:
                        #     LiveEquityResult.objects.filter(symbol=e.symbol,strike="Put").delete()
                        #     LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                        #     callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put Crossed",opencrossed="Nil",time=putcrossedsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        #     callone.save()
                        # elif e.symbol in putonepercentsetDict:
                        #     LiveEquityResult.objects.filter(symbol=e.symbol,strike="Put").delete()
                        #     LiveEquityResult.objects.filter(symbol = e.symbol).delete()
                        #     callone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put 1 percent",opencrossed="Nil",time=putonepercentsetDict[e.symbol],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        #     callone.save()
                        # else:
                        print("default update")
                        LiveEquityResult.objects.filter(symbol=e.symbol).delete()
                        putone = LiveEquityResult(symbol=e.symbol,open=liveData[e.symbol][1],high=liveData[e.symbol][2],low=liveData[e.symbol][3],prev_day_close=liveData[e.symbol][4],ltp=liveData[e.symbol][0],strike="Put",opencrossed="Nil",time=liveData[e.symbol][5],date=dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),section=section,difference=difference,change_perc=liveData[e.symbol][6])
                        putone.save()
                except Exception as ex:
                    print(ex)
    except websocket.WebSocketConnectionClosedException as e:
        print('This caught the websocket exception in equity realtime')
        td_app.disconnect()
        td_app.disconnect()
        # return render(request,"testhtml.html",{'symbol':item,'counter':1}) 
    except IndexError as e:
        print('This caught the exception in equity realtime')
        print(e)
        td_app.disconnect()
        td_app.disconnect()
        # return render(request,"testhtml.html",{'symbol':item,'counter':1}) 
    except Exception as e:
        print(e)
        td_app.disconnect()
        td_app.disconnect()
        # return render(request,"testhtml.html",{'symbol':item,'counter':1}) 
while True:
    equity()