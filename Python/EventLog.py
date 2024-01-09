import abi
import requests
from web3 import Web3

api_key = 'UEM1DEPN6FKE81DAMFRCD2HW3RHT2DPJF2'

address = '0x7564D0ABB9c9AAAdff18259D1bA18F8827B2f0Ec'

url = f'https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'

# Realizează solicitarea HTTP pentru a obține tranzacțiile
response = requests.get(url)
transactions_data = response.json()

event_name="OrderCompleted"
web3=Web3(Web3.HTTPProvider("https://ethereum-sepolia.publicnode.com"))
contract=web3.eth.contract(address=address,abi=abi.shopABI)

event_signature = web3.keccak(text=event_name + '(' + ','.join(param['type'] for param in contract.events[event_name]._get_event_abi().get('inputs', [])) + ')').hex()

# Parcurge tranzacțiile și afișează datele
for transaction in transactions_data['result']:
    hash=transaction['hash']
    txReceipt=web3.eth.get_transaction_receipt(hash)
    logs=txReceipt['logs']
    for log in logs:
        log_topics=log['topics']
        log_data = log['data']

        if web3.to_hex(log_topics[0])==event_signature:
            decodedEvent=contract.events.OrderCompleted().process_log(log)
            mytxt="Id tranzactie: "+web3.to_hex(decodedEvent['args']['orderId'])+"\nDetalii: "+decodedEvent['args']['message']+"\nLista produse:"+str(decodedEvent['args']['prodList'])+"\n------------------------------------"
            print(mytxt)
  #  print(decodedevent)

#print(  contract.events["OrderCompleted"])
#print(vent_signature)

