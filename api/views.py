import gc
import json
import os

import pandas as pd
import mysql.connector
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

CHUNK_SIZE = 500

# Encodings a intentar al leer CSVs (orden de prioridad)
CSV_ENCODINGS = ["latin-1", "iso-8859-1", "cp1252", "utf-8"]


# ─── Conexion directa a MySQL ─────────────────────────────────────────────────
def _get_conn():
    db = settings.DATABASES["default"]
    return mysql.connector.connect(
        host=db["HOST"],
        port=int(db["PORT"]),
        user=db["USER"],
        password=db["PASSWORD"],
        database=db["NAME"],
        charset="utf8mb4",
        use_unicode=True,
    )


# ─── Lee un CSV probando encodings hasta que uno funcione ────────────────────
def _leer_csv(ruta, sep="|"):
    for enc in CSV_ENCODINGS:
        try:
            return pd.read_csv(
                ruta, sep=sep, dtype=str, keep_default_na=False, encoding=enc
            )
        except (UnicodeDecodeError, LookupError):
            continue
    raise ValueError(
        f"No se pudo leer {os.path.basename(ruta)} con ningun encoding conocido."
    )


# ─── Resuelve ruta priorizando /Corregidos ────────────────────────────────────
def _resolver(carpeta, nombre_original, nombre_corregido):
    ruta_corregida = os.path.join(carpeta, "Corregidos", nombre_corregido)
    if os.path.isfile(ruta_corregida):
        return ruta_corregida
    ruta_original = os.path.join(carpeta, nombre_original)
    if os.path.isfile(ruta_original):
        return ruta_original
    return None


# ─── Busca el archivo de movimientos (.xlsx o .xls) ──────────────────────────
def _buscar_excel(carpeta):
    """
    Devuelve (ruta, engine).
    Ignora archivos temporales de LibreOffice (.~lock.*) y Excel (~$*).
    Busca primero en /Corregidos y luego en la raiz.
    """
    extensiones = {".xlsx": "openpyxl", ".xls": "xlrd"}

    for directorio in [os.path.join(carpeta, "Corregidos"), carpeta]:
        if not os.path.isdir(directorio):
            continue
        for f in os.listdir(directorio):
            if f.startswith("~$") or f.startswith(".~lock"):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in extensiones:
                return os.path.join(directorio, f), extensiones[ext]

    return None, None


# ─── REGLA A — Empleados Activos (solo disco, sin BD) ────────────────────────
def _regla_a_empleados_activos(carpeta, logs):
    ruta = _resolver(
        carpeta,
        "zafiro_info_Empleados_Activos.csv",
        "zafiro_info_Empleados_Activos_Corregido.csv",
    )

    if not ruta:
        logs.append("AVISO [A]: No se encontro Empleados_Activos - se omite.")
        return

    logs.append(f"Regla A - {os.path.basename(ruta)}")
    df = _leer_csv(ruta)

    columnas_faltantes = [c for c in ("FFAA", "GRADO_FA") if c not in df.columns]
    if columnas_faltantes:
        logs.append(f"  AVISO: columnas no encontradas: {columnas_faltantes}")
    else:
        mascara = (df["FFAA"].str.strip() == "") & (df["GRADO_FA"].str.strip() == "")
        n = int(mascara.sum())
        df.loc[mascara, "FFAA"] = "Civil"
        df.loc[mascara, "GRADO_FA"] = "Civil"
        df.to_csv(ruta, sep="|", index=False, encoding="utf-8")
        logs.append(f'  -> {n} fila(s) marcadas como "Civil". Archivo guardado.')

    del df
    gc.collect()


# ─── REGLA B — Movimientos (carga en lotes a BD) ─────────────────────────────
def _regla_b_movimientos(carpeta, logs):
    ruta, engine = _buscar_excel(carpeta)

    if not ruta:
        logs.append(
            "AVISO [B]: No se encontro archivo Excel de Movimientos - se omite."
        )
        return

    logs.append(f"Regla B - {os.path.relpath(ruta, carpeta)} (engine: {engine})")

    # header=1: fila 0 = encabezado basura del reporte, fila 1 = nombres reales de columna
    df = pd.read_excel(ruta, header=1, dtype=str, engine=engine)
    df = df.fillna("")

    total = len(df)
    logs.append(f"  Filas a procesar: {total}")

    conn = _get_conn()
    cursor = conn.cursor()
    n_chunk = 0

    try:
        for inicio in range(0, total, CHUNK_SIZE):
            n_chunk += 1
            chunk = df.iloc[inicio : inicio + CHUNK_SIZE].copy()
            lote_json = chunk.to_json(orient="records", force_ascii=False)

            # Nombre real del SP
            cursor.callproc("sincronizar_tabla_mov_total_con_chunk_csv", [lote_json])
            conn.commit()

            fin = min(inicio + CHUNK_SIZE, total)
            logs.append(f"  Lote {n_chunk}: filas {inicio + 1}-{fin} OK")

            del chunk, lote_json
            gc.collect()

        logs.append(f"  -> Movimientos cargados: {total} filas en {n_chunk} lote(s).")
    finally:
        cursor.close()
        conn.close()

    del df
    gc.collect()


