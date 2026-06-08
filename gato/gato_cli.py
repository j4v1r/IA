from gato.gato import (
    jugar_minimax,
    #jugar_alpha_beta
)


def menu_gato():

    print("\n=== GATO ===")
    print("1. Jugar contra Minimax")
    print("2. Jugar contra Poda Alfa-Beta")
    print("3. Regresar")

    while True:

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion in ("1", "2", "3"):
            return opcion

        print("Opción no válida.")


def run():

    while True:

        opcion = menu_gato()

        if opcion == "3":
            return

        elif opcion == "1":

            print(
                "\n=== MINIMAX ==="
            )

            jugar_minimax()

        elif opcion == "2":

            print(
                "\n=== PODA ALFA-BETA ==="
            )

            #jugar_alpha_beta()

        input(
            "\nPresione ENTER para continuar..."
        )