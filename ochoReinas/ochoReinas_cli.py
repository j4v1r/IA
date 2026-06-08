import random
import os

from ochoReinas.ochoReinas import (
    hill_climbing,
    mostrar_camino,
    random_restart_hill_climbing,
    recocido_simulado,
    imprimir_tablero,
    heuristica
)

def leer_tablero():

    while True:

        try:

            entrada = input(
                "\nIngrese las 8 filas separadas por espacios\n"
                "Ejemplo: 5 2 7 1 4 0 6 3\n> "
            )

            tablero = list(map(int, entrada.split()))

            if len(tablero) != 8:
                raise ValueError

            if any(x < 0 or x > 7 for x in tablero):
                raise ValueError

            return tablero

        except ValueError:

            print(
                "\nError: Debe ingresar exactamente "
                "8 números entre 0 y 7."
            )


def menu_8_reinas():
    os.system('cls')
    print("\n=== 8 REINAS ===")
    print("1. Hill Climbing")
    print("2. Recocido Simulado")
    print("3. Regresar")

    while True:

        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2", "3"):
            return opcion

        print("Opción no válida.")


def run():

    while True:

        opcion = menu_8_reinas()

        if opcion == "3":
            return

        tablero = leer_tablero()

        print("\nTablero inicial:")
        print(tablero)

        imprimir_tablero(tablero)

        print(
            f"\nConflictos iniciales: "
            f"{heuristica(tablero)}"
        )

        if opcion == "1":

            # Intentar desde el tablero del usuario
            solucion, exito, camino = hill_climbing(tablero)

            print("\n====================================")
            print("BÚSQUEDA DESDE EL TABLERO INGRESADO")
            print("====================================")

            mostrar_camino(camino)

            if exito:

                print("\n====================================")
                print("SOLUCIÓN ENCONTRADA CON HILL CLIMBING")
                print("====================================")

                print(solucion)

                imprimir_tablero(solucion)

            else:

                print("\n====================================")
                print("ÓPTIMO LOCAL")
                print(
                    f"Conflictos restantes: "
                    f"{heuristica(solucion)}"
                )
                print("====================================")

                print(
                    "\nIniciando Random Restart..."
                )

                solucion = random_restart_hill_climbing()

                if solucion:

                    print("\n====================================")
                    print("SOLUCIÓN ENCONTRADA CON RANDOM RESTART")
                    print("====================================")

                    print(solucion)

                    imprimir_tablero(solucion)

                else:

                    print(
                        "\nNo fue posible encontrar "
                        "una solución."
                    )

        elif opcion == "2":

            print(
                "\n=== RECOCIDO "
                "SIMULADO ==="
            )

            solucion, conflictos = (
                recocido_simulado(tablero)
            )

            if conflictos == 0:

                print(
                    "\nSOLUCIÓN "
                    "ENCONTRADA"
                )

            else:

                print(
                    "\nNo se alcanzó "
                    "una solución perfecta"
                )

                print(
                    f"Conflictos: "
                    f"{conflictos}"
                )

            print(solucion)

            imprimir_tablero(solucion)

        input(
            "\nPresione ENTER para continuar..."
        )