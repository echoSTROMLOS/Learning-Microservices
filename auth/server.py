import jwt, datetime, os 
from flask import Flask, request, render_template

import pymysql
import pymysql.cursors

server = Flask(__name__)

@server.route('/login', methods=['POST']) 
def login():
    auth = request.authorization 
    if not auth:
        return "missing credentials", 401 
   
    connection = pymysql.connections.Connection(
                host= os.environ.get("MYSQL_HOST"),
                user= os.environ.get("MYSQL_USER"),
                password = os.environ.get("MYSQL_PASSWORD"),
                database= os.environ.get("MYSQL_DB"),
                port= int(os.environ.get("MYSQL_PORT"))   
            )
    cursor = connection.cursor()
    sql_c = "SELECT email, password FROM user WHERE email=%s", (auth.username)
    res = cursor.execute(sql_c)
    if res > 0 :
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401        

def createJWT(username, secret, authz):
    return jwt.encode(
        {
        "username" : username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc)
        + datetime.timedelta(days=1),
        "iat" : datetime.datetime.utcnow(),
        "admin" : authz,
        },
        secret,
        algorithm="HS256",
    )


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401
    # #bearer <token>
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode (
            encoded_jwt,
            os.environ.get("JWT_SECRET"),
            algorithms= ["HS256"]
        )
    except:
        return "not authorized", 403
    
    return decoded, 200



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
