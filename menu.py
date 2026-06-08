import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
 
from sokoban.sokoban_cli import run as run_sokoban
from frozenLake.frozenLake_cli import run as run_frozenLake
from ochoReinas.ochoReinas_cli import run as run_ochoReinas
from gato.gato_cli import run as run_gato

def mostrarMenu():
    os.system('cls')
    print("=== RESOLVEDOR DE ALGORITMOS IA ===")
    print("1. Frozen Lake (BFS/DFS) \n2. Sokoban (A*) \n3. 8 Reinas (Hill Climbing) \n4. Gato (Minimax/Poda Alfa-Beta) \n5. Salir")

def pedirOpcion():
    while True:
        opcion = input("Elige una opción: ").strip()
        if opcion in ("1", "2", "3", "4", "5"):
            return opcion
        print("  Opcion no valida. Ingresa algún número del 1 al 5.")

def main():
    while True:
        mostrarMenu()
        opcion = pedirOpcion()
 
        try:
            match opcion:
                case "1":
                    os.system('cls')
                    run_frozenLake()
                case "2":
                    os.system('cls')
                    run_sokoban()
                case "3":
                    os.system('cls')
                    run_ochoReinas()
                case "4":
                    os.system('cls')
                    run_gato()
                case "5":
                    sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nJuego interrumpido.")
 
        siguiente = mostrarMenu()
        if siguiente == "2":
            sys.exit(0)
        # Si eligio 1, el ciclo while vuelve a mostrar el menu
 
if __name__ == "__main__":
    main()