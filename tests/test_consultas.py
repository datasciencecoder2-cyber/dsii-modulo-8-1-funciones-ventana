"""Verifica sintaxis, numero de filas y calculos de las tres ventanas."""
import sys
from pathlib import Path
import sqlite3
import unittest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from ejecutar import leer_consultas  # noqa: E402


class TestFuncionesVentana(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = sqlite3.connect(":memory:")
        cls.con.row_factory = sqlite3.Row
        cls.con.executescript((RAIZ / "datos_ejemplo.sql").read_text(encoding="utf-8"))
        cls.consultas = leer_consultas(RAIZ / "consultas_ventana.sql")
        cls.total_filas = cls.con.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        cls.resultados = [cls.con.execute(sql).fetchall() for sql in cls.consultas]

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_01_tres_consultas_ejecutables(self):
        self.assertEqual(len(self.consultas), 3)

    def test_02_las_tres_conservan_todas_las_filas(self):
        self.assertEqual(self.total_filas, 15)
        for resultado in self.resultados:
            self.assertEqual(len(resultado), self.total_filas)

    def test_03_promedio_por_cliente(self):
        por_pedido = {fila["pedido_id"]: fila for fila in self.resultados[0]}
        self.assertEqual(por_pedido[1]["promedio_gasto_cliente"], 150.0)
        self.assertEqual(por_pedido[2]["promedio_gasto_cliente"], 262.5)
        self.assertEqual(por_pedido[11]["promedio_gasto_cliente"], 375.0)
        self.assertEqual(por_pedido[1]["categoria"], "Electronica")

    def test_04_acumulado_con_desempate_por_id(self):
        filas = self.resultados[1]
        self.assertEqual([fila["pedido_id"] for fila in filas[:3]], [1, 2, 3])
        self.assertEqual([fila["ventas_acumuladas"] for fila in filas[:3]], [100, 600, 800])
        self.assertEqual(filas[-1]["ventas_acumuladas"], 3050)

    def test_05_porcentaje_por_categoria(self):
        por_pedido = {fila["pedido_id"]: fila for fila in self.resultados[2]}
        self.assertEqual(por_pedido[2]["porcentaje_categoria"], 32.26)
        self.assertEqual(por_pedido[4]["porcentaje_categoria"], 66.67)

    def test_06_categoria_sin_ventas_no_divide_por_cero(self):
        filas = [fila for fila in self.resultados[2] if fila["categoria"] == "Servicios"]
        self.assertEqual(len(filas), 2)
        self.assertTrue(all(fila["porcentaje_categoria"] is None for fila in filas))

    def test_07_uso_de_particiones_y_marco(self):
        sql = "\n".join(self.consultas).upper()
        self.assertGreaterEqual(sql.count("PARTITION BY"), 2)
        self.assertIn("ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW", sql)

    def test_08_porcentajes_suman_100_por_categoria_con_ventas(self):
        from collections import defaultdict
        totales = defaultdict(float)
        for fila in self.resultados[2]:
            if fila["porcentaje_categoria"] is not None:
                totales[fila["categoria"]] += fila["porcentaje_categoria"]
        for total in totales.values():
            self.assertAlmostEqual(total, 100, delta=0.02)


if __name__ == "__main__":
    unittest.main()
