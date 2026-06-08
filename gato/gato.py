# gato.py

import math

HUMANO = "X"
IA = "O"
VACIO = " "

nodos_evaluados = 0


# ---------------------------------------
# Mostrar tablero
# ---------------------------------------
def imprimir_tablero(tablero):

    print()

    for fila in range(3):

        print(
            f" {tablero[fila*3]} |"
            f" {tablero[fila*3+1]} |"
            f" {tablero[fila*3+2]}"
        )

        if fila < 2:
            print("---+---+---")

    print()


# ---------------------------------------
# Verificar ganador
# ---------------------------------------
def ganador(tablero):

    lineas = [

        (0,1,2),
        (3,4,5),
        (6,7,8),

        (0,3,6),
        (1,4,7),
        (2,5,8),

        (0,4,8),
        (2,4,6)

    ]

    for a,b,c in lineas:

        if (
            tablero[a] != VACIO and
            tablero[a] == tablero[b] ==
            tablero[c]
        ):
            return tablero[a]

    return None


# ---------------------------------------
# Terminal
# ---------------------------------------
def terminal(tablero):

    return (
        ganador(tablero) is not None or
        VACIO not in tablero
    )


# ---------------------------------------
# Evaluación
# ---------------------------------------
def evaluar(tablero):

    g = ganador(tablero)

    if g == IA:
        return 1

    if g == HUMANO:
        return -1

    return 0


# ---------------------------------------
# Minimax
# ---------------------------------------
def minimax(
    tablero,
    profundidad,
    es_max,
    nivel=0
):

    global nodos_evaluados

    nodos_evaluados += 1

    if terminal(tablero):

        valor = evaluar(tablero)

        print(
            "   " * nivel +
            f"Hoja -> {valor}"
        )

        return valor

    if es_max:

        mejor = -math.inf

        print(
            "   " * nivel +
            "MAX analiza:"
        )

        for i in range(9):

            if tablero[i] == VACIO:

                tablero[i] = IA

                valor = minimax(
                    tablero,
                    profundidad + 1,
                    False,
                    nivel + 1
                )

                tablero[i] = VACIO

                print(
                    "   " * nivel +
                    f"Movimiento {i}"
                    f" => {valor}"
                )

                mejor = max(
                    mejor,
                    valor
                )

        print(
            "   " * nivel +
            f"MAX devuelve {mejor}"
        )

        return mejor

    else:

        mejor = math.inf

        print(
            "   " * nivel +
            "MIN analiza:"
        )

        for i in range(9):

            if tablero[i] == VACIO:

                tablero[i] = HUMANO

                valor = minimax(
                    tablero,
                    profundidad + 1,
                    True,
                    nivel + 1
                )

                tablero[i] = VACIO

                print(
                    "   " * nivel +
                    f"Movimiento {i}"
                    f" => {valor}"
                )

                mejor = min(
                    mejor,
                    valor
                )

        print(
            "   " * nivel +
            f"MIN devuelve {mejor}"
        )

        return mejor

# ---------------------------------------
# Alfa-Beta
# ---------------------------------------
def alfa_beta(
    tablero,
    profundidad,
    es_max,
    alfa = -math.inf,
    beta = math.inf,
    nivel=0
):

    global nodos_evaluados

    nodos_evaluados += 1

    if terminal(tablero):

        valor = evaluar(tablero)

        print(
            "   " * nivel +
            f"Hoja -> {valor}"
        )

        return valor

    if es_max:

        mejor = -math.inf

        print(
            "   " * nivel +
            "MAX analiza (alfa={alfa}, beta={beta}):"
        )

        for i in range(9):

            if tablero[i] == VACIO:

                tablero[i] = IA

                valor = alfa_beta(
                    tablero,
                    profundidad + 1,
                    False,
                    alfa,
                    beta,
                    nivel + 1
                )

                tablero[i] = VACIO

                print(
                    "   " * nivel +
                    f"Movimiento {i}"
                    f" => {valor}"
                )

                mejor = max(
                    mejor,
                    valor
                )

                alfa = max(
                    alfa, 
                    mejor
                )

                if alfa >= beta:
                    print(("   " * nivel + f"--- Poda MAX en movimiento {i} (alfa={alfa} >= beta={beta}) ---"))
                    break

        print(
            "   " * nivel +
            f"MAX devuelve {mejor}"
        )

        return mejor

    else:

        mejor = math.inf

        print(
            "   " * nivel +
            "MIN analiza (alfa={alfa}, beta={beta}):"
        )

        for i in range(9):

            if tablero[i] == VACIO:

                tablero[i] = HUMANO

                valor = alfa_beta(
                    tablero,
                    profundidad + 1,
                    True,
                    alfa,
                    beta,
                    nivel + 1
                )

                tablero[i] = VACIO

                print(
                    "   " * nivel +
                    f"Movimiento {i}"
                    f" => {valor}"
                )

                mejor = min(
                    mejor,
                    valor
                )

                beta = min(
                    beta,
                    mejor
                )

                if alfa >= beta:
                    print(("   " * nivel + f"--- Poda MIN en movimiento {i} (alfa={alfa} >= beta={beta}) ---"))
                    break

        print(
            "   " * nivel +
            f"MIN devuelve {mejor}"
        )

        return mejor

