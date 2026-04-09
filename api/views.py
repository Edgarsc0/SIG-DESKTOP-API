import gc
import io
import json
import os
import queue
import subprocess
import threading
import uuid

import pandas as pd
import mysql.connector
from django.conf import settings
from django.http import StreamingHttpResponse, FileResponse, HttpResponseForbidden
from openpyxl import load_workbook
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# ─── Automatización Selenium ──────────────────────────────────────────────────
# Modo prueba: servidor mock local (React)
SCRIPTS_DIR_PRUEBA = "/home/edgar/ANAM/mock-zafiro/scripts"
# Modo real: scripts de web scraping contra el portal ANAM
SCRIPTS_DIR_REAL = "/home/edgar/ANAM/SIG-DEKTOP/resources/scripts"

# El corrector heurístico siempre es el binario real (no cambia)
CORREGIR_EXE = "/home/edgar/ANAM/SIG-DEKTOP/resources/scripts/corregir_heuristico"

# session_id → lista de Popen activos (para poder cancelarlos)
_active_procs: dict[str, list] = {}


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


def _run_proc(cmd, cwd, active_list):
    """
    Ejecuta un subproceso y hace yield de eventos SSE por cada línea
    de stdout (tipo 'log') y stderr (tipo 'error').
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=cwd,
    )
    active_list.append(proc)

    q = queue.Queue()

    def _reader(stream, tipo):
        for line in stream:
            line = line.rstrip()
            if line:
                q.put((tipo, line))
        q.put(None)

    t1 = threading.Thread(target=_reader, args=(proc.stdout, "log"), daemon=True)
    t2 = threading.Thread(target=_reader, args=(proc.stderr, "error"), daemon=True)
    t1.start()
    t2.start()

    done = 0
    while done < 2:
        item = q.get()
        if item is None:
            done += 1
        else:
            yield _sse({"type": item[0], "text": item[1]})

    t1.join()
    t2.join()
    proc.wait()

    if proc in active_list:
        active_list.remove(proc)

    if proc.returncode not in (0, -9, None):
        yield _sse(
            {"type": "error", "text": f"Proceso terminó con código {proc.returncode}"}
        )


CHUNK_SIZE = 500

# Columnas de la tabla domicilios (= archivo Escolaridad)
_COLS_DOMICILIOS = [
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
_SQL_INSERT_DOMICILIOS = (
    f"INSERT INTO domicilios ({', '.join(f'`{c}`' for c in _COLS_DOMICILIOS)}) "
    f"VALUES ({', '.join(['%s'] * len(_COLS_DOMICILIOS))})"
)

# Encodings a intentar al leer CSVs (orden de prioridad)
CSV_ENCODINGS = ["latin-1", "iso-8859-1", "cp1252", "utf-8"]


# ─── Conexion directa a MySQL ─────────────────────────────────────────────────
def _get_conn():
    db = settings.MYSQL_DB
    return mysql.connector.connect(
        host=db["HOST"],
        port=int(db["PORT"]),
        user=db["USER"],
        password=db["PASSWORD"],
        database=db["NAME"],
        charset="utf8mb4",
        use_unicode=True,
        connection_timeout=15,
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


# ─── Detecta el engine correcto por magic bytes (ignora la extensión) ────────
_MAGIC_ZIP = b"PK\x03\x04"  # .xlsx / ooxml
_MAGIC_OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"  # .xls  / OLE2-CFBF


def _excel_engine(ruta: str) -> str | None:
    """Devuelve 'openpyxl', 'xlrd', o None según los magic bytes del archivo."""
    try:
        with open(ruta, "rb") as fh:
            magic = fh.read(8)
        if magic[:4] == _MAGIC_ZIP:
            return "openpyxl"
        if magic[:8] == _MAGIC_OLE:
            return "xlrd"
    except OSError:
        pass
    return None


# ─── Busca el archivo de movimientos (.xlsx o .xls) ──────────────────────────
def _buscar_excel(carpeta):
    """
    Devuelve (ruta, engine).
    Ignora archivos temporales de LibreOffice (.~lock.*) y Excel (~$*).
    Busca primero en /Corregidos y luego en la raiz.
    El engine se determina por magic bytes, no por extensión.
    """
    for directorio in [os.path.join(carpeta, "Corregidos"), carpeta]:
        if not os.path.isdir(directorio):
            continue
        for f in os.listdir(directorio):
            if f.startswith("~$") or f.startswith(".~lock"):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in (".xlsx", ".xls"):
                ruta = os.path.join(directorio, f)
                engine = _excel_engine(ruta)
                if engine:
                    return ruta, engine

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
_SQL_INSERT_MOV_POS = (
    f"INSERT IGNORE INTO MOV_POS ({', '.join(f'`{c}`' for c in _COLS_MOV_POS)}) "
    f"VALUES ({', '.join(['%s'] * len(_COLS_MOV_POS))})"
)


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
TABLAS_PERMITIDAS = {"domicilios", "FAMILIAR", "MOV_POS", "MOV_TOTAL", "HISTORIAL_POS"}


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


# ─── Helper: deduplicar tabla y devolver stats ───────────────────────────────
def _deduplicar_tabla_interno(tabla, logs):
    """
    Llama al SP deduplicar_<tabla> y devuelve { eliminados, total_final }.
    Reutiliza _TABLAS_DEDUP que ya existe en el archivo.
    """
    sp_name = _TABLAS_DEDUP.get(tabla)
    if not sp_name:
        return {}
    conn = _get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc(sp_name)
        resultados = list(cursor.stored_results())
        fila = resultados[0].fetchone() if resultados else {}
        conn.commit()
        eliminados = fila.get("eliminados", 0)
        total_final = fila.get("total_final", 0)
        logs.append(
            f"  Dedup {tabla}: {eliminados} eliminados, {total_final} en tabla."
        )
        return {"eliminados": eliminados, "total_final": total_final}
    except Exception as e:
        logs.append(f"ERROR deduplicando {tabla}: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()


# ─── ENDPOINT SSE: ejecutar descarga ─────────────────────────────────────────
def ejecutar_descarga(request):
    """
    GET /api/ejecutar-descarga/?ids=1,2&headless=true&detectarCorregir=false&subirBD=false
    Devuelve stream SSE con logs.
    Eventos: { type: 'session'|'log'|'error'|'done', ... }
    """
    ids = [int(i) for i in request.GET.get("ids", "").split(",") if i.strip()]
    headless = request.GET.get("headless", "true") != "false"
    detectar_corregir = request.GET.get("detectarCorregir", "false") == "true"
    subir_bd_flag = request.GET.get("subirBD", "false") == "true"
    modo_prueba = request.GET.get("modoPrueba", "true") == "true"
    año = int(request.GET.get("año", 0)) or None

    scripts_dir = SCRIPTS_DIR_PRUEBA if modo_prueba else SCRIPTS_DIR_REAL

    session_id = str(uuid.uuid4())
    temp_dir = f"/tmp/descarga_{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    _active_procs[session_id] = []

    def stream():
        try:
            yield _sse({"type": "session", "sessionId": session_id})

            headless_arg = "1" if headless else "0"

            modo_tag = "[PRUEBA]" if modo_prueba else "[REAL]"
            yield _sse(
                {"type": "log", "text": f"Modo: {modo_tag} — scripts en {scripts_dir}"}
            )

            for file_id in ids:
                if file_id == 6:
                    for script_name in ["consultas.js", "descargarExcel.js"]:
                        yield _sse(
                            {"type": "log", "text": f"Ejecutando {script_name}..."}
                        )
                        yield from _run_proc(
                            ["node", script_name, temp_dir, headless_arg],
                            scripts_dir,
                            _active_procs[session_id],
                        )
                else:
                    yield _sse(
                        {"type": "log", "text": f"Descargando archivo ID {file_id}..."}
                    )
                    yield from _run_proc(
                        ["node", "index.js", str(file_id), temp_dir, headless_arg],
                        scripts_dir,
                        _active_procs[session_id],
                    )

            if detectar_corregir:
                if os.path.exists(CORREGIR_EXE):
                    output_dir = os.path.join(temp_dir, "Corregidos")
                    os.makedirs(output_dir, exist_ok=True)
                    csv_files = [
                        f for f in os.listdir(temp_dir) if f.lower().endswith(".csv")
                    ]
                    for csv_file in csv_files:
                        input_path = os.path.join(temp_dir, csv_file)
                        output_path = os.path.join(
                            output_dir, csv_file.replace(".csv", "_Corregido.csv")
                        )
                        yield _sse({"type": "log", "text": f"Corrigiendo: {csv_file}"})
                        yield from _run_proc(
                            [
                                CORREGIR_EXE,
                                input_path,
                                "--corregir",
                                "--salida",
                                output_path,
                            ],
                            scripts_dir,
                            _active_procs[session_id],
                        )
                else:
                    yield _sse(
                        {
                            "type": "error",
                            "text": "AVISO: corrector no disponible — se omite.",
                        }
                    )

            bd_stats = []
            if subir_bd_flag:
                yield _sse(
                    {"type": "log", "text": "Iniciando carga a base de datos..."}
                )

                # ── Regla A — corrección en disco, sin inserción en BD ────────
                logs_a: list[str] = []
                try:
                    _regla_a_empleados_activos(temp_dir, logs_a)
                except Exception as e:
                    logs_a.append(f"ERROR Regla A: {e}")
                for line in logs_a:
                    t = (
                        "error"
                        if line.upper().startswith(("ERROR", "AVISO"))
                        else "log"
                    )
                    yield _sse({"type": t, "text": line})

                # ── Regla B — MOV_TOTAL por chunks (streaming) ───────────────
                ruta_xlsx, engine_xlsx = _buscar_excel(temp_dir)
                if ruta_xlsx:
                    yield _sse(
                        {
                            "type": "log",
                            "text": f"Regla B - {os.path.basename(ruta_xlsx)} (engine: {engine_xlsx})",
                        }
                    )
                    try:
                        df_b = pd.read_excel(
                            ruta_xlsx, header=1, dtype=str, engine=engine_xlsx
                        )
                        df_b = df_b.fillna("")
                        total_b = len(df_b)
                        yield _sse(
                            {"type": "log", "text": f"  Filas a procesar: {total_b}"}
                        )

                        conn_b = _get_conn()
                        cur_b = conn_b.cursor()
                        n_chunk = 0
                        try:
                            # Borrar registros del año antes de insertar
                            if año:
                                cur_b.execute(
                                    "DELETE FROM MOV_TOTAL WHERE AÑO = %s", (año,)
                                )
                                conn_b.commit()
                                yield _sse(
                                    {
                                        "type": "log",
                                        "text": f"  Registros del año {año} eliminados: {cur_b.rowcount} fila(s).",
                                    }
                                )
                            else:
                                yield _sse(
                                    {
                                        "type": "error",
                                        "text": "  AVISO: no se especificó año — se omite la limpieza previa.",
                                    }
                                )

                            for inicio in range(0, total_b, CHUNK_SIZE):
                                n_chunk += 1
                                chunk = df_b.iloc[inicio : inicio + CHUNK_SIZE].copy()
                                lote_json = chunk.to_json(
                                    orient="records", force_ascii=False
                                )
                                cur_b.callproc(
                                    "sincronizar_tabla_mov_total_con_chunk_csv",
                                    [lote_json],
                                )
                                conn_b.commit()
                                fin = min(inicio + CHUNK_SIZE, total_b)
                                yield _sse(
                                    {
                                        "type": "log",
                                        "text": f"  Lote {n_chunk}: filas {inicio + 1}–{fin} OK",
                                    }
                                )
                                del chunk, lote_json
                                gc.collect()
                            yield _sse(
                                {
                                    "type": "log",
                                    "text": f"  -> Movimientos cargados: {total_b} filas en {n_chunk} lote(s).",
                                }
                            )
                        finally:
                            cur_b.close()
                            conn_b.close()

                        del df_b
                        gc.collect()

                        dedup_b = _deduplicar_tabla_interno("MOV_TOTAL", [])
                        yield _sse(
                            {
                                "type": "log",
                                "text": f'  Dedup MOV_TOTAL: {dedup_b.get("eliminados", 0)} eliminados, {dedup_b.get("total_final", 0)} en tabla.',
                            }
                        )
                        bd_stats.append(
                            {
                                "label": "Movimientos ANAM",
                                "tabla": "MOV_TOTAL",
                                "insertadas": total_b,
                                "eliminados": dedup_b.get("eliminados", 0),
                                "total_final": dedup_b.get("total_final", 0),
                            }
                        )
                    except Exception as e:
                        yield _sse({"type": "error", "text": f"ERROR Regla B: {e}"})

                # ── Regla C — FAMILIAR por chunks (streaming) ────────────────
                ruta_fam = _resolver(
                    temp_dir,
                    "zafiro_info_Familiares.csv",
                    "zafiro_info_Familiares_Corregido.csv",
                )
                if ruta_fam:
                    yield _sse(
                        {
                            "type": "log",
                            "text": f"Regla C - {os.path.basename(ruta_fam)}",
                        }
                    )
                    try:
                        df_c = _leer_csv(ruta_fam)
                        df_c = df_c.fillna("")
                        df_c = df_c.rename(
                            columns={
                                "NUM_EXTERIOR": "CIUDAD_1",
                                "NUMER_INTERIOR": "CIUDAD_2",
                            }
                        )
                        total_c = len(df_c)
                        yield _sse(
                            {"type": "log", "text": f"  Filas a procesar: {total_c}"}
                        )

                        conn_c = _get_conn()
                        cur_c = conn_c.cursor()
                        n_chunk = 0
                        try:
                            for inicio in range(0, total_c, CHUNK_SIZE):
                                n_chunk += 1
                                chunk = df_c.iloc[inicio : inicio + CHUNK_SIZE].copy()
                                lote_json = chunk.to_json(
                                    orient="records", force_ascii=False
                                )
                                cur_c.callproc(
                                    "sincronizar_tabla_familiar_con_chunk_csv",
                                    [lote_json],
                                )
                                conn_c.commit()
                                fin = min(inicio + CHUNK_SIZE, total_c)
                                yield _sse(
                                    {
                                        "type": "log",
                                        "text": f"  Lote {n_chunk}: filas {inicio + 1}–{fin} OK",
                                    }
                                )
                                del chunk, lote_json
                                gc.collect()
                            yield _sse(
                                {
                                    "type": "log",
                                    "text": f"  -> Familiares cargados: {total_c} filas en {n_chunk} lote(s).",
                                }
                            )
                        finally:
                            cur_c.close()
                            conn_c.close()

                        del df_c
                        gc.collect()

                        dedup_c = _deduplicar_tabla_interno("FAMILIAR", [])
                        yield _sse(
                            {
                                "type": "log",
                                "text": f'  Dedup FAMILIAR: {dedup_c.get("eliminados", 0)} eliminados, {dedup_c.get("total_final", 0)} en tabla.',
                            }
                        )
                        bd_stats.append(
                            {
                                "label": "Familiares",
                                "tabla": "FAMILIAR",
                                "insertadas": total_c,
                                "eliminados": dedup_c.get("eliminados", 0),
                                "total_final": dedup_c.get("total_final", 0),
                            }
                        )
                    except Exception as e:
                        yield _sse({"type": "error", "text": f"ERROR Regla C: {e}"})

                # ── Regla D — domicilios / Escolaridad (streaming) ───────────
                ruta_esc = _resolver(
                    temp_dir,
                    "zafiro_info_Escolaridad.csv",
                    "zafiro_info_Escolaridad_Corregido.csv",
                )
                if ruta_esc:
                    yield _sse(
                        {
                            "type": "log",
                            "text": f"Regla D - {os.path.basename(ruta_esc)}",
                        }
                    )
                    try:
                        df_d = _leer_csv(ruta_esc)
                        df_d = df_d.fillna("")
                        total_d = len(df_d)
                        yield _sse(
                            {"type": "log", "text": f"  Filas a procesar: {total_d}"}
                        )

                        conn_d = _get_conn()
                        cur_d = conn_d.cursor()
                        n_chunk = 0
                        try:
                            # Truncar tabla antes de insertar (reemplazo completo)
                            cur_d.execute("TRUNCATE TABLE `domicilios`")
                            conn_d.commit()
                            yield _sse(
                                {"type": "log", "text": "  Tabla domicilios truncada."}
                            )

                            for inicio in range(0, total_d, CHUNK_SIZE):
                                n_chunk += 1
                                chunk = df_d.iloc[inicio : inicio + CHUNK_SIZE]
                                params = [
                                    tuple(row.get(c) or None for c in _COLS_DOMICILIOS)
                                    for row in chunk.to_dict("records")
                                ]
                                cur_d.executemany(_SQL_INSERT_DOMICILIOS, params)
                                conn_d.commit()
                                fin = min(inicio + CHUNK_SIZE, total_d)
                                yield _sse(
                                    {
                                        "type": "log",
                                        "text": f"  Lote {n_chunk}: filas {inicio + 1}–{fin} OK",
                                    }
                                )
                                gc.collect()
                            yield _sse(
                                {
                                    "type": "log",
                                    "text": f"  -> Escolaridad cargada: {total_d} filas en {n_chunk} lote(s).",
                                }
                            )
                        finally:
                            cur_d.close()
                            conn_d.close()

                        del df_d
                        gc.collect()

                        dedup_d = _deduplicar_tabla_interno("domicilios", [])
                        yield _sse(
                            {
                                "type": "log",
                                "text": f'  Dedup domicilios: {dedup_d.get("eliminados", 0)} eliminados, {dedup_d.get("total_final", 0)} en tabla.',
                            }
                        )
                        bd_stats.append(
                            {
                                "label": "Escolaridad",
                                "tabla": "domicilios",
                                "insertadas": total_d,
                                "eliminados": dedup_d.get("eliminados", 0),
                                "total_final": dedup_d.get("total_final", 0),
                            }
                        )
                    except Exception as e:
                        yield _sse({"type": "error", "text": f"ERROR Regla D: {e}"})

                # ── Regla E — MOV_POS / Posiciones (streaming) ──────────────
                ruta_pos = _resolver(
                    temp_dir,
                    "zafiro_info_Posiciones.csv",
                    "zafiro_info_Posiciones_Corregido.csv",
                )
                if ruta_pos:
                    yield _sse(
                        {
                            "type": "log",
                            "text": f"Regla E - {os.path.basename(ruta_pos)}",
                        }
                    )
                    try:
                        df_e = _leer_csv(ruta_pos)
                        df_e = df_e.fillna("")
                        total_e = len(df_e)
                        yield _sse(
                            {"type": "log", "text": f"  Filas a procesar: {total_e}"}
                        )

                        conn_e = _get_conn()
                        cur_e = conn_e.cursor()
                        n_chunk = 0
                        try:
                            cur_e.execute("TRUNCATE TABLE `MOV_POS`")
                            conn_e.commit()
                            yield _sse(
                                {"type": "log", "text": "  Tabla MOV_POS truncada."}
                            )

                            for inicio in range(0, total_e, CHUNK_SIZE):
                                n_chunk += 1
                                chunk = df_e.iloc[inicio : inicio + CHUNK_SIZE]
                                params = [
                                    tuple(row.get(c) or None for c in _COLS_MOV_POS)
                                    for row in chunk.to_dict("records")
                                ]
                                cur_e.executemany(_SQL_INSERT_MOV_POS, params)
                                conn_e.commit()
                                fin = min(inicio + CHUNK_SIZE, total_e)
                                yield _sse(
                                    {
                                        "type": "log",
                                        "text": f"  Lote {n_chunk}: filas {inicio + 1}–{fin} OK",
                                    }
                                )
                                gc.collect()
                            yield _sse(
                                {
                                    "type": "log",
                                    "text": f"  -> Posiciones cargadas: {total_e} filas en {n_chunk} lote(s).",
                                }
                            )
                        finally:
                            cur_e.close()
                            conn_e.close()

                        del df_e
                        gc.collect()

                        dedup_e = _deduplicar_tabla_interno("MOV_POS", [])
                        yield _sse(
                            {
                                "type": "log",
                                "text": f'  Dedup MOV_POS: {dedup_e.get("eliminados", 0)} eliminados, {dedup_e.get("total_final", 0)} en tabla.',
                            }
                        )
                        bd_stats.append(
                            {
                                "label": "Posiciones",
                                "tabla": "MOV_POS",
                                "insertadas": total_e,
                                "eliminados": dedup_e.get("eliminados", 0),
                                "total_final": dedup_e.get("total_final", 0),
                            }
                        )
                    except Exception as e:
                        yield _sse({"type": "error", "text": f"ERROR Regla E: {e}"})

            archivos = []
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    archivos.append(os.path.relpath(os.path.join(root, f), temp_dir))

            yield _sse(
                {
                    "type": "done",
                    "sessionId": session_id,
                    "archivos": archivos,
                    "bdStats": bd_stats,
                }
            )

        except Exception as e:
            yield _sse({"type": "error", "text": f"Error interno: {e}"})
        finally:
            _active_procs.pop(session_id, None)

    response = StreamingHttpResponse(stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


# ─── ENDPOINT: servir archivo descargado ─────────────────────────────────────
def obtener_archivo(request, session_id, nombre):
    """
    GET /api/obtener-archivo/<session_id>/<path:nombre>/
    Para XLSX/XLS: quita la primera fila (basura del reporte) antes de entregar.
    """
    temp_dir = os.path.realpath(f"/tmp/descarga_{session_id}")
    file_path = os.path.realpath(os.path.join(temp_dir, nombre))

    if not file_path.startswith(temp_dir + os.sep):
        return HttpResponseForbidden()

    if not os.path.isfile(file_path):
        from django.http import HttpResponse as HR

        return HR(status=404)

    ext = os.path.splitext(file_path)[1].lower()

    if ext in (".xlsx", ".xls"):
        # Usar magic bytes, no la extensión, para elegir el engine correcto
        engine = _excel_engine(file_path)
        if engine:
            try:
                df = pd.read_excel(file_path, header=1, dtype=str, engine=engine)
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)
                from django.http import HttpResponse as HR

                resp = HR(
                    buffer.read(),
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                resp["Content-Disposition"] = (
                    f'attachment; filename="{os.path.basename(file_path)}"'
                )
                return resp
            except Exception:
                pass  # fallback: servir el archivo tal como está

    return FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=os.path.basename(file_path),
    )


# ─── ENDPOINT: cancelar descarga ─────────────────────────────────────────────
@api_view(["POST"])
def cancelar_descarga(request):
    """POST /api/cancelar-descarga/ — { sessionId }"""
    session_id = request.data.get("sessionId", "")
    procs = _active_procs.pop(session_id, [])
    for proc in procs:
        try:
            proc.kill()
        except Exception:
            pass
    return Response({"ok": True})


# ─── ENDPOINT: insertar historial de posición ────────────────────────────────
_COLS_HISTORIAL_POS = [
    "Nº Posición Actual",
    "NO_EMPLEADO",
    "NOMBRE EMPLEADO",
    "FECHA ENTRADA POS",
    "FECHA FIN POS",
    "MOTIVO SALIDA",
    "F ENTRADA SALARIO BASE",
    "F ENTRADA PLAN SAL",
    "F ENTRADA GRADO",
    "F ENTRADA ESCALA",
    "F FIN SALARIO BASE",
    "F FIN PLAN SAL",
    "F FIN GRADO",
    "F FIN ESCALA",
]

_KEY_MAP_HISTORIAL_POS = {
    "Nº Posición Actual": "no_pos",
    "NO_EMPLEADO": "no_empleado",
    "NOMBRE EMPLEADO": "nombre_empleado",
    "FECHA ENTRADA POS": "fecha_entrada",
    "FECHA FIN POS": "fecha_fin",
    "MOTIVO SALIDA": "motivo_salida",
    "F ENTRADA SALARIO BASE": "salario_entrada",
    "F ENTRADA PLAN SAL": "f_entrada_plan_sal",
    "F ENTRADA GRADO": "grado_entrada",
    "F ENTRADA ESCALA": "escala_entrada",
    "F FIN SALARIO BASE": "salario_fin",
    "F FIN PLAN SAL": "f_fin_plan_sal",
    "F FIN GRADO": "grado_fin",
    "F FIN ESCALA": "escala_fin",
}


@api_view(["POST"])
def insertar_historial_pos(request):
    """
    POST /api/insertar-historial-pos/
    Body JSON: { "rows": [...] }  — bulk insert
    """
    rows = request.data.get("rows", [])
    if not rows:
        return Response(
            {"ok": False, "error": "rows vacío"}, status=status.HTTP_400_BAD_REQUEST
        )

    cols = ", ".join(f"`{c}`" for c in _COLS_HISTORIAL_POS)
    placeholders = ", ".join(["%s"] * len(_COLS_HISTORIAL_POS))
    sql = f"INSERT INTO HISTORIAL_POS ({cols}) VALUES ({placeholders})"
    params = [
        tuple(row.get(_KEY_MAP_HISTORIAL_POS[c]) or None for c in _COLS_HISTORIAL_POS)
        for row in rows
    ]

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


# ─── ENDPOINT: obtener posiciones distintas de MOV_POS ───────────────────────
@api_view(["GET"])
def posiciones_mov_pos(request):
    """GET /api/posiciones-mov-pos/ — devuelve lista de Nº Pos Actual distintas"""
    conn = _get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT DISTINCT(`Nº Pos Actual`) FROM MOV_POS WHERE `Nº Pos Actual` IS NOT NULL AND `Nº Pos Actual` != ''"
        )
        rows = cursor.fetchall()
        posiciones = [r[0] for r in rows]
        return Response(
            {"ok": True, "posiciones": posiciones}, status=status.HTTP_200_OK
        )
    except mysql.connector.Error as err:
        return Response(
            {"ok": False, "error": str(err)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    finally:
        cursor.close()
        conn.close()
