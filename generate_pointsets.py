#!/usr/bin/env python3
"""génère un fichier contanant :

SEED = ... # graine pour le générateur aléatoire (permet des résultats reproductibles)

IDS = [...] # liste des identifiants de jeux de points

MALFORMED_ID = "invalid-id-1234" # un ID malformé
UNKNOWN_ID = "..." # un ID qui n'est pas dans IDS

POINTS = {"id1": b"...", # données binaires du jeu de points
           "id2": b"...",
           ...
        }
        
TRIANGLES = {"id1": b"...", # données binaires du jeu de triangles
             "id2": b"...",
             ...
}

Format binaire pour chaque fichier:
- 4 bytes unsigned int (little-endian): N (nombre de points)
- N * 8 bytes: pour chaque point 4 bytes float X, 4 bytes float Y (little-endian)

La représentation binaire de Triangles est donc en deux parties:

- La première partie décrit les sommets et est strictement la même que pour un PointSet
- La seconde partie décrit les triangles à proprement parler et se compose de:
  - 4 bytes (un unsigned long) qui représente le nombre de triangles
  - 3 x 4 x {nombre de triangles} bytes, pour chaque triangle il y a donc 12 bytes, chaque 4 bytes sont un unsigned long qui référence l'indice d'un sommet du triangle dans le PointSet.
"""

import argparse
import os
import random
import struct
from typing import TextIO


def random_hex_digit() -> str:
    return random.choice("0123456789abcdef")

def random_hex_digit_variant() -> str:
    return random.choice("89ab")

def uuid4() -> str:
    """Génère un UUID4 aléatoire sous forme de chaîne de caractères. utilise le module random pour la reproductibilité."""
    return (
        f"{''.join(random_hex_digit() for _ in range(8))}-"
        f"{''.join(random_hex_digit() for _ in range(4))}-"
        f"4{''.join(random_hex_digit() for _ in range(3))}-"
        f"{random_hex_digit_variant()}{''.join(random_hex_digit() for _ in range(3))}-"
        f"{''.join(random_hex_digit() for _ in range(12))}"
    )

# IDS = [
#     "781a1a6b-0162-49aa-84c1-0339327e2f8e",
#     "57e859a2-538c-46a4-a90f-2fa025971f51",
#     "8cde6ebb-fcdf-4613-988e-50dc2c7b8046",
#     "f8df89cb-4b6f-4a90-9726-461e30e4c147",
#     "c9679012-97fb-4e2c-93c2-4138d172867f",
#     "60054c38-6e7d-466e-bc20-39d7e287f1b3",
#     "12c81354-19f6-470a-8830-219d670b6372",
#     "6460fab1-e41f-411c-87a0-d34dd2753fe1",
#     "ac4b10ee-3e96-4b06-88c6-01fcab404170",
#     "d94e2a5c-dc6e-4a8c-8deb-4b2bc22e3e0c"
# ]

DATASETS_PY = "tests/datasets.py"
OUT_DIR = "tests"
COORD_MIN = -1000.0
COORD_MAX = 1000.0


def generate_ids(n : int) -> list[str]:
    result = []
    for _ in range(n):
        result.append(str(uuid4()))
    return result

def generate_unknown_id(existing_ids : list[str]) -> str:
    while True:
        candidate = uuid4()
        if candidate not in existing_ids:
            return candidate

def generate_pointset(min_points : int, max_points : int) -> list[tuple[float, float]]:
    n = random.randint(min_points, max_points)
    points = set() # use a set to avoid duplicates
    while len(points) < n:
        x = random.uniform(COORD_MIN, COORD_MAX)
        y = random.uniform(COORD_MIN, COORD_MAX)
        points.add((x, y))
    return list(points)
    
def encode_pointset(points : list[tuple[float, float]]) -> bytes:
    result : bytes = struct.pack("<I", len(points))
    for point in points:
        result += struct.pack("<ff", point[0], point[1])
    return result

