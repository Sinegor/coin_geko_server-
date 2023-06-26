function send_request() {
  function construct_data(){
      let cryptoSheet = SpreadsheetApp.openById('12WpFL4N-Uj8BjDKbqkezcAcBA8mX8aLMwJ-sX-XokKU')
      let investSheet = cryptoSheet.getSheetByName('Invest')
      let sizeSheet = investSheet.getLastRow()
      let crudArrow = investSheet.getRange(2,3,sizeSheet-1,3).getValues()
      let coinsArrow = []
      for (let coin of crudArrow){
        coinsArrow.push(coin[0])
      }
      return coinsArrow
    }
  
  function requestData(coins){
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
      let cryptoSheet = SpreadsheetApp.openById('12WpFL4N-Uj8BjDKbqkezcAcBA8mX8aLMwJ-sX-XokKU')
      let investSheet = cryptoSheet.getSheetByName('Invest')
      let sizeSheet = investSheet.getLastRow()
      for (let i=2; i<sizeSheet+1; i++){
        let currentCoin = investSheet.getRange(i,3).getValue()
        let cellPrice = investSheet.getRange(i,priceColumn)
        let cellSupplay = investSheet.getRange(i, supplayColumn)
        if (typeof(data[currentCoin]) == 'object'){
          cellPrice.setValue(data[currentCoin]['price'])
          cellSupplay.setValue(data[currentCoin]['circulating_supply'])
        }else{
          cellPrice.setValue(data[currentCoin])
          cellSupplay.setValue(data[currentCoin])
        }
      }
     }
  let coinsList = construct_data()
  let coinGekoData = requestData(coinsList)
  setCellValues(coinGekoData, 8, 16)
}
send_request()
