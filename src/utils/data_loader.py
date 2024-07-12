import csv
from src.config import DATA_PATH

def load_csv():
    datos = []
    with open(DATA_PATH, newline='') as csvfile:
        lector_csv = csv.reader(csvfile, delimiter=',')
        for fila in lector_csv:
            datos.append(fila)
    return datos