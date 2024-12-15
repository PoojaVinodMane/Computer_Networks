# Efficient Load Balancing Mechanism in Software Defined Networks

## Introduction
This project implements a response-time-based load balancing strategy using an OpenFlow switch and evaluates its performance compared to Round Robin (RR) and Random load balancing strategies. The load balancer dynamically forwards client requests to backend servers based on the selected algorithm while monitoring metrics such as latency, response time, and throughput.

## Features
- Implements three load balancing algorithms:
  - **Round Robin (RR)**: Distributes requests evenly across servers.
  - **Random**: Assigns requests randomly to servers.
  - **Least Response Time**: Forwards requests to the server with the shortest response time.
- Supports concurrent client connections using threading.
- Logs session-level metrics (latency, response time, throughput) after each client request.
- Provides overall metrics for performance evaluation.

## Performance Evaluation
### Observation:
- When using the Least Response Time strategy, latency and throughput are higher compared to Random and Round Robin strategies.
- Server 2, with intentional random delays, handles fewer requests, leading servers 1 and 3 to manage most of the load.
### Conclusion:
- Least Response Time strategy ensures better performance in terms of overall response time and queue handling compared to static methods like Round Robin or Random.
