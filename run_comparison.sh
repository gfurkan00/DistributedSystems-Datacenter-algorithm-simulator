#!/bin/bash

# Script per eseguire il confronto completo tra Primary-Backup e LOWI
# Genera grafici Latency vs Throughput

echo "========================================"
echo "  CONFRONTO PRIMARY-BACKUP vs LOWI"
echo "========================================"
echo ""

# Crea directory output se non esiste
mkdir -p output/comparison

echo "📊 Esecuzione simulazioni Primary-Backup..."
echo ""

# Primary-Backup - 4 livelli di workload
echo "  [1/4] Primary-Backup LOW..."
uv run main.py --config configs/comparison_primary_backup_low.yml

echo ""
echo "  [2/4] Primary-Backup MEDIUM..."
uv run main.py --config configs/comparison_primary_backup_medium.yml

echo ""
echo "  [3/4] Primary-Backup HIGH..."
uv run main.py --config configs/comparison_primary_backup_high.yml

echo ""
echo "  [4/4] Primary-Backup EXTREME..."
uv run main.py --config configs/comparison_primary_backup_extreme.yml

echo ""
echo "✅ Primary-Backup completato!"
echo ""
echo "========================================"
echo ""

echo "📊 Esecuzione simulazioni LOWI..."
echo ""

# LOWI - 4 livelli di workload
echo "  [1/4] LOWI LOW..."
uv run main.py --config configs/comparison_lowi_low.yml

echo ""
echo "  [2/4] LOWI MEDIUM..."
uv run main.py --config configs/comparison_lowi_medium.yml

echo ""
echo "  [3/4] LOWI HIGH..."
uv run main.py --config configs/comparison_lowi_high.yml

echo ""
echo "  [4/4] LOWI EXTREME..."
uv run main.py --config configs/comparison_lowi_extreme.yml

echo ""
echo "✅ LOWI completato!"
echo ""
echo "========================================"
echo ""

echo "📈 Generazione grafico comparativo..."
uv run src/metrics/plot_latency_vs_throughput.py

echo ""
echo "========================================"
echo "  ✅ CONFRONTO COMPLETATO!"
echo "========================================"
echo ""
echo "📊 Risultati disponibili in:"
echo "   - CSV logs: output/comparison/*.csv"
echo "   - Grafico: output/latency_vs_throughput.png"
echo ""
