from datetime import datetime, date
import pyotp
import math
import pandas as pd
import requests
import time
from smartapi import SmartConnect
import json
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
# from knox.models import AuthToken
from .models import *
# from .forms import nse_dataForm
from datetime import datetime, date
from .serializers import *
import datetime
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.views import login

# Create your views here.


def home(request):
    data = stock_detail.objects.all().order_by("buy_time").values()
    return render(request, "nse.html", {"data": data})


class stock_details(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        nse_objs = stock_detail.objects.all().order_by('-buy_time')
        # demo = stock_detail.objects.values_list().values()
        # # for i in demo:
        # #     for j,k in i.items():
        # #         print(k)
        # print(demo)
        serializer = stockListSerializer(nse_objs, many=True)
        return Response(
            {"status": True, "msg": "stock details fetched", "data": serializer.data}

        )

    def put(self, request):
        try:
            data = request.data
            if not data.get("id"):
                return Response({"status": False, "msg": "id is required", "data": {}})

            obj = stock_detail.objects.get(id=data.get("id"))
            serializer = stockPostSerializer(obj, data=data, partial=True)
            if ('exit_price' in data):
                data["status"] = "SELL"
                data["sell_buy_time"] = datetime.datetime.today()
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "msg": "Successfully SELL Stock",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "msg": "invalid data",
                        "data": serializer.errors,
                    }
                )
        except Exception as e:
            print(e)
            return Response({"status": False, "msg": "Invalid id", "data": {}})

    def post(self, request):

        try:
            data = request.data
            
            serializer = stockPostSerializer(data=data)
            data["status"] = "BUY"
            if serializer.is_valid():
                serializer.save()
                get_data = live.objects.values('set')
                for i in get_data:
                    if i['set'] == 1.0:
                        data = request.data
                        base_strike_price = float(data['base_strike_price'])
                        live_dd =  data['live_Strike_price']
                        brid_price = data['buy_price']
                        squareoff = data['squareoff']
                        stoploss = data['stoploss']
                        percentions = data['percentage']
                        stock_name_nse = data['stock_name']
                        # squareoff = data['sell_price']
                        # stoploss = data['stop_loseprice']
                        tg = (brid_price * 0.05)
                        # print("hello", tg)
                        print("anand", percentions)

                        

                        number_of_quantity = nse_setting.objects.values_list().values()
                        for a in number_of_quantity:
                           
                            if a['id'] == percentions:
                                quantity = a['quantity_bn']

                        q_id= stock_detail.objects.values_list().values()
                        for x in q_id:
                            if  x['buy_price'] == brid_price and  x['live_Strike_price'] == live_dd :
                                get_id = x['id']
                                print('get_id',get_id)
                        
                        username = 'H117838'
                        apikey = 'SqtdCpAg'
                        pwd = '4689'
                        totp = pyotp.TOTP("K7QDKSEXWD7KRO7EVQCUHTFK2U").now()
                        obj = SmartConnect(api_key=apikey)
                        dataa = obj.generateSession(username, pwd, totp)
                        # data
                        # refreshToken= data['data']['refreshToken']
                        # feedToken=obj.getfeedToken()
                        # userProfile= obj.getProfile(refreshToken)
                        # print(userProfile)

                        # print("quantity",type(quantity)) 

                        def place_order(token, symbol, qty,exch_seg ,buy_sell,ordertype ,price, variety='ROBO', triggerprice=5):
                            print("qty",qty)
                            qnt = float(qty) * quantity
                            qnt_data = int(qnt)
                            qnt_place =str(qnt_data)
                            print(qnt_place)
                            try:
                                orderparams = {
                                    "variety": 'ROBO',
                                    "tradingsymbol": symbol,
                                    "symboltoken": token,
                                    "transactiontype": 'BUY',
                                    'exchange': exch_seg,
                                    "ordertype": 'LIMIT',
                                    "producttype": 'BO',
                                    "duration": "DAY",
                                    "price": brid_price,
                                    "squareoff": squareoff,
                                    "stoploss": stoploss,
                                    # "quantity":qnt_place,

                                    "trailingStopLoss": tg,
                                }
                                print(orderparams)
                                orderId = obj.placeOrder(orderparams)
                                print("The order id is: {}".format(orderId))
                                stock_detail.objects.filter(id = get_id).update(orderid = orderId)

                            except Exception as e:
                                print(
                                    "Order placement failed: {}".format(e.message))

                        def place_order_stock(token, symbol, qty,exch_seg ,buy_sell,ordertype ,price, variety='ROBO', triggerprice=5):
                            print("qty",qty)
                            B_D = str(brid_price)
                            qnt = float(qty) * quantity
                            qnt_data = int(qnt)
                            qnt_place =str(qnt_data)
                            print(qnt_place)
                            try:
                                orderparams = {
                                    "variety": 'NORMAL',
                                    "tradingsymbol": symbol,
                                    "symboltoken": token,
                                    "transactiontype": 'BUY',
                                    'exchange': 'NFO',
                                    "ordertype": 'LIMIT',
                                    "producttype": 'CARRYFORWARD',
                                    "duration": "DAY",
                                    "price": '30',    
                                    "squareoff": squareoff,
                                    "stoploss": stoploss,
                                    "quantity":qnt_place,

                                   
                                }
                                print(orderparams)
                                orderId = obj.placeOrder(orderparams)
                                print("The order id is: {}".format(orderId))
                                data_of_q = stock_detail.objects.filter(id = get_id).update(orderid = orderId)
                                print('data_of_q',data_of_q)

                            except Exception as e:
                                print(
                                    "Order placement failed: {}".format(e.message))    

                        url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
                        d = requests.get(url).json()
                        token_df = pd.DataFrame.from_dict(d)
                        token_df['expiry'] = pd.to_datetime(
                            token_df['expiry']).apply(lambda x: x.date())
                        token_df = token_df.astype({'strike': float})

                        def getTokenInfo(symbol, exch_seg='NSE', instrumenttype='OPTIDX', strike_price='', pe_ce='CE', expiry_day=None):
                            df = token_df
                            strike_price = strike_price*100
                            if exch_seg == 'NSE':
                                eq_df = df[(df['exch_seg'] == 'NSE')]
                                return eq_df[eq_df['name'] == symbol]
                            elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
                                return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
                            elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
                                return df[(df['exch_seg'] == 'NFO') & (df['expiry'] == expiry_day) & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

                        a = date(2023,1,12)      
                        exprity_stock  = date(2023,1,25)
                        
                        if percentions == 2 :
                            symbol = 'BANKNIFTY'
                            
                            print("1",symbol)

                            pe_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',base_strike_price,'PE',a).iloc[0]
                            place_order(pe_strike_symbol['token'],pe_strike_symbol['symbol'],pe_strike_symbol['lotsize'],'BUY','MARKET',0,'NORMAL','NFO')
                            print("nifty pe",pe_strike_symbol)
                                
                        elif percentions == 1:
                            symbol = 'BANKNIFTY'

                            print("symbol",symbol)
                            ce_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',base_strike_price,'CE',a).iloc[0]
                            place_order(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')
                            print("NIFTY ce",ce_strike_symbol)

                            

                        elif percentions == 4:
                            symbol = 'NIFTY'
                            qty = 25
                            pe_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',base_strike_price,'PE',a).iloc[0]
                            place_order(pe_strike_symbol['token'],pe_strike_symbol['symbol'],pe_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO',qty)
                            print("BANKNIFTY pe",pe_strike_symbol)


                        elif percentions == 3:
                            symbol = 'NIFTY'
                            ce_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',base_strike_price,'CE',a).iloc[0]
                            place_order(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')


                            print("BANKNIFTY ce",ce_strike_symbol)

                        elif percentions == 5: 
                            symbol = stock_name_nse
                            print("stock_name_nse",stock_name_nse)
                            ce_strike_symbol = getTokenInfo(symbol,'NFO','OPTSTK',base_strike_price,'CE',exprity_stock).iloc[0]
                            place_order_stock(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NSE')
                           
                            print("stock ce", ce_strike_symbol)

                       
                return Response(
                    {"status": True, "msg": "Successfully BUY Stock",
                        "data": serializer.data}
                )

            else:
                return Response(
                    {"status": False, "msg": "invalid data",
                        "data": serializer.errors}
                )

        except Exception as e:
            print(e)
        return Response(
            {
                "status": False,
                "msg": "Somthing Went Wrong",
            }
        )

        # _mutable = data._mutable
        # data._mutable = True


# <-------------------------------- setting ---------------------------------->

class setting_nse(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        nse_objs = nse_setting.objects.all()
        serializer = settingSerializer(nse_objs, many=True)
        return Response(
            {"status": True, "msg": "settings fetched", "data": serializer.data}
        )

    def post(self, request):

        try:
            data = request.data
            # _mutable = data._mutable
            # data._mutable = True
            serializer = settingSerializer(data=data)

            # data["sell_buy_time"] = "-"
            # data._mutable = _mutable
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": True, "msg": "success data", "data": serializer.data}
                )

            else:
                return Response(
                    {"status": False, "msg": "invalid data",
                        "data": serializer.errors}
                )

        except Exception as e:
            print(e)
        return Response(
            {
                "status": False,
                "msg": "Somthing Went Wrong",
            }
        )

    def put(self, request):
        try:
            data = request.data
            if not data.get("id"):
                return Response({"status": False, "msg": "id is required", "data": {}})

            obj = nse_setting.objects.get(id=data.get("id"))
            serializer = settingSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "msg": "success data anand",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "msg": "invalid data anand",
                        "data": serializer.errors,
                    }
                )
        except Exception as e:
            print(e)
            return Response({"status": False, "msg": "Invalid id", "data": {}})

    def delete(self, request):
        try:
            data = request.data
            if not data.get('id'):
                return Response({
                    'status': False,
                    'msg': 'Id is required',
                    'data': {}
                })
            obj = nse_setting.objects.get(id=data.get('id'))
            if request.method == "DELETE":
                obj.delete()
                return Response({
                    'status': True,
                    'msg': 'successfully deleted data',
                })
            else:
                return Response({
                    'status': False,
                    'msg': 'Provide Delete method',
                })
        except Exception as e:
            print(e)
        return Response({
            'status': False,
            'msg': 'Invalid Id',
            'data': {}
        })


@api_view(['PUT'])
def patch_stock(request, pk):

    try:
        data = request.data
        obj = nse_setting.objects.get(id=pk)
        serializer = settingSerializer(obj, data=data, partial=True)
        print("hello")
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'msg': 'success data', 'data': serializer.data})
        else:
            return Response({'status': False, 'msg': 'invalid data', 'data': serializer.errors})
    except Exception as e:
        print(e)
        return Response({'status': False, 'msg': 'Invalid uid', 'data': {}})


@api_view(['DELETE'])
def delete_stock(request, pk):
    try:
        obj = nse_setting.objects.get(id=pk)
        obj.delete()
        return Response({'status': True, 'msg': 'success DELETE data'})
    except Exception as e:
        print(e)
        return Response({'status': False, 'msg': 'Invalid uid', 'data': {}})


@api_view(['GET'])
def get_nse_data(self, request, pk):
    if request.method == 'GET':
        snippets = nse_setting.objects.get(id=pk)
        serializer = settingSerializer(snippets, many=True)
        return Response(serializer.data)
        # nse_objs = nse_setting.objects.all( id = pk)
        # serializer = settingSerializer(nse_objs, many=True)
        # return Response(
        #     {"status": True, "msg": "nse_profit fetched", "data": serializer.data}


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return nse_setting.objects.get(pk=pk)
        except nse_setting.DoesNotExist:
            raise "Http404"

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = settingSerializer(snippet)
        return Response(serializer.data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class PcrStockName(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        nse_objs = pcr_stock_name.objects.all().order_by('-pcr').values()
        serializer = pcr_stock_nameSerializer(nse_objs, many=True)
        return Response(
            {"status": True, "msg": "Stock Details Fetched", "data": serializer.data}
        )

    def post(self, request):

        try:
            data = request.data
            serializer = pcr_stock_nameSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": True, "msg": "Successfully Post Data",
                        "data": serializer.data}
                )
            else:
                return Response(
                    {"status": False, "msg": "invalid data",
                        "data": serializer.errors}
                )

        except Exception as e:
            print(e)
        return Response(
            {
                "status": False,
                "msg": "Somthing Went Wrong",
            }
        )

    def put(self, request):
        try:
            data = request.data
            print(data)
            if not data.get("name"):
                return Response({"status": False, "msg": "name is required", "data": {}})

            obj = pcr_stock_name.objects.get(name=data.get("name"))
            print(obj)
            serializer = pcr_stock_nameSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "msg": "successfully Update Stock Data",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "msg": "invalid data",
                        "data": serializer.errors,
                    }
                )
        except Exception as e:
            print(e)
            return Response({"status": False, "msg": "Invalid StockName", "data": {}})


