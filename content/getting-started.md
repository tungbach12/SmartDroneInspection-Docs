---
title: "Getting Started"
weight: 10
---

# Getting Started with SmartDroneInspection

This guide covers setting up your local development environment for the SmartDroneInspection multi-repo platform.

## Prerequisites

- **Docker Desktop** (with Compose support)
- **Java 21 JDK** (e.g. Eclipse Temurin or OpenJDK 21)
- **Node.js 20+** and **npm**
- **Flutter SDK 3.13+** (for mobile development)
- **Git**

---

## 1. Backend (Java 21 / Spring Boot 4.1.0)

The backend is organized as a Spring Modulith modular monolith under `backend/`.

### Start Local Infrastructure

Start PostgreSQL 17 (with `pgvector` and `pgcrypto`) and MinIO:

```powershell
cd backend
docker compose up -d
```

- **PostgreSQL**: `localhost:5432` (database: `smartdroneinspection`)
- **MinIO S3 API**: `http://localhost:9000`
- **MinIO Console**: `http://localhost:9001` (user: `local_minio_admin`, pass: `local_dev_only_change_me`)

### Build and Test

Run verification, code formatting checks, unit tests, and Modulith architecture tests:

```powershell
# Windows PowerShell
.\mvnw.cmd verify

# Linux / macOS
./mvnw verify
```

To auto-format code using Google Java Format:

```powershell
mvn spotless:apply
```

### Run API Server

```powershell
# Windows PowerShell
.\mvnw.cmd spring-boot:run

# Linux / macOS
./mvnw spring-boot:run
```

- **Swagger UI**: [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
- **OpenAPI JSON**: [http://localhost:8080/v3/api-docs](http://localhost:8080/v3/api-docs)
- **Health Check**: [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health)

---

## 2. Frontend (React 19 + TypeScript + Vite)

The web portal for Platform Administrators, Organization Managers, and Service Operations Managers is located under `frontend/`.

```powershell
cd frontend
npm install
npm run dev
```

- **Web Portal**: [http://localhost:3000](http://localhost:3000)
- **Production Build**: `npm run build`
- **Linter**: `npm run lint` (Oxlint)

---

## 3. Mobile (Flutter + Riverpod)

The mobile application for Inspectors and Maintenance Engineers is located under `mobile/`.

```powershell
cd mobile
flutter pub get
dart run build_runner build --delete-conflicting-outputs
flutter run
```

---

## 4. Architecture Overview

- **Feature-owned Domain**: Each Spring Modulith module owns its domain package; for example, auth entities are in `com.smartdroneinspection.users.domain`.
+ **Vertical Feature Slices**: Each feature module contains its API, domain, service, repository, and DTO records as needed. Request/response DTOs live under `<module>/api/dto/request` and `<module>/api/dto/response`. A global `com.smartdroneinspection.domain` entity module is intentionally avoided.
- **Monadic Result Pattern**: Business results use `Result<T>` (`Result.ok(...)` / `Result.err(...)`).
- **Standardized Error Handling**: Unhandled exceptions map to RFC 7807 `ProblemDetail`.
- **Consumer Model**: The platform delegates drone execution to the external **SmartDroneHub** platform via REST.
