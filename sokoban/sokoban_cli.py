import heapq

class SokobanSolver:
    def __init__(self, tablero_cadenas):
        """
        tablero_cadenas: lista de strings, cada string es una fila.
        Caracteres:
        0 -> espacio vacio
        P -> jugador (debe haber exactamente uno)
        X -> muro
        B -> caja
        _ -> boton
        """
        self.tablero_cadenas = tablero_cadenas
        self.alto = len(tablero_cadenas)
        self.ancho = len(tablero_cadenas[0]) if self.alto > 0 else 0
        
        self.muros = set()
        self.botones = set()
        self.cajas = set()
        self.jugador = None
        
        # Validar ancho consistente
        for y, fila in enumerate(tablero_cadenas):
            if len(fila) != self.ancho:
                raise ValueError(f"La fila {y} tiene {len(fila)} columnas, se esperaban {self.ancho}")
            for x, ch in enumerate(fila):
                if ch == 'X':
                    self.muros.add((x, y))
                elif ch == 'B':
                    self.cajas.add((x, y))
                elif ch == '_':
                    self.botones.add((x, y))
                elif ch == 'P':
                    if self.jugador is not None:
                        raise ValueError("Solo puede haber un jugador (P)")
                    self.jugador = (x, y)
                elif ch == '0':
                    continue
                else:
                    raise ValueError(f"Caracter invalido '{ch}' en ({x}, {y})")
        
        if self.jugador is None:
            raise ValueError("Debe haber un jugador (P)")
        
        if len(self.botones) == 0:
            raise ValueError("Debe haber al menos un boton (_)")
        
        if len(self.botones) > len(self.cajas):
            raise ValueError("No puede haber mas botones que cajas")
        
        # Validar que nada este sobre muro
        if self.jugador in self.muros:
            raise ValueError("El jugador no puede estar sobre un muro")
        for c in self.cajas:
            if c in self.muros:
                raise ValueError(f"Caja en {c} sobre muro")
        for b in self.botones:
            if b in self.muros:
                raise ValueError(f"Boton en {b} sobre muro")
        
        self.cajas = frozenset(self.cajas)
        self.botones = frozenset(self.botones)
        self.muros = frozenset(self.muros)
    
    def es_meta(self, cajas):
        return all(caja in self.botones for caja in cajas)
    
    def es_celda_valida(self, x, y):
        return (0 <= x < self.ancho and 0 <= y < self.alto and
                (x, y) not in self.muros)
    
    def movimientos_validos(self, jugador, cajas):
        dirs = [(0, 1, 'abajo'), (0, -1, 'arriba'),
                (1, 0, 'derecha'), (-1, 0, 'izquierda')]
        resultados = []
        x, y = jugador
        
        for dx, dy, nombre in dirs:
            nx, ny = x + dx, y + dy
            nueva_pos_jug = (nx, ny)
            
            if not self.es_celda_valida(nx, ny):
                continue
            
            if nueva_pos_jug in cajas:
                cx, cy = nx + dx, ny + dy
                nueva_pos_caja = (cx, cy)
                
                if (self.es_celda_valida(cx, cy) and
                    nueva_pos_caja not in cajas):
                    nuevas_cajas = set(cajas)
                    nuevas_cajas.remove(nueva_pos_jug)
                    nuevas_cajas.add(nueva_pos_caja)
                    resultados.append((nueva_pos_jug, frozenset(nuevas_cajas), nombre, 2))
            else:
                resultados.append((nueva_pos_jug, cajas, nombre, 1))
        
        return resultados
    
    def heuristica(self, cajas):
        if not self.botones:
            return 0
        lista_botones = list(self.botones)
        total = 0
        for caja in cajas:
            min_dist = min(abs(caja[0] - b[0]) + abs(caja[1] - b[1])
                           for b in lista_botones)
            total += min_dist
        return total
    
    def resolver(self):
        start_state = (self.jugador, self.cajas, [])
        g_score = {(self.jugador, self.cajas): 0}
        f_score = {(self.jugador, self.cajas): self.heuristica(self.cajas)}
        
        open_set = [(f_score[(self.jugador, self.cajas)], start_state)]
        heapq.heapify(open_set)
        visitados = set()
        visitados.add((self.jugador, self.cajas))
        
        while open_set:
            _, (jugador, cajas, camino) = heapq.heappop(open_set)
            
            if self.es_meta(cajas):
                return camino
            
            for nuevo_jug, nuevas_cajas, direccion, costo in self.movimientos_validos(jugador, cajas):
                nuevo_estado = (nuevo_jug, nuevas_cajas)
                if nuevo_estado in visitados:
                    continue
                
                nuevo_camino = camino + [direccion]
                g_tentativo = g_score[(jugador, cajas)] + costo
                
                if nuevo_estado not in g_score or g_tentativo < g_score[nuevo_estado]:
                    g_score[nuevo_estado] = g_tentativo
                    f_score[nuevo_estado] = g_tentativo + self.heuristica(nuevas_cajas)
                    heapq.heappush(open_set, (f_score[nuevo_estado],
                                              (nuevo_jug, nuevas_cajas, nuevo_camino)))
                    visitados.add(nuevo_estado)
        return None
    
    def imprimir_tablero(self, jugador, cajas):
        tablero = [['.' for _ in range(self.ancho)] for _ in range(self.alto)]
        
        for mx, my in self.muros:
            tablero[my][mx] = '#'
        for bx, by in self.botones:
            if tablero[by][bx] != '#':
                tablero[by][bx] = 'O'
        for cx, cy in cajas:
            if (cx, cy) in self.botones:
                tablero[cy][cx] = 'X'
            elif tablero[cy][cx] != '#':
                tablero[cy][cx] = 'C'
        
        jx, jy = jugador
        if tablero[jy][jx] == 'O':
            tablero[jy][jx] = 'J'
        elif tablero[jy][jx] not in ['C', 'X', '#']:
            tablero[jy][jx] = 'J'
        
        print("  " + " ".join(str(i) for i in range(self.ancho)))
        for y in range(self.alto):
            print(f"{y} " + " ".join(tablero[y]))
        print()


