import heapq
import collections
import os

class frozenLakeSolver:
    def __init__(self, tablero_cadenas):
        """
        tablero_cadenas: lista de strings, cada string es una fila.
        Caracteres:
        P -> punto de partida del jugador (debe haber exactamente uno)
        H -> agujero (el jugador no debe pisarlo)
        F -> bloque de hielo
        G -> meta (debe haber al menos una)
        """
        self.tablero_cadenas = tablero_cadenas
        self.alto = len(tablero_cadenas)
        self.ancho = len(tablero_cadenas[0]) if self.alto > 0 else 0
        
        self.holes = set()
        self.goal = None
        self.jugador = None
        
        # Validar ancho consistente y mapear el entorno
        for y, fila in enumerate(tablero_cadenas):
            if len(fila) != self.ancho:
                raise ValueError(f"La fila {y} tiene {len(fila)} columnas, se esperaban {self.ancho}")
            for x, ch in enumerate(fila):
                if ch == 'H':
                    self.holes.add((x, y))
                elif ch == 'G':
                    if self.goal is not None:
                        raise ValueError("Solo puede existir una meta (G)")
                    self.goal = (x, y)
                elif ch == 'P':
                    if self.jugador is not None:
                        raise ValueError("Solo puede haber un punto de partida para el jugador (P)")
                    self.jugador = (x, y)
                elif ch == 'F':
                    continue
                else:
                    raise ValueError(f"Caracter invalido '{ch}' en ({x}, {y})")
        
        if self.jugador is None:
            raise ValueError("Debe haber haber un punto de partida para el jugador (P)")
        
        if self.goal is None:
            raise ValueError("Debe haber exactamente una meta (G)")
        
        self.holes = frozenset(self.holes)
    
    def es_meta(self,  pos):
        return pos == self.goal
    
    def es_celda_valida(self, x, y):
        return (0 <= x < self.ancho and 0 <= y < self.alto and
                (x, y) not in self.holes)
    
    def movimientos_validos(self, posicion):
        dirs = [(0, 1, 'abajo'), (0, -1, 'arriba'),
                (1, 0, 'derecha'), (-1, 0, 'izquierda')]
        resultados = []
        x, y = posicion
        
        for dx, dy, nombre in dirs:
            nx, ny = x + dx, y + dy
            if self.es_celda_valida(nx, ny):
                resultados.append(((nx, ny), nombre))
        
        return resultados
    
    def resolver_bfs(self):
        queue = collections.deque([(self.jugador, [])])
        visitados = set()
        visitados.add(self.jugador)
        
        while queue:
            actual, camino = queue.popleft()
            
            if self.es_meta(actual):
                return camino
            
            for nuevo_estado, direccion in self.movimientos_validos(actual):
                if nuevo_estado not in visitados:
                    visitados.add(nuevo_estado)
                    nuevo_camino = camino + [direccion]
                    queue.append((nuevo_estado, nuevo_camino))
                    
        return None
    
    def resolver_dfs(self):
        stack = [(self.jugador, [])]
        visitados = set()
        
        while stack:
            actual, camino = stack.pop()
            
            if actual in visitados:
                continue
            visitados.add(actual)

            if self.es_meta(actual):
                return camino
            
            for nuevo_estado, direccion in self.movimientos_validos(actual):
                if nuevo_estado not in visitados:
                    nuevo_camino = camino + [direccion]
                    stack.append((nuevo_estado, nuevo_camino))
                    
        return None
    
    def imprimir_tablero(self, jugador_pos):
        tablero = [['.' for _ in range(self.ancho)] for _ in range(self.alto)]
        
        for hx, hy in self.holes:
            tablero[hy][hx] = 'H'
        gx, gy = self.goal
        tablero[gy][gx] = 'G'
        
        jx, jy = jugador_pos
        if tablero[jy][jx] == 'G':
            tablero[jy][jx] = 'W'
        else:
            tablero[jy][jx] = 'P'
        
        print("  " + " ".join(str(i) for i in range(self.ancho)))
        for y in range(self.alto):
            print(f"{y} " + " ".join(tablero[y]))
        print()

def elegirAlgoritmo():
    os.system('cls')
    print("\nElige el algoritmo de búsqueda:")
    print("1. BFS (Búsqueda en Anchura)")
    print("2. DFS (Búsqueda en Profundidad)")
    print("3. Regresar al menú anterior")
    while True:
        opcion = int(input("Opción: "))
        if opcion in (1, 2, 3):
            return opcion
        else:
            print("Opción no válida. Ingresa un número del 1 al 3.")



def run():
    print("=== RESOLVEDOR FROZEN LAKE (BFS / DFS) ===")
    print("\nINSTRUCCIONES:")
    print("Debes ingresar varias lineas que representan el lago congelado.")
    print("Cada linea debe tener la misma longitud.")
    print("Caracteres validos:")
    print("  P  -> Inicio")
    print("  G  -> Meta")
    print("  F  -> Bloque de hielo")
    print("  H  -> Agujero")
    print("Ejemplo:")
    print("PFFF")
    print("FHFH")
    print("FFFH")
    print("HFFG")
    print("Para terminar de ingresar, deja una linea vacia.\n")

    print("Ingresa el tablero linea por linea:")
    lineas = []
    while True:
        linea = input().strip()
        if linea == "":
            if len(lineas) == 0:
                print("Debes ingresar al menos una linea.")
                continue
            break
        lineas.append(linea)

    try:
        solver = frozenLakeSolver(lineas)  
    except ValueError as e:
        print(f"Error: {e}")
        input("\nPresiona cualquier tecla para continuar...")
        return

    dir_map = {
        'arriba': (0, -1),
        'abajo': (0, 1),
        'izquierda': (-1, 0),
        'derecha': (1, 0)
    }
    
    while True:
        opcion = elegirAlgoritmo()
        os.system('cls')
        
        print("\n--- Configuración inicial ---")
        solver.imprimir_tablero(solver.jugador)

        if opcion == 2:
            print("Buscando solución con DFS...")
            solucion = solver.resolver_dfs()
        elif opcion == 3:
            return
        else:       
            print("Buscando solución con BFS...")
            solucion = solver.resolver_bfs()
        
        if solucion is None:
            print("No se encontro solucion para este nivel.")
        else:
            print(f"Solucion encontrada en {len(solucion)} movimientos:")
            print(" -> ".join(solucion))

            print("\n--- Simulacion de la solucion ---")
            jugador_act = solver.jugador
            solver.imprimir_tablero(jugador_act)
            
            input("Presiona Enter para comenzar la simulacion paso a paso...")
            
            for i, movimiento in enumerate(solucion):
                input(f"\nPaso {i+1}: {movimiento} -> Enter")
                dx, dy = dir_map[movimiento]
                jugador_act = (jugador_act[0] + dx, jugador_act[1] + dy)
                solver.imprimir_tablero(jugador_act)
            
            print("\n¡META ALCANZADA!")
        input("\nPresiona cualquier tecla para continuar...")

if __name__ == "__main__":
    run()