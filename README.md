# Data Science II — Unidad 8, Módulo 8.1

## Análisis de pedidos con funciones de ventana SQL

**Objetivo:** resolver tres preguntas de negocio sin perder el detalle de las transacciones: (1) promedio de gasto por cliente, (2) ventas acumuladas de toda la empresa y (3) porcentaje de cada pedido dentro de su categoría.

La solución usa **SQLite**, funciones `AVG() OVER`, `SUM() OVER`, `PARTITION BY` y `ORDER BY`; no depende de paquetes externos. Está implementada sobre una tabla ficticia `pedidos` con los campos `pedido_id`, `cliente_id`, `fecha`, `importe`, `categoria`.

## Archivos del repositorio

| Archivo | Contenido |
| --- | --- |
| `consultas_ventana.sql` | Tres consultas independientes, ordenadas y comentadas. Es el **entregable SQL principal**. |
| `datos_ejemplo.sql` | Crea la tabla y agrega 15 pedidos ficticios para reproducir las métricas. |
| `ejecutar.py` | Ejecuta las consultas con SQLite en memoria e imprime las primeras cinco filas de cada resultado. |
| `tests/test_consultas.py` | Ocho pruebas para validar los cálculos, la preservación de filas y el tratamiento de totales cero. |
| `.gitignore` | Evita publicar bases y archivos temporales. |

## Cómo ejecutar

Requisito: **Python 3.10 o superior**. `sqlite3` ya está incluido en la biblioteca estándar.

En Windows (PowerShell), dentro de la carpeta del proyecto:

```powershell
py ejecutar.py
py -m unittest discover -s tests -v
```

En macOS/Linux, reemplazar `py` por `python3`. El script crea una base **solo en memoria** y no genera archivos `.db` ni requiere conexión a Internet. También se puede ejecutar el SQL desde la consola de SQLite, creando una base temporal con `datos_ejemplo.sql` y luego ejecutando `consultas_ventana.sql`.

## Decisiones SQL (explicación solicitada)

### Consulta 1 — ¿Por qué usamos `PARTITION BY cliente_id`?

`AVG(importe) OVER (PARTITION BY cliente_id)` calcula el **promedio de los pedidos registrados de cada cliente** y muestra ese promedio al lado de cada transacción. Sin `PARTITION BY`, se calcularía el promedio global de todos los pedidos y se repetiría para todos los clientes. No agregamos `GROUP BY` porque reduciría las filas y perderíamos el detalle individual. El promedio se calcula sobre **todo el historial disponible**, no como una media móvil hasta cada fecha.

### Consulta 2 — ¿Qué ocurre si quitamos `ORDER BY` dentro de `OVER()`?

La expresión `SUM(importe) OVER (ORDER BY fecha, pedido_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` acumula los importes **fila por fila** según fecha e identificador de pedido. El identificador resuelve de manera determinista los empates de pedidos realizados el mismo día. Si quitáramos el `ORDER BY` **del interior de `OVER()`**, la suma dejaría de ser acumulada y obtendríamos el **total general de la empresa repetido en cada fila**. El `ORDER BY` externo solo ordena cómo se muestran las filas y no sustituye el orden de la ventana.

### Consulta 3 — ¿Por qué otra partición?

`SUM(importe) OVER (PARTITION BY categoria)` calcula el total de cada categoría, sin reducir el número de pedidos. El porcentaje de cada pedido es `100 * importe / total_categoria`. `NULLIF(total_categoria, 0)` evita división entre cero: si toda la categoría suma cero, el porcentaje es indefinido (`NULL`) en vez de inventar un valor. La multiplicación por `100.0` evita división entera.

## Resultados de referencia (datos ficticios)

- **15 pedidos** antes y después de cada consulta. No se pierde ninguna fila.
- **Total de la empresa:** 3.050,00 unidades monetarias.
- **Promedio del cliente 101:** 150,00 (cuatro pedidos).
- **Pedido 2:** representa **32,26 %** de la categoría Electrónica (500 / 1.550).
- **Pedidos en la misma fecha:** el acumulado se desempata por `pedido_id`.
- **Categoría Servicios:** contiene dos pedidos de importe cero; su porcentaje retorna `NULL` por denominador cero.

Para comprobarlo ejecutá las **8 pruebas automáticas**; sus cálculos verifican las tres consultas. Todos estos resultados corresponden exclusivamente al conjunto de ejemplo y **no** a ventas reales.

## Principios de calidad

1. Palabras clave SQL en mayúsculas y consultas comentadas según la pregunta de negocio.
2. `ROWS BETWEEN ...` explícito para evitar que varias transacciones del mismo día compartan por accidente el mismo acumulado por un marco tipo `RANGE`.
3. No se crea una tabla agregada: las funciones de ventana conservan las filas.
4. Al no almacenar archivos de base de datos, cualquier persona puede reproducir las consultas desde los datos de ejemplo versionados.
