import json
import csv
import requests
from collections import defaultdict

# Prometheus server URL
prometheus_server = 'http://192.168.49.2:30989'

# Queries for each metric
queries = {
    "cpu_usage": 'sum(rate(container_cpu_usage_seconds_total{pod="nodeapp-deployment-6cc654cb66-4ftbf"}[5m])) by (pod)',
    "memory_usage": 'container_memory_usage_bytes{pod="nodeapp-deployment-6cc654cb66-4ftbf"}',
    "network_receive": 'sum(rate(container_network_receive_bytes_total{pod="nodeapp-deployment-6cc654cb66-4ftbf"}[5m])) by (pod)',
    "network_transmit": 'sum(rate(container_network_transmit_bytes_total{pod="nodeapp-deployment-6cc654cb66-4ftbf"}[5m])) by (pod)',
    "network_receive_errors": 'sum(rate(container_network_receive_errors_total{pod="nodeapp-deployment-6cc654cb66-4ftbf"}[5m])) by (pod)',
    "network_transmit_errors": 'sum(rate(container_network_transmit_errors_total{pod="nodeapp-deployment-6cc654cb66-4ftbf"}[5m])) by (pod)',
    "replicas": 'kube_deployment_status_replicas{deployment="nodeapp-deployment"}'
}

# Function to fetch data from Prometheus
def fetch_prometheus_data(query):
    response = requests.get(f'{prometheus_server}/api/v1/query', params={'query': query})
    return response.json()

# Initialize a dictionary to store the combined data
combined_data = defaultdict(lambda: {
    'cpu_usage': None,
    'memory_usage': None,
    'network_receive': None,
    'network_transmit': None,
    'network_receive_errors': None,
    'network_transmit_errors': None,
    'replicas': None,
    'pod': None
})

# Fetch and process data for each metric
for metric, query in queries.items():
    data = fetch_prometheus_data(query)
    for result in data['data']['result']:
        if metric == "replicas":
            replicas = result['value'][1]
            for timestamp in combined_data:
                combined_data[timestamp]['replicas'] = replicas
        else:
            pod = result['metric'].get('pod', 'N/A')
            if 'values' in result:
                for value in result['values']:
                    timestamp, metric_value = value
                    combined_data[timestamp][metric] = metric_value
                    combined_data[timestamp]['pod'] = pod
            elif 'value' in result:
                timestamp, metric_value = result['value']
                combined_data[timestamp][metric] = metric_value
                combined_data[timestamp]['pod'] = pod

# Write the combined data to a CSV file
with open('nodeapp_metrics.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['timestamp', 'pod', 'cpu_usage', 'memory_usage', 'network_receive', 'network_transmit', 'network_receive_errors', 'network_transmit_errors', 'replicas'])

    for timestamp, metrics in sorted(combined_data.items()):
        writer.writerow([
            timestamp,
            metrics['pod'],
            metrics['cpu_usage'],
            metrics['memory_usage'],
            metrics['network_receive'],
            metrics['network_transmit'],
            metrics['network_receive_errors'],
            metrics['network_transmit_errors'],
            metrics['replicas']
        ])

print("CSV file 'nodeapp_metrics.csv' created successfully.")
