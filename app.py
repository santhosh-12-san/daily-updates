from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/hello")
def get_request():



    
    return jsonify({"message": "this is get request"})

@app.post("/add-user")
def post_request():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")

    return jsonify({
        "message": "user added successfully",
        "user": {
            "name": name,
            "age": age
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