import requests
import pprint
import json



class index(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        headers = {'user-agent': 'my-app/0.0.1'}
        response = requests.get(url, headers=headers)
        data = response.text
        parse_json = json.loads(data)
        active_case = parse_json['filtered']['data']
        for i in active_case:
            print(i)

# import pyotp


class live_nse(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        nse_objs = live.objects.all()
        serializer = liveSerializer(nse_objs, many=True)
        return Response(
            {"status": True, "msg": "settings fetched", "data": serializer.data})

    def put(self, request):
        try:
            data = request.data
            print(data)
            if not data.get("id"):
                return Response({"status": False, "msg": "name is required", "data": {}})

            obj = live.objects.get(id=data.get("id"))
            serializer = liveSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "msg": "successfully Update Stock Data",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "msg": "invalid data",
                        "data": serializer.errors,
                    }
                )
        except Exception as e:
            print(e)
            return Response({"status": False, "msg": "Invalid StockName", "data": {}})


class Dropdownselect(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        nse_objs = dropdown_stock_name.objects.all()
        serializer = dropdownSerializer(nse_objs, many=True)
        return Response(
            {"status": True, "msg": "Stock Details Fetched", "data": serializer.data}
        )

    def post(self, request):

        try:
            data = request.data
            serializer = dropdownSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": True, "msg": "Successfully Post Data",
                        "data": serializer.data}
                )
            else:
                return Response(
                    {"status": False, "msg": "invalid data",
                        "data": serializer.errors}
                )

        except Exception as e:
            print(e)
        return Response(
            {
                "status": False,
                "msg": "Somthing Went Wrong",
            }
        )

    def put(self, request):
        try:
            data = request.data
            print(data)
            if not data.get("id"):
                return Response({"status": False, "msg": "name is required", "data": {}})

            obj = dropdown_stock_name.objects.get(id=data.get("id"))
            print(obj)
            serializer = dropdownSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "msg": "successfully Update Stock Data",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "status": False,
                        "msg": "invalid data",
                        "data": serializer.errors,
                    }
                )
        except Exception as e:
            print(e)
            return Response({"status": False, "msg": "Invalid StockName", "data": {}})

