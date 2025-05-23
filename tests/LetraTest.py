import pytest
from Letra import Letra  # Asegúrate de que la ruta del import sea correcta

# Escenario 1: letra minúscula 'm'
@pytest.fixture
def letra_m():
    return Letra('m')

# Escenario 2: letra mayúscula 'P'
@pytest.fixture
def letra_p():
    return Letra('P')

# Escenario 3: letra minúscula 'a'
@pytest.fixture
def letra_a():
    return Letra('a')

# Escenario 4: letra mayúscula 'Z'
@pytest.fixture
def letra_z():
    return Letra('Z')

# Test 1: Comparar 'm' con 'M' y 'm'
def test_es_igual1(letra_m):
    assert letra_m.es_igual(Letra('M')), "Las letras deben ser iguales"
    assert letra_m.es_igual(Letra('m')), "Las letras deben ser iguales"

# Test 2: Comparar 'P' con 'p' y 'P'
def test_es_igual2(letra_p):
    assert letra_p.es_igual(Letra('p')), "Las letras deben ser iguales"
    assert letra_p.es_igual(Letra('P')), "Las letras deben ser iguales"

# Test 3: Comparar 'a' con 'A' y 'a'
def test_es_igual3(letra_a):
    assert letra_a.es_igual(Letra('A')), "Las letras deben ser iguales"
    assert letra_a.es_igual(Letra('a')), "Las letras deben ser iguales"

# Test 4: Comparar 'Z' con 'z' y 'Z'
def test_es_igual4(letra_z):
    assert letra_z.es_igual(Letra('z')), "Las letras deben ser iguales"
    assert letra_z.es_igual(Letra('Z')), "Las letras deben ser iguales"

# Test 5: Comparar 'P' con 'J' y 'j' (no iguales)
def test_es_igual5(letra_p):
    assert not letra_p.es_igual(Letra('J')), "Las letras no deben ser iguales"
    assert not letra_p.es_igual(Letra('j')), "Las letras no deben ser iguales"

# Test 6: Comparar 'P' con 'x' y 'X' (no iguales)
def test_es_igual6(letra_p):
    assert not letra_p.es_igual(Letra('x')), "Las letras no deben ser iguales"
    assert not letra_p.es_igual(Letra('X')), "Las letras no deben ser iguales"
