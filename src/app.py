from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai')
def software():
    return render_template('ai.html')

@app.route('/docs')
def docs():
    return render_template('docs.html')

# if __name__ == '__main__':
#     app.run(debug=True)
