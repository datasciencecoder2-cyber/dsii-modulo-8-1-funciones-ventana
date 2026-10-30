-- CONSULTA 1: ¿Cuanto gasta, en promedio, cada cliente en los pedidos registrados?
-- AVG() OVER(PARTITION BY cliente_id) calcula el promedio por cliente
-- sin resumir las filas: cada pedido mantiene sus cinco campos originales.
SELECT
    pedido_id,
    cliente_id,
    fecha,
    importe,
    categoria,
    ROUND(AVG(importe) OVER (PARTITION BY cliente_id), 2) AS promedio_gasto_cliente
FROM pedidos
ORDER BY cliente_id, fecha, pedido_id;

-- CONSULTA 2: ¿Como evoluciona el total acumulado de ventas de la empresa?
-- ORDER BY dentro de OVER establece la secuencia temporal del acumulado.
-- pedido_id desempata pedidos del mismo dia; ROWS garantiza avance fila a fila.
-- No usamos PARTITION BY porque queremos el acumulado de toda la empresa.
SELECT
    pedido_id,
    fecha,
    importe,
    SUM(importe) OVER (
        ORDER BY fecha, pedido_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS ventas_acumuladas
FROM pedidos
ORDER BY fecha, pedido_id;

-- CONSULTA 3: ¿Que porcentaje del importe total de su categoria representa cada pedido?
-- SUM() OVER(PARTITION BY categoria) mantiene todos los pedidos individuales.
-- NULLIF evita dividir por cero: cuando una categoria suma cero, el porcentaje
-- no esta definido y se devuelve NULL (no un porcentaje inventado).
SELECT
    pedido_id,
    cliente_id,
    fecha,
    importe,
    categoria,
    ROUND(
        100.0 * importe /
        NULLIF(SUM(importe) OVER (PARTITION BY categoria), 0),
        2
    ) AS porcentaje_categoria
FROM pedidos
ORDER BY categoria, fecha, pedido_id;
