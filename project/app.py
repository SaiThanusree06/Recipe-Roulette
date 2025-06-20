# app.py
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

SPOONACULAR_API_KEY = 'd4ee3fe2de554c4684b25e856704d0a5'  # Replace with your actual API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    ingredient = request.args.get('ingredient')
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredient}&number=6&apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Enrich with recipe URLs
    recipes = []
    for item in data:
        info_url = f"https://api.spoonacular.com/recipes/{item['id']}/information?apiKey={SPOONACULAR_API_KEY}"
        info = requests.get(info_url).json()
        recipes.append({
            'title': item['title'],
            'image': item['image'],
            'sourceUrl': info.get('sourceUrl', '#')
        })
    return jsonify({'recipes': recipes})

if __name__ == '__main__':
    app.run(debug=True)
