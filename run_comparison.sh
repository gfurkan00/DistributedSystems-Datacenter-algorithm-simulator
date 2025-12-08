#!/bin/bash

mkdir -p output/comparison

echo "📊 Esecuzione simulazioni Primary-Backup..."
echo ""

echo "  [1/4] Primary-Backup LOW..."
uv run main.py --config configs/primary-backup/comparison/comparison_primary_backup_low.yml

echo ""
echo "  [2/4] Primary-Backup MEDIUM..."
uv run main.py --config configs/primary-backup/comparison/comparison_primary_backup_medium.yml

echo ""
echo "  [3/4] Primary-Backup HIGH..."
uv run main.py --config configs/primary-backup/comparison/comparison_primary_backup_high.yml

echo ""
echo "  [4/4] Primary-Backup EXTREME..."
uv run main.py --config configs/primary-backup/comparison/comparison_primary_backup_extreme.yml

echo ""
echo "✅ Primary-Backup completato!"
echo ""
echo "========================================"
echo ""

echo "📊 Esecuzione simulazioni LOWI..."
echo ""

echo "  [1/4] LOWI LOW..."
uv run main.py --config configs/lowi/comparison/comparison_lowi_low.yml

echo ""
echo "  [2/4] LOWI MEDIUM..."
uv run main.py --config configs/lowi/comparison/comparison_lowi_medium.yml

echo ""
echo "  [3/4] LOWI HIGH..."
uv run main.py --config configs/lowi/comparison/comparison_lowi_high.yml

echo ""
echo "  [4/4] LOWI EXTREME..."
uv run main.py --config configs/lowi/comparison/comparison_lowi_extreme.yml

echo ""
echo "✅ LOWI completato!"
echo ""
echo "========================================"
echo ""

echo "📊 Esecuzione simulazioni Basic Paxos..."
echo ""

echo "  [1/4] PAXOS LOW..."
uv run main.py --config configs/paxos/comparison/comparison_paxos_low.yml

echo ""
echo "  [2/4] PAXOS MEDIUM..."
uv run main.py --config configs/paxos/comparison/comparison_paxos_medium.yml

echo ""
echo "  [3/4] PAXOS HIGH..."
uv run main.py --config configs/paxos/comparison/comparison_paxos_high.yml

echo ""
echo "  [4/4] PAXOS EXTREME..."
uv run main.py --config configs/paxos/comparison/comparison_paxos_extreme.yml

echo ""
echo "✅ BASIC PAXOS completato!"
echo ""
echo "========================================"
echo ""

echo "📈 Generazione grafico comparativo..."
uv run ./metrics/plot_latency_vs_throughput.py
