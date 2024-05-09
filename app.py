from flask import Flask, render_template
from fertility import fertility
from disease import disease
from fertilizer import fertilizer 
from soil import soil
from price import price

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/service')
def service():
    return render_template('service.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
app.register_blueprint(fertility, url_prefix='/fertility')
app.register_blueprint(disease, url_prefix='/disease')
app.register_blueprint(fertilizer,url_prefix='/fertilizer')
app.register_blueprint(soil,url_prefix='/soil')
app.register_blueprint(price,url_prefix='/price')

if __name__ == '__main__':
    app.run(debug=True)
