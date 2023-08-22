from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alrajhi.html')
def alrajhi():
    return render_template('alrajhi.html')  # Replace 'alrajhi.html' with the actual filename

@app.route('/aramco.html')
def aramco():
    return render_template('aramco.html')  # Replace 'aramco.html' with the actual filename

@app.route('/jarir.html')
def jarir():
    return render_template('jarir.html')  # Replace 'jarir.html' with the actual filename

@app.route('/stc.html')
def stc():
    return render_template('stc.html')  # Replace 'stc.html' with the actual filename

if __name__ == '__main__':
    app.run(debug=True)
