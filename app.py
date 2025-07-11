from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

EMOJI_MAP = {
    '吉田': '🐱',
    '大野': '🐶',
    '藤井': '🐰',
}

WEEKDAYS = ['月', '火', '水', '木', '金', '土', '日']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'shifts' not in session:
        session['shifts'] = []

    if request.method == 'POST':
        date = request.form.get('date')
        name_with_emoji = request.form.get('name')

        if not date or not name_with_emoji:
            error = "日付とスタッフ名は必須です。"
            return render_template('index.html', error=error)

        name = name_with_emoji.split()[0]
        emoji = EMOJI_MAP.get(name, '')
        formatted_name = f"{name} {emoji}"

        weekday = WEEKDAYS[datetime.strptime(date, "%Y-%m-%d").weekday()]

        shifts = session['shifts']
        shifts.append({'date': date, 'weekday': weekday, 'name': formatted_name})
        session['shifts'] = shifts

        return redirect(url_for('result'))

    return render_template('index.html')


@app.route('/result')
def result():
    shifts = session.get('shifts', [])
    grouped_shifts = defaultdict(list)

    try:
        sorted_shifts = sorted(shifts, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        for idx, shift in enumerate(sorted_shifts):
            grouped_shifts[shift['date']].append({
                'name': shift['name'],
                'weekday': shift['weekday'],
                'index': idx
            })
    except Exception:
        for idx, shift in enumerate(shifts):
            grouped_shifts[shift['date']].append({
                'name': shift['name'],
                'weekday': shift.get('weekday', ''),
                'index': idx
            })

    return render_template('result.html', grouped_shifts=grouped_shifts)

@app.route('/clear')
def clear():
    session['shifts'] = []
    return redirect(url_for('result'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_shift(index):
    shifts = session.get('shifts', [])
    if 0 <= index < len(shifts):
        del shifts[index]
        session['shifts'] = shifts
    return redirect(url_for('result'))

if __name__ == '__main__':
    app.run(debug=True, port=1111)