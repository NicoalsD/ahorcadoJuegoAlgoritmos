import pytest
from Letra import Letra
from Palabra import Palabra

@pytest.fixture
def escenario_palabra():
    letras = [
        Letra('v'),
        Letra('e'),
        Letra('c'),
        Letra('t'),
        Letra('o'),
        Letra('r')
    ]
    palabra = Palabra("vector")
    jugadas = []
    num_intentos = 6
    return palabra, letras, jugadas, num_intentos

def test_palabra(escenario_palabra):
    palabra, letras, jugadas, num_intentos = escenario_palabra

    # Probar si cada letra está en la palabra
    for i in range(num_intentos):
        letra_intento = letras[i]
        jugadas.append(letra_intento)
        assert palabra.esta_letra(letra_intento), "La letra sí está en la palabra"

    # Probar si la palabra está completa con las jugadas realizadas
    assert palabra.esta_completa(jugadas), "La palabra ya está completa"

    