from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample data
users = {'user1': 'password1', 'user2': 'password2'}
user_baskets = {1: [], 2: []}  # Persistent basket storage with IDs
user_basket_ids = {'user1': 1, 'user2': 2}
products = [
    {'id': 1, 'name': 'Product 1', 'price': 10.00, 'image': 'apple.png'},
    {'id': 2, 'name': 'Product 2', 'price': 20.00, 'image': 'pineapple.png'},
    {'id': 3, 'name': 'Product 3', 'price': 30.00, 'image': 'banana.png'},
]


@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            session['basket_id'] = user_basket_ids[username]
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('basket_id', None)
    return redirect(url_for('index'))

@app.route('/add_to_basket/<int:product_id>')
def add_to_basket(product_id):
    if 'basket_id' in session:
        product = next((p for p in products if p['id'] == product_id), None)
        if product:
            user_baskets[session['basket_id']].append(product)
    return redirect(url_for('index'))

@app.route('/basket/<int:basket_id>')
def basket(basket_id):
    if basket_id not in user_baskets:
        return "Basket not found", 404
    return render_template('basket.html', basket=user_baskets[basket_id], basket_id=basket_id)

@app.route('/remove_from_basket/<int:basket_id>/<int:product_id>', methods=['POST'])
def remove_from_basket(basket_id, product_id):
    if 'basket_id' not in session or session['basket_id'] != basket_id:
        return "Unauthorized action", 403

    basket = user_baskets.get(basket_id)
    if not basket:
        return "Basket not found", 404

    product = next((p for p in basket if p['id'] == product_id), None)
    if product:
        basket.remove(product)
        return redirect(url_for('basket', basket_id=basket_id))
    else:
        return "Product not found in basket", 404

@app.route('/edit/basket/<int:basket_id>')
def edit_basket(basket_id):
    if 'basket_id' not in session or session['basket_id'] != basket_id:
        return "Unauthorized access", 403
    if basket_id not in user_baskets:
        return "Basket not found", 404
    return render_template('edit_basket.html', basket=user_baskets[basket_id], basket_id=basket_id)

@app.route('/remove_item/<int:basket_id>/<int:product_id>', methods=['POST'])
def remove_item(basket_id, product_id):
    if 'basket_id' not in session or session['basket_id'] != basket_id:
        return "Unauthorized action", 403
    if basket_id not in user_baskets:
        return "Basket not found", 404

    basket = user_baskets.get(basket_id, [])
    product = next((p for p in basket if p['id'] == product_id), None)
    if product:
        basket.remove(product)
    return redirect(url_for('edit_basket', basket_id=basket_id))

if __name__ == '__main__':
    app.run(debug=True)
