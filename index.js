const express = require('express');
const client = require('prom-client');

const app = express();
const register = new client.Registry();

// Default metrics
client.collectDefaultMetrics({ register });

// Custom metrics example
const counter = new client.Counter({
  name: 'node_request_operations_total',
  help: 'The total number of processed requests',
  labelNames: ['method'],
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.get('/', (req, res) => {
  counter.inc({ method: req.method });
  res.send('Hello, World!');
});

app.listen(4000, () => {
  console.log('Server is running on port 4000');
});
