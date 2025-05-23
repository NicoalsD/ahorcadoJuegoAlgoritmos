import random
from enum import Enum
from typing import List
from Palabra import Palabra
from Letra import Letra


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
        

    def iniciar_juego(self):
        pass

    def jugar_letra(self, letra: Letra) -> bool:
        pass

    def dar_palabra_actual(self) -> Palabra:
        pass

    def dar_palabra(self, posicion: int) -> Palabra:
        pass

    def dar_intentos_disponibles(self) -> int:
        pass

    def dar_jugadas(self) -> List[Letra]:
        pass

    def dar_ocurrencias(self) -> List[Letra]:
        pass

    def dar_estado(self) -> Estado:
        pass

    def letra_utilizada(self, letra: Letra) -> bool:
        pass

    def metodo1(self) -> str:
        return "Respuesta 1"

    def metodo2(self) -> str:
        return "Respuesta 2"