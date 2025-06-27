from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'
@app.route('/', methods=['GET', 'POST'])

def index():

    if 'shifts' not in session:
        session['shifts'] = []
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        
        if not date or not name:
            error = "日付とスタッフ名は必須です。"
            return render_template('index.html', error=error)

        shifts = session['shifts']
        shifts.append({'date': date, 'name': name})
        session['shifts'] = shifts 

        return redirect(url_for('result'))
    return render_template('index.html')



@app.route('/result')
def result():
    shifts = session.get('shifts', [])

    return render_template('result.html', shifts=shifts)

if __name__ == '__main__':
    app.run(debug=True, port=1111)