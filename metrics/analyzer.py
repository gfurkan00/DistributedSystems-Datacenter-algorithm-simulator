import argparse
import pandas as pd

from dataclasses import dataclass
from typing import Optional

TIME_UNIT_TO_SECONDS = 1e-3


@dataclass
class LatencyThroughput:
    average_latency_ms: float
    throughput_per_seconds: float


def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="CSV file to analyse")
    args = parser.parse_args()
    if not args.path:
        raise RuntimeError("CSV file not specified")
    return args


def extract_request_id_vectorized(payload_series: pd.Series) -> pd.Series:
    return payload_series.str.extract(r"'request_id':\s*'([^']+)'")[0]


def analyze_csv(csv_path: str) -> Optional[LatencyThroughput]:
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Errore lettura CSV {csv_path}: {e}")
        return None

    requests_sent = df[
        (df['event_type'] == 'SEND') &
        (df['message_type'] == 'CLIENT_REQUEST')
    ].copy()

    responses_received = df[
        (df['event_type'] == 'RECEIVE') &
        (df['message_type'] == 'CLIENT_RESPONSE')
    ].copy()

    requests_sent['request_id'] = extract_request_id_vectorized(requests_sent['payload'])
    responses_received['request_id'] = extract_request_id_vectorized(responses_received['payload'])

    requests_sent = requests_sent[['request_id', 'timestamp']].rename(columns={'timestamp': 'send_time'})
    responses_received = responses_received[['request_id', 'timestamp']].rename(columns={'timestamp': 'receive_time'})

    completed = pd.merge(requests_sent, responses_received, on='request_id', how='inner')

    completed = completed.groupby('request_id').agg({
        'send_time': 'min',
        'receive_time': 'max'
    }).reset_index()

    num_completed = len(completed)
    print(f"Requests sent: {len(requests_sent)} | Responses: {len(responses_received)} | Completed: {num_completed}")


    t_first = completed['send_time'].min()
    t_last = completed['receive_time'].max()
    duration_units = t_last - t_first

    duration_seconds = duration_units * TIME_UNIT_TO_SECONDS

    throughput = num_completed / duration_seconds if duration_seconds > 0 else 0

    completed['latency_units'] = completed['receive_time'] - completed['send_time']

    avg_latency_ms = completed['latency_units'].mean()

    return LatencyThroughput(
        average_latency_ms=avg_latency_ms,
        throughput_per_seconds=throughput,
    )


if __name__ == '__main__':
    args = _parse_arguments()
    metrics = analyze_csv(args.path)
    print(f"Average Latency: {metrics.average_latency_ms:.4f} ms")
    print(f"Throughput: {metrics.throughput_per_seconds:.2f} req/s")