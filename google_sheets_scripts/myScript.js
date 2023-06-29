function send_request() {
// Get their table list of coins in the form of an array
  function construct_data(){
      let cryptoSheet = SpreadsheetApp.openById('12WpFL4N-Uj8BjDKbqkezcAcBA8mX8aLMwJ-sX-XokKU')
      let investSheet = cryptoSheet.getSheetByName('Coin Geko ids')
      let sizeSheet = investSheet.getLastRow()
// crudArrow is array of arrays
      let crudArray = investSheet.getRange(2,1,sizeSheet-1,1).getValues()
      let coinsArray = []
      for (let coin of crudArray){
        coinsArray.push(coin[0])
      }
      return coinsArray
    }
  
  function requestData(coins){
  //send request to server-layer
      let requestUrl = 'http://94.142.136.139:80/crypto/cryptodata'
      let options = {
        'method': 'post',
        'contentType': 'application/json',
        'payload': JSON.stringify(coins)
      }
      let crudCoinGekoResp = UrlFetchApp.fetch(requestUrl, options)
      let result = crudCoinGekoResp.getContentText()
      return JSON.parse(result)
      }
  
  function setCellValues(data, priceColumn, supplayColumn){
//Place the received data to the corresponding cells of the sheet
      let cryptoSheet = SpreadsheetApp.openById('12WpFL4N-Uj8BjDKbqkezcAcBA8mX8aLMwJ-sX-XokKU')
      let investSheet = cryptoSheet.getSheetByName('Invest')
      let sizeSheet = investSheet.getLastRow()
      for (let i=2; i<sizeSheet+1; i++){
        let currentCoin = investSheet.getRange(i,2).getValue()
        let cellPrice = investSheet.getRange(i,priceColumn)
        let cellSupplay = investSheet.getRange(i, supplayColumn)
        if (currentCoin in data){
          cellPrice.setValue(data[currentCoin]['price'])
          cellSupplay.setValue(data[currentCoin]['circulating_supply'])
        }else{
          cellPrice.setValue('Проверьте правильность заполнения полей "Symbol" и "Coin Geko ids"')
          cellSupplay.setValue('Error')
        }
      }
     }
  let coinsList = construct_data()
  let coinGekoData = requestData(coinsList)
  setCellValues(coinGekoData, 7, 15)
}



