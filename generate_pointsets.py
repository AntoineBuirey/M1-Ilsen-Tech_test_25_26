#!/usr/bin/env python3
"""
Génère 10 jeux de point sets binaires à partir des identifiants trouvés
dans tests/datasets.json.

Format binaire pour chaque fichier:
- 4 bytes unsigned int (little-endian): N (nombre de points)
- N * 8 bytes: pour chaque point 4 bytes float X, 4 bytes float Y (little-endian)
"""

import os
import struct
import random

IDS = [
    "781a1a6b-0162-49aa-84c1-0339327e2f8e",
    "57e859a2-538c-46a4-a90f-2fa025971f51",
    "8cde6ebb-fcdf-4613-988e-50dc2c7b8046",
    "f8df89cb-4b6f-4a90-9726-461e30e4c147",
    "c9679012-97fb-4e2c-93c2-4138d172867f",
    "60054c38-6e7d-466e-bc20-39d7e287f1b3",
    "12c81354-19f6-470a-8830-219d670b6372",
    "6460fab1-e41f-411c-87a0-d34dd2753fe1",
    "ac4b10ee-3e96-4b06-88c6-01fcab404170",
    "d94e2a5c-dc6e-4a8c-8deb-4b2bc22e3e0c"
]

DATASETS_PY = "tests/datasets.py"
OUT_DIR = "tests"
MIN_POINTS = 10
MAX_POINTS = 200
COORD_MIN = -1000.0
COORD_MAX = 1000.0

def generate_pointset():
    n = random.randint(MIN_POINTS, MAX_POINTS)
    result : bytes = struct.pack("<I", n)
    for _ in range(n):
        x = random.uniform(COORD_MIN, COORD_MAX)
        y = random.uniform(COORD_MIN, COORD_MAX)
        result += struct.pack("<ff", x, y)
    return result

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    result = {}
    for ident in IDS:
        dataset = generate_pointset()
        result[ident] = dataset
    
    with open(DATASETS_PY, "w") as f:
        f.write("# Auto-generated dataset file\n")
        f.write("IDS = [\n")
        for ident in IDS:
            f.write(f'    "{ident}",\n')
        f.write("]\n\n")
        
        f.write("DATASETS = {\n")
        for ident, dataset in result.items():
            f.write(f'    "{ident}": b"""')
            f.write(''.join(f'\\x{byte:02x}' for byte in dataset))
            f.write('""",\n')
        f.write("}\n")
        

if __name__ == "__main__":
    main()