from http import HTTPStatus

from vereinswebseite import app, db
from vereinswebseite.models import AccessTokenSchema, AccessToken
from flask import request
from uuid import uuid4

from vereinswebseite.request_utils import success_response, generate_error, generate_success

OneAccessToken = AccessTokenSchema()
ManyAccessToken = AccessTokenSchema(many=True)

AccessTokenLength = 8

token_invalid = generate_error("Registrierungscode existiert nicht", HTTPStatus.NOT_FOUND)


@app.route('/accessToken/validate')
def validate_access_token():
    token = request.json['token']
    access_token = AccessToken.query.get(token)

    return generate_success({
        "valid": access_token is not None
    })


@app.route('/accessToken/delete')
def delete_access_token():
    token = request.json['token']
    access_token = AccessToken.query.get(token)

    if not access_token:
        return token_invalid

    db.session.delete(access_token)
    db.session.commit()
    return success_response


@app.route('/accessToken', methods=["POST"])
def create_access_token():
    access_token = str(uuid4())[0:AccessTokenLength].upper()
    token = AccessToken(access_token)

    db.session.add(token)
    db.session.commit()

    result = OneAccessToken.jsonify(token)

    return result


@app.route('/accessToken', methods=['GET'])
def all_access_token():
    all_tokens = AccessToken.query.all()

    response = {"tokens": []}

    for token in all_tokens:
        response["tokens"].append(token.token)

    return response
