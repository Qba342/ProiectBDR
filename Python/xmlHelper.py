import xml.etree.ElementTree as ET
from typing import List


class clientHandler():
    def __init__(self,databaseFile):
        self._databasefile=databaseFile
        self.tree=ET.parse(databaseFile)

    def getPrivateKey(self):
        root=self.tree.getroot()
        #print(root.find('privateKey').text)
        return root.find('privateKey').text

    def getDetails(self):
        root = self.tree.getroot()
        name=root.find('accdetails/name').text
        surname = root.find('accdetails/surname').text
        address = root.find('accdetails/address').text
        number = root.find('accdetails/phoneNumber').text
        email = root.find('accdetails/email').text
        return (name,surname,address,number,email)

    def setPrivateKey(self,privKey):
        root=self.tree.getroot()
        key=root.find('privateKey')
        key.text=privKey
        self.tree.write(self._databasefile)

    def setDetails(self,name='',surname='',address='',number='',email=''):
        root=self.tree.getroot()
        nameEntity=root.find('accdetails/name')
        surnameEntity=root.find('accdetails/surname')
        addressEntity = root.find('accdetails/address')
        numberEntity = root.find('accdetails/phoneNumber')
        emailEntity = root.find('accdetails/email')

        if name!='':
            nameEntity.text=name
        if surname!='':
            surnameEntity.text=surname
        if address!='':
            addressEntity.text=address
        if number!='':
            numberEntity.text=number
        if emailEntity!='':
            emailEntity.text=email
        self.tree.write(self._databasefile)


class Product():
    def __init__(self,productID,productName,productDetail,productPhoto):
        self._productID=productID
        self._productName=productName
        self._productDetail=productDetail
        self._productPhoto=productPhoto

    def getData(self):
        return {"id":self._productID,"name":self._productName,"details":self._productDetail,"image_path":self._productPhoto}


class productHandler():
    def __init__(self,databaseFile):
        self._databasefile=databaseFile
        self.tree=ET.parse(databaseFile)
        self._productList=[]

    def _updateProducts(self):
        root=self.tree.getroot()
        prodcutEntities=root.findall('product')
        for i in prodcutEntities:
            x=Product(i.find('productID').text,i.find('productName').text,i.find('productDetail').text,i.find('productPhoto').text)
            self._productList.append(x)

    def getProductList(self)->List[Product]:
        self._updateProducts()
        return self._productList

    def getProductListIDS(self)->List[int]:
        returnList=[]
        root = self.tree.getroot()
        prodcutEntities = root.findall('product')
        for i in prodcutEntities:
            x = int(i.find('productID').text)
            returnList.append(x)
        return returnList
#c=clientHandler('clientDatabase.xml')
#c.setDetails(surname='cuba')

#p=productHandler('productDatabase.xml')
#p.getProductListIDS()
#list=p.getProductList()
#print(list)