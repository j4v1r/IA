import heapq
import math

#### SOKOBAN ####
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

#### GBFS ####
class Position:
    x: int
    y: int
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return "[{},{}]".format(self.x, self.y)
    def __eq__(self,other):
      if not isinstance(other,Position):
        return False
      return self.x==other.x and self.y==other.y

class Grid:
    width: int
    height: int
    values: list
    pos_inicial: Position
    pos_final: Position
    bloqueados = []
    def __init__(self,width: int, height: int):
        self.width = width
        self.height = height
        self.values = [[None for _ in range(width)] for _ in range(height)]
        pass
    def rellenar(self,values):
        cont_i=0
        cont_j=0
        for i in values:
            cont_j=0
            for j in i:
                match(j):
                    case 'I':
                        self.pos_inicial=Position(cont_i, cont_j)
                        pass
                    case 'F':
                        self.pos_final = Position(cont_i, cont_j)
                    case 'X':
                        self.bloqueados.append(Position(cont_i, cont_j))
                self.values[cont_i][cont_j] = j
                cont_j+=1
            cont_i+=1
        pass
    def __str__(self):
        resultado = ""
        for i in self.values:
            resultado += "[ "
            for j in i:
                match(j):
                    case 0:
                        resultado += "0 "
                    case 'X':
                        resultado += "X "
                    case 'F':
                        resultado += "F "
                    case 'I':
                        resultado += "I "
            resultado += "]\n"
        resultado += "Cuadricula de {} x {}".format(self.width,self.height)
        return resultado
        pass

class PosCost:
  pos: Position
  cost=0
  def __init__(self,pos,cost):
    self.pos=pos
    self.cost=cost
    pass
  def __repr__(self):
    return "{}({})".format(self.pos,self.cost)
  pass
class GBFS:
    pos_actual: Position
    open = []
    closed = []
    grid: Grid
    def __init__(self, grid: Grid):
        self.grid = grid 
        self.pos_actual = grid.pos_inicial
        
        choice = int(input("Elija 0 para usar heurística euclidiana, 1 para heurística Manhattan: "))
        funcion_costo = self.get_distance_euclidean if choice==0 else self.get_distance_manhattan
        while not self.pos_actual == self.grid.pos_final:
            neighbors = self.get_neighbors(self.pos_actual, funcion_costo)
            print("POSICIÓN ACTUAL: ", self.pos_actual)
            for neighbor in neighbors:
                self.to_open(neighbor)
            print("OPEN:", self.open)
            self.to_closed()
            print("CLOSE:", self.closed)
            #self.open=[PosCost(Position(2,3),-4),PosCost(Position(2,4),7),PosCost(Position(1,1),1)]
            self.pos_actual = self.get_min_cost().pos
            self.open.clear()
            print("\n")
        print("llegada a POSICIÓN FINAL: ", self.grid.pos_final)

        

        
        

        
    def get_neighbors(self, pos, cost):
      neighbors = []
      movs = [(1,0),(-1,0),(0,1),(0,-1)]
      for dx,dy in movs:
        new_x,new_y=pos.x+dx, pos.y+dy
        if 0<=new_x<self.grid.height and 0<=new_y<self.grid.width:
          son = Position(new_x,new_y)
          if not son in self.grid.bloqueados:
            neighbors.append(PosCost(son,cost(son)))
      return neighbors
      pass

    def to_open(self, neighbor):
        if neighbor.pos in self.closed:
            return
        self.open.append(neighbor)
        pass
    def to_closed(self):
        self.closed.append(self.pos_actual)
        pass
      
    def get_distance_manhattan(self,pos):
      return abs(pos.x-self.grid.pos_final.x)+abs(pos.y-self.grid.pos_final.y)
      pass
    def get_distance_euclidean(self,pos)-> float:
       return math.sqrt(math.pow(pos.x-self.grid.pos_final.x,2 + math.pow(pos.y-self.grid.pos_final.y,2)))
       pass
    def get_min_cost(self):
       return min(self.open, key=lambda x : x.cost)
       pass

def launch_gbfs():
    quad = Grid(7,4)
    X='X'
    F='F'
    I='I'
    quad.rellenar(
        [[0,X,0,0,0,0,0],
        [0,0,0,X,F,X,X],
        [0,X,0,X,0,0,0],
        [I,X,0,0,0,0,0]]
    )
    print(quad)
    gbfs: GBFS = GBFS(quad)
    pass

def launch_sokoban():
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


def main():
    print("Elige un problema a resolver: ")
    print("Sokoban -> Escribe 'S'")
    print("GBFS -> Escribe 'G'")
    print("Salir -> Pulsa otra tecla")
    opcion = input()
    match opcion:
        case 'S':
            launch_sokoban()
            return
            pass
        case 'G':
            launch_gbfs()
            return
            pass
        case _:
            return
            pass
            
   

if __name__ == "__main__":
    main()
