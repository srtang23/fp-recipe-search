from flask import Flask, render_template, request
import requests

app = Flask(__name__)

RECIPE_API_KEY = 'YOUR API KEY'
RECIPE_API_URL = 'https://api.api-ninjas.com/v1/recipe'
INDEXED_RESULTS = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    dish_name = request.form['dish_name']
    params = {'query': dish_name, 'offset': 0}
    headers = {'X-Api-Key': RECIPE_API_KEY}
    response = requests.get(RECIPE_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        recipes = response.json()

        if not recipes:
            return render_template('error.html', message="Cannot find recipes for {}".format(dish_name))

        for recipe in recipes:
            INDEXED_RESULTS.append(recipe)
        return render_template('search.html', dish_name=dish_name, recipes=recipes)
    else:
        return render_template('error.html', message="The website just crashed. Please try again later.")

@app.route('/generate-recipe/<result_index>')
def generate_recipe_info(result_index):
    recipe = INDEXED_RESULTS[int(result_index) - 1]
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)