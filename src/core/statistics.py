from typing import List, Dict, Any
import math
from collections import defaultdict
from src.core.logger.utils import LoggerEvent, EventType
from src.core.utils import MessageType

class Statistics:
    def __init__(self, events: List[LoggerEvent]):
        self.events = events
        self.metrics = self._calculate_metrics()

    def _calculate_metrics(self) -> Dict[str, Any]:
        if not self.events:
            return {}

        # 1. Latency Calculation
        # Map request_id -> {start_time, end_time}
        req_times = defaultdict(dict)
        
        for event in self.events:
            # Start: When Client sends CLIENT_REQUEST
            if event.event_type == EventType.SEND and event.message_type == MessageType.CLIENT_REQUEST:
                if 'start' not in req_times[event.message_id]:
                    req_times[event.message_id]['start'] = event.timestamp
            
            # End: When Client receives CLIENT_RESPONSE
            elif event.event_type == EventType.RECEIVE and event.message_type == MessageType.CLIENT_RESPONSE:
                # The event.request_id is the ID of the RESPONSE message, not the original request.
                # We need to extract the original request_id from the payload.
                # Payload is a dict (or string representation of dict) like: {'request_id': '...', 'status': 'committed'}
                try:
                    payload = event.payload
                    if isinstance(payload, str):
                        # It might be a string representation of a dict if loaded from CSV or just logged that way
                        import ast
                        payload = ast.literal_eval(payload)
                    
                    original_req_id = payload.get('request_id')
                    if original_req_id and 'end' not in req_times[original_req_id]:
                        req_times[original_req_id]['end'] = event.timestamp
                except Exception:
                    pass # Failed to parse payload, skip

        latencies = []
        for rid, times in req_times.items():
            if 'start' in times and 'end' in times:
                latencies.append(times['end'] - times['start'])

        num_requests = len(latencies)
        if num_requests == 0:
            return {"total_requests": 0}

        avg_latency = sum(latencies) / num_requests
        latencies.sort()
        min_latency = latencies[0]
        max_latency = latencies[-1]
        p95_latency = latencies[int(num_requests * 0.95)]
        p99_latency = latencies[int(num_requests * 0.99)]

        # 2. Throughput (Requests / Total Duration)
        start_time = self.events[0].timestamp
        end_time = self.events[-1].timestamp
        duration = end_time - start_time
        throughput = num_requests / duration if duration > 0 else 0

        # 3. Network Overhead (Total Messages / Total Requests)
        total_messages = len([e for e in self.events if e.event_type == EventType.SEND])
        overhead = total_messages / num_requests if num_requests > 0 else 0

        return {
            "total_requests": num_requests,
            "duration_sec": duration,
            "throughput_rps": throughput,
            "latency_avg_ms": avg_latency * 1000,
            "latency_min_ms": min_latency * 1000,
            "latency_max_ms": max_latency * 1000,
            "latency_p95_ms": p95_latency * 1000,
            "latency_p99_ms": p99_latency * 1000,
            "network_overhead_msg_per_req": overhead
        }

    def print_report(self):
        m = self.metrics
        if not m or m.get("total_requests", 0) == 0:
            print("\n--- No successful requests analyzed ---")
            return

        print("\n" + "="*40)
        print(f"   SIMULATION METRICS REPORT")
        print("="*40)
        print(f"Total Requests Completed: {m['total_requests']}")
        print(f"Total Duration:           {m['duration_sec']:.4f} s")
        print(f"Throughput:               {m['throughput_rps']:.2f} req/s")
        print("-" * 40)
        print("LATENCY (Client-to-Client):")
        print(f"  Avg: {m['latency_avg_ms']:.2f} ms")
        print(f"  Min: {m['latency_min_ms']:.2f} ms")
        print(f"  Max: {m['latency_max_ms']:.2f} ms")
        print(f"  P95: {m['latency_p95_ms']:.2f} ms")
        print(f"  P99: {m['latency_p99_ms']:.2f} ms")
        print("-" * 40)
        print(f"Network Overhead: {m['network_overhead_msg_per_req']:.2f} messages/req")
        print("="*40 + "\n")
