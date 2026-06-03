# ✦ AeroCanvas

[![FastAPI Engine](https://img.shields.io/badge/API_Gateway-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![GraalVM Native](https://img.shields.io/badge/Compute_Core-GraalVM_AOT-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://www.graalvm.org/)
[![Gemini 2.5](https://img.shields.io/badge/Cognitive_Layer-Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white)](https://deepmind.google/technologies/gemini/)

A high-performance, multi-language compute engine designed to optimize media transformation pipelines. By compiling our core computational pipeline into standalone native machine binaries using GraalVM Ahead-of-Time (AOT) compilation, the system completely bypasses traditional JVM cold-start penalties and executes spatial convolution filters with sub-millisecond efficiency.

---

## 🎬 Live System Demonstration

### 1. Cognitive Agent Execution Loop
*The Gemini-driven agentic layer intercepting a natural language prompt, intelligently resolving the mathematical filter mode, executing live function calling, and streaming the processed assets.*

![AI Agent Function Calling Demo](frontend/assests/agent_demo.gif)

### 2. High-Performance Web UI Interactive Canvas
*The UI layer executing lightning-fast asynchronous requests to the local gateway cluster, leveraging cache-busting timestamping to defeat aggressive browser storage behaviors.*

![Web UI Execution Demo](frontend/assests/canvas_demo.gif)

---

## 🏗️ System Architecture & Data Flow

The platform utilizes a decoupled, 4-tier micro-stack layout built on a common shared disk-plane to minimize memory copy overheads:

```text
[ Human Operator ] ────► ( Natural Language Prompt ) ────► [ ai_orchestrator ]
                                                                  │
                                                        ( Live Function Call )
                                                                  ▼
[ HTML5 / Canvas ] ◄──── ( Cache-Busted Link ) ◄─── [ api_gateway (FastAPI) ]
       │                                                          │
 (Multipart Upload)                                        (Subprocess Spawn)
       ▼                                                          ▼
## 📊 Performance Benchmarks & Compute Analysis
[ workspace_data/input.ppm ] ─────────────────────────► [ core_engine (Native Binary) ]
Execution Target Profile,Average Cold Start Latency,Compute Execution Speed,Peak Memory Footprint (RSS)
Standard JVM (java Main),142.50 ms,18.40 ms,112.00 MB
GraalVM Native AOT (.exe),1.80 ms,4.10 ms,28.30 MB
Performance Multiplier,~79x Faster Init,~4.5x Faster Execution,74.7% Memory Reduction

