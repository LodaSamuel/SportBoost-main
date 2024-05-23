from flask import Flask, render_template, session, redirect, url_for, request, flash
import sqlite3 as sq
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'il_tuo_segreto'

def get_db():
    conn = sq.connect('db.db')
    conn.row_factory = sq.Row
    return conn

@app.route('/')
def index():
    query = request.args.get('query', '').strip()
    conn = get_db()
    cur = conn.cursor()
    
    if query:
        cur.execute("SELECT * FROM articolo WHERE nome LIKE ? OR sport LIKE ?", ('%' + query + '%', '%' + query + '%'))
    else:
        cur.execute('SELECT * FROM articolo')
    
    rows = cur.fetchall()
    conn.close()
    
    return render_template('index.html', items=rows, query=query)

@app.route('/item/<int:id>')
def item(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM articolo WHERE id = ?', (id,))
    row = cur.fetchone()
    conn.close()
    if row is None:
        return "Articolo non trovato", 404
    return render_template('item.html', item=row)

@app.route('/cart')
def cart():
    conn = get_db()
    cur = conn.cursor()
    items = []

    cart_items = {}
    total_price = 0  # Inizializza il prezzo totale a zero
    if 'username' in session:
        if 'cart' in session:
            for item_id in session['cart']:
                cart_items[item_id] = cart_items.get(item_id, 0) + 1

            for item_id, quantity in cart_items.items():
                cur.execute('SELECT * FROM articolo WHERE id = ?', (item_id,))
                item = dict(cur.fetchone())
                item['quantita'] = quantity
                items.append(item)
                total_price += item['prezzo'] * quantity  # Aggiungi il prezzo dell'articolo moltiplicato per la quantità

    conn.close()
    return render_template('cart.html', items=items, total_price=total_price)  # Passa total_price al template


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Controlla se l'utente è autenticato
    if 'username' not in session:
        flash('Effettua l\'accesso per aggiungere articoli al carrello', 'error')
        return redirect(url_for('login'))

    # Altrimenti, procedi con l'aggiunta dell'articolo al carrello
    quantity = int(request.form.get('quantity', 1))
    session['cart'] = session.get('cart', [])
    for _ in range(quantity):
        session['cart'].append(item_id)
    return redirect(url_for('item', id=item_id))


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        session['cart'] = [i for i in session['cart'] if i != item_id]
    return redirect(url_for('cart'))

@app.route('/purchase', methods=['POST'])
def purchase():
    return render_template('purchase_confirmation.html')

@app.route('/map')
def map():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM negozio')
    rows = cur.fetchall()
    negozi = [dict(row) for row in rows]
    conn.close()
    return render_template('map.html', negozi=negozi)

@app.route('/store_products')
def store_products():
    negozio_id = request.args.get('negozio_id', type=int)
    query = request.args.get('query', '').strip()
    conn = get_db()
    cur = conn.cursor()

    if query:
        cur.execute('''
            SELECT articolo.* FROM articolo
            JOIN negozioArticolo ON articolo.id = negozioArticolo.id_articolo
            WHERE negozioArticolo.id_negozio = ? AND (articolo.nome LIKE ? OR articolo.sport LIKE ?)
        ''', (negozio_id, '%' + query + '%', '%' + query + '%'))
    else:
        cur.execute('''
            SELECT articolo.* FROM articolo
            JOIN negozioArticolo ON articolo.id = negozioArticolo.id_articolo
            WHERE negozioArticolo.id_negozio = ?
        ''', (negozio_id,))

    rows = cur.fetchall()
    conn.close()

    return render_template('index.html', items=rows, query=query)


@app.route('/map_item/<int:item_id>')
def map_item(item_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT negozio.* FROM negozio
        JOIN negozioArticolo ON negozio.id = negozioArticolo.id_negozio
        WHERE negozioArticolo.id_articolo = ?
    ''', (item_id,))
    rows = cur.fetchall()
    negozi = [dict(row) for row in rows]
    conn.close()
    return render_template('map_item.html', negozi=negozi)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM utente WHERE username = ?', (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login effettuato con successo!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username o password non validi', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        indirizzo = request.form['indirizzo']
        preferenza = request.form['preferenza']

        hashed_password = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO utente (username, password, indirizzo, preferenza) VALUES (?, ?, ?, ?)',
                    (username, hashed_password, indirizzo, preferenza))
        conn.commit()
        conn.close()

        flash('Registrazione avvenuta con successo! Ora puoi effettuare il login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logout effettuato con successo!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
