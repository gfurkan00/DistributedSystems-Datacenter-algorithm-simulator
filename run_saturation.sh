#!/bin/bash

echo "🚀 Esecuzione Simulazioni Saturazione"
echo "======================================"
echo ""

mkdir -p output/comparison

# Array delle configurazioni
LOWI_CONFIGS=("saturation_lowi_70" "saturation_lowi_90" "saturation_lowi_110")
PB_CONFIGS=("saturation_pb_50" "saturation_pb_100" "saturation_pb_150" "saturation_pb_200")

# LOWI (già fatto 50)
echo "📊 LOWI Saturazione Tests"
echo "-------------------------"

for i in "${!LOWI_CONFIGS[@]}"; do
    config="${LOWI_CONFIGS[$i]}"
    num=$((i+2))
    total=7
    echo ""
    echo "[$num/$total] $config..."
    uv run main.py --config "configs/${config}.yml" 2>&1 | tail -5
    
    # Quick analysis
    if [ -f "output/comparison/${config#saturation_}.csv" ]; then
        echo "  ✅ CSV generato"
    else
        echo "  ❌ CSV non trovato!"
    fi
done

echo ""
echo "📊 Primary-Backup Saturazione Tests"
echo "------------------------------------"

for i in "${!PB_CONFIGS[@]}"; do
    config="${PB_CONFIGS[$i]}"
    num=$((i+4))
    total=7
    echo ""
    echo "[$num/$total] $config..."
    uv run main.py --config "configs/${config}.yml" 2>&1 | tail -5
    
    # Quick analysis
    if [ -f "output/comparison/${config#saturation_}.csv" ]; then
        echo "  ✅ CSV generato"
    else
        echo "  ❌ CSV non trovato!"
    fi
done

echo ""
echo "======================================"
echo "✅  Simulazioni Completate!"
echo "======================================"
echo ""
echo "📁 Risultati in: output/comparison/"
ls -lh output/comparison/*sat*.csv 2>/dev/null | wc -l
echo " file CSV generati"
