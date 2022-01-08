
from flask import Flask, request, abort
from mock_data import catalog
import json  
import random 


app = Flask(__name__)

me = {
        "name": "Will",
        "last": "Cisneros",
        "age": 38,
        "hobbies": [],
        "address": {
            "street": "Evergreen",
            "number": 42,
            "city": "Springfield"
        }
    }

@app.route("/")
def home():
    return "Hello from Python"

@app.route("/test")
def any_name():
    return "I'm a test function."

# return the full naame getting the values from the dictionary
@app.route("/about")
def about():
    return me["name"] + " " + me["last"]




# ***************************************************************
# ********************* API ENDPOINTS ***************************
# ***************************************************************



@app.route("/api/catalog")
def get_catalog():
    # TODO: read the catalog from the database
    return json.dumps(catalog)



@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json() 
    print (product)

    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should be at least 5 chars long")


    if not "price" in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a valid number")



    if product["price"] <= 0:
        return abort(400, "Price should be greater than zero")


    product["_id"] = random.randint(1000, 100000)
    catalog.append(product)


    return json.dumps(product) 



@app.route("/api/cheapest")
def get_cheapest():
    # find the cheapest product on the catalog list   
    cheap = catalog[0]
    for product in catalog:
        if product["price"] < cheap["price"]:
            cheap = product 
        
    # return it as json
    return json.dumps(cheap)


@app.route("/api/products/<id>")
def get_product(id):
    # find the product whose _id is equal to id
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)

    # return as json
    return "Not Found"



# endpoint to retreive all the products by category
@app.route("/api/catalog/<category>")
def get_by_category(category):
    result = []
    category = category.lower()
    for product in catalog:
        if product["category"].lower() == category:
            result.append(product)
            
            
    return json.dumps(result)






@app.route("/api/categories")
def get_categories():
    result = []
    for product in catalog:
        cat = product["category"]

        if cat not in result:
            result.append(cat)

    return json.dumps(result)


#  start the server 
app.run(debug=True)
