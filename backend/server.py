from flask import Flask, render_template, request, jsonify
from optimizers.value_optimizer import solve_value_problem as generate_value_lineups
from optimizers.points_optimizer import solve_points_problem as generate_points_lineups
from optimizers.probability_optimizer import solve_probability_problem as generate_probability_lineups

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize/value', methods=['POST'])
def optimize_value():
    data = request.json
    try:
        lineups, counts = generate_value_lineups(
            data['num_coins'],
            data['lineup_size'],
            data['probabilities'],
            data['head_points'],
            data['tail_points'],
            data['max_repeating'],
            data['required_lineups'],
            data.get('min_appearances', {}),
            data.get('max_appearances', {})
        )
        summary = {f"Coin {i+1}": counts[i] for i in range(len(counts))}
        return jsonify({'lineups': lineups, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/optimize/points', methods=['POST'])
def optimize_points():
    data = request.json
    try:
        lineups, counts = generate_points_lineups(
            data['num_coins'],
            data['lineup_size'],
            data['head_points'],
            data['tail_points'],
            data['max_repeating'],
            data['required_lineups'],
            data.get('min_appearances', {}),
            data.get('max_appearances', {})
        )
        summary = {f"Coin {i+1}": counts[i] for i in range(len(counts))}
        return jsonify({'lineups': lineups, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/optimize/probability', methods=['POST'])
def optimize_probability():
    data = request.json
    try:
        lineups, counts = generate_probability_lineups(
            data['num_coins'],
            data['lineup_size'],
            data['probabilities'],
            data['max_repeating'],
            data['required_lineups'],
            data.get('min_appearances', {}),
            data.get('max_appearances', {})
        )
        summary = {f"Coin {i+1}": counts[i] for i in range(len(counts))}
        return jsonify({'lineups': lineups, 'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