def encode_triangles(points : list[tuple[float, float]], triangles : list[tuple[int, int, int]]) -> bytes:
    pointset_bytes = encode_pointset(points)
    result : bytes = pointset_bytes
    result += struct.pack("<I", len(triangles))
    for triangle in triangles:
        result += struct.pack("<III", triangle[0], triangle[1], triangle[2])
    return result


def create_triangle(points : list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Créé des triangles entre tous les points
    """
    triangles = []
    # Triangulation très basique : on crée des triangles en reliant chaque point avec le point suivant et le point après le suivant
    n = len(points)
    for i in range(n - 2):
        triangles.append((i, i + 1, i + 2))
    return triangles


def plot_triangles(points : list[tuple[float, float]], triangles : list[tuple[int, int, int]]) -> None:
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    triang = mtri.Triangulation(x, y, triangles)

    plt.triplot(triang, color='blue')
    plt.plot(x, y, 'o', color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Triangulation')
    plt.show()

def write_SEED(file : TextIO, seed : int) -> None:
    file.write(f"SEED = {seed}\n\n")

def write_IDS(file : TextIO, ids : list[str]) -> None:
    file.write("IDS = [\n")
    for ident in ids:
        file.write(f'    "{ident}",\n')
    file.write("]\n\n")
    
def write_INVALID_ID(file : TextIO, invalid_id : str) -> None:
    file.write(f'MALFORMED_ID = "{invalid_id}"\n\n')

def write_UNKNOWN_ID(file : TextIO, unknown_id : str) -> None:
    file.write(f'UNKNOWN_ID = "{unknown_id}"\n\n')
    
def write_POINT_DATASETS(file : TextIO, datasets : dict[str, bytes]) -> None:
    file.write("POINTS = {\n")
    for ident, dataset in datasets.items():
        file.write(f'    "{ident}": b"""')
        file.write(''.join(f'\\x{byte:02x}' for byte in dataset))
        file.write('""",\n')
    file.write("}\n\n")

def write_TRIANGLE_DATASETS(file : TextIO, datasets : dict[str, bytes]) -> None:
    file.write("TRIANGLES = {\n")
    for ident, dataset in datasets.items():
        file.write(f'    "{ident}": b"""')
        file.write(''.join(f'\\x{byte:02x}' for byte in dataset))
        file.write('""",\n')
    file.write("}\n")

def main():
    argparser = argparse.ArgumentParser(description="Génère des jeux de points pour les tests.")
    argparser.add_argument("--seed", "-s", type=int, default=random.randint(0, 2**64), help="Graine pour le générateur aléatoire.")
    argparser.add_argument("-nb_items", "-n", type=int, default=10, help="Nombre de jeux de points à générer.")
    argparser.add_argument("--min-points", type=int, default=3, help="Nombre minimum de points par jeu.")
    argparser.add_argument("--max-points", type=int, default=200, help="Nombre maximum de points par jeu.")
    args = argparser.parse_args()
    
    random.seed(args.seed)
    
    ids = generate_ids(args.nb_items)
    
    points_set = {}
    triangles_set = {}
    for id in ids:
        dataset = generate_pointset(args.min_points, args.max_points)
        points_set[id] = encode_pointset(dataset)
        triangles = create_triangle(dataset)
        triangles_set[id] = encode_triangles(dataset, triangles)
        # plot_triangles(dataset, triangles)
    
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(DATASETS_PY, "w") as f:
        f.write("# Auto-generated dataset file\n")
        write_SEED(f, args.seed)
        write_IDS(f, ids)
        write_INVALID_ID(f, "invalid-id-1234")
        write_UNKNOWN_ID(f, generate_unknown_id(ids))
        write_POINT_DATASETS(f, points_set)
        write_TRIANGLE_DATASETS(f, triangles_set)
        

if __name__ == "__main__":
    main()