import requests
import csv
import time
from datetime import datetime

# Prometheus server URL
PROMETHEUS = 'http://<your-prometheus-server>:9090'

# Queries for each metric
QUERIES = {
    'kube_deployment_status_replicas': 'kube_deployment_status_replicas{deployment="nodeapp-deployment"}',
    'nginx_ingress_controller_requests': 'sum(rate(nginx_ingress_controller_requests[1m]))',
    'nginx_ingress_controller_request_size': 'sum(rate(nginx_ingress_controller_request_size_sum[1m]))',
    'nginx_ingress_controller_nginx_process_connections': 'nginx_ingress_controller_nginx_process_connections{state="active"}',
    'container_memory_usage_bytes': 'sum(container_memory_usage_bytes{pod=~"nodeapp-deployment.*"})',
    'container_cpu_usage_seconds_total': 'sum(rate(container_cpu_usage_seconds_total{pod=~"nodeapp-deployment.*"}[1m]))'
}

# Time range for data collection
START_TIME = int(time.time()) - 3600  # Start time (1 hour ago)
END_TIME = int(time.time())  # End time (current time)
STEP = '60s'  # Query step (1 minute resolution)

# Function to fetch data from Prometheus
def fetch_metric(metric_name, query):
    url = f'{PROMETHEUS}/api/v1/query_range'
    params = {
        'query': query,
        'start': START_TIME,
        'end': END_TIME,
        'step': STEP
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    result = response.json()['data']['result']
    return result

# Function to save data to CSV
def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(['timestamp'] + list(data.keys()))
        # Get the timestamps (assumes all metrics have the same timestamps)
        timestamps = [datetime.fromtimestamp(float(ts[0])).strftime('%Y-%m-%d %H:%M:%S') for ts in data[next(iter(data))]]
        for i, timestamp in enumerate(timestamps):
            row = [timestamp]
            for metric_name in data:
                row.append(data[metric_name][i][1])  # Add the value for each metric
            writer.writerow(row)

# Main function
def main():
    data = {}
    for metric_name, query in QUERIES.items():
        result = fetch_metric(metric_name, query)
        if result:
            data[metric_name] = result[0]['values']
        else:
            print(f"No data found for metric {metric_name}")
    
    save_to_csv(data, 'metrics_data.csv')
    print("Data saved to metrics_data.csv")

if __name__ == '__main__':
    main()
