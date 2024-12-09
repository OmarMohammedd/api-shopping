from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# إعدادات MongoDB
app.config["MONGO_URI"] = "mongodb+srv://omar:omar@cluster0.f9ottjh.mongodb.net/testapi?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db

# تحويل ObjectId إلى نص
def to_json(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "description": product.get("description", "")
    }

# عرض جميع المنتجات (GET)
@app.route("/products", methods=["GET"])
def get_products():
    products = db.products.find()
    return jsonify([to_json(product) for product in products])

# إضافة منتج جديد (POST)
@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    new_product = {
        "name": data["name"],
        "price": data["price"],
        "description": data.get("description", "")
    }
    result = db.products.insert_one(new_product)
    return jsonify({"message": "Product added successfully!", "id": str(result.inserted_id)}), 201

# تحديث منتج (PUT)
@app.route("/products/<id>", methods=["PUT"])
def update_product(id):
    data = request.json
    db.products.update_one({"_id": ObjectId(id)}, {"$set": data})
    updated_product = db.products.find_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product updated successfully!", "product": to_json(updated_product)})

# حذف منتج (DELETE)
@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    db.products.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Product deleted successfully!"})

# تشغيل الخادم
if __name__ == "__main__":
    app.run(debug=True, port=5000)
