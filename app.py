from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    content = file.read().decode()
    lines = content.strip().splitlines()

    scale = float(lines[1])
    lattice = np.array([list(map(float, l.split())) for l in lines[2:5]]) * scale
    elements = lines[5].split()
    counts = list(map(int, lines[6].split()))
    total_atoms = sum(counts)

    coord_start = 8 if lines[7][0].lower() == 's' else 7
    coords = np.array([
        list(map(float, lines[i].split()[:3]))
        for i in range(coord_start, coord_start + total_atoms)
    ])
    if lines[7][0].lower() in ['d', 's']:
        coords = coords @ lattice

    volume = abs(np.linalg.det(lattice))
    com = coords.mean(axis=0)

    return jsonify({
        "elements": elements,
        "counts": counts,
        "total_atoms": total_atoms,
        "volume": round(volume, 3),
        "center_of_mass": [round(x, 3) for x in com.tolist()]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
