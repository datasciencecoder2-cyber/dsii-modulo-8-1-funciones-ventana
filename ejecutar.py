"""Ejecuta las tres consultas SQL en SQLite sin crear archivos .db."""
from pathlib import Path
import sqlite3

RAIZ = Path(__file__).resolve().parent


def leer_consultas(ruta: Path) -> list[str]:
    """Separa sentencias SQL completas respetando su sintaxis y comentarios."""
    pendientes = ""
    consultas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines(keepends=True):
        pendientes += linea
        if sqlite3.complete_statement(pendientes):
            consultas.append(pendientes.strip())
            pendientes = ""
    if pendientes.strip():
        raise ValueError("El archivo SQL termina con una sentencia incompleta.")
    return consultas


def main() -> None:
    with sqlite3.connect(":memory:") as conexion:
        conexion.row_factory = sqlite3.Row
        conexion.executescript((RAIZ / "datos_ejemplo.sql").read_text(encoding="utf-8"))
        consultas = leer_consultas(RAIZ / "consultas_ventana.sql")
        print("DATA SCIENCE II | MODULO 8.1 | FUNCIONES DE VENTANA")
        cantidad = conexion.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
        print(f"Pedidos originales: {cantidad}")
        for numero, consulta in enumerate(consultas, start=1):
            resultado = conexion.execute(consulta)
            registros = resultado.fetchall()
            print(f"\nCONSULTA {numero} | Filas: {len(registros)}")
            print(" | ".join(columna[0] for columna in resultado.description))
            for fila in registros[:5]:
                print(" | ".join("NULL" if dato is None else str(dato) for dato in fila))
            if len(registros) > 5:
                print(f"... ({len(registros) - 5} filas adicionales)")
        print("\nEJECUCION FINALIZADA: OK")


if __name__ == "__main__":
    main()
