import hashlib
import hmac
import base64


def createSecretHash(client_id, client_secret, username):
    message = username + client_id
    key = str(client_secret).encode('utf-8')
    msg = str(message).encode('utf-8')
    secret_hash = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256)
    return base64.b64encode(secret_hash.digest()).decode()