# ---------------------------------------
# Mejor movimiento IA
# ---------------------------------------
def mejor_movimiento(tablero):

    global nodos_evaluados

    nodos_evaluados = 0

    mejor_valor = -math.inf
    mejor_mov = -1

    print("\n================================")
    print("ANÁLISIS MINIMAX")
    print("================================\n")

    for i in range(9):

        if tablero[i] == VACIO:

            tablero[i] = IA

            valor = minimax(
                tablero,
                0,
                False,
                1
            )

            tablero[i] = VACIO

            print(
                f"\nMovimiento {i}"
                f" tiene valor {valor}"
            )

            if valor > mejor_valor:

                mejor_valor = valor
                mejor_mov = i

    print("\n================================")
    print(
        f"Mejor movimiento: "
        f"{mejor_mov}"
    )
    print(
        f"Valor minimax: "
        f"{mejor_valor}"
    )
    print(
        f"Nodos evaluados: "
        f"{nodos_evaluados}"
    )
    print("================================\n")

    return mejor_mov


# ---------------------------------------
# Juego
# ---------------------------------------
def jugar_minimax():

    tablero = [VACIO] * 9

    print("\n=== GATO CON MINIMAX ===\n")

    print(
        "Posiciones:\n"
    )

    print(
        " 0 | 1 | 2\n"
        "---+---+---\n"
        " 3 | 4 | 5\n"
        "---+---+---\n"
        " 6 | 7 | 8\n"
    )

    while True:

        imprimir_tablero(tablero)

        movimiento = int(
            input(
                "Tu movimiento: "
            )
        )

        if (
            movimiento < 0 or
            movimiento > 8 or
            tablero[movimiento] != VACIO
        ):
            print(
                "Movimiento inválido"
            )
            continue

        tablero[movimiento] = HUMANO

        if terminal(tablero):

            break

        print(
            "\nLa IA está pensando...\n"
        )

        mov = mejor_movimiento(
            tablero
        )

        tablero[mov] = IA

        if terminal(tablero):

            break

    imprimir_tablero(tablero)

    g = ganador(tablero)

    if g == HUMANO:

        print("Ganaste")

    elif g == IA:

        print("La IA gana")

    else:

        print("Empate")

# ---------------------------------------
# Mejor movimiento IA
# ---------------------------------------
def mejor_movimiento_alfa_beta(tablero):

    global nodos_evaluados

    nodos_evaluados = 0

    mejor_valor = -math.inf
    mejor_mov = -1

    print("\n================================")
    print("ANÁLISIS PODA ALFA-BETA")
    print("================================\n")

    for i in range(9):

        if tablero[i] == VACIO:

            tablero[i] = IA

            valor = alfa_beta(
                tablero,
                0,
                False,
                -math.inf,
                math.inf,
                1
            )

            tablero[i] = VACIO

            print(
                f"\nMovimiento {i}"
                f" tiene valor {valor}"
            )

            if valor > mejor_valor:

                mejor_valor = valor
                mejor_mov = i

    print("\n================================")
    print(
        f"Mejor movimiento: "
        f"{mejor_mov}"
    )
    print(
        f"Valor minimax: "
        f"{mejor_valor}"
    )
    print(
        f"Nodos evaluados: "
        f"{nodos_evaluados}"
    )
    print("================================\n")

    return mejor_mov


# ---------------------------------------
# Juego
# ---------------------------------------
def jugar_alpha_beta():

    tablero = [VACIO] * 9

    print("\n=== GATO CON PODA ALFA-BETA ===\n")

    print(
        "Posiciones:\n"
    )

    print(
        " 0 | 1 | 2\n"
        "---+---+---\n"
        " 3 | 4 | 5\n"
        "---+---+---\n"
        " 6 | 7 | 8\n"
    )

    while True:

        imprimir_tablero(tablero)

        movimiento = int(
            input(
                "Tu movimiento: "
            )
        )

        if (
            movimiento < 0 or
            movimiento > 8 or
            tablero[movimiento] != VACIO
        ):
            print(
                "Movimiento inválido"
            )
            continue

        tablero[movimiento] = HUMANO

        if terminal(tablero):

            break

        print(
            "\nLa IA está pensando...\n"
        )

        mov = mejor_movimiento_alfa_beta(
            tablero
        )

        tablero[mov] = IA

        if terminal(tablero):

            break

    imprimir_tablero(tablero)

    g = ganador(tablero)

    if g == HUMANO:

        print("Ganaste")

    elif g == IA:

        print("La IA gana")

    else:

        print("Empate")


# ---------------------------------------
# Main
# ---------------------------------------
if __name__ == "__main__":
    jugar_minimax()