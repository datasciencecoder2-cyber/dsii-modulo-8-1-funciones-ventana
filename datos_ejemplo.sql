-- Unidad 8, modulo 8.1: dataset ficticio de pedidos para verificar las ventanas.
-- Las fechas se guardan en formato ISO (AAAA-MM-DD) para orden cronologico.
-- El importe es no negativo y se expresa en unidades monetarias de ejemplo.

CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    importe NUMERIC NOT NULL CHECK (importe >= 0),
    categoria TEXT NOT NULL
);

INSERT INTO pedidos (pedido_id, cliente_id, fecha, importe, categoria) VALUES
    (1, 101, '2023-01-02', 100.00, 'Electronica'),
    (2, 102, '2023-01-02', 500.00, 'Electronica'),
    (3, 101, '2023-01-05', 200.00, 'Hogar'),
    (4, 103, '2023-01-07', 300.00, 'Deportes'),
    (5, 102, '2023-01-07', 250.00, 'Hogar'),
    (6, 103, '2023-02-01', 150.00, 'Electronica'),
    (7, 101, '2023-02-03', 250.00, 'Electronica'),
    (8, 102, '2023-02-03', 100.00, 'Deportes'),
    (9, 104, '2023-02-12', 400.00, 'Hogar'),
    (10, 103, '2023-03-01', 200.00, 'Hogar'),
    (11, 104, '2023-03-01', 350.00, 'Electronica'),
    (12, 101, '2023-03-06', 50.00, 'Deportes'),
    (13, 105, '2023-03-10', 0.00, 'Servicios'),
    (14, 105, '2023-03-11', 0.00, 'Servicios'),
    (15, 102, '2023-03-14', 200.00, 'Electronica');
