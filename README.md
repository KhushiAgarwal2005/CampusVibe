# 🚀 CampusVibe — Cloud-Native RAG Knowledge Base

> A production-style, cloud-native knowledge platform that combines **Retrieval-Augmented Generation (RAG)** with a complete **DevOps and GitOps deployment pipeline** on AWS.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit\&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes\&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?logo=helm\&logoColor=white)
![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazonaws)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?logo=jenkins\&logoColor=white)
![Argo CD](https://img.shields.io/badge/Argo%20CD-EF7B4D?logo=argo\&logoColor=white)

---

## 📌 Overview

**CampusVibe** is a RAG-based knowledge management and question-answering platform designed to provide intelligent responses from campus-related information and documents.

The application combines a **Streamlit frontend**, **MongoDB Atlas** for metadata management, **Firebase Storage** for document storage, and a **Retrieval-Augmented Generation pipeline** using **LlamaIndex** and semantic embeddings.

The application is containerized with **Docker** and deployed to **Amazon EKS** using **Helm**.

The complete deployment process follows a **CI/CD + GitOps workflow**:

```text
Developer
    │
    ▼
GitHub
    │
    ▼
Jenkins CI Pipeline
    │
    ├── Build Docker Image
    ├── Push Image to Docker Hub
    └── Update Image Tag
            │
            ▼
        Git Repository
            │
            ▼
          Argo CD
            │
            ▼
        Amazon EKS
            │
            ├── Deployment
            ├── Service
            ├── HPA
            ├── PDB
            ├── Liveness Probe
            ├── Readiness Probe
            └── Ingress
                    │
                    ▼
              AWS ALB
                    │
                    ▼
             CampusVibe App
```

---

# ✨ Key Features

### 🤖 RAG-Based Question Answering

* Retrieval-Augmented Generation architecture
* Semantic document retrieval
* Hugging Face sentence-transformer embeddings
* LlamaIndex-based RAG pipeline
* Local LLM inference using Ollama
* Supports campus-related knowledge retrieval

### 🗄️ Data & Storage

* **MongoDB Atlas** for metadata
* **Firebase Storage** for document storage
* Persistent storage for the Ollama workload
* Kubernetes PersistentVolume and PersistentVolumeClaim

### ☁️ Cloud-Native Deployment

* Docker containerization
* Kubernetes orchestration
* Amazon EKS deployment
* Helm-based application packaging
* AWS Load Balancer Controller
* AWS Application Load Balancer

### 🔄 CI/CD Pipeline

* GitHub as source control
* Jenkins for continuous integration
* Docker image build automation
* Versioned Docker image tags
* Docker Hub image registry

### 🔁 GitOps with Argo CD

* Declarative Kubernetes deployments
* Automatic synchronization
* Git as the source of truth
* Continuous deployment through Argo CD
* Application health monitoring

### 📈 Kubernetes Reliability & Scaling

* Horizontal Pod Autoscaler (HPA)
* Pod Disruption Budget (PDB)
* Liveness probes
* Readiness probes
* Replica management
* Pod scheduling controls
* Resource requests and limits

---

# 🏗️ Technology Stack

| Category             | Technology                           |
| -------------------- | ------------------------------------ |
| Frontend             | Streamlit                            |
| Programming Language | Python                               |
| RAG Framework        | LlamaIndex                           |
| Embeddings           | Hugging Face / Sentence Transformers |
| LLM                  | Ollama / Llama                       |
| Database             | MongoDB Atlas                        |
| File Storage         | Firebase Storage                     |
| Containerization     | Docker                               |
| Orchestration        | Kubernetes                           |
| Package Management   | Helm                                 |
| Cloud Platform       | AWS                                  |
| Kubernetes Service   | Amazon EKS                           |
| Load Balancer        | AWS Application Load Balancer        |
| CI                   | Jenkins                              |
| Container Registry   | Docker Hub                           |
| GitOps / CD          | Argo CD                              |
| Source Control       | GitHub                               |

---

# 📂 Project Structure

```text
CampusVibe/
│
├── campusvibe/
│   ├── Chart.yaml
│   ├── values.yaml
│   │
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── hpa.yaml
│       ├── pdb.yaml
│       ├── pvc.yaml
│       └── serviceaccount.yaml
│
├── Jenkinsfile
├── Dockerfile
├── requirements.txt
├── app.py
└── README.md
```

> The exact application files may vary depending on the repository structure.

---

# 🐳 Docker

The application is packaged as a Docker image to ensure consistent execution across development and production environments.

### Build the image

```bash
docker build -t campusvibe .
```

### Run locally

```bash
docker run -p 8501:8501 campusvibe
```

The application can then be accessed at:

```text
http://localhost:8501
```

---

# ☸️ Kubernetes Deployment

CampusVibe is deployed to **Amazon EKS** using Helm.

### Create namespace

```bash
kubectl create namespace campusvibe
```

### Install Helm chart

```bash
helm install campusvibe ./campusvibe \
  -n campusvibe
```

### Check deployment

```bash
kubectl get pods -n campusvibe
```

### Check services

```bash
kubectl get svc -n campusvibe
```

### Check ingress

```bash
kubectl get ingress -n campusvibe
```

---

# ⛵ Helm

The application is packaged as a reusable Helm chart.

The Helm chart contains Kubernetes manifests for:

* Deployment
* Service
* Ingress
* Horizontal Pod Autoscaler
* Pod Disruption Budget
* PersistentVolumeClaim
* ServiceAccount

Configuration is managed through:

```text
values.yaml
```

This allows environment-specific configuration without modifying Kubernetes manifests directly.

---

# 🔄 CI/CD Pipeline

The project uses **Jenkins** to automate the Continuous Integration workflow.

### Pipeline Flow

```text
GitHub Push
     │
     ▼
Jenkins Pipeline Trigger
     │
     ▼
Checkout Source Code
     │
     ▼
Build Docker Image
     │
     ▼
Tag Image
     │
     ▼
Push Image to Docker Hub
     │
     ▼
Update Kubernetes Deployment Configuration
     │
     ▼
Argo CD Detects Change
```

The pipeline produces versioned Docker image tags, allowing controlled application releases and easy rollback.

Example:

```text
campusvibe:11
campusvibe:12
campusvibe:13
campusvibe:latest
```

---

# 🔁 GitOps with Argo CD

Argo CD is used as the Continuous Delivery and GitOps tool.

The Git repository acts as the **single source of truth** for the Kubernetes deployment configuration.

### GitOps Workflow

```text
Developer
    │
    ▼
GitHub
    │
    ▼
Jenkins
    │
    ▼
Docker Hub
    │
    ▼
Kubernetes Manifest / Helm Values Updated
    │
    ▼
Argo CD
    │
    ▼
Amazon EKS
```

Argo CD continuously monitors the Git repository and synchronizes the desired state with the Kubernetes cluster.

The CampusVibe application is expected to maintain:

```text
SYNC STATUS: Synced
HEALTH STATUS: Healthy
```

---

# 🌐 AWS Application Load Balancer

The application is exposed externally using the **AWS Load Balancer Controller** and a Kubernetes Ingress resource.

```text
Internet
    │
    ▼
AWS Application Load Balancer
    │
    ▼
Kubernetes Ingress
    │
    ▼
CampusVibe Service
    │
    ▼
CampusVibe Pods
```

This provides external access to the CampusVibe application through an AWS-managed Application Load Balancer.

---

# 📈 Horizontal Pod Autoscaler

The CampusVibe application uses Kubernetes HPA to automatically adjust the number of application replicas based on resource utilization.

Example configuration:

```text
Minimum Replicas: 1
Maximum Replicas: 4
CPU Target: 60%
```

Check HPA status:

```bash
kubectl get hpa -n campusvibe
```

---

# 🛡️ Pod Disruption Budget

A Pod Disruption Budget is configured to improve application availability during voluntary disruptions such as:

* Node maintenance
* Cluster upgrades
* Node draining
* Kubernetes infrastructure changes

Check PDB:

```bash
kubectl get pdb -n campusvibe
```

---

# ❤️ Liveness & Readiness Probes

The CampusVibe application uses Kubernetes health probes.

### Liveness Probe

Determines whether the container is still functioning correctly.

If the application becomes unhealthy, Kubernetes can restart the container.

### Readiness Probe

Determines whether the application is ready to receive traffic.

Traffic is only routed to pods that pass the readiness check.

This improves application reliability and prevents traffic from being sent to unhealthy or unready pods.

---

# 🔐 Kubernetes Security & Scheduling

The deployment includes Kubernetes best practices such as:

* Kubernetes ServiceAccounts
* Resource requests
* Resource limits
* Pod affinity / anti-affinity rules
* Pod distribution considerations
* Replica management
* Health probes
* Pod Disruption Budget

These configurations help improve workload reliability, resource management, and high availability.

---

# 📊 Monitoring & Verification

Useful Kubernetes commands:

### View Pods

```bash
kubectl get pods -n campusvibe
```

### View Deployment

```bash
kubectl get deployment -n campusvibe
```

### View HPA

```bash
kubectl get hpa -n campusvibe
```

### View PDB

```bash
kubectl get pdb -n campusvibe
```

### View Ingress

```bash
kubectl get ingress -n campusvibe
```

### View all resources

```bash
kubectl get all -n campusvibe
```

---

# 🚀 Deployment Architecture

```text
                         ┌──────────────────┐
                         │     Developer    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     GitHub       │
                         │ Source + Helm    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Jenkins      │
                         │   CI Pipeline    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Docker Hub    │
                         │  Versioned Image │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Argo CD      │
                         │   GitOps / CD     │
                         └────────┬─────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │          AWS EKS              │
                  │                               │
                  │  ┌─────────────────────────┐  │
                  │  │     CampusVibe          │  │
                  │  │                         │  │
                  │  │ Deployment              │  │
                  │  │ Service                 │  │
                  │  │ HPA                     │  │
                  │  │ PDB                     │  │
                  │  │ Liveness / Readiness    │  │
                  │  │ Ingress                 │  │
                  │  └────────────┬────────────┘  │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     AWS ALB      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  CampusVibe App  │
                         └──────────────────┘
```

---

# 🧪 Project Validation Checklist

* [x] Docker image successfully built
* [x] Docker image pushed to Docker Hub
* [x] Jenkins CI pipeline configured
* [x] Kubernetes cluster created on AWS EKS
* [x] Helm chart created
* [x] Application deployed using Helm
* [x] Argo CD configured for GitOps
* [x] Application synchronized through Argo CD
* [x] AWS Load Balancer configured
* [x] HPA configured
* [x] PDB configured
* [x] Liveness probe configured
* [x] Readiness probe configured
* [x] Kubernetes resource management configured

---

# 🎯 Project Goals

The primary goals of CampusVibe are:

1. Build an intelligent RAG-based knowledge platform.
2. Containerize the application using Docker.
3. Deploy the application on Kubernetes.
4. Automate CI using Jenkins.
5. Implement GitOps-based CD using Argo CD.
6. Use Helm for Kubernetes application packaging.
7. Deploy the infrastructure on AWS EKS.
8. Expose the application through an AWS Application Load Balancer.
9. Implement Kubernetes scalability and reliability practices.
10. Demonstrate a complete production-style DevOps workflow.

---

# 👨‍💻 Author

**Reyansh Chandak**

B.Tech Computer Science & Engineering

---

# ⭐ Project Highlights

> **CampusVibe demonstrates the integration of AI/ML, RAG, Cloud Computing, Kubernetes, CI/CD, and GitOps into a complete cloud-native application deployment workflow.**

```text
AI / RAG
   +
Docker
   +
Kubernetes
   +
Helm
   +
Jenkins CI
   +
Argo CD GitOps
   +
AWS EKS
   +
AWS ALB
   =
CampusVibe 🚀
```

---

