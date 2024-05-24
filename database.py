import sqlite3


# Connessione al database
conn = sqlite3.connect('db.db')
cursor = conn.cursor()

# immagini_da_aggiungere = [
#     ('1', 'static/images/pallone_da_calcio.png'),
#     ('2', 'static/images/scarpe_da_calcio.png'),
#     ('3', 'static/images/canestro.png'),
#     ('4', 'static/images/occhialini_nuoto.png'),
#     ('5', 'static/images/palla_pallavolo.png'),
#     ('6', 'static/images/palla_basket.png'),
#     ('7', 'static/images/mazza_baseball.png'),
#     ('8', 'static/images/racchetta_tennis.png'),
#     ('9', 'static/images/pallina_tennis.png'),
#     ('10', 'static/images/canna_da_pesca.png'),
#     ('11', 'static/images/guantoni_boxe.png'),
#     ('12', 'static/images/tavolo_ping_pong.png'),
#     ('13', 'static/images/manubrio_10kg.png'),
#     ('14', 'static/images/scarpe_atletica.png'),
# ]

# for id_articolo, percorso_immagine in immagini_da_aggiungere:
#     cursor.execute("UPDATE articolo SET immagine = ? WHERE id = ?", (percorso_immagine, id_articolo))

# cursor.execute("""
               

#                """
#                )

# Commit delle modifiche
conn.commit()

# Chiusura della connessione
conn.close()
