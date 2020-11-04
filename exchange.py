import requests
import csv
from flask import Flask, render_template, request, redirect


app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get('rates')


def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)


def rates_to_csv():
    fieldnames = ['currency', 'code', 'bid', 'ask']
    with open('rates.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rates)
rates_to_csv()


def convert(self, code, amount):
    initial_amount = amount
    result = round((amount * code),4)
    return result


@app.route('/form', methods=["GET", "POST"])
def form():
    codes = get_codes()
    result = ""
    if request.method == "POST":
        data = request.form
        currency = data.get('code')
        amount = data.get('amount')
        for rate in rates:
            print(rate)
            if rate.get('code') == currency:
                ask = rate.get('ask')
                break
        result = float(amount) * float(ask)
    return render_template("API_Zadanie.html", codes = codes, result = result)

