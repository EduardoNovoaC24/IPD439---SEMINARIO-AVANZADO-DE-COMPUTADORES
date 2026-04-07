"""
IPD439 - Seminario Avanzado de Computadores
Tarea 2 - Pregunta 1(b)
Análisis de precisión y exactitud de tareas periódicas FreeRTOS

Uso:
    python3 analisis_periodos.py <archivo_csv>

El archivo CSV debe ser exportado desde PulseView con:
    File -> Export Comma-separated values...

Las señales deben estar en los canales correctos:
    - CH_TAREA1: canal de la Tarea 1 (período 100 ms)
    - CH_TAREA2: canal de la Tarea 2 (período 200 ms)
"""

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURACIÓN - Modificar según tu captura
# =============================================================================

ARCHIVO_CSV   = "Tarea_2_b"   # nombre del archivo CSV exportado de PulseView
CH_TAREA1     = 2              # índice de columna (0-based) para la Tarea 1
CH_TAREA2     = 3              # índice de columna (0-based) para la Tarea 2
SAMPLE_RATE   = 20000          # Hz - frecuencia de muestreo usada en PulseView
T_ESP_TAREA1  = 100.0          # ms - período esperado Tarea 1
T_ESP_TAREA2  = 200.0          # ms - período esperado Tarea 2

# =============================================================================
# LECTURA DEL CSV Y DETECCIÓN DE TRANSICIONES
# =============================================================================

def leer_transiciones(archivo, ch1, ch2):
    """Lee el CSV y devuelve las listas de transiciones de cada canal."""
    trans_ch1, trans_ch2 = [], []
    prev1, prev2 = None, None

    with open(archivo) as f:
        reader = csv.reader(f)
        next(reader)  # saltar encabezado
        for i, row in enumerate(reader):
            v1, v2 = int(row[ch1]), int(row[ch2])
            if prev1 is not None:
                if prev1 != v1:
                    trans_ch1.append((i, v1))
                if prev2 != v2:
                    trans_ch2.append((i, v2))
            prev1, prev2 = v1, v2

    return trans_ch1, trans_ch2


def calcular_periodos(transiciones, sample_rate):
    """Calcula períodos en ms a partir de flancos de subida consecutivos."""
    rising = np.array([t[0] for t in transiciones if t[1] == 1])
    periodos = np.diff(rising) / sample_rate * 1000  # convertir a ms
    return periodos


# =============================================================================
# ESTADÍSTICAS
# =============================================================================

def calcular_estadisticas(periodos, T_esp, nombre):
    """Calcula e imprime las estadísticas de precisión y exactitud."""
    mean    = np.mean(periodos)
    std     = np.std(periodos, ddof=1)
    mn, mx  = np.min(periodos), np.max(periodos)
    err_abs = mean - T_esp
    err_rel = abs(err_abs) / T_esp * 100

    print(f"\n{'='*50}")
    print(f"  {nombre}")
    print(f"{'='*50}")
    print(f"  N muestras         : {len(periodos)}")
    print(f"  Período esperado   : {T_esp:.4f} ms")
    print(f"  Promedio (T̄)      : {mean:.4f} ms")
    print(f"  Error absoluto     : {err_abs:+.4f} ms")
    print(f"  Error relativo     : {err_rel:.4f} %")
    print(f"  Desv. estándar σ   : {std:.4f} ms  (jitter)")
    print(f"  Mínimo             : {mn:.4f} ms")
    print(f"  Máximo             : {mx:.4f} ms")
    print(f"  Rango (máx - mín)  : {mx - mn:.4f} ms")

    return mean, std, mn, mx, err_abs, err_rel


# =============================================================================
# GRÁFICOS
# =============================================================================

