import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple, Dict, List

def extract_request_id(payload: str) -> str:
    try:
        if "'request_id':" in payload:
            parts = payload.split("'request_id': '")
            if len(parts) > 1:
                request_id = parts[1].split("'")[0]
                return request_id
        return None
    except:
        return None  

def analyze_csv(csv_path: str) -> Tuple[float, float]:
    # Leggi CSV
    df = pd.read_csv(csv_path)
    
    # Estrai richieste inviate
    requests_sent_raw = df[
        (df['event_type'] == 'SEND') &
        (df['message_type'] == 'CLIENT_REQUEST')
    ][['payload', 'timestamp']]
    
    requests_sent_raw['request_id'] = requests_sent_raw['payload'].apply(extract_request_id)
    requests_sent = requests_sent_raw[['request_id', 'timestamp']].rename(columns={'timestamp': 'send_time'})
    
    print("\n--- Richieste inviate ---")
    print(requests_sent)
    print(f"Totale richieste inviate: {len(requests_sent)}")
    
    # Estrai risposte ricevute
    responses_received = df[
        (df['event_type'] == 'RECEIVE') &
        (df['message_type'] == 'CLIENT_RESPONSE')
    ][['payload', 'timestamp']].rename(columns={'timestamp': 'receive_time'})
    
    responses_received['request_id'] = responses_received['payload'].apply(extract_request_id)
    responses_received = responses_received.dropna(subset=['request_id'])
    responses_received = responses_received[['request_id', 'receive_time']]
    
    print("\n---Risposte ricevute ---")
    print(responses_received)
    print(f"Totale risposte ricevute: {len(responses_received)}")
    
    completed = pd.merge(requests_sent, responses_received, on='request_id', how='inner')
    
    print("\n--- DEBUG: Richieste completate (merge) ---")
    print(completed)
    print(f"Totale richieste completate: {len(completed)}")

    completed = completed.groupby('request_id').agg({
    'send_time': 'min',
    'receive_time': 'max'
    }).reset_index()
    
    print("\n--- DEBUG: Richieste completate (merge) ---")
    print(completed)
    print(f"Totale richieste completate: {len(completed)}")
    
    # Calcola latenza
    completed['latency'] = completed['receive_time'] - completed['send_time']
    
    print("\n--- DEBUG: Con latenze calcolate ---")
    print(completed[['request_id', 'send_time', 'receive_time', 'latency']].head(10))
    
    # Calcola throughput
    t_first = completed['send_time'].min()
    t_last = completed['receive_time'].max()
    duration = t_last - t_first
    
    num_completed = len(completed)
    throughput = num_completed / duration if duration > 0 else 0
    
    print(f"\n--- DEBUG: Calcolo throughput ---")
    print(f"Prima richiesta: {t_first:.4f}s")
    print(f"Ultima risposta: {t_last:.4f}s")
    print(f"Durata: {duration:.4f}s")
    print(f"Richieste completate: {num_completed}")
    print(f"Throughput: {throughput:.2f} req/s")
    
    avg_latency_ms = completed['latency'].mean() * 1000
    
    print(f"Latenza media: {avg_latency_ms:.2f} ms")
    print("-" * 50)
    
    return throughput, avg_latency_ms



if __name__ == '__main__':

    tput_pb, lat_pb = analyze_csv('output/example_low_.csv')
    print(f"   Latenza media:  {lat_pb:.2f} ms")
    print(f"   Throughput:     {tput_pb:.2f} req/s")