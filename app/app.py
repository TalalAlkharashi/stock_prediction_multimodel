from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alrajhi.html')
def alrajhi():
    company_data = yf.download('1120.SR', period='1mo')
    price = company_data['Close']
    date = company_data.index
    return render_template('alrajhi.html', price = price,  date = date)  # Replace 'alrajhi.html' with the actual filename

@app.route('/aramco.html')
def aramco():
    company_data = yf.download('2222.SR', period='1mo')
    price = company_data['Close']
    date = company_data.index
    return render_template('aramco.html', price = price,  date = date)  # Replace 'aramco.html' with the actual filename

@app.route('/jarir.html')
def jarir():
    company_data = yf.download('4190.SR', period='1mo')
    price = company_data['Close']
    date = company_data.index
    return render_template('jarir.html', price = price,  date = date)  # Replace 'jarir.html' with the actual filename

@app.route('/stc.html')
def stc():
    company_data = yf.download('7010.SR', period='1mo')
    price = company_data['Close']
    date = company_data.index
    return render_template('stc.html', price = price,  date = date)  # Replace 'stc.html' with the actual filename

if __name__ == '__main__':
    app.run(debug=True)
