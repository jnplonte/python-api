from flask import jsonify

def notFound(failed):
    response = jsonify(failed('notfound', ''))
    response.status_code = 404

    return response