from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response, render_template

app = Flask(__name__)


def data_import() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'citiesData'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM biostats')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


@app.route('/')
def index() -> str:
    js = json.dumps(data_import())
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route('/index/<int:bio_id>', methods=['GET'])
def record_view(bio_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats WHERE id=%s', bio_id)
    result = cursor.fetchall()
    return render_template('index.html', title='index Form', biostats=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')