from flask import Flask, redirect, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'exemplo'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Only peoples with a valid Token can view this!'})

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'teste':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        return redirect('/protected?token={}'.format(token))
    return make_response('Could verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)