## 最簡單的form 是由html的 form tag組成

`action=""` 表單完成後要丟到哪個位址，空白則代表這個表單原本的位址
`method="get OR post"` 丟的時候要用什麼方法
`<input type="submit" value="進入網站">` 丟出去的動作

django用urls.py 內的url來作為應對的對口，然後用views.py來反應。如果是同一位址，那麼views就要判斷是否有帶資料進來，如果無，則渲染空表單，如果有則處理資料，然後重導至適當的地方。  
當然也可以讓表單用來呈現資料，那就是讓資料放到表單裡然後再渲染。  

## request, views的第一個參數

資料放在request.GET或request.POST中，以字典資料結構存在，另外注意csrf token的處理，這會放在request.META。如果request.POST沒有csrf token的資料則會報錯。  


## django forms.py
