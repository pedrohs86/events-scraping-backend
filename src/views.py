from flask import Blueprint, request, jsonify

from src.bots.feiras import search_feiras
from src.bots.sympla import search_sympla
from src.common.utils import ResponseAPI

bp = Blueprint("bp", __name__)

@bp.route('/search', methods=['POST'])
def postSearch():
    data = request.json if request.json is not None else {}  # type: ignore 
    result_list = []
    pages = set()
    events_list_filter = set()

    try:
        result_feiras = search_feiras(data)
        result_sympla = search_sympla('https://www.sympla.com.br/categorias', data, pages, events_list_filter)
        
        if 'except' in result_feiras:
            raise Exception('Error no site feiras')
        if 'except' in result_sympla:
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
    
    return ResponseAPI(ResponseAPI.SUCCESS, 'Successfuly', result_list)

@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response