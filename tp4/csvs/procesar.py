import re
import numpy as np
import pandas as pd


def limpiar_datos_osciloscopio(archivo_in, archivo_out, max_puntos=1500):
    # 1. Leer las primeras 6 líneas para extraer el Sampling Rate
    sampling_rate = None
    with open(archivo_in, "r") as f:
        header = [f.readline().strip() for _ in range(6)]

    for line in header:
        if "Sampling Rate" in line:
            match = re.search(r"Sampling Rate:([\d\.]+)([kM]?)Sa/s", line)
            if match:
                valor = float(match.group(1))
                unidad = match.group(2)
                if unidad == "M":
                    sampling_rate = valor * 1e6
                elif unidad == "k":
                    sampling_rate = valor * 1e3
                else:
                    sampling_rate = valor

    if not sampling_rate:
        raise ValueError(
            f"No se pudo encontrar el Sampling Rate en {archivo_in}"
        )

    # El intervalo de tiempo entre puntos (en milisegundos)
    dt = (1 / sampling_rate) * 1000

    # 2. Detectar si es 1 o 2 canales mirando los datos
    with open(archivo_in, "r") as f:
        for _ in range(6):
            f.readline()  # saltar encabezado
        linea_datos = f.readline()
        num_canales = 2 if "," in linea_datos else 1

    # 3. Cargar los datos numéricos saltando el encabezado de 6 líneas
    if num_canales == 1:
        df = pd.read_csv(archivo_in, skiprows=6, header=None, names=["Ch1"])
    else:
        df = pd.read_csv(
            archivo_in,
            skiprows=6,
            header=None,
            names=["Ch1", "Ch2"],
            sep=r"\s*,\s*",
            engine="python",
        )

    # 4. Crear la columna de Tiempo (ms) y pasar amplitudes de mV a V (dividiendo por 1000)
    df.insert(0, "Tiempo", np.arange(len(df)) * dt)
    df["Ch1"] = df["Ch1"] / 1000.0
    if num_canales == 2:
        df["Ch2"] = df["Ch2"] / 1000.0

    # 5. Reducir puntos (Downsampling) para que LaTeX no explote
    if len(df) > max_puntos:
        factor = int(np.ceil(len(df) / max_puntos))
        df_reducido = df.iloc[::factor].copy()
    else:
        df_reducido = df

    # Guardar CSV limpio listo para LaTeX
    df_reducido.to_csv(archivo_out, index=False)
    print(
        f"✓ {archivo_in} procesado -> {archivo_out} ({len(df_reducido)} puntos)"
    )


# --- EJECUCIÓN (Cambiá los nombres por tus archivos reales) ---
# limpiar_datos_osciloscopio('DEFAULT2.csv', 'default2.csv')
# limpiar_datos_osciloscopio('DEFAULT5.csv', 'default5.csv')
# limpiar_datos_osciloscopio('DEFAULT6.csv', 'default6.csv')
# limpiar_datos_osciloscopio('DEFAULT9.csv', 'default9.csv')
# limpiar_datos_osciloscopio('DEFAULTA.csv', 'defaultA.csv')
# limpiar_datos_osciloscopio('DEFAULTB.csv', 'defaultB.csv')
limpiar_datos_osciloscopio('DEFAULTC.csv', 'defaultC.csv')
# limpiar_datos_osciloscopio('DEFAULTD.csv', 'defaultD.csv')
# limpiar_datos_osciloscopio('DEFAULTE.csv', 'defaultE.csv')
# limpiar_datos_osciloscopio('DEFAULTF.csv', 'defaultF.csv')
# limpiar_datos_osciloscopio('DEFAULTG.csv', 'defaultG.csv')

