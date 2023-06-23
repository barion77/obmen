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
    return jsonify({'fullName': 'test', 'shortName': 'test', 'imageUrlP': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAGoAagMBEQACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAGAAMEBQcCAQj/xABBEAABAgQDBAYGBwYHAAAAAAABAgMABAURBiExEkFRYRMycYGR8CJCobHB0QcUFTRScuEzYmOC0vEjJENzkpOy/8QAGgEAAgMBAQAAAAAAAAAAAAAAAAQBAgMFBv/EAC0RAAICAQMCBQMEAwEAAAAAAAABAgMRBCExEkEFEyIyUYGx0RQzkfBhcaFS/9oADAMBAAIRAxEAPwDcYAFAAoAItQqEpTmelnX0NI3bRzPYN8UnZGtZk8EpN8ApPY8CyUUmRW9/FdyT4frCFviEV7V/P4No0t8lO9iPEUwfvTMuD6raAbePzhOXiFj7mipiRzUq4Tc1h7wPzjL9dZ8st5S+B1quYhY6tRS7ydQPlF46+xd/sR5MSzlMcTzBAqdPS4je4wTcd2fwhqvxH/0s/wDDOVHwFNIr9Nq4H1OYSXN7SslDu390dCu+uz2sxlBrktI2KigAUACgAUACgAGMTYrbpqjJyCRMTx3eq328+UJanVqrZcmsK3ICHUPTkwZmpPKmHlfiOQ5W8iOJZfObzkajBIkpbSZR5YyU3YjsjOKytzWIyhW2kKEVaw8EcHUQQKABG9jYXIESlkCCkJefJ2Sw+nNK0GxvG+9e6eSHFBXQMXvSriJOunaQcm5r+r5+/WOlptdnaf8AP5Fp1fAdIUFpCkkEEXBB1EdUXOoAFAAoABjGWIVU1pMlIkGefGX8NPHthLV6nylhcmtcOpgRLsBlJJO24rNazqox5+c3JjiWBy44xQkeZSpxtxCBfpLDuF/nGkXsWj8nKZNTI2SsHlaIm8lms8CLS91j3xUr0saeUWUbSwm2nWiUk2HSyveqrcqxtvLQC4boSTqNPnDddOdkVbSGKdOpnJkOpUFAm1wLRa+vpjgE8lu42h1BQ4m6TuhFNp5QNF1g6urp0yikz7hVLuG0u6r1TwPLz2djRapex8fYVtr7o0ER1xcUAEWpzrdOkXpt7qNIKrcTuHeYpZNVxcmSll4MrQ67OTDtQmjtPTCib8E7vPC0eavsc5vI9COEOnIXjAuGuHZYfZDBdbSFG5zGepjuaOKVK2FbPcWqWmho2gd0NdK+CmWNqQgq6ifCDpj8Bli6JA9RPgIOlfAZZw5LtOJKVtNqB1BSDeDC+AywZxBhCn1GXWiXablpko2EuBF0p/l3d0V8iGcrYt5j7gqzQ5iivNy8ynqgnaT1VdhjlattNpjMGnHKJsIFhqZZD7JQcjqk8DFoy6XkhrIfYLrCqrSgl8/5qXPRu31PA+d4Mej0lvmQ35QlZHpYQQ0ZgT9I04Vpk6Yg/tldI5+UafHwjm+IW4io/X8G1McvIObo4Q4SKex9anmWbXuq5HZF64uUsIhvAZTFQlKTJXmnigNj01BJNvAR26JwrSrb3FZqUvVgepM43UZBubYKy07cpLiClRFyNCARpDTae6M8PuSMkm6jaAkqK3iijUNbSarOply6bICgSTzsLkJ5nKBkZLCSnpadRtyryXE63HDjGULYWe1l3FrkfKQRpGhUgVGSTPsLYcyNrtq/CYzvpjbDDLwk4vIDrSpClIWLLSSlQ4Eax52UXFtMbR5EATcKzZp+J2k3s1Op2Ffm3e23iY6Xh9vTNL6GF0co0vOO6KGaYpd+sYtmc7pYaSgcsgfiY4PiEs2MbpXpIUc43CXCsoEocm1dcnYRyG/zyh3Swx6jG19ijxPjuhU2ruSTi5hx5qyXi01dKTbS9xfLhDMtLKx9SIhaorDC/DFRlapQ5WckXC4w4FbKikpPWI0PMGHaK3CtRZlOSlJssHWgsEHQxqtipn+LcJSdYxR9oTKVqWltCFIRkHABltfpaEr9TOMnCKNYVprLL6mt/USlSAAU5bI0A4QpVmEuruaS9SwE42VAEaHMR2FhrIqNLHpkRBIG4nYDNUKxo6kK79D7vbHF18Om7PyM1P0lTCRqR5twsKl5lPWZdSoWjamXTLJSSya+hQWhK06KFxHqMZEDLKqb4mqv+6PjHndd+4/9jtXCOBCZqwvoV00pm2hJ8bmOjTtWjCW8mfP2JZZ+YrU3NpSpaZl1Tpy6tzcg9kdODXSjBp5Nx+i9gM4HpeyrauhZvbi4o/GNU8ojuFgOYEQBT1P74rsHujn6j9xm8PaRowLF7J3Mo1f8IjqU/towlyz1zr90XIBfGA/xpU8Uq94jleJcx+oxT3B6OYbEao/dFfmT7xF6/cRLg1mmkmnSpOpZRfwEepr9iOfLkznETXQYsn0nRwJWPAfOOFr44sf97DdPtIsIGwUYcd6Smlq+aFkHsOfzh2iWYYMpL1ZAHHNAdYqz06wp5th9QUFMrNkqIzuNMznD1Nia6TKUXyHmBA5L4UkG1jbsF55A9dXDKHYNOKMmsMv21rLg9EAc4thAV1SznFW4D3RzNR+4zevgaS1mNVK4RikX4L1ADbaU7ki0daK6YpCzeXkaJzJMSAL4tUFPspGqEX8THJ8QeZpf4GaV6WygjmmpFqAKmUNp6zjiUjz3RpUsyKy4NgZQGmW2xohIT4R6pbLAgAv0hSvQVGRqIHoLHQuHhw9/sjl+I18S+TeiXYo44o0WdAeUzNLOfRFHp2Hh8Y1peGRJZCQSAnpbaSptSFX1zBjoV6eVkepMxc+l4J0lKiVlW2LD0b6aZkmH6oOEFFmMnl5JIFo0KkKakFPvFwLAvaFbdPKcupM1jNJYHJeUSyoKWoKWNLbovVp1B5fJEp52HXTlbdG5QYKhvyAzJMD2AC598zc5MPqNkKNkA7k6CPP32eZY5D0Y9MUiBC4D1FlftDEskxa6GT0zndmPd7Ye0NfVYv7wY2ywjUrR6ETKzElMFXpD8pYdIRtNk7lDT5d8Y31+ZBxLQlh5M0lXFKQUOgh1s7CwdbiPM2R6ZD8XlF1Qxm8q+VgNnjFqu4MLKSgsyKAM03PvMdvS7VL+9xWx+om9IN4IhgoeF0bgYAPOkUrqi0BGT1OWZ1gA8dI2DfdvO6Bv5JRR1KY6dtTLBOwclrTv5DlHP1N/WuiPBtXHDyygqoS1LISkAXVaEXFYGIbsrXHEttqWs2SBcwsll4Qdgs+j6mLZlHanMos9Nn0L7kfr8BHf0NPTDq+fsJWyy8BfD5kKAADxvRFy0wa1Iouk/eWx/wCvPxMcvXaZP1r6/k3qn2G6GEqkg8gghw3y3WysY5kIuK3Gc5LlmdfZbCGynZGlxDMNROCwijgm8lY5XZ1Li0Et5KIHoRP6y0nyoj8rVJ5SdtxSM9BsRdau0q64kj7VmuKP+MT+qsI8uIjVJs+skfywfqrA8uI0px58gvuKUOB08IxlOU/cycJcCOQipIP1d9LjgbRnsE3POKM2gsbnNBpS8Q1BKbKFPYILqx654Dzz4RtpNK5y3+v4MLbMGoNpShCUISEpSLADQCO8ljYTOoAFAB4pIUkhQBBFiDvgACKtQZuivrnqKguyijtPSf4eafPju5Wo0jj6ocfYYhZ2YzK1aUmmttlZ297aslJ7R8YQexutxtlCXXVuuBJUo3A4REcPclkmLlRxDe1mdIkBxKUp0EBB1ABU1mo/V2yhGQ0U5uHIc4hv4LxS5ZX0ShTeIHLgKYkAbKdIzXyHnt4Rvp9NKzdcfJSy7GyNMp8jL0+VRLSjYQ0jQcTxPOOxCEYR6YibbbyyTFyBQAKABQAKAAfreE6fVFl9AMrNah5rK55jf7DCtulhZvwzSNjiDU1Q6/TibsoqDI9Zs2XbzyMc6zQzi+M/6N43JjYrcvL2TNyc1LqGVltxi49POxbOR0Yhplv2yv8AqV8oMogbcxFKKOzLIedV+6384OeCR1hGIallJ08y6D/qzHo+z+8bQ09s+EUc4ot6bgtlLqZmszCp58aIOSB3b/YOUO16KK3nv/jsZStb4CpCEoSEoSEpSLAAWAEPJY2RkdQAKABQAKABQAKABQAeGADxSUrTZaQocCLxADJkJMm5lGCePRiK+XD4Jyx1tptoWabQgfupAiySXBB1viUB7AAoAFAAoAFAB//Z'})
    full,short,image = db_api.get_coins()
    for x in full:
        data.append({'fullName': x,'shortName': short[counter],'imageUrlP': image[counter]})
        counter +=1
    return jsonify(data)

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

@app.route('/newOrder/<receiveAmount>/<receiveCurrency>/<sendAmount>/<sendCurrency>/<receiver>/<email>/<referalCode>/<status>',methods = ['GET'])
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
    app.run(port=8000, debug=True)