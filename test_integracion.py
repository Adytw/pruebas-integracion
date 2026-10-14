import sqlite3
import pytest
from app import crear_app

@pytest.fixture
def cliente(tmp_path):
    # BD temporal y limpia para cada prueba
    db = tmp_path / "test.db"
    app = crear_app(str(db))
    app.config["TESTING"] = True
    return app.test_client(), db

def test_api_guarda_pedido_en_bd(cliente):
    client, db = cliente
    # 1. La API recibe el pedido
    res = client.post("/pedidos", json={"producto": "Vainilla 1kg", "cantidad": 3})
    # 2. Responde lo esperado
    assert res.status_code == 201
    assert res.get_json()["producto"] == "Vainilla 1kg"
    # 3. El dato si esta en la BD
    fila = sqlite3.connect(db).execute(
        "SELECT producto, cantidad FROM pedidos"
        " WHERE id = ?", (res.get_json()["id"],)
    ).fetchone()
    assert fila == ("Vainilla 1kg", 3)

def test_guardar_y_consultar_pedido(cliente):
    client, _ = cliente
    creado = client.post("/pedidos", json={"producto": "Extracto", "cantidad": 5}).get_json()
    res = client.get(f"/pedidos/{creado['id']}")
    assert res.status_code == 200
    assert res.get_json()["cantidad"] == 5

def test_datos_invalidos_no_llegan_a_bd(cliente):
    client, db = cliente
    res = client.post("/pedidos", json={"producto": "", "cantidad": -1})
    assert res.status_code == 400
    total = sqlite3.connect(db).execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    assert total == 0