# ─── REGLA C — Familiares (carga en lotes a BD) ──────────────────────────────
def _regla_c_familiares(carpeta, logs):
    ruta = _resolver(
        carpeta,
        "zafiro_info_Familiares.csv",
        "zafiro_info_Familiares_Corregido.csv",
    )

    if not ruta:
        logs.append("AVISO [C]: No se encontro Familiares.csv - se omite.")
        return

    logs.append(f"Regla C - {os.path.basename(ruta)}")
    df = _leer_csv(ruta)
    df = df.fillna("")

    # El nuevo SP espera CIUDAD_1/CIUDAD_2 en el JSON
    df = df.rename(columns={"NUM_EXTERIOR": "CIUDAD_1", "NUMER_INTERIOR": "CIUDAD_2"})

    total = len(df)
    logs.append(f"  Filas a procesar: {total}")

    conn = _get_conn()
    cursor = conn.cursor()
    n_chunk = 0

    try:
        for inicio in range(0, total, CHUNK_SIZE):
            n_chunk += 1
            chunk = df.iloc[inicio : inicio + CHUNK_SIZE].copy()
            lote_json = chunk.to_json(orient="records", force_ascii=False)

            cursor.callproc("sincronizar_tabla_familiar_con_chunk_csv", [lote_json])
            conn.commit()

            fin = min(inicio + CHUNK_SIZE, total)
            logs.append(f"  Lote {n_chunk}: filas {inicio + 1}-{fin} OK")

            del chunk, lote_json
            gc.collect()

        logs.append(f"  -> Familiares cargados: {total} filas en {n_chunk} lote(s).")
    finally:
        cursor.close()
        conn.close()

    del df
    gc.collect()


