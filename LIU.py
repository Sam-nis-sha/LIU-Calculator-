from flask import Flask, request, jsonify

app = Flask(__name__)

# Route d'accueil
@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Calculateur LIU</title>
            <link rel="stylesheet" type="text/css" href="/static/style.css">
        </head>
        <body>
            <div style="text-align: center;">
             <h1>Calculateur LIU</h1>
            <form action="/liu" method="get">
                <label for="A">Peak Total Bilirubin :</label>
                <input type="number" step="0.01" name="A" required>
                <select name="unit">
                    <option value="µmol/l">µmol/l</option>
                    <option value="mg/l">mg/l</option>
                </select>
                <br><br>

                <label for="B">Peak PT :</label>
                <input type="number" step="0.01" name="B" required><br><br>

                <label for="C">Peak Ammonia (µmol/l) :</label>
                <input type="number" step="0.01" name="C" required><br><br>

                <button type="submit">Calculer le LIU</button>
            </form>
         </div>
        </body>
        </html>
    '''

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Renvoie une réponse vide avec un statut "Pas de contenu"


# Fonction pour calculer le LIU
def calcul_LIU(A, B, C, unit):
    if unit=="mg/l" :
        LIU_score = (3.507 *A) + (45.51 * B) + (0.254 * C)
    elif unit=="µmol/l" : 
        LIU_score = (3.507 * (A / 17.1)) + (45.51 * B) + (0.254 * C)
    return LIU_score

# Route pour calculer le LIU
@app.route('/liu', methods=['GET'])
def calculer_liu():
    try:
        # Récupérer les paramètres de l'URL
        A = float(request.args.get('A'))
        unit = request.args.get("unit")    #Unité selectionnée 
        B = float(request.args.get('B'))
        C = float(request.args.get('C'))

        # Calculer le LIU
        liu = calcul_LIU(A, B, C, unit)

        # Retourner le résultat sous forme HTML
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Calculateur LIU</title>
                <link rel="stylesheet" type="text/css" href="/static/style.css">
            </head>
             <body>
                <div style="text-align: center;">
                <h1>Résultat LIU</h1>
                <p>Peak Total Bilirubin : {A:.2f} {unit}</p>
                <p>Peak PT : {B}</p>
                <p>Peak Ammonia : {C} µmol/L</p>
                <h3 class="result">LIU calculé : {liu:.2f}</h3>
                <a href="/">Revenir au formulaire</a>
                <p>
                    <span><strong>Pour plus d'informations :</strong></span>
                    <a href="https://pubmed.ncbi.nlm.nih.gov/23260095/">Référence</a>
                </p>
            </div>            
            </body>
            </html>
        """
    except Exception as e:
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Erreur</title>
                <link rel="stylesheet" type="text/css" href="/static/style.css">
            </head>
            <body>
                <h1>Erreur dans le calcul</h1>
                <p>{str(e)}</p>
                <a href="/">Revenir au formulaire</a>
            </body>
            </html>
        """, 400

# Lancer le serveur Flask
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Récupère le port défini par Render ou utilise 5000 par défaut
    app.run(debug=True, host="0.0.0.0", port=port)
