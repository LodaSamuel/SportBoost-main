import sqlite3

# Connessione al database
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# Lista di tuple contenenti il nome dell'articolo e il percorso dell'immagine
immagini_da_aggiungere = [
    ('1', 'static/images/pallone_da_calcio.jpg'),
    #('2', 'static/images/scarpe_da_calcio.jpg'),
    #('3', 'static/images/canestro.jpg'),
    #('4', 'static/images/occhialini_nuoto.jpg'),
    #('5', 'static/images/palla_pallavolo.jpg'),
    #('6', 'static/images/palla_basket.jpg'),
    #('7', 'static/images/mazza_baseball.jpg'),
    #('8', 'static/images/racchetta_tennis.jpg'),
    #('9', 'static/images/pallina_tennis.jpg'),
    #('10', 'static/images/canna_da_pesca.jpg'),
    #('11', 'static/images/guantoni_boxe.jpg'),
    #('12', 'static/images/tavolo_ping_pong.jpg'),
    #('13', 'static/images/manubrio_10kg.jpg'),
    #('14', 'static/images/scarpe_atletica.jpg'),
    # Aggiungi qui le coppie (nome_articolo, percorso_immagine) per gli altri articoli
]

# Esecuzione delle query di aggiornamento per ciascuna immagine
for id_articolo, percorso_immagine in immagini_da_aggiungere:
    cursor.execute("UPDATE articolo SET immagine = ? WHERE id = ?", (percorso_immagine, id_articolo))

# Commit delle modifiche
conn.commit()

# Chiusura della connessione
conn.close()
