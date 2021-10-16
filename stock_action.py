import http.client
import json
from base64 import b64encode
from stock_checking import stockData
import math

class stockDo:

    def __init__(self, login, password) -> None:
        self.login = str(login)
        self.password = str(password)
        self.header = {
            "Authorization": "Basic {}".format(
                b64encode(bytes(f"{self.login}:{self.password}", "utf-8")).decode("ascii")),
            "Content-Type": "application/json"
        }
    def stock_action(self, exchange, share, buySell, amount):
        conn = http.client.HTTPSConnection("zsutstockserver.azurewebsites.net")
        # Klasa zczytuje ceny i ilosc akcji sprzedazy/kupowania
        # Cena danej spolki
        # Limit czyli ilosc dostepnych akcji, przyda sie zeby program nie chcial kupic wiecej niz jest
        info = stockData()
        price = 0
        if buySell == "buy":    #dla kupienia trzeba sprawdzic cene sprzedazy i na odwrot
            price = (info.check_price(exchange, share, "sell"))[0]
            price = math.ceil(price)    #zaokraglenie do calkowitych od gory
            limit = (info.check_price(exchange, share, "sell"))[1]
            if limit < amount:      #jezeli wiecej masz kupic niz mozna ustawia sie na max dostepnych
                amount = int(limit)
        elif buySell == "sell":
            price = (info.check_price(exchange, share, "buy"))[0]
            price = math.floor(price)   #zaokraglenie do calkowitych od dolu
            limit = (info.check_price(exchange, share, "buy"))[1]
            if limit < amount:
                amount = int(limit)
        body = json.dumps({
                "stockExchange":f'{exchange}',
                "share":f'{share}',
                "amount":amount,
                "price":price
                })

        #komenda zakupu
        conn.request("POST", url=f"/api/{str(buySell)}offer", headers=self.header, body=body)   #wysyla zlecenie
        if conn.getresponse().status == 200:
            return "ok"
        else:
            print("ERROR")
            print(conn.getresponse().read())

        #print(response)
        #print(response.status)





if __name__ == "__main__":
    mail = input("podaj mail ")
    password = input("podaj haslo ")
    gielda = input("Podaj w tej kolejnosci po spacji: gielda nazwa_akcji buy_or_sell ilosc: ")
    gielda = gielda.split()
    action = stockDo(mail, password)
    for i in range(5):
        action.stock_action(gielda[0],gielda[1],gielda[2],int(gielda[3]))
    