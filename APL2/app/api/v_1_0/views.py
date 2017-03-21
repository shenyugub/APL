from . import api
from flask import jsonify, g
from . import auth_basic, auth_token


@api.route('/<int:uid>')
def test(uid):
    return 'id = %d' % uid


@api.route('/login')
@auth_basic.login_required
def login():
    token = g.user.generate_auth_token(2592000)
    return jsonify({'status': 0, 'message': '', 'token': token})


@api.route('/notes/')
@auth_token.login_required
def get_notes():

    notes = g.user.notes
    return jsonify({'status': 0, 'message': '', 'notes': [note.to_json() for note in notes]})


# @api.errorhandler(404)
# def page_not_found(e):
#     return "Api: Page Not Found"
#
#
# @api.errorhandler(500)
# def server_error(e):
#     return "Api: Server Error"
#
