import random
import math

N = 8

import math

N = 8


# ---------------------------------------
# Calcula conflictos entre reinas
# ---------------------------------------
def heuristica(tablero):

    conflictos = 0

    for i in range(N):

        for j in range(i + 1, N):

            if tablero[i] == tablero[j]:
                conflictos += 1

            elif abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1

    return conflictos


# ---------------------------------------
# Genera vecinos moviendo una reina
# ---------------------------------------
def generar_vecinos(tablero):

    vecinos = []

    for col in range(N):

        fila_original = tablero[col]

        for nueva_fila in range(N):

            if nueva_fila != fila_original:

                vecino = tablero.copy()
                vecino[col] = nueva_fila

                vecinos.append(vecino)

    return vecinos


# ---------------------------------------
# Hill Climbing
# ---------------------------------------
def hill_climbing(tablero):

    actual = tablero.copy()

    camino = [{
        "tablero": actual.copy(),
        "conflictos": heuristica(actual)
    }]

    while True:

        h_actual = heuristica(actual)

        if h_actual == 0:
            return actual, True, camino

        vecinos = generar_vecinos(actual)

        mejor_vecino = actual
        mejor_h = h_actual

        for vecino in vecinos:

            h_vecino = heuristica(vecino)

            if h_vecino < mejor_h:

                mejor_vecino = vecino
                mejor_h = h_vecino

        # Óptimo local
        if mejor_h >= h_actual:

            return actual, False, camino

        actual = mejor_vecino

        camino.append({
            "tablero": actual.copy(),
            "conflictos": mejor_h
        })


def random_restart_hill_climbing(max_intentos=1000):

    for intento in range(1, max_intentos + 1):

        tablero = [
            random.randint(0, N - 1)
            for _ in range(N)
        ]

        solucion, exito, camino = hill_climbing(
            tablero
        )

        if exito:

            print(
                f"\nRandom Restart "
                f"encontró solución "
                f"en el intento {intento}"
            )

            mostrar_camino(camino)

            return solucion

        else:

            print(
                f"Reinicio {intento}: "
                f"óptimo local con {heuristica(solucion)} conflictos"
            )

    return None


# ---------------------------------------
# Imprimir tablero
# ---------------------------------------
def imprimir_tablero(tablero):

    for fila in range(N):

        for col in range(N):

            if tablero[col] == fila:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        print()

    print()


# ---------------------------------------
# Detectar movimiento
# ---------------------------------------
def movimiento(anterior, actual):

    for col in range(N):

        if anterior[col] != actual[col]:

            return (
                col,
                anterior[col],
                actual[col]
            )

    return None


# ---------------------------------------
# Mostrar camino
# ---------------------------------------
def mostrar_camino(camino):

    print("\nPASO 0 (Estado inicial)")
    print("Tablero:", camino[0]["tablero"])
    print("Conflictos:", camino[0]["conflictos"])

    imprimir_tablero(
        camino[0]["tablero"]
    )

    for paso in range(1, len(camino)):

        anterior = camino[paso - 1]["tablero"]
        actual = camino[paso]["tablero"]

        col, fila1, fila2 = movimiento(
            anterior,
            actual
        )

        print(f"\nPASO {paso}")

        print(
            f"Movimiento: Reina columna {col} "
            f"de fila {fila1} a fila {fila2}"
        )

        print(
            f"Conflictos: "
            f"{camino[paso]['conflictos']}"
        )

        print(
            "Estado:",
            actual
        )

        imprimir_tablero(actual)


# ---------------------------------------
# Programa principal
# ---------------------------------------
if __name__ == "__main__":
    
    print("Ingrese las filas de las 8 reinas")

    tablero = list(
        map(
            int,
            input(
                "Ejemplo: 5 2 7 1 4 0 6 3\n> "
            ).split()
        )
    )

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