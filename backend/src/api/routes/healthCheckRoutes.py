from flask import Flask, jsonify
from src.api.scrapers.vlr_scrapers import get_match_data

app = Flask(__name__)

"""
Rotas responsávei por checar a saúde do scrapper, verificando se ele retorna
dados válidos de partidas.

TODO: Adicionar validações robustas em relação ao dados retornados pelo scrapper.
"""

def check_data(data):
    return data and data.get('team_1')

@app.route('/spikePlanted')
def home():
    return jsonify({"message": "Bem-vindo à API SpikePlanted! 🚀 \n"
                    "Esta API é dedicada a fornecer dados de partidas de Valorant a partir do site VLR.gg.\n"
                    "version: beta 0.0.1"})


"""
Rota fixa para checar saude da API e do Scrapper - Partida
Partida base: LOUD vs OpTic
"""
@app.route('/health-check/match/loud-vs-optic')
def health_check_loud_optic():
    
    fixed_match_url = "https://www.vlr.gg/130685/loud-vs-optic-gaming-valorant-champions-2022-gf"
    
    data = get_match_data(fixed_match_url)
    
    if check_data(data):
        return jsonify(data), 200
    else:
        response = {
            "status": "ERROR",
            "message": "Scrapper não retornou dados.",
            "test_url": get_match_data
        }
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)