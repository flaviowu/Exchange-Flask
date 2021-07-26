from flask import Flask, render_template, request, redirect
import requests
API_KEY = ''


def getMoedas():
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/codes'
    req = requests.get(url)
    dados = req.json()
    return dados['supported_codes']


def getCotacao(moedas):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{moedas["de"]}/{moedas["para"]}'
    req = requests.get(url)
    dados = req.json()
    return dados['conversion_rate']


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    moedas = getMoedas()
    if request.method == 'POST':
        moeda1 = request.form['moeda1']
        moeda2 = request.form['moeda2']
        quantia_str = request.form['quantia']
        quantia_str = quantia_str.replace(",",".")
        if quantia_str.replace(".", "").isnumeric() == True:
            quantia_float = float(quantia_str)
        else:
            quantia_float = 1.0

        cambio = getCotacao({'de': moeda1, 'para': moeda2})
        quantia_convertida = round(quantia_float * cambio, 4)
        resultado = str(f"{moeda1} {quantia_float:.2f} = {moeda2} {quantia_convertida}")
        return render_template('index.html', moedas=moedas, resultado=resultado)

    return render_template('index.html', moedas=moedas)


if __name__ == '__main__':
    app.run(debug=True)
