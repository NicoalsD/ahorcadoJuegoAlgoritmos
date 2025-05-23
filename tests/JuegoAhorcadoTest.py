import pytest
from JuegoAhorcado import JuegoAhorcado, Estado
from Letra import Letra
from Palabra import Palabra

@pytest.fixture
def juego():
    return JuegoAhorcado()

def test_inicializacion(juego):
    for i in range(juego.TOTAL_PALABRAS):
        assert juego.dar_palabra(i) is not None, f"La palabra {i} debe estar inicializada"

    assert juego.dar_intentos_disponibles() == JuegoAhorcado.MAX_INTENTOS, \
        f"El número de intentos debe ser {JuegoAhorcado.MAX_INTENTOS}"
    assert juego.dar_estado() == Estado.NO_INICIADO, \
        "El estado del juego debe ser NO_INICIADO"

def test_iniciar_juego(juego):
    juego.iniciar_juego()
    assert juego.dar_estado() == Estado.JUGANDO, "El estado del juego es incorrecto"
    assert juego.dar_intentos_disponibles() == JuegoAhorcado.MAX_INTENTOS, \
        f"El número de intentos debe ser {JuegoAhorcado.MAX_INTENTOS}"
    assert len(juego.dar_jugadas()) == 0, "El vector de letras jugadas debe estar vacío"
    assert juego.dar_palabra_actual() is not None, "No se ha escogido aleatoriamente una palabra"

def test_jugar_letra_sin_iniciar(juego):
    letra = Letra('a')
    assert not juego.jugar_letra(letra), "Si no se ha iniciado el juego, no se puede jugar una letra"

def test_jugar_letra_en_juego_iniciado(juego):
    juego.iniciar_juego()
    actual = juego.dar_palabra_actual()
    jugadas = actual.dar_letras()
    letra_intento = Letra('a')

    # Se simula que todas las letras fueron adivinadas
    assert actual.esta_completa(jugadas), "La palabra ya fue adivinada"

    ocurrencias = actual.dar_ocurrencias(jugadas)
    assert "_" not in ocurrencias, "Todas las letras deben ser visibles"

    resultado = juego.jugar_letra(letra_intento)

    if resultado:
        assert any(j.es_igual(letra_intento) for j in juego.dar_jugadas()), \
            "La letra jugada debe estar en el vector de jugadas"
    else:
        intentos_esperados = JuegoAhorcado.MAX_INTENTOS - 1
        assert juego.dar_intentos_disponibles() == intentos_esperados, \
            f"El número de intentos debe ser {intentos_esperados}"
        if intentos_esperados == 0:
            assert juego.dar_estado() == Estado.AHORCADO, "El estado del juego debe ser AHORCADO"
        assert not actual.esta_letra(letra_intento), "La letra no está en la palabra"