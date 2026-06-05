import heapq
import pygame
import sys

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


class SokobanPygame:
    def __init__(self, solver, solucion):
        pygame.init()
        self.solver = solver
        self.solucion = solucion
        self.paso_actual = 0
        
        # Estado actual para simulacion
        self.jugador_act = solver.jugador
        self.cajas_act = set(solver.cajas)
        
        self.celda_size = 60
        self.ancho = solver.ancho
        self.alto = solver.alto
        
        # Configurar ventana
        self.screen = pygame.display.set_mode((self.ancho * self.celda_size, 
                                               self.alto * self.celda_size + 100))
        pygame.display.set_caption("Sokoban - Simulador de Solucion")
        
        # Fuentes
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colores
        self.colores = {
            'suelo': (240, 240, 240),
            'pared': (51, 51, 51),
            'caja': (205, 127, 50),     # color cobre
            'caja_objetivo': (255, 215, 0),  # dorado
            'objetivo': (144, 238, 144),  # verde claro
            'jugador': (65, 105, 225),   # azul real
            'jugador_objetivo': (30, 144, 255),
            'texto': (0, 0, 0),
            'boton': (200, 200, 200),
            'boton_hover': (170, 170, 170)
        }
        
        # Botones
        self.botones_rect = {}
        self.crear_botones()
        
        self.clock = pygame.time.Clock()
        self.mensaje = ""
        self.mensaje_tiempo = 0
    
    def crear_botones(self):
        """Crea los botones de control"""
        ancho_ventana = self.ancho * self.celda_size
        y_base = self.alto * self.celda_size + 20
        
        botones_info = [
            ("Anterior", 20),
            ("Siguiente", 150),
            ("Reiniciar", 280),
            ("Auto", 410)
        ]
        
        for texto, x in botones_info:
            rect = pygame.Rect(x, y_base, 100, 40)
            self.botones_rect[texto] = rect
    
    def dibujar_tablero(self):
        """Dibuja el tablero con el estado actual"""
        for y in range(self.alto):
            for x in range(self.ancho):
                x1 = x * self.celda_size
                y1 = y * self.celda_size
                
                # Determinar que hay en esta celda
                es_muro = (x, y) in self.solver.muros
                es_boton = (x, y) in self.solver.botones
                es_caja = (x, y) in self.cajas_act
                es_jugador = (x, y) == self.jugador_act
                
                # Dibujar fondo
                if es_boton and not es_muro:
                    color_fondo = self.colores['objetivo']
                else:
                    color_fondo = self.colores['suelo']
                
                pygame.draw.rect(self.screen, color_fondo, (x1, y1, self.celda_size, self.celda_size))
                pygame.draw.rect(self.screen, (128, 128, 128), (x1, y1, self.celda_size, self.celda_size), 1)
                
                # Dibujar muro
                if es_muro:
                    pygame.draw.rect(self.screen, self.colores['pared'], 
                                   (x1, y1, self.celda_size, self.celda_size))
                    # Textura de ladrillo
                    pygame.draw.line(self.screen, (68, 68, 68),
                                   (x1, y1 + self.celda_size//2),
                                   (x1 + self.celda_size, y1 + self.celda_size//2), 2)
                else:
                    # Dibujar elementos
                    if es_caja:
                        if es_boton:
                            color_caja = self.colores['caja_objetivo']
                            pygame.draw.rect(self.screen, color_caja,
                                           (x1+5, y1+5, self.celda_size-10, self.celda_size-10))
                            # Dibujar X
                            texto_x = self.font.render("X", True, (255, 255, 255))
                            self.screen.blit(texto_x, (x1 + self.celda_size//2 - 10, 
                                                       y1 + self.celda_size//2 - 15))
                        else:
                            pygame.draw.rect(self.screen, self.colores['caja'],
                                           (x1+5, y1+5, self.celda_size-10, self.celda_size-10))
                    
                    if es_jugador:
                        if es_boton:
                            color_jug = self.colores['jugador_objetivo']
                        else:
                            color_jug = self.colores['jugador']
                        
                        pygame.draw.circle(self.screen, color_jug,
                                         (x1 + self.celda_size//2, y1 + self.celda_size//2),
                                         self.celda_size//2 - 10)
                        # Ojos
                        pygame.draw.circle(self.screen, (255, 255, 255),
                                         (x1 + self.celda_size//3, y1 + self.celda_size//3), 5)
                        pygame.draw.circle(self.screen, (255, 255, 255),
                                         (x1 + 2*self.celda_size//3, y1 + self.celda_size//3), 5)
    
    def dibujar_controles(self):
        """Dibuja los botones y la información"""
        y_base = self.alto * self.celda_size
        
        # Fondo de la zona de controles
        pygame.draw.rect(self.screen, (240, 240, 240),
                        (0, y_base, self.ancho * self.celda_size, 100))
        
        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        for texto, rect in self.botones_rect.items():
            color = self.colores['boton_hover'] if rect.collidepoint(mouse_pos) else self.colores['boton']
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            
            texto_surface = self.small_font.render(texto, True, self.colores['texto'])
            texto_rect = texto_surface.get_rect(center=rect.center)
            self.screen.blit(texto_surface, texto_rect)
        
        # Informacion de pasos
        info_text = f"Paso {self.paso_actual} de {len(self.solucion)}"
        info_surface = self.font.render(info_text, True, self.colores['texto'])
        self.screen.blit(info_surface, (20, y_base + 70))
        
        # Mostrar movimiento actual si hay
        if self.paso_actual > 0 and self.paso_actual <= len(self.solucion):
            mov_text = f"Ultimo movimiento: {self.solucion[self.paso_actual - 1]}"
            mov_surface = self.small_font.render(mov_text, True, (100, 100, 255))
            self.screen.blit(mov_surface, (300, y_base + 75))
        
        # Mostrar mensaje temporal
        if self.mensaje and pygame.time.get_ticks() - self.mensaje_tiempo < 2000:
            msg_surface = self.small_font.render(self.mensaje, True, (255, 0, 0))
            msg_rect = msg_surface.get_rect(center=(self.ancho * self.celda_size // 2, y_base + 40))
            self.screen.blit(msg_surface, msg_rect)
    
    def siguiente_paso(self):
        """Avanza un paso en la simulacion"""
        if self.paso_actual >= len(self.solucion):
            self.mensaje = "Solucion completada!"
            self.mensaje_tiempo = pygame.time.get_ticks()
            return
        
        movimiento = self.solucion[self.paso_actual]
        
        dir_map = {
            'arriba': (0, -1),
            'abajo': (0, 1),
            'izquierda': (-1, 0),
            'derecha': (1, 0)
        }
        
        dx, dy = dir_map[movimiento]
        self.jugador_act = (self.jugador_act[0] + dx, self.jugador_act[1] + dy)
        
        # Verificar si empujo una caja
        if self.jugador_act in self.cajas_act:
            caja_nueva = (self.jugador_act[0] + dx, self.jugador_act[1] + dy)
            self.cajas_act.remove(self.jugador_act)
            self.cajas_act.add(caja_nueva)
        
        self.paso_actual += 1
        
        # Verificar si es solucion
        if self.solver.es_meta(frozenset(self.cajas_act)):
            self.mensaje = "SOLUCION COMPLETA!"
            self.mensaje_tiempo = pygame.time.get_ticks()
    
    def paso_anterior(self):
        """Retrocede un paso en la simulacion"""
        if self.paso_actual == 0:
            self.mensaje = "Ya estas al inicio"
            self.mensaje_tiempo = pygame.time.get_ticks()
            return
        
        # Reiniciar y avanzar hasta el paso anterior
        self.reiniciar()
        for _ in range(self.paso_actual - 1):
            self.siguiente_paso()
    
    def reiniciar(self):
        """Reinicia la simulacion al estado inicial"""
        self.paso_actual = 0
        self.jugador_act = self.solver.jugador
        self.cajas_act = set(self.solver.cajas)
        self.mensaje = "Reiniciado"
        self.mensaje_tiempo = pygame.time.get_ticks()
    
    def auto_play(self):
        """Ejecuta automaticamente la solucion completa"""
        for _ in range(len(self.solucion) - self.paso_actual):
            self.siguiente_paso()
            self.dibujar_tablero()
            self.dibujar_controles()
            pygame.display.flip()
            pygame.time.wait(300)  # Esperar 300ms entre movimientos
    
    def run(self):
        """Bucle principal de pygame"""
        running = True
        auto_mode = False
        auto_timer = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for texto, rect in self.botones_rect.items():
                        if rect.collidepoint(mouse_pos):
                            if texto == "Siguiente":
                                self.siguiente_paso()
                            elif texto == "Anterior":
                                self.paso_anterior()
                            elif texto == "Reiniciar":
                                self.reiniciar()
                            elif texto == "Auto":
                                self.auto_play()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.siguiente_paso()
                    elif event.key == pygame.K_LEFT:
                        self.paso_anterior()
                    elif event.key == pygame.K_r:
                        self.reiniciar()
                    elif event.key == pygame.K_SPACE:
                        self.auto_play()
            
            # Limpiar pantalla
            self.screen.fill(self.colores['suelo'])
            
            # Dibujar todo
            self.dibujar_tablero()
            self.dibujar_controles()
            
            # Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
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
    print("Para terminar de ingresar, escribe 'FIN' o deja una linea vacia.\n")
    
    print("Ingresa el tablero linea por linea:")
    lineas = []
    while True:
        linea = input().strip()
        if linea == "" or linea.upper() == "FIN":
            if len(lineas) == 0:
                print("Debes ingresar al menos una linea.")
                continue
            break
        lineas.append(linea)
    
    try:
        solver = SokobanSolver(lineas)
        
        print("\n--- Configuracion inicial ---")
        print("Buscando solucion con A*...")
        solucion = solver.resolver()
        
        if solucion is None:
            print("No se encontro solucion para este nivel.")
            return
        
        print(f"Solucion encontrada en {len(solucion)} movimientos:")
        print(" -> ".join(solucion))
        print("\nAbriendo ventana grafica con Pygame...")
        print("\nCONTROLES:")
        print("  Boton Siguiente o Flecha Derecha: Avanzar un paso")
        print("  Boton Anterior o Flecha Izquierda: Retroceder un paso")
        print("  Boton Reiniciar o Tecla R: Reiniciar simulacion")
        print("  Boton Auto o Barra Espaciadora: Reproducir automaticamente")
        
        # Iniciar pygame
        app = SokobanPygame(solver, solucion)
        app.run()
        
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")


if __name__ == "__main__":
    main()
