import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Parameters
start_time = datetime(2024, 5, 5, 12, 0)
interval = timedelta(minutes=30)
num_rows = 4 * 7 * 48  # Approximately 4 weeks of data (4 weeks * 7 days * 48 intervals/day)

# Generate time series
timestamps = [start_time + i * interval for i in range(num_rows)]

# Generate base sinusoidal trend with peaks in the evening and night
time_of_day = np.array([t.hour + t.minute / 60 for t in timestamps])  # Hours in decimal
day_of_week = np.array([t.weekday() for t in timestamps])

# Sinusoidal base trend
base_trend = 5 * np.sin((time_of_day - 12) * 2 * np.pi / 24) + 5  # Peaks around evening (18:00) and night

# Adjust for weekends
weekend_adjustment = np.where(day_of_week >= 5, 1.5, 1)  # Higher multiplier for weekends
adjusted_trend = base_trend * weekend_adjustment

# Add noise to the base trend
np.random.seed(0)
noise = np.random.normal(0, 1, size=num_rows)  # Noise level
smooth_replicas = np.clip(adjusted_trend + noise, 0, 10)

# Ensure replicas count is an integer
smooth_replicas = np.round(smooth_replicas).astype(int)

# Generate other metrics
nginx_requests = np.random.randint(100, 1000, size=num_rows)
request_size = np.random.randint(500, 5000, size=num_rows)  # in bytes
nginx_connections = np.random.randint(10, 100, size=num_rows)
memory_usage = np.random.randint(1000000, 10000000, size=num_rows)  # in bytes
cpu_usage = np.random.uniform(0.1, 5.0, size=num_rows)  # in seconds

# Create DataFrame
df = pd.DataFrame({
    'timestamp': timestamps,
    'kube_deployment_status_replicas': smooth_replicas,
    'nginx_ingress_controller_requests': nginx_requests,
    'nginx_ingress_controller_request_size': request_size,
    'nginx_ingress_controller_nginx_process_connections': nginx_connections,
    'container_memory_usage_bytes': memory_usage,
    'container_cpu_usage_seconds_total': cpu_usage
})

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Save to CSV
df.to_csv('../ml-api/datasets/autoscaler_metrics.csv', index=True)

# Plot to visualize
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['kube_deployment_status_replicas'], label='Replicas Count')
plt.title('Generated Replicas Count with Sinusoidal Pattern and Noise')
plt.xlabel('Timestamp')
plt.ylabel('Replicas Count')
plt.legend()
plt.show()

print("Dataset 'autoscaler_metrics_sinusoidal.csv' has been generated.")
