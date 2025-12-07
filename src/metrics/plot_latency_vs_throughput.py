import matplotlib.pyplot as plt
from pathlib import Path
from analyzer import analyze_csv

def plot_comparison(protocols_data: dict, output_path: str = 'output/latency_vs_throughput.png'):
    plt.figure(figsize=(12, 8))
    
    styles = {
        0: {'color': '#2E86AB', 'marker': 'o', 'linestyle': '-'},  # Blu
        1: {'color': '#A23B72', 'marker': 's', 'linestyle': '-'},  # Viola
        2: {'color': '#F18F01', 'marker': '^', 'linestyle': '-'},  # Arancione
    }
    
    for idx, (protocol_name, csv_files) in enumerate(protocols_data.items()):
        throughputs = []
        latencies = []
        
        for csv_path in csv_files:
            # Verifica che il file esista
            if not Path(csv_path).exists():
                print(f"⚠️  File non trovato: {csv_path}")
                continue
            
            print(f"\n  📄 {csv_path}")
            
            # Analizza il CSV
            tput, lat = analyze_csv(csv_path)
            
            if tput > 0:  # Solo se l'analisi ha successo
                throughputs.append(tput)
                latencies.append(lat)
                print(f"     → Throughput: {tput:.2f} req/s, Latency: {lat:.2f} ms")
            else:
                print(f"Analisi fallita (nessuna richiesta completata)")
        
        # Plotta i dati di questo protocollo
        if throughputs:
            style = styles.get(idx, {'color': 'gray', 'marker': 'o', 'linestyle': '-'})
            plt.plot(
                throughputs, 
                latencies,
                marker=style['marker'],
                linestyle=style['linestyle'],
                color=style['color'],
                linewidth=2,
                markersize=10,
                label=protocol_name,
                alpha=0.8
            )
            
            print(f"\n  ✅ {len(throughputs)} punti aggiunti al grafico")
        else:
            print(f"\n  ❌ Nessun dato valido per {protocol_name}")
    
    # Configurazione grafico
    plt.xlabel('Throughput (req/s)', fontsize=14, fontweight='bold')
    plt.ylabel('Latency (ms)', fontsize=14, fontweight='bold')
    plt.title('Latency vs Throughput - Protocol Comparison', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    # Salva il grafico
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n{'='*60}")
    print(f"  ✅ Grafico salvato in: {output_path}")
    print(f"{'='*60}\n")
    
    # Opzionale: mostra il grafico
    # plt.show()


if __name__ == '__main__':
    protocols_data = {
        'Primary-Backup': [
            '../../output/example_primary_backup_furkan.csv',
        ],
        
        'LOWI': [
            '../../output/example_lowi_furkan.csv',
        ],
    }
    
    # Genera il grafico
    plot_comparison(protocols_data, output_path='../../output/latency_vs_throughput.png')
