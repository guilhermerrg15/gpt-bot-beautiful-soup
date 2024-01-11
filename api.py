from flask import Flask, request
import json
import uuid

app = Flask(__name__)

@app.route('/logs')
def list():
    lista = []
    try:
        with open("db.json", "r") as arq:
            lista = json.loads(arq.read())
    except Exception as e:
        return {"message": str(e)}, 400
    return lista, 200

@app.route('/logs', methods=["POST"])
def create():
    lista = []
    body = request.json
    body["_id"] = str(uuid.uuid4())
    with open("db.json", "r+") as arq:
        lines = arq.read()
        lista = json.loads(lines)
        lista.append(body)
        arq.seek(0)
        arq.write(json.dumps(lista))
        arq.truncate()
    return body, 201

@app.route('/logs/<string:_id>', methods=["GET"])
def get(_id):
    try:
        with open("db.json", "r") as arq:
            lista = json.loads(arq.read())
            for item in lista:
                if item["_id"] == _id:
                    return item, 200
        return {"message": "Registro não encontrado"}, 404
    except Exception as e:
        return {"message": str(e)}, 400

@app.route('/logs/<string:_id>', methods=["PUT"])
def update(_id):
    try:
        with open("db.json", "r+") as arq:
            lista = json.loads(arq.read())
            for i, item in enumerate(lista):
                if item["_id"] == _id:
                    body = request.json
                    lista[i] = body
                    arq.seek(0)
                    arq.write(json.dumps(lista))
                    arq.truncate()
                    return body, 200
        return {"message": "Registro não encontrado"}, 404
    except Exception as e:
        return {"message": str(e)}, 400

@app.route('/logs/<string:_id>', methods=["DELETE"])
def delete(_id):
    try:
        with open("db.json", "r+") as arq:
            lista = json.loads(arq.read())
            for i, item in enumerate(lista):
                if item["_id"] == _id:
                    deleted_item = lista.pop(i)
                    arq.seek(0)
                    arq.write(json.dumps(lista))
                    arq.truncate()
                    return deleted_item, 200
        return {"message": "Registro não encontrado"}, 404
    except Exception as e:
        return {"message": str(e)}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)


