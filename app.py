from flask import Flask, render_template, session, redirect, url_for, request, flash
import sqlite3 as sq
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'il_tuo_segreto'

#recupero database
def get_db():
    conn = sq.connect('db.db')
    conn.row_factory = sq.Row
    return conn

#creazione carrello
def create_cart():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO carrello DEFAULT VALUES')
    cart_id = cur.lastrowid
    conn.commit()
    conn.close()
    return cart_id

#creazione utente
def create_user(username, password, indirizzo, preferenza):
    hashed_password = generate_password_hash(password)
    cart_id = create_cart()

    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO utente (username, password, indirizzo, preferenza, id_carrello) VALUES (?, ?, ?, ?, ?)',
                (username, hashed_password, indirizzo, preferenza, cart_id))
    conn.commit()
    conn.close()

#aggiunta articolo al carrello
def add_item_to_cart(user_id, item_id, quantity):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO articoloCarrello (id_articolo, id_carrello, quantita) VALUES (?, ?, ?)',
                (item_id, user_id, quantity))
    conn.commit()
    conn.close()

#homepage
@app.route('/')
def index():
    query = request.args.get('query', '').strip()
    conn = get_db()
    cur = conn.cursor()

    #preferenze utente
    if 'user_id' in session:
        user_id = session['user_id']
        cur.execute('SELECT preferenza FROM utente WHERE id = ?', (user_id,))
        user_preference = cur.fetchone()
        if user_preference:
            preferenza = user_preference['preferenza']
            cur.execute("SELECT * FROM articolo WHERE sport = ? AND (nome LIKE ? OR sport LIKE ?)", (preferenza, '%' + query + '%', '%' + query + '%'))
            preferred_items = cur.fetchall()
            cur.execute("SELECT * FROM articolo WHERE sport != ? AND (nome LIKE ? OR sport LIKE ?)", (preferenza, '%' + query + '%', '%' + query + '%'))
            other_items = cur.fetchall()
            rows = preferred_items + other_items
        else:
            cur.execute("SELECT * FROM articolo WHERE nome LIKE ? OR sport LIKE ?", ('%' + query + '%', '%' + query + '%'))
            rows = cur.fetchall()
    else:
        cur.execute("SELECT * FROM articolo WHERE nome LIKE ? OR sport LIKE ?", ('%' + query + '%', '%' + query + '%'))
        rows = cur.fetchall()

    conn.close()

    return render_template('index.html', items=rows, query=query)

#pagina articolo
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

#pagina carrello
@app.route('/cart')
def cart():
    conn = get_db()
    cur = conn.cursor()
    items = []
    total_price = 0

    #carrello differenziato per ogni utente
    if 'username' in session:
        user_id = session.get('user_id')
        cur.execute('''
            SELECT articolo.id, articolo.nome, articolo.sport, SUM(articoloCarrello.quantita) AS quantita, articolo.prezzo, articolo.immagine
            FROM articoloCarrello
            JOIN articolo ON articolo.id = articoloCarrello.id_articolo
            WHERE articoloCarrello.id_carrello = ?
            GROUP BY articolo.id, articolo.nome, articolo.sport, articolo.prezzo
        ''', (user_id,))
        items = [dict(row) for row in cur.fetchall()]
        total_price = sum(item['prezzo'] * item['quantita'] for item in items)

    conn.close()
    return render_template('cart.html', items=items, total_price=total_price)

#aggiunta articolo al carrello
@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    #controllo autenticazione
    if 'username' not in session:
        flash('Effettua l\'accesso per aggiungere articoli al carrello', 'error')
        return redirect(url_for('login'))

    quantity = int(request.form.get('quantity', 1))
    user_id = session.get('user_id')
    add_item_to_cart(user_id, item_id, quantity)
    return redirect(url_for('item', id=item_id))

#rimozione articolo dal carrello
@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):

    user_id = session['user_id']

    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM articoloCarrello WHERE id_carrello = ? AND id_articolo = ?', (user_id, item_id))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

#acquisto articoli
@app.route('/purchase', methods=['POST'])
def purchase():

    user_id = session['user_id']

    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM articoloCarrello WHERE id_carrello = ?', (user_id,))
    conn.commit()
    conn.close()

    return render_template('purchase_confirmation.html')

#mappa negozi
@app.route('/map')
def map():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM negozio')
    rows = cur.fetchall()
    negozi = [dict(row) for row in rows]
    conn.close()
    return render_template('map.html', negozi=negozi)

#pagina catalogo negozio
@app.route('/store_products')
def store_products():
    negozio_id = request.args.get('negozio_id', type=int)
    query = request.args.get('query', '').strip()
    conn = get_db()
    cur = conn.cursor()
    print(negozio_id)
    #ricerca
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

    return render_template('home_negozio.html', items=rows, query=query, negozio_id = negozio_id)

#mappa negozi con un certo articolo
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

#login
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
            return redirect(url_for('index'))
        else:
            flash('Username o password non validi', 'danger')

    return render_template('login.html')

#registrazione
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        indirizzo = request.form['indirizzo']
        preferenza = request.form['preferenza']

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM utente WHERE username = ?', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash('Username già esistente', 'danger')
            return redirect(url_for('register'))

        create_user(username, password, indirizzo, preferenza)

        cur.execute('SELECT * FROM utente WHERE username = ?', (username,))

        user = cur.fetchone()
        session['user_id'] = user['id']
        session['username'] = user['username']
        conn.close()

        return redirect(url_for('index'))
        
    else:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT articolo.sport FROM articolo')
        sport = cur.fetchall()
        conn.close()

        return render_template('register.html', sport=sport)

#logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
