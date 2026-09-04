---
title: "Getting Started"
weight: 10
---

# Getting Started

This guide explains how to set up the local development environment for **SmartDroneInspection** across Backend, Database, Frontend, and Mobile.

---

## 1. Prerequisites

* **.NET 9 / .NET 10 SDK**
* **Docker & Docker Compose** (for PostgreSQL 17 + pgvector, MinIO)
* **Node.js 20+ & npm**
* **Flutter SDK 3.24+** (for Mobile development)

---

## 2. Infrastructure Setup (Docker)

Start the local PostgreSQL 17 database with `pgvector` extension and MinIO Object Storage:

```bash
# Start Docker containers
docker run -d \
  --name smartdroneinspection-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=smartdroneinspection \
  -p 5432:5432 \
  pgvector/pgvector:pg17

# MinIO Object Storage
docker run -d \
  --name smartdroneinspection-minio \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -p 9000:9000 -p 9001:9001 \
  minio/minio server /data --console-address ":9001"
```

---

## 3. Backend Setup

The Backend can be run in two modes based on team preferences:

### Running MinimalClean (Recommended)

```bash
cd backend/MinimalClean
dotnet build
dotnet run --project src/MinimalClean.Architecture.Web
```

API will be accessible at:
* Swagger / Scalar UI: `https://localhost:7080/scalar/v1` or `http://localhost:5080/swagger`
* Health Check: `https://localhost:7080/health`

### Database Migrations

```bash
cd backend/MinimalClean
dotnet ef database update -p src/MinimalClean.Architecture.Web -s src/MinimalClean.Architecture.Web
```

---

## 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

* Dev Server runs on `http://localhost:3000` (proxies `/api` to `https://localhost:7080`).
* Build check: `npm run build` (TypeScript strict).

---

## 5. Mobile Setup

```bash
cd mobile
flutter pub get
flutter run
```
