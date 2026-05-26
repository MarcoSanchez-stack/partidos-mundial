# Registra los puntos de cada equipo, los partidos jugados, goles a favor y en contra, y mostrara la tabla de posiciones del grupo.

from datetime import datetime
from typing import List, Tuple, Optional


class Equipo:
    ## Representa un equipo participante en el grupo
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.partidos_jugados = 0
        self.victorias = 0
        self.empates = 0
        self.derrotas = 0
        self.goles_a_favor = 0
        self.goles_en_contra = 0
    
    def puntos(self) -> int:
        ## Calcula los puntos totales del equipo
        return (self.victorias * 3) + (self.empates * 1)
    
    def diferencia_goles(self) -> int:
        """Calcula la diferencia de goles"""
        return self.goles_a_favor - self.goles_en_contra
    
    def registrar_victoria(self, goles_a_favor: int, goles_en_contra: int):
        ## Registra una victoria
        self.partidos_jugados += 1
        self.victorias += 1
        self.goles_a_favor += goles_a_favor
        self.goles_en_contra += goles_en_contra
    
    def registrar_empate(self, goles_a_favor: int, goles_en_contra: int):
        ## Registra un empate
        self.partidos_jugados += 1
        self.empates += 1
        self.goles_a_favor += goles_a_favor
        self.goles_en_contra += goles_en_contra
    
    def registrar_derrota(self, goles_a_favor: int, goles_en_contra: int):
        # Registra una derrota 
        self.partidos_jugados += 1
        self.derrotas += 1
        self.goles_a_favor += goles_a_favor
        self.goles_en_contra += goles_en_contra
    
    def __repr__(self) -> str:
        return (f"Equipo({self.nombre}, PJ:{self.partidos_jugados}, "
                f"Pts:{self.puntos}, GF:{self.goles_a_favor}, GC:{self.goles_en_contra})")


class Partido:
    #Representa un partido o los partidos jugados entre dos equipos en el grupo
    
    def __init__(self, equipo1: str, equipo2: str, goles1: int, goles2: int, fecha: str = None):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.goles1 = goles1
        self.goles2 = goles2
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def __repr__(self) -> str:
        return f"{self.equipo1} {self.goles1} - {self.goles2} {self.equipo2} ({self.fecha})"


