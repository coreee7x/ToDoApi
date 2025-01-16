from flask import Flask, request, send_file, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import uuid

# initialisiere Flask-Server
app = Flask(__name__)

# Swagger UI-Konfiguration
SWAGGER_URL = '/docs'  # URL für Swagger UI
API_URL = '/swagger.json'  # Endpunkt für die Swagger-Datei

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ToDo-Api"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Route für Swagger-Datei
@app.route('/swagger.json', methods=['GET'])
def get_swagger():
    return send_file('swagger.json', mimetype='application/json')

todo_listen = []  # [{id, name}]
todo_einträge = []  # [{id, name, beschreibung, liste_id}]

# Liefert alle Einträge einer Todo-Liste zurück.
@app.route('/getAllEinträge', methods=['GET'])
def getAllEinträgeById():
    params = request.args
    liste_id = params.get('liste_id')

    if not liste_id:
        return jsonify({"error": "Listen-ID fehlt"}), 400
    
    einträge = [eintrag for eintrag in todo_einträge if eintrag['liste_id'] == liste_id]

    return jsonify(einträge), 200

# Route die alle Listen zurückgibt
@app.route('/getAllListen', methods=['GET'])
def getAllListen():
    return jsonify(todo_listen)

# Fügt eine neue Todo-Liste hinzu.
@app.route('/insertListe', methods=['POST'])
def insertListe():
    params = request.json

    if 'name' not in params:
        return jsonify({"error": "Name der Liste fehlt"}), 400
    
    liste_id = str(uuid.uuid4())
    todo_listen.append({"id": liste_id, "name": params['name']})

    return jsonify({"message": "Liste erstellt", "id": liste_id}), 201

# Fügt einen Eintrag zu einer bestehenden Todo-Liste hinzu.
@app.route('/insertEintrag', methods=['POST'])
def insertEintrag():
    params = request.json

    if 'name' not in params or 'beschreibung' not in params or 'liste_id' not in params:
        return jsonify({"error": "Fehlende Felder: name, beschreibung oder liste_id"}), 400
    
    if not any(liste['id'] == params['liste_id'] for liste in todo_listen):
        return jsonify({"error": "Liste mit der angegebenen ID existiert nicht"}), 404
    
    eintrag_id = str(uuid.uuid4())

    todo_einträge.append({
        "id": eintrag_id,
        "name": params['name'],
        "beschreibung": params['beschreibung'],
        "liste_id": params['liste_id']
    })
    return jsonify({"message": "Eintrag erstellt", "id": eintrag_id}), 201

# Aktualisiert einen bestehenden Eintrag einer Todo-Liste.
@app.route('/updateEintrag', methods=['PUT'])
def updateEintrag():
    params = request.json

    if 'id' not in params or 'name' not in params or 'beschreibung' not in params:
        return jsonify({"error": "Fehlende Felder: id, name oder beschreibung"}), 400

    eintrag_id = params['id']
    eintrag = []
    
    for item in todo_einträge:
        if item['id'] == eintrag_id:
            eintrag = item
            break

    if not eintrag:
        return jsonify({"error": "Eintrag mit der angegebenen ID existiert nicht"}), 404

    # Aktualisiere die Felder des Eintrags
    eintrag['name'] = params['name']
    eintrag['beschreibung'] = params['beschreibung']

    return jsonify({"message": "Eintrag erfolgreich aktualisiert", "id": eintrag_id}), 200

# Löscht einen einzelnen Eintrag einer Todo-Liste. 
@app.route('/deleteEintrag', methods=['DELETE'])
def deleteEintrag():
    params = request.json

    if 'id' not in params:
        return jsonify({"error": "Es wurde keine ID des Eintrags mit angegeben"}), 400
    
    eintrag_id = params['id']
    eintrag = []

    for item in todo_einträge:
        if item['id'] == eintrag_id:
            eintrag = item
            break
    
    if not eintrag:
        return jsonify({"error": "Eintrag mit der angegebenen ID existiert nicht"}), 404

    todo_einträge.remove(eintrag)

    return jsonify({"message": "Eintrag wurde gelöscht", "id": eintrag_id}), 200

# Löscht eine komplette Todo-Liste mit allen Einträgen
@app.route('/deleteListe', methods=['DELETE'])
def deleteListe():
    params = request.json

    if 'id' not in params:
        return jsonify({"error": "Es wurde keine ID der Liste mit angegeben"}), 400
    
    liste_id = params['id']
    liste = []

    for item in todo_listen:
        if item['id'] == liste_id:
            liste = item
            break
    
    if not liste:
        return jsonify({"error": "Liste mit der angegebenen ID existiert nicht"}), 404

    todo_listen.remove(liste)
    eintrag_delete = []

    for eintrag in todo_einträge:
        if(eintrag['liste_id'] == liste_id):
            eintrag_delete.append(eintrag)

    for eintrag in eintrag_delete:
        todo_einträge.remove(eintrag)

    return jsonify({"message": "Liste mit Einträgen wurde gelöscht", "id": liste_id}), 200

if __name__ == '__main__':
 # starte Flask-Server
 app.run(host='0.0.0.0', port=5000)
