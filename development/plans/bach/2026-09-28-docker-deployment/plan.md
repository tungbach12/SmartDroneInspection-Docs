# Implementation Plan: Docker Deployment for Backend and Web

**Feature Branch**:
- Backend: `feat/docker-deployment`
- Frontend: `feat/docker-deployment`
- Docs: `docs/docker-deployment`
**Created**: 2026-09-28
**Spec**: [spec.md](./spec.md)
**Owner**: Bách

## Proposed Changes

### Backend Repository (`SmartDroneInspection-backend/`)

- Add `Dockerfile`: multi-stage build using `maven:3.9-eclipse-temurin-21` and `eclipse-temurin:21-jre-alpine`.
  - Dependency caching with `mvn dependency:resolve dependency:resolve-plugins`.
  - Build fat jar with `mvn -DskipTests clean package`.
  - Runtime executes under non-root user `appuser`.
  - Healthcheck probes `http://localhost:8080/actuator/health`.
- Add `.dockerignore`: exclude `target/`, IDE files, `.git/`, `.env*`.
- Add `.env.example`: template with all required keys, generation commands, and security guidelines.
- Update `docker-compose.yml`:
  - Keep `postgres` (pgvector 17) and `minio` services; bind ports to `127.0.0.1` by default.
  - Add `backend` service with `depends_on` healthy postgres & minio, active profile `prod`.
  - Add `web` service (from frontend directory) with `depends_on` healthy backend.
  - Expose `web` on `${WEB_PORT:-80}`.
- Update `README.md`: document single-command full-stack deployment alongside host development workflow.

### Frontend Repository (`SmartDroneInspection-frontend/`)

- Add `Dockerfile`: multi-stage build using `node:22-alpine` and `nginx:1.27-alpine`.
  - `npm ci --legacy-peer-deps` for deterministic dependencies.
  - `npm run build` producing static assets.
  - Healthcheck probes `http://localhost:80/`.
- Add `nginx.conf`:
  - Reverse proxy `/api/` to `backend:8080` (same-origin, eliminates CORS, preserves HttpOnly refresh cookie).
  - SPA fallback: `try_files $uri $uri/ /index.html` with no-cache header on HTML.
  - Static asset caching (`1y`, immutable).
  - Gzip compression and standard security headers.
- Add `.dockerignore`: exclude `node_modules/`, `dist/`, `.git/`, IDE files.

### Docs Repository (`SmartDroneInspection-docs/`)

- Add `spec.md` and `plan.md` in `development/plans/bach/2026-09-28-docker-deployment/`.

## Verification Checklist

- [x] Frontend image builds cleanly: `smartdroneinspection-web:test` verified.
- [ ] Backend image builds cleanly: `smartdroneinspection-backend:test`.
- [x] Docker Compose configuration parses and validates: `docker compose config`.
- [ ] Complete stack build verification via `docker compose build`.
- [ ] Host backend test suite remains green: `./mvnw.cmd verify`.
