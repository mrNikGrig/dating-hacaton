from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat_page():
    """Страница для загрузки и анализа чатов"""
    return render_template('chat.html')


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # if request.method == 'POST':
#     #     # ... существующая логика обработки файла ...
#     #     return render_template('index.html', 
#     #                          analysis=analysis_results,
#     #                          filename=unique_filename)
    
#     return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)