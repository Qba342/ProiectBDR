interface IERC20 {
    function totalSupply() external view returns (uint);

    function balanceOf(address account) external view returns (uint);

    function transfer(address recipient, uint amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint);

    function approve(address spender, uint amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}


contract Shop {

    ///////////DECL ZONE//////////////////
        struct Product {
        uint256 id;
        uint256 price;
    }//aici este un produs. dorim sa asociem id-ul cu pretul
    Product[] private _productList;//aici e lista de produse care va fi de fapt baza de date la nivelul acestui contract
    mapping(uint256 => bool) private isIdSet;
    mapping(uint256=> uint256) private priceMap;
    
    address private _leu;
    address private _owner;
    /////////////END DECL ZONE///////////////
    /////////////CONSTRUCTOR/OWNER////////////
    constructor  () public{
        _owner=msg.sender;
    }

    modifier onlyOwner() {
    require(_owner == msg.sender, "Ownership Assertion: Caller of the function is not the owner.");
    _;
    }
    //////////////END CONSTRUCTOR/OWNER///////////

    ///////////////////METHODS/SETTERS/////////////
    function changeLeuContract(address newLeuContract) public onlyOwner{
        _leu=newLeuContract;
    }

    function addProduct(uint256 FCid, uint256 FCprice)public onlyOwner{

        require(!isIdSet[FCid],"This id is already set");//daca dam de un id gata setat, ne intoarcem
        Product memory newProduct=Product(FCid,FCprice);
        _productList.push(newProduct);
        isIdSet[FCid]=true;
        priceMap[FCid]=FCprice;
    }

    function removeProduct(uint256 FCid)public onlyOwner{
        require(isIdSet[FCid],"You cannot delete the product because it doesnt exist");
        uint256 indexToRemove = findObjectIndex(FCid);
        _productList[indexToRemove] = _productList[_productList.length - 1];
        _productList.pop();
        isIdSet[FCid]=false;
        priceMap[FCid]=0;

    }



    function buyFromShop(uint256[] memory combinedList)public  {

        require(combinedList.length%2==0,"Lista data ca argument nu este ok");

        uint256[] memory listOfProdIDs=new uint256[](combinedList.length/2);
        uint256[] memory listOfNumbersOrdered=new uint256[](combinedList.length/2);

        for (uint256 i=0; i<combinedList.length/2; i++){
            listOfProdIDs[i]=combinedList[i];
            listOfNumbersOrdered[i]=combinedList[combinedList.length/2+i];
        }

        uint256 totalValue=0;
        for (uint256 i = 0; i < listOfProdIDs.length; i++)
        {
            require(isIdSet[listOfProdIDs[i]],"Un produs din lista trimisa nu se afla in baza de date");
            require(listOfNumbersOrdered[i]>0,"Nu poti comanda -1 produs :) ");
            totalValue+=priceMap[listOfProdIDs[i]]*listOfNumbersOrdered[i];
        }
        //return totalValue;
        
        IERC20 leu=IERC20(_leu);//instantiem contractul de lei
        leu.transferFrom(msg.sender,_owner,totalValue);//transferam de la adresa care doreste sa cumpere la cel care detine contractul

    }

    ////////////////////END METHODS/SETTERS////////////


    //////////////////////GETTERS/HELPERS/////////////////
     function getOwner() external view returns (address){
        return _owner;
    }
    function getProductList() external view returns (Product[] memory){
        return _productList;
    }

    function findObjectIndex(uint256 FCid) internal view returns (uint256) {
        //
        for (uint256 i = 0; i < _productList.length; i++) {
            if (_productList[i].id == FCid) {
                return i;
            }
        }
        return 0; // Return a large value if the object is not found
    }
    ////////////////////END GETTERS/HELPERS///////////////

}