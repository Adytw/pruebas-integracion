# Pruebas de integración en DevOps

**Tema:** una API de pedidos (Flask) que guarda en una base de datos (SQLite).
**Qué probamos:** que la API y la base de datos funcionen **juntas**: la API responde bien **y** el dato realmente se guardó.
**Plataforma DevOps:** GitHub Actions (gratis, en la nube, no hay que instalar nada).

## Archivos

| Archivo | Qué es |
|---|---|
| `app.py` | La API: `POST /pedidos` guarda un pedido, `GET /pedidos/<id>` lo consulta |
| `test_integracion.py` | Las 3 pruebas de integración (pytest) |
| `requirements.txt` | Dependencias: flask y pytest |
| `.github/workflows/ci.yml` | El pipeline: corre las pruebas solo en cada cambio |

## Las 3 pruebas

| Prueba | Qué verifica |
|---|---|
| `test_api_guarda_pedido_en_bd` | La API responde 201 **y** el pedido sí está en la BD |
| `test_guardar_y_consultar_pedido` | Lo que se guarda por POST se puede leer por GET |
| `test_datos_invalidos_no_llegan_a_bd` | La API rechaza datos malos (400) y la BD queda vacía |

## Procedimiento (todo desde el navegador)

> Necesitas una cuenta de GitHub ya creada.

1. **Fork:** abre el repositorio compartido → botón **Fork** (arriba a la derecha) → **Create fork**.
2. **Habilitar Actions:** en tu fork, pestaña **Actions** → **"I understand my workflows, go ahead and enable them"**.
   ⚠️ En los forks vienen desactivadas; si te saltas este paso no corre nada.
3. **Ejecutar:** a la izquierda elige **Pruebas de integracion** → **Run workflow** → **Run workflow**.
   Espera ~30 s, entra a la ejecución → job **integracion** → paso **Ejecutar pruebas de integracion**. Debes ver `3 passed` ✅.
4. **Romperlo a propósito:** abre `app.py` → lápiz ✏️ (Edit) → busca la línea:
   ```python
   (producto, cantidad))
   ```
   cámbiala por:
   ```python
   (producto, cantidad + 1))
   ```
   → **Commit changes**.
5. **Ver la falla:** ve a **Actions**. El pipeline arrancó **solo** y sale ❌.
   Falla `test_api_guarda_pedido_en_bd`: la API respondió 201, pero en la BD quedó `cantidad = 4` en vez de 3.
   Ese es el riesgo típico: cada módulo funciona solo, pero falla al comunicarse.
6. **Revertir:** vuelve a editar `app.py`, regresa la línea a `(producto, cantidad))` → Commit → vuelve a ✅.

## Opcional: correrlo en tu computadora

Requiere Python 3.10+.

```bash
pip install -r requirements.txt
python -m pytest -v
```