def run():
    print("=== RESOLVEDOR SOKOBAN (Busqueda Informada A*) ===")
    print("\nINSTRUCCIONES:")
    print("Debes ingresar varias lineas que representan el tablero.")
    print("Cada linea debe tener la misma longitud.")
    print("Caracteres validos:")
    print("  0  -> espacio vacio")
    print("  P  -> jugador (solo uno)")
    print("  X  -> muro")
    print("  B  -> caja")
    print("  _  -> boton (donde debe ir la caja)")
    print("Ejemplo:")
    print("0PXXX000")
    print("0000B0_0")
    print("XXXXB000")
    print("_0000000")
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
        solver = SokobanSolver(lineas)
        print("\n--- Configuracion inicial ---")
        solver.imprimir_tablero(solver.jugador, solver.cajas)
        
        print("Buscando solucion con A*...")
        solucion = solver.resolver()
        
        if solucion is None:
            print("No se encontro solucion para este nivel.")
        else:
            print(f"Solucion encontrada en {len(solucion)} movimientos:")
            print(" -> ".join(solucion))
            
            print("\n--- Simulacion de la solucion ---")
            jugador_act = solver.jugador
            cajas_act = set(solver.cajas)
            solver.imprimir_tablero(jugador_act, frozenset(cajas_act))
            
            dir_map = {
                'arriba': (0, -1),
                'abajo': (0, 1),
                'izquierda': (-1, 0),
                'derecha': (1, 0)
            }
            
            input("Presiona Enter para comenzar la simulacion paso a paso...")
            
            for i, movimiento in enumerate(solucion):
                input(f"\nPaso {i+1}: {movimiento} -> Enter")
                dx, dy = dir_map[movimiento]
                jugador_act = (jugador_act[0] + dx, jugador_act[1] + dy)
                
                if jugador_act in cajas_act:
                    caja_nueva = (jugador_act[0] + dx, jugador_act[1] + dy)
                    cajas_act.remove(jugador_act)
                    cajas_act.add(caja_nueva)
                
                solver.imprimir_tablero(jugador_act, frozenset(cajas_act))
            
            print("\nSOLUCION COMPLETA - Todos los botones presionados")
    
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")

if __name__ == "__main__":
    run()