import random
from flask import Flask,jsonify
import db_api
import json
import string
import requests
from flask_cors import CORS
from flask import send_file

db_api.create_db()

app = Flask(__name__, static_folder="static")
CORS(app)



@app.route('/static/<svgFile>')
def serve_content(svgFile):
    return send_file(f'static/{svgFile}', mimetype='image/svg+xml')




@app.route('/calculator/<sendCurrencyName>/<receiveCurrencyName>/<sendAmount>/<receiveAmount>/<isChangeReceiveAmount>',methods = ['POST'])
def calculate(sendCurrencyName,receiveCurrencyName,sendAmount,receiveAmount,isChangeReceiveAmount):
    params  = {'api_key':'e22f49a14d79ce53c6648a3be28a307c4cb0a89afe2469f3feadae3ae98c544b'}
    if 'ERC20' in str(sendCurrencyName):
        sendCurrencyName = 'USDT'
    elif 'TRC20' in str(sendCurrencyName):
        receiveCurrencyName = 'USDT'
    if str(isChangeReceiveAmount) == 'True':
        data = requests.get(f'https://min-api.cryptocompare.com/data/blockchain/mining/calculator?fsyms={receiveCurrencyName}&tsyms={sendCurrencyName}',params=params).text
        data = json.loads(data)
        price = data['Data'][f'{receiveCurrencyName}']['Price'][sendCurrencyName]
        totalPrice = float(receiveAmount)*float(price)
    else:
        data = requests.get(f'https://min-api.cryptocompare.com/data/blockchain/mining/calculator?fsyms={sendCurrencyName}&tsyms={receiveCurrencyName}',params=params).text
        data = json.loads(data)
        price = data['Data'][f'{sendCurrencyName}']['Price'][receiveCurrencyName]
        totalPrice = float(sendAmount)*float(price)
    return jsonify(amount = totalPrice)
    

@app.route('/coins',methods = ['GET'])
def show_index1():
    data = []
    counter = 0 
    full,short,image = db_api.get_coins()
    for x in full:
        data.append({'fullName': x,'shortName': short[counter],'imageUrlP': image[counter]})
        counter +=1
    return jsonify(data,)

@app.route('/user/<id>',methods = ['GET'])
def getUser(id):
    if str(id).isdigit():
        return jsonify(id=int(id))
    else:
        id = db_api.getId()
        db_api.registerUser(id)
        return jsonify(id=id)



@app.route('/transactions',methods = ['GET'])
def transactionsList():
    data = []
    counter = 0 
    txHash,block,fromm,to,value = db_api.transactions()
    for x in txHash:
        data.append({'txHash': x,'block': block[counter],'fromm': fromm[counter],'to': to[counter],'value': value[counter]})
        counter +=1
    return jsonify(data,)

@app.route('/order/<orderId>',methods = ['GET'])
def orderupd(orderId):
    usr = db_api.checkOrder(orderId)
    if not usr:
        return jsonify(error = 'not found')
    else:
        receiveAmount,receiveCurrency,sendAmount,sendCurrency,receiver,email,referalCode,status,wallet = db_api.getOrderInfo(orderId)
        return jsonify(receiveAmount = receiveAmount,receiveCurrency = receiveCurrency,sendAmount = sendAmount,sendCurrency = sendCurrency,receiver = receiver,email = email,referalCode = referalCode,status = status,wallet = wallet)

