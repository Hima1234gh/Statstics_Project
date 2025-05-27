from flask import Flask, request, jsonify, render_template
from stat_1 import CentralTendency
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    content = request.json
    ct = CentralTendency(None, None)
    ct.grouped = content.get('grouped', False)
    if ct.grouped:
        ct.classes = content.get('classes', [])
        ct.frequencies = content.get('frequencies', [])
    else:
        ct.data = content.get('data', [])

    result = ct.compute_all()
    return jsonify(result)

@app.route('/cumulative', methods=['POST'])
def cumulative():
    content = request.json
    ct = CentralTendency(None, None)
    ct.grouped = content.get('grouped', False)
    if ct.grouped:
        ct.classes = content.get('classes', [])
        ct.frequencies = content.get('frequencies', [])
        table = ct.generate_cumulative_frequency_table()
        return jsonify(table)
    return jsonify({'error': 'Data must be grouped'}), 400

@app.route('/histogram', methods=['POST'])
def histogram():
    content = request.json
    ct = CentralTendency(None, None)
    ct.grouped = content.get('grouped', False)
    ct.classes = content.get('classes', [])
    ct.frequencies = content.get('frequencies', [])
    img_data = ct.plot_histogram()
    if img_data:
        return jsonify({'image': img_data})
    return jsonify({"error": "Histogram could not be generated."}), 400


if __name__ == '__main__':
    app.run(debug=True)
