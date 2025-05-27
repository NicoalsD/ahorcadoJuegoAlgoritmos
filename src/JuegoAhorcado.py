__author__ = "Nicolas Alejandro Diaz Acosta"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "nicolas.diazacost@campusucc.edu.co"

import random
from enum import Enum
from typing import List
from src.Palabra import Palabra
from src.Letra import Letra


class Estado(Enum):
    NO_INICIADO = 1
    JUGANDO = 2
    GANADOR = 3
    AHORCADO = 4

class JuegoAhorcado:
    TOTAL_PALABRAS = 12
    MAX_INTENTOS = 6

    def __init__(self):
        self.diccionario: List[Palabra] = [
            Palabra("algoritmo"),
            Palabra("contenedora"),
            Palabra("avance"),
            Palabra("ciclo"),
            Palabra("indice"),
            Palabra("instrucciones"),
            Palabra("arreglo"),
            Palabra("vector"),
            Palabra("inicio"),
            Palabra("cuerpo"),
            Palabra("recorrido"),
            Palabra("patron"),
        ]
        
        # HAy que inicializar las variables del jueguitoo
        self.palabra_actual = None                    # No hay palabra seleccionada aún
        self.jugadas = []                            # Lista vacía de letras jugadas
        self.intentos_disponibles = self.MAX_INTENTOS # Empezamos con 6 intentos
        self.estado = Estado.NO_INICIADO 

    def iniciar_juego(self):
        # Generamos un número aleatorio entre 0 y 11 (TOTAL_PALABRAS - 1)
        posicion_aleatoria = random.randint(0, self.TOTAL_PALABRAS - 1)
        
        # Seleccionamos la palabra en esa posición del diccionario
        self.palabra_actual = self.diccionario[posicion_aleatoria]
        
        # Reiniciamos todas las variables del juego
        self.jugadas = []                            # Limpiamos las jugadas anteriores
        self.intentos_disponibles = self.MAX_INTENTOS # Restauramos los 6 intentos
        self.estado = Estado.JUGANDO                 # Cambiamos el estado a jugando

    def jugar_letra(self, letra: Letra) -> bool:
        # Verificamos si el juego está en estado de juego
        if self.estado != Estado.JUGANDO:
            # Si no estamos jugando, no se puede jugar una letra
            return False
        
        # Verificamos si la letra ya fue utilizada anteriormente
        if self.letra_utilizada(letra):
            # Si ya fue utilizada, no la procesamos
            return False
        
        # Agregamos la letra a la lista de jugadas
        self.jugadas.append(letra)
        
        # Verificamos si la letra está en la palabra actual
        if self.palabra_actual.esta_letra(letra):
            # ¡La letra SÍ está en la palabra!
            
            # Verificamos si con esta letra se completó la palabra
            if self.palabra_actual.esta_completa(self.jugadas):
                # Si se completó, el jugador ganó
                self.estado = Estado.GANADOR
            
            # Retornamos True porque la letra estaba en la palabra
            return True
        else:
            # ¡La letra NO está en la palabra!
            
            # Perdemos un intento
            self.intentos_disponibles -= 1
            
            # Verificamos si se acabaron los intentos
            if self.intentos_disponibles == 0:
                # Si no quedan intentos, el jugador fue ahorcado
                self.estado = Estado.AHORCADO
            
            # Retornamos False porque la letra no estaba en la palabra
            return False

    def dar_palabra_actual(self) -> Palabra:
        return self.palabra_actual

    def dar_palabra(self, posicion: int) -> Palabra:
        # Verificamos que la posición esté dentro del rango válido
        if 0 <= posicion < self.TOTAL_PALABRAS:
            return self.diccionario[posicion]
        
        # Si la posición no es válida, retornamos None
        return None

    def dar_intentos_disponibles(self) -> int:
        return self.intentos_disponibles

    def dar_jugadas(self) -> List[Letra]:
        return self.jugadas

    def dar_ocurrencias(self) -> List[Letra]:
        # Si no hay palabra actual, retornamos lista vacía
        if self.palabra_actual is None:
            return []
        
        # Usamos el método de la palabra para obtener las ocurrencias
        return self.palabra_actual.dar_ocurrencias(self.jugadas)

    def dar_estado(self) -> Estado:
        return self.estado
    
    def letra_utilizada(self, letra: Letra) -> bool:
        # Recorremos todas las jugadas realizadas
        for jugada in self.jugadas:
            # Comparamos cada jugada con la letra usando es_igual
            if jugada.es_igual(letra):
                # Si encontramos la letra, ya fue utilizada
                return True
        
        # Si no la encontramos, no ha sido utilizada
        return False

    def metodo1(self) -> str:
        return "Respuesta 1"

    def metodo2(self) -> str:
        return "Respuesta 2"
