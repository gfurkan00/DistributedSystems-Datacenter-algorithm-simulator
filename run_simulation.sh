#!/bin/bash

echo "======================================"
echo "Simulations start"
echo "======================================"
echo ""

mkdir -p output/saturation

LOWI_CONFIGS=("saturation_lowi_50" "saturation_lowi_70" "saturation_lowi_90" "saturation_lowi_110")
PAXOS_CONFIGS=("saturation_paxos_50" "saturation_paxos_70" "saturation_paxos_90" "saturation_paxos_110")
PB_CONFIGS=("saturation_pb_50" "saturation_pb_70" "saturation_pb_90" "saturation_pb_110")

echo ""
echo "📊 LOWI"
echo "-------------------------"

for i in "${!LOWI_CONFIGS[@]}"; do
    config="${LOWI_CONFIGS[$i]}"
    num=$((i+1))
    total=${#LOWI_CONFIGS[@]}
    echo ""
    echo "[$num/$total] $config..."
    uv run main.py --config "configs/lowi/saturation/${config}.yml" 2>&1 | tail -8
done

echo""
echo "📊 PAXOS"
echo "-------------------------"

for i in "${!PAXOS_CONFIGS[@]}"; do
    config="${PAXOS_CONFIGS[$i]}"
    num=$((i+1))
    total=${#PAXOS_CONFIGS[@]}
    echo ""
    echo "[$num/$total] $config..."
    uv run main.py --config "configs/paxos/saturation/${config}.yml" 2>&1 | tail -8
done

echo ""
echo "📊 Primary-Backup"
echo "------------------------------------"

for i in "${!PB_CONFIGS[@]}"; do
    config="${PB_CONFIGS[$i]}"
    num=$((i+1))
    total=${#PB_CONFIGS[@]}
    echo ""
    echo "[$num/$total] $config..."
    uv run main.py --config "configs/primary-backup/saturation/${config}.yml" 2>&1 | tail -8
done

echo ""
echo "======================================"
echo "✅  Simulations Done!"
echo "======================================"

echo ""
echo "📈 Generazione grafico comparativo..."
uv run ./metrics/plot_latency_vs_throughput.py --output "output/plot.png"