class GrupoMundial:
    # Representa un grupo del mundial con sus equipos, partidos y tablas de posiciones
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.equipos: dict = {}
        self.partidos: List[Partido] = []
    
    def agregar_equipo(self, nombre_equipo: str):
        # Esto agrega un nuevo grupo al mundial, teniendo en cuenta o revisando si no existe ya previamente en el grupo
        if nombre_equipo in self.equipos:
            print(f"⚠️  El equipo '{nombre_equipo}' ya existe en el grupo")
            return False
        
        self.equipos[nombre_equipo] = Equipo(nombre_equipo)
        print(f"✓ Equipo '{nombre_equipo}' agregado al grupo")
        return True
    
    def registrar_partido(self, equipo1: str, equipo2: str, goles1: int, goles2: int, 
                         fecha: str = None) -> bool:
        """Registra un nuevo partido y actualiza estadísticas"""
        # Validar que los equipos existan
        if equipo1 not in self.equipos:
            print(f"❌ El equipo '{equipo1}' no existe en el grupo")
            return False
        
        if equipo2 not in self.equipos:
            print(f"❌ El equipo '{equipo2}' no existe en el grupo")
            return False
        
        if equipo1 == equipo2:
            print("❌ Un equipo no puede jugar contra sí mismo")
            return False
        
        # Crear el partido
        partido = Partido(equipo1, equipo2, goles1, goles2, fecha)
        self.partidos.append(partido)
        
        # Actualizar estadísticas
        team1 = self.equipos[equipo1]
        team2 = self.equipos[equipo2]
        
        if goles1 > goles2:
            team1.registrar_victoria(goles1, goles2)
            team2.registrar_derrota(goles2, goles1)
        elif goles2 > goles1:
            team2.registrar_victoria(goles2, goles1)
            team1.registrar_derrota(goles1, goles2)
        else:  # Empate
            team1.registrar_empate(goles1, goles2)
            team2.registrar_empate(goles2, goles1)
        
        print(f"✓ Partido registrado: {partido}")
        return True
    
    def obtener_tabla_posiciones(self) -> List[Equipo]:
        # inprimira la tabla de posiciones ordenada por puntos, diferencia de goles y goles a favor
        return sorted(
            self.equipos.values(),
            key=lambda e: (e.puntos(), e.diferencia_goles(), e.goles_a_favor),
            reverse=True
        )
    
    def mostrar_tabla(self):
        # Muestra la tabla de posiciones del grupo
        tabla = self.obtener_tabla_posiciones()
        
        if not tabla:
            print(f"El grupo '{self.nombre}' no tiene equipos registrados")
            return
        
        print(f"\n{'='*80}")
        print(f"TABLA DE POSICIONES - GRUPO {self.nombre.upper()}")
        print(f"{'='*80}")
        print(f"{'Pos':<4} {'Equipo':<20} {'PJ':<4} {'PG':<3} {'PE':<3} {'PP':<3} "
              f"{'GF':<4} {'GC':<4} {'DG':<4} {'Pts':<4}")
        print(f"{'-'*80}")
        
        for posicion, equipo in enumerate(tabla, 1):
            print(f"{posicion:<4} {equipo.nombre:<20} {equipo.partidos_jugados:<4} "
                  f"{equipo.victorias:<3} {equipo.empates:<3} {equipo.derrotas:<3} "
                  f"{equipo.goles_a_favor:<4} {equipo.goles_en_contra:<4} "
                  f"{equipo.diferencia_goles():<4} {equipo.puntos():<4}")
        
        print(f"{'='*80}\n")
    
    def mostrar_partidos(self):
        # Muestra todos los partidos jugados o registrados en el grupo
        if not self.partidos:
            print(f"\nNo hay partidos registrados en el grupo '{self.nombre}'")
            return
        
        print(f"\n{'='*80}")
        print(f"PARTIDOS JUGADOS - GRUPO {self.nombre.upper()}")
        print(f"{'='*80}")
        
        for i, partido in enumerate(self.partidos, 1):
            print(f"{i}. {partido}")
        
        print(f"{'='*80}\n")
    
    def obtener_estadisticas_equipo(self, nombre_equipo: str) -> Optional[dict]:
        # Devuelve un diccionario conn las estasdisticas de un equipo en especifico, si no existe el equipo devuelve None
        if nombre_equipo not in self.equipos:
            return None
        
        equipo = self.equipos[nombre_equipo]
        return {
            'Nombre': equipo.nombre,
            'Partidos jugados': str(equipo.partidos_jugados),
            'Victorias': equipo.victorias,
            'Empates': equipo.empates,
            'Derrotas': equipo.derrotas,
            'Goles a favor': equipo.goles_a_favor,
            'Goles en contra': equipo.goles_en_contra,
            'Diferencia de goles': equipo.diferencia_goles(),
            'Puntos': equipo.puntos()
        }


def main():
    #gestor de resultados del mundial.
    print("🌍 GESTOR DE RESULTADOS DEL MUNDIAL\n")
    
    # Crear un grupo
    grupo = GrupoMundial("A")
    
    # Agregar equipos
    equipos = ["Argentina", "Francia", "Polonia", "Arabia Saudita"]
    for equipo in equipos:
        grupo.agregar_equipo(equipo)
    
    print("\n📋 Registrando partidos...\n")
    
    # Registrar partidos
    partidos = [
        ("Argentina", "Arabia Saudita", 1, 2, "2022-11-22"),
        ("Francia", "Polonia", 4, 1, "2022-11-22"),
        ("Argentina", "Polonia", 2, 0, "2022-11-26"),
        ("Francia", "Arabia Saudita", 2, 1, "2022-11-26"),
        ("Argentina", "Francia", 3, 3, "2022-12-18"),
        ("Polonia", "Arabia Saudita", 2, 0, "2022-12-18"),
    ]
    
    for equipo1, equipo2, goles1, goles2, fecha in partidos:
        grupo.registrar_partido(equipo1, equipo2, goles1, goles2, fecha)
    
    # Mostrar resultados
    grupo.mostrar_partidos()
    grupo.mostrar_tabla()
    
    # Mostrar estadísticas de un equipo
    print("📊 ESTADÍSTICAS DETALLADAS")
    print("="*80)
    for equipo_nombre in equipos:
        stats = grupo.obtener_estadisticas_equipo(equipo_nombre)
        if stats:
            print(f"\n{equipo_nombre}:")
            for clave, valor in stats.items():
                if clave != 'Nombre':
                    print(f"  {clave}: {valor}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
