from flask import Flask, request, jsonify

from src.feiras import search_feiras
from src.sympla import search_sympla

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def getHelloWorld():
    return 'Hello World'


@app.route('/search', methods=['POST'])
def postSearch():
    data = request.json
    # print(data['search'])
    result_list = []
    pages = set()
    events_list_filter = set()

    try:
        result_feiras = search_feiras(data['search'])
        result_sympla = search_sympla('https://www.sympla.com.br/categorias', data['search'], pages, events_list_filter)

        if result_feiras == 'except':
            raise Exception('Error no site feiras')
        if result_sympla == 'except':
            raise Exception('Error no site Sympla')

    except Exception as e:
        error = {
            "result": False,
            "message": e.__str__()
        }
        return jsonify(error), 400

    for i in range(len(result_feiras)):
        result_list.append(result_feiras[i])

    for result in result_sympla:
        if result.name != 'Sem Titulo':
            result_list.append(result.toJSON())

    return jsonify(result_list)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=8000)
