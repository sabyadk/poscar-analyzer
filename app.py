from flask import Flask, request, jsonify
import numpy as np
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables frontend-backend communication

@app.route('/')
def home():
    return 'POSCAR Analyzer is running!'

@app.route('/analyze', methods=['POST'])
def analyze_poscar():
    file = request.files['file']
    lines = file.read().decode().splitlines()

    lattice = []
    atomic_coords = []
    scale = float(lines[1].strip())

    for i in range(2, 5):
        vec = [float(x) for x in lines[i].split()]
        lattice.append(vec)

    # You can add more parsing logic here...

    result = {
        'scale_factor': scale,
        'lattice_vectors': lattice,
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