# ─── ENDPOINT: chunk de Movimientos ──────────────────────────────────────────
@api_view(["POST"])
def subir_movimientos_chunk(request):
    """
    POST /api/subir-movimientos-chunk/
    Body JSON: { "rows": [ {...}, {...}, ... ] }
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    lote_json = json.dumps(rows, ensure_ascii=False)
    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.callproc("sincronizar_tabla_mov_total_con_chunk_csv", [lote_json])
        conn.commit()
        return Response({"ok": True}, status=status.HTTP_200_OK)
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


@api_view(["POST"])
def cargar_familiar_csv(request):
    """
    POST /api/cargar-familiar-csv/
    Body JSON: { "rows": [ {...}, {...}, ... ] }
    INSERT puro — la tabla debe estar truncada antes de la primera llamada.
    El CSV trae NUM_EXTERIOR y NUMER_INTERIOR que se insertan en CIUDAD_1 y CIUDAD_2.
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"}, status=status.HTTP_400_BAD_REQUEST
        )

    campos_db = [
        "HR_ID_PERSONA",
        "EMPLID",
        "HR_CURP",
        "HR_NOMBRE",
        "LAST_NAME100",
        "HR_SECND_LAST_NAME",
        "PARENTESCO",
        "MISMO_DOMICILIO",
        "CORREO_ELECTRÓNICO",
        "TELÉFONO_PARTICULAR",
        "TELÉFONO_CELULAR",
        "CODIGO_POSTAL",
        "COLONIA",
        "ASENTAMIENTO",
        "PAIS",
        "ENTIDAD",
        "MUNICIPIO",
        "CIUDAD",
        "CIUDAD_1",
        "CIUDAD_2",
        "SEXO",
    ]

    sql = f"""
        INSERT INTO FAMILIAR ({', '.join(f'`{c}`' for c in campos_db)})
        VALUES ({', '.join(['%s'] * len(campos_db))})
    """

    def fila_a_tuple(r):
        return (
            r.get("HR_ID_PERSONA") or None,
            r.get("EMPLID") or None,
            r.get("HR_CURP") or None,
            r.get("HR_NOMBRE") or None,
            r.get("LAST_NAME100") or None,
            r.get("HR_SECND_LAST_NAME") or None,
            r.get("PARENTESCO") or None,
            r.get("MISMO_DOMICILIO") or None,
            r.get("CORREO_ELECTRÓNICO") or None,
            r.get("TELÉFONO_PARTICULAR") or None,
            r.get("TELÉFONO_CELULAR") or None,
            r.get("CODIGO_POSTAL") or None,
            r.get("COLONIA") or None,
            r.get("ASENTAMIENTO") or None,
            r.get("PAIS") or None,
            r.get("ENTIDAD") or None,
            r.get("MUNICIPIO") or None,
            r.get("CIUDAD") or None,
            r.get("NUM_EXTERIOR") or None,  # → CIUDAD_1
            r.get("NUMER_INTERIOR") or None,  # → CIUDAD_2
            r.get("SEXO") or None,
        )

    params = [fila_a_tuple(r) for r in rows]

    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, params)
        conn.commit()
        return Response(
            {"ok": True, "insertadas": len(rows)}, status=status.HTTP_200_OK
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


@api_view(["POST"])
def cargar_domicilios_csv(request):
    """
    POST /api/cargar-domicilios-csv/
    Body JSON: { "rows": [ {...}, {...}, ... ] }
    INSERT puro — la tabla debe estar truncada antes de la primera llamada.
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"}, status=status.HTTP_400_BAD_REQUEST
        )

    campos = [
        "NO_EMPLEADO",
        "HR_ID_PERSONA",
        "POSITION_NBR",
        "NOMBRE_COMPLETO",
        "RFC",
        "CURP",
        "PUESTO_ESTRUCTURAL",
        "PUESTO_FUNCIONAL",
        "PUESTO",
        "ESCOLARIDAD_TIPO",
        "ESCOLARIDAD_NIVRL",
        "ESCOLARIDAD_AREA",
        "CARRERA",
        "CENTRO_ESCOLAR",
        "HUMANOS_STATUS",
        "ESTATUS_NOMINA",
        "PHONE",
        "PHONE1",
        "CALLE",
        "HR_NUMERO_EXTERIOR",
        "HR_NUMERO_INTERIOR",
        "POSTAL",
        "COLONIA",
        "HR_MUNICIPIO",
        "ESTADO",
        "EMAIL_ADDR2",
        "EMAIL_ADDR",
        "DEPTID",
        "UNIDAD_ADMINISTRATIVA",
    ]

    sql = f"""
        INSERT INTO domicilios ({', '.join(f'`{c}`' for c in campos)})
        VALUES ({', '.join(['%s'] * len(campos))})
    """

    params = [tuple(r.get(c) or None for c in campos) for r in rows]

    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, params)
        conn.commit()
        return Response(
            {"ok": True, "insertadas": len(rows)}, status=status.HTTP_200_OK
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


# ─── ENDPOINT: bulk insert MOV_POS ──────────────────────────────────────────
_COLS_MOV_POS = [
    "Nº Pos Actual",
    "F Efva",
    "Estado Psn",
    "Fecha Captura",
    "Cd Motivo",
    "Motivo",
    "Cd UN",
    "Unidad de Negocio",
    "Unidad Adva#",
    "Cd Departamento",
    "Cd Puesto",
    "Estado Ptal",
    "Fecha Est",
    "Máximo",
    "Depnd Drt",
    "Depnd Indrt",
    "Ubicación",
    "Nvl Direc",
    "Plan Sal",
    "Grado",
    "Esc",
    "Puesto Ptal",
    "Partida Ptal",
    "Gp Pago",
    "Prog Beneficios",
    "F/H Últ Actz",
    "Por",
    "Hr Estd/Semn",
    "Descr",
    "Gp Trabajo",
    "Org Code",
    "Grupo Cd Sal",
    "FormalDesc",
    "Pto Compt",
    "Posn Clv",
    "Presupuesto",
    "Nombre Puesto",
]


@api_view(["POST"])
def bulk_insert_movpos(request):
    """
    POST /api/bulk-insert-movpos/
    Body JSON: { "rows": [ {...}, {...}, ... ] }
    INSERT IGNORE puro — la tabla debe estar truncada antes de la primera llamada.
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"}, status=status.HTTP_400_BAD_REQUEST
        )

    sql = (
        f"INSERT IGNORE INTO MOV_POS ({', '.join(f'`{c}`' for c in _COLS_MOV_POS)}) "
        f"VALUES ({', '.join(['%s'] * len(_COLS_MOV_POS))})"
    )
    params = [tuple(r.get(c) or None for c in _COLS_MOV_POS) for r in rows]

    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, params)
        conn.commit()
        return Response(
            {"ok": True, "insertadas": len(rows)}, status=status.HTTP_200_OK
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


# ─── ENDPOINT: deduplicar tabla ──────────────────────────────────────────────
_TABLAS_DEDUP = {
    "FAMILIAR": "deduplicar_familiar",
    "domicilios": "deduplicar_domicilios",
    "MOV_POS": "deduplicar_mov_pos",
    "MOV_TOTAL": "deduplicar_mov_total",
}


@api_view(["POST"])
def deduplicar_tabla(request):
    """
    POST /api/deduplicar-tabla/
    Body JSON: { "tabla": "FAMILIAR" | "domicilios" | "MOV_POS" | "MOV_TOTAL" }
    Llama al SP deduplicar_<tabla> y devuelve { eliminados, total_final }.
    """
    tabla = request.data.get("tabla", "").strip()
    if tabla not in _TABLAS_DEDUP:
        return Response(
            {"ok": False, "error": f'Tabla no permitida: "{tabla}"'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    conn = _get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc(_TABLAS_DEDUP[tabla])
        resultados = list(cursor.stored_results())
        fila = resultados[0].fetchone() if resultados else {}
        conn.commit()
        return Response(
            {
                "ok": True,
                "eliminados": fila.get("eliminados", 0),
                "total_final": fila.get("total_final", 0),
            },
            status=status.HTTP_200_OK,
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


# ─── ENDPOINT: truncar tabla ─────────────────────────────────────────────────
TABLAS_PERMITIDAS = {"domicilios", "FAMILIAR", "MOV_POS", "MOV_TOTAL"}


@api_view(["POST"])
def truncar_tabla(request):
    """
    POST /api/truncar-tabla/
    Body JSON: { "tabla": "domicilios" | "FAMILIAR" }
    """
    tabla = request.data.get("tabla", "").strip()

    if tabla not in TABLAS_PERMITIDAS:
        return Response(
            {"ok": False, "error": f'Tabla no permitida: "{tabla}"'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE `{tabla}`")
        conn.commit()
        return Response({"ok": True, "tabla": tabla}, status=status.HTTP_200_OK)
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


@api_view(["POST"])
def eliminar_registros_movimientos(request):
    """
    POST /api/eliminar-registros-movimientos/
    Body JSON: { "año": 2026 }
    """

    año = request.data.get("año", None)
    if not año:
        return Response(
            {"ok": False, "error": "año vacío"}, status=status.HTTP_400_BAD_REQUEST
        )
    conn = _get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM MOV_TOTAL WHERE año={año}")
        conn.commit()
        return Response({"ok": True, "eliminados": cursor.rowcount})
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()


_COLS_MOV_TOTAL = [
    "Posición",
    "Id_empl",
    "Nombre",
    "Paterno",
    "Apellido Matern",
    "Acción",
    "Acción (Nombre)",
    "Motivo",
    "Motivo (Nombre)",
    "F/Efva",
    "Sec",
    "F/Captura",
    "Est HR",
    "Estado Pago",
    "Ptda Ptal",
    "UN",
    "U/Admva",
    "Id/Depto",
    "Depnd Drt",
    "Plan Sal",
    "Grado",
    "Esc",
    "Puesto Ptal",
    "Nivel Tabular",
    "Gp Pago",
    "Prog Beneficios",
    "Sal Base",
    "Cd Puesto",
    "Ubicación",
    "ID Estbl",
    "Slda Prevista",
    "F/H Últ Actz",
    "Por",
    "Últ Inicio",
    "F/Inicial",
    "Gp Trabajo",
    "Grupo Cd Sal",
    "Antig Empr",
    "RFC",
    "CURP",
    "Id Persona",
    "Descr Larga",
    "Niv# Jerarquico",
    "Descr Larga1",
    "Género",
    "Fecha Entrada",
    "F Posición",
]


@api_view(["POST"])
def insertar_movimientos(request):
    """
    POST /api/insertar-movimientos/
    Body JSON: { "rows": [ {...}, {...}, ... ], "año": 2026 }
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"}, status=status.HTTP_400_BAD_REQUEST
        )

    año = request.data.get("año", None)

    todas_cols = _COLS_MOV_TOTAL + ["AÑO"]
    sql = (
        f"INSERT INTO MOV_TOTAL ({', '.join(f'`{c}`' for c in todas_cols)}) "
        f"VALUES ({', '.join(['%s'] * len(todas_cols))})"
    )
    params = [tuple(r.get(c) or None for c in _COLS_MOV_TOTAL) + (año,) for r in rows]

    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, params)
        conn.commit()
        return Response(
            {"ok": True, "insertadas": len(rows)}, status=status.HTTP_200_OK
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()
