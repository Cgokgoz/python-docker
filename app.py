import mysql.connector
import json
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Docker!'


@app.route('/widgets', methods=['GET', 'POST'])
def get_widgets():
    if request.method == 'GET':
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="inventory"
        )
        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM widgets")

        row_headers = [x[0] for x in cursor.description]

        results = cursor.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(row_headers, result)))

        cursor.close()

        return json.dumps(json_data)
    elif request.method == 'POST':

        name = request.form['name']
        description = request.form['description']

        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="p@ssw0rd1",
            database="inventory"
        )
        cursor = mydb.cursor()

        query = "INSERT INTO widgets VALUES (%s,%s); "
        values = (name, description)
        cursor.execute(query, values)
        mydb.commit()

        cursor.close()
        return 'Recorded!'


@app.route('/db')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
