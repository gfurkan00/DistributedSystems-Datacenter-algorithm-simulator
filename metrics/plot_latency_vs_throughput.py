import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from analyzer import analyze_csv, LatencyThroughput


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, help="Output plot file path", required=True)
    return parser.parse_args()


def list_csv_files(directory: str | Path) -> list[str]:
    directory = Path(directory)
    if not directory.exists():
        print(f"⚠️  Directory non trovata: {directory}")
        return []
    return [str(p) for p in directory.glob("*.csv")]


def plot_comparison(protocols_data: dict, output_path: str):
    plt.figure(figsize=(12, 8))

    # Definizione stili per coerenza
    styles = {
        0: {'color': '#1f77b4', 'marker': 'o', 'linestyle': '-', 'label': 'Primary-Backup'},  # Blu
        1: {'color': '#ff7f0e', 'marker': 's', 'linestyle': '-', 'label': 'LOWI'},  # Arancione
        2: {'color': '#2ca02c', 'marker': '^', 'linestyle': '-', 'label': 'Paxos'},  # Verde
    }

    # Mappatura nomi protocollo a indici stile
    proto_to_idx = {
        'Primary-Backup': 0,
        'LOWI': 1,
        'PAXOS': 2
    }

    for protocol_name, folder_path in protocols_data.items():
        csv_files = list_csv_files(directory=folder_path)

        # Lista di tuple (throughput, latency) per poterle ordinare
        data_points = []

        print(f"\n📊 Analisi protocollo: {protocol_name}...")

        for csv_path in csv_files:
            metrics: LatencyThroughput = analyze_csv(csv_path)

            if metrics and metrics.throughput_per_seconds > 0:
                data_points.append((metrics.throughput_per_seconds, metrics.average_latency_ms))
            else:
                print(f"  ❌ Skip {Path(csv_path).name}: dati non validi")

        # ORDINAMENTO FONDAMENTALE: Ordina per throughput (asse X)
        # Altrimenti il grafico a linee fa zig-zag
        data_points.sort(key=lambda x: x[0])

        if data_points:
            # Separa x e y dopo l'ordinamento
            x_vals = [pt[0] for pt in data_points]
            y_vals = [pt[1] for pt in data_points]

            idx = proto_to_idx.get(protocol_name, 0)
            style = styles.get(idx, styles[0])

            plt.plot(
                x_vals,
                y_vals,
                marker=style['marker'],
                linestyle=style['linestyle'],
                color=style['color'],
                linewidth=2.5,
                markersize=8,
                label=protocol_name,
                alpha=0.8
            )
            print(f"  ✅ Plottati {len(data_points)} punti.")
        else:
            print(f"  ⚠️  Nessun dato valido per {protocol_name}")

    # Configurazione grafico
    plt.xlabel('Throughput (req/s)', fontsize=14, fontweight='bold')
    plt.ylabel('Average Latency (ms)', fontsize=14, fontweight='bold')
    plt.title('Latency vs Throughput Saturation', fontsize=16, fontweight='bold', pad=20)
    plt.legend(fontsize=12, loc='upper left', frameon=True)
    plt.grid(True, alpha=0.3, linestyle='--')

    # Imposta limiti assi per pulizia (parte da 0)
    plt.ylim(bottom=0)
    plt.xlim(left=0)

    plt.tight_layout()

    # Salva il grafico
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n{'=' * 60}")
    print(f"  🖼️  Grafico salvato in: {output_path}")
    print(f"{'=' * 60}\n")


if __name__ == '__main__':
    args = _parse_arguments()

    # Assicurati che questi percorsi esistano o adattali
    protocols_data = {
        'Primary-Backup': 'output/saturation/primary-backup/',
        #'LOWI': 'output/saturation/lowi/',
        'PAXOS': 'output/saturation/paxos/',
    }

    plot_comparison(protocols_data=protocols_data, output_path=args.output)