@app.route('/confirm/<orderId>',methods = ['POST'])
def confirm(orderId):
    db_api.changeStatus(orderId)
    receiveAmount,receiveCurrency,sendAmount,sendCurrency,receiver,email,referalCode,status,wallet = db_api.getOrderInfo(orderId)
    print(referalCode)
    if str(referalCode) != 'null':
        if 'e' in str(sendAmount).lower():
            sendAmount = float(sendAmount)  
            sendAmount = format(sendAmount, 'f')  
        if 'e' in str(receiveAmount).lower():
            receiveAmount = float(receiveAmount)  
            receiveAmount = format(receiveAmount, 'f')  
        telegram_api_url = 'https://api.telegram.org/bot6020406063:AAELjm1Q6gnnMblDZL1Umdia0nB768VW0vQ/sendMessage'
        id = db_api.getUserId(referalCode)
        print(sendAmount)
        print(receiveAmount)
        payload = {
            'chat_id': f'{id}',
            'text': f'[{referalCode}]\n<b>Мамонт обозначил заявку как оплаченную</b>\n\n<b>{sendAmount} {sendCurrency} -> {round(float(receiveAmount),6)} {receiveCurrency}\n{email}\n{status}</b>',
            'parse_mode': 'HTML',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(telegram_api_url, data=json.dumps(payload), headers=headers)
    return jsonify(status = 'confirmed')

@app.route('/msgSave/<text>/<userId>/<timestamp>/<user>',methods = ['POST'])
def msgSave(text,userId,timestamp,user):
    # Пример использования функции send_telegram_message
    telegram_message = f'Сообщение в ТП от пользователя {userId}\n\n{text}'
    inline_keyboard = {
        'inline_keyboard': [
            [{'text': 'Ответить', 'callback_data': f'uans_{userId}'}]
        ]
    }

    send_telegram_message(telegram_message, inline_keyboard)
    db_api.addMsg(text,userId,timestamp,user)
    return jsonify(reponse = 'success')


def send_telegram_message(message, inline_keyboard):
    telegram_api_url = 'https://api.telegram.org/bot6020406063:AAELjm1Q6gnnMblDZL1Umdia0nB768VW0vQ/sendMessage'
    payload = {
        'chat_id': '2146918790',
        'text': message,
        'reply_markup': inline_keyboard
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(telegram_api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print('Message sent successfully.')
    else:
        print('Failed to send message. Error:', response.text)




@app.route('/msgHistory/<id>',methods = ['GET'])
def getUsers(id):
    try:
        messages,timestamp,user = db_api.getMessages(id)
        print(f'msg - {messages}')
        print(f'time - {timestamp}')
        timestamp = sorted(timestamp)
        data = []
        counter = 0 
        for x in timestamp:
            data.append({'text': db_api.get_message(x),'timestamp': timestamp[counter],'user': db_api.get_user(x)})
            counter +=1
        return jsonify(data)
    except:
        return jsonify(error = 'not found')

@app.route('/genTrans',methods = ['GET'])
def transactionsGeneratiin():
    block = random.randint(100000,999999)
    coins = ['ADA','BCH','BNB','BTC','DASH','DOGE','DOT','ETC','ETH','FTM','LTC','MATIC','SHIB','SOL','TRX','USDT','XMR','XRP','XTZ','ZEC','ZRX']
    value = f'{round(random.uniform(0.1, 1.3),2)} {random.choice(coins)}'
    txHash = f'{id_generator(10)}...'
    fromm = f'{address_generator(6)}...'
    to = f'{address_generator(6)}...'
    return jsonify(txHash=txHash,block=block,fromAddress=fromm,to=to,value=value)

@app.route('/newOrder/<receiveAmount>/<receiveCurrency>/<sendAmount>/<sendCurrency>/<receiver>/<email>/<referalCode>/<status>',methods = ['POST'])
def newOrder(receiveAmount,receiveCurrency,sendAmount,sendCurrency,receiver,email,referalCode,status):
    orderIdd = random.randint(111111,999999)
    if str(referalCode) != 'null':
        if 'e' in str(sendAmount).lower():
            sendAmount = float(sendAmount)  
            sendAmount = format(sendAmount, 'f')  
        if 'e' in str(receiveAmount).lower():
            receiveAmount = float(receiveAmount)  
            receiveAmount = format(receiveAmount, 'f')  
        telegram_api_url = 'https://api.telegram.org/bot6020406063:AAELjm1Q6gnnMblDZL1Umdia0nB768VW0vQ/sendMessage'
        id = db_api.getUserId(referalCode)
        payload = {
            'chat_id': f'{id}',
            'text': f'[{referalCode}]\n<b>Мамонт создал заявку</b>\n\n<b>{sendAmount} {sendCurrency} -> {receiveAmount} {receiveCurrency}\n{email}\n{status}</b>',
            'parse_mode': 'HTML',
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(telegram_api_url, data=json.dumps(payload), headers=headers)
    orderId = db_api.addOrder(orderIdd,receiveAmount,receiveCurrency,sendAmount,sendCurrency,receiver,email,referalCode,status)
    return jsonify(orderId = orderIdd)

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def address_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    app.run(port=8000)