from flask import Flask, request, jsonify

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def __str__(self):
        return f"ID: {self.id}, User: {self.username}, Pass: {self.password}, Email: {self.email}"

ListUsers = [
    User(id=1, username="usuari1", password="12345", email="usuari1@gmail.com"),
    User(id=2, username="usuari2", password="123", email="usuari2@gmail.com")
]

class DaoUsers:
    def __init__(self):
        self.users = ListUsers
        
    def getUserByUsername(self, username):

        for u in self.users:

            if u.username == username:

                return u

        return None

app = Flask(__name__)
DaoUser = DaoUsers()

@app.route('/tapatappV1/validate_parameters', methods=['GET'])
def validate_parameters():
    username = request.args.get('username')
    email = request.args.get('email')
    
    errors = []
    
    if not username:

        errors.append("Username parameter is missing.")

    if not email:

        errors.append("Email parameter is missing.")
        
    if errors:
        return jsonify({"errors": errors}), 400
    
    return jsonify({"message": "Parameters are valid."}), 200

@app.route('/tapatappV1/Username', methods=["GET"])
def getUse():
    username = request.args.get('username')
    if username:
        user = DaoUser.getUserByUsername(username)
        
        if user:

            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email
            }), 200

        return jsonify({"error": "User not found"}), 404

    return jsonify({"error": "Username not provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10050)

@app.route('/tapatappV1/register', methods=['POST'])
def register():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if DaoUser.getUserByUsername(username):
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(id=len(ListUsers) + 1, username=username, password=password, email=email)
    ListUsers.append(new_user)

    return jsonify({"message": "User registered successfully"}), 201

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
