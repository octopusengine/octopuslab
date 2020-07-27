from flask import Flask, request, render_template
from os import listdir
app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    input_text = request.form['text_box']
    if request.method == 'POST':
        with open('display.txt', 'w') as f:
            f.write(str(input_text))
    return render_template('index.html', text=input_text)


@app.route('/display.txt')
def test():
    with open('display.txt', 'r') as f:
        return f.read()


if __name__ == '__main__':
    app.debug = True
    app.run()
