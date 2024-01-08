import abi
from web3 import Web3
import time

w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia.publicnode.com"))


tokenContract="0x0A92f94579B117427c1416968d3288C995015255"
shopContract="0x7564D0ABB9c9AAAdff18259D1bA18F8827B2f0Ec"


priv="45a97d0617b02bee539c004cb735054b5e0471eb67a61bff6e45a5fda2f701d4"

class ClientInterface():##o vom folosi inclusiv in cadrul aplicatiei grafice
    def __init__(self, privateKey,details,tokenContract,shopContract):
        self._privateKey=privateKey
        try:
            self._publicKey=w3.eth.account.from_key(str(privateKey))#aici scoatem cheia publica necesara pentru tranzactii
        except:
            print("Cheia privata nu respecta criteriile")
        self._details=details
        self._tokenContract=w3.eth.contract(address=tokenContract,abi=abi.tokenAbi)
        self._shopContract=w3.eth.contract(address=shopContract,abi=abi.shopABI)
        self._tokenAddress=tokenContract
        self._shopAddress=shopContract



    def _allowLeiOnContract(self):#asta se va folosi daca nu exista allowance
        contract = self._tokenContract
        nonce = w3.eth.get_transaction_count(self._publicKey.address)
        TxnBuild=contract.functions.approve(
            shopContract,
            100000).build_transaction({
            'from':self._publicKey.address,
            'nonce':nonce
        })
        signedTX = w3.eth.account.sign_transaction(TxnBuild,self._privateKey)
        responseTX = w3.eth.send_raw_transaction(signedTX.rawTransaction)
        print(w3.to_hex(responseTX))  ##de testat

    def _checkAllowance(self):
        resp=self._tokenContract.functions.allowance(self._publicKey.address,self._shopAddress).call()#trebuie sa avem allow la spend pentru a putea da call functiei
        if resp>10000:#consideram ca daca avem mai multi lei decat trebuie, putem sa facem cumparaturi
            return True
        return False

    def BuyWithLei(self,listOfProdsAndValues,details):#interactiune cu baza de date mare
        contract = self._shopContract
        if self._checkAllowance()==False:#daca nu avem voie sa tranzactionam, vom face allow pe tranzactionare
            self._allowLeiOnContract()
            time.sleep(2)

        nonce = w3.eth.get_transaction_count(self._publicKey.address) #vom vedea cate tranzactii am facut pana acum
        TxnBuild = contract.functions.buyFromShop(
            listOfProdsAndValues,  #
            details
        ).build_transaction({
            'from': self._publicKey.address,
            'nonce': nonce,
        })
        signedTX=w3.eth.account.sign_transaction(TxnBuild,private_key=self._privateKey)
        responseTX=w3.eth.send_raw_transaction(signedTX.rawTransaction)
        print(w3.to_hex(responseTX))##de testat

    def getPublicAddress(self):
        return self._publicKey.address
    def getLeiBalance(self):
        resp = self._tokenContract.functions.balanceOf(self._publicKey.address).call()
        return resp
    def getProductList(self):
        mylist=self._shopContract.functions.getProductList().call()
        firstitems = list(map(lambda x: x[0], mylist))
        return firstitems
    def getRawProductList(self):
        mylist = self._shopContract.functions.getProductList().call()
        return mylist

#intf=ClientInterface(priv,"nuAm",tokenContract,shopContract)
#print(intf.getLeiBalance())
#print(intf._checkAllowance())
#mylist=intf.getProductList()
#firstitems=list(map(lambda x: x[0], mylist))
#print(firstitems)

#intf._allowLeiOnContract()
#intf.BuyWithLei([2,2],'Test')