from telethon import TelegramClient, events
import re
import time
import aiohttp
import asyncio
# pprint.pprint(os.path.abspath(binance.__file__))
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance import BinanceSocketManager

import yaml


def buy(coinToBuy, true):
    global time
    time.sleep(3)
    if (true):
        try:
            test_order = binanceClient.create_test_order(symbol='BNBUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=0.1)
            try:
                buy_limit = binanceClient.create_order(symbol='BNBUSDT', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=0.1)
                time.sleep(3)
                order = binanceClient.get_all_orders(symbol='BNBUSDT', limit=1)
                if order:
                    time = order[0]['time']
                    bought_at = buy_limit['fills'][0]['price']
                    print(f"order {order[0]['orderId']} has been placed on BNB with {order[0]['origQty']} at {time} and bought at {bought_at}")
                else:
                    print('Could not get last order from Binance!')
                    time.sleep(3)
            except Exception as e:
                print(e)
                time.sleep(3)
        except BinanceAPIException as e:
            print (e.status_code)
            print (e.message)
            time.sleep(3)

def checkMessage(event):
    @client.on(events.NewMessage(dictionary['channelID']))
    async def my_event_handler(event):
        print(event.message.message)
        flag = False
        coinToBuy = ''
        for x in dictionary['coins']:
            if x not in event.message.message:
                continue
            else:
                for y in dictionary['wordsForConfirmation']:
                    if y in event.message.message:
                        flag =True
                        coinToBuy = x
                        print(x)
                        buy(coinToBuy)
                        break
                    else:
                        continue
                break

if __name__ == '__main__':

    stream = open("config.yaml", 'r')
    dictionary = yaml.load(stream, Loader=yaml.FullLoader)

    if dictionary['testnet']:
        binanceClient = Client(dictionary['TEST_API_KEY'], dictionary['TEST_API_SECRET'])
    else:
        binanceClient = Client(dictionary['LIVE_API_KEY'], dictionary['LIVE_API_SECRET'])

    if dictionary['testnet']:
        binanceClient.API_URL = dictionary['testnet_URL']

    client = TelegramClient(dictionary['bot_token'], dictionary['api_id'], dictionary['api_hash']).start()
    bsm = BinanceSocketManager(binanceClient)
    checkMessage(client)
    client.run_until_disconnected()