def graficar_periodos_tiempo(p1, m1, s1, T1,
                              p2, m2, s2, T2):
    """Gráfico de períodos en función del número de ciclo."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 7))

    # --- Tarea 1 ---
    axes[0].plot(p1, 'o-', markersize=3, color='steelblue', linewidth=1)
    axes[0].axhline(T1, color='red',   linestyle='--',
                    label=f'Esperado: {T1} ms')
    axes[0].axhline(m1, color='green', linestyle='--',
                    label=f'Promedio: {m1:.4f} ms')
    axes[0].fill_between(range(len(p1)), m1 - s1, m1 + s1,
                         alpha=0.2, color='green',
                         label=f'±σ = {s1:.4f} ms')
    axes[0].set_title('Tarea 1 (CH2): Período medido a lo largo del tiempo')
    axes[0].set_xlabel('Número de ciclo')
    axes[0].set_ylabel('Período [ms]')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.4)
    axes[0].set_ylim([T1 - 1, T1 + 1])

    # --- Tarea 2 ---
    axes[1].plot(p2, 's-', markersize=3, color='darkorange', linewidth=1)
    axes[1].axhline(T2, color='red',   linestyle='--',
                    label=f'Esperado: {T2} ms')
    axes[1].axhline(m2, color='green', linestyle='--',
                    label=f'Promedio: {m2:.4f} ms')
    axes[1].fill_between(range(len(p2)), m2 - s2, m2 + s2,
                         alpha=0.2, color='green',
                         label=f'±σ = {s2:.4f} ms')
    axes[1].set_title('Tarea 2 (CH3): Período medido a lo largo del tiempo')
    axes[1].set_xlabel('Número de ciclo')
    axes[1].set_ylabel('Período [ms]')
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.4)
    axes[1].set_ylim([T2 - 1, T2 + 1])

    plt.tight_layout()
    plt.savefig('periodos_tiempo.png', dpi=200, bbox_inches='tight')
    print("\n[OK] Guardado: periodos_tiempo.png")
    plt.show()


def graficar_histogramas(p1, m1, T1, p2, m2, T2):
    """Histograma de los períodos medidos."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].hist(p1, bins=20, color='steelblue', edgecolor='white')
    axes[0].axvline(T1, color='red',   linestyle='--',
                    label=f'Esperado: {T1} ms')
    axes[0].axvline(m1, color='green', linestyle='--',
                    label=f'Promedio: {m1:.4f} ms')
    axes[0].set_title('Tarea 1 (CH2): Histograma de períodos')
    axes[0].set_xlabel('Período [ms]')
    axes[0].set_ylabel('Frecuencia')
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.4)

    axes[1].hist(p2, bins=20, color='darkorange', edgecolor='white')
    axes[1].axvline(T2, color='red',   linestyle='--',
                    label=f'Esperado: {T2} ms')
    axes[1].axvline(m2, color='green', linestyle='--',
                    label=f'Promedio: {m2:.4f} ms')
    axes[1].set_title('Tarea 2 (CH3): Histograma de períodos')
    axes[1].set_xlabel('Período [ms]')
    axes[1].set_ylabel('Frecuencia')
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.4)

    plt.tight_layout()
    plt.savefig('histograma_periodos.png', dpi=200, bbox_inches='tight')
    print("[OK] Guardado: histograma_periodos.png")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    # Permitir pasar el archivo por argumento
    archivo = sys.argv[1] if len(sys.argv) > 1 else ARCHIVO_CSV

    print(f"Leyendo archivo: {archivo}")
    print(f"Canal Tarea 1: columna {CH_TAREA1} | Canal Tarea 2: columna {CH_TAREA2}")
    print(f"Sample rate: {SAMPLE_RATE} Hz")

    # Leer transiciones
    trans1, trans2 = leer_transiciones(archivo, CH_TAREA1, CH_TAREA2)
    print(f"\nTransiciones detectadas -> Tarea 1: {len(trans1)} | Tarea 2: {len(trans2)}")

    # Calcular períodos
    periodos1 = calcular_periodos(trans1, SAMPLE_RATE)
    periodos2 = calcular_periodos(trans2, SAMPLE_RATE)

    # Estadísticas
    m1, s1, mn1, mx1, e1, er1 = calcular_estadisticas(
        periodos1, T_ESP_TAREA1, "Tarea 1 - período 100 ms")
    m2, s2, mn2, mx2, e2, er2 = calcular_estadisticas(
        periodos2, T_ESP_TAREA2, "Tarea 2 - período 200 ms")

    # Gráficos
    graficar_periodos_tiempo(periodos1, m1, s1, T_ESP_TAREA1,
                              periodos2, m2, s2, T_ESP_TAREA2)
    graficar_histogramas(periodos1, m1, T_ESP_TAREA1,
                         periodos2, m2, T_ESP_TAREA2)
