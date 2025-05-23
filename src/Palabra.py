from typing import List
from Letra import Letra

class Palabra:
    """
    Clase para representar una palabra del juego.
    """

    def __init__(self, p_palabra: str):
        """
        Construye una nueva palabra a partir de su representación en string.
        :param p_palabra: La palabra que se quiere construir.
        """
        pass
    def esta_completa(self, p_jugadas: List[Letra]) -> bool:
        """
        Indica si con las letras jugadas ya es posible conocer la palabra completa.
        :param p_jugadas: Lista con las letras jugadas.
        :return: True si la palabra está completamente adivinada, False en caso contrario.
        """
        pass

    def _buscar_letra_en_lista(self, p_letra: Letra, lista_letras: List[Letra]) -> bool:
        """
        Indica si una letra se encuentra en una lista dada.
        :param p_letra: Letra que se está buscando.
        :param lista_letras: Lista de letras en la que se busca.
        :return: True si está la letra, False en caso contrario.
        """
        pass

    def esta_letra(self, p_letra: Letra) -> bool:
        """
        Informa si una letra hace parte de la palabra.
        :param p_letra: Letra a consultar.
        :return: True si la letra está en la palabra, False de lo contrario.
        """
        pass

    def dar_ocurrencias(self, p_jugadas: List[Letra]) -> List[Letra]:
        """
        Devuelve una lista con las letras jugadas correctamente, reemplazando las no adivinadas con "_".
        :param p_jugadas: Letras jugadas.
        :return: Lista de letras visibles (las que han sido adivinadas o "_" para las desconocidas).
        """
        pass

    def dar_letras(self) -> List[Letra]:
        """
        Devuelve el arreglo con las letras de la palabra.
        :return: Lista de letras que componen la palabra.
        """
        pass