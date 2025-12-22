# 🚀 learning-jenkins – CI Evolution (Level 1 → Level 4)

This repository documents the **evolution of a real-world Jenkins CI pipeline**, progressing step by step from a minimal setup to a **production-grade CI system**.

The focus is not just *making Jenkins work*, but understanding **why each capability is added and when**.

---

## 🟢 Level 1 – Basic CI Pipeline

**Goal:** Establish a working Jenkins pipeline.

- Simple Jenkinsfile
- Code checkout
- Run unit tests
- Fail fast on errors ❌

This level builds the foundation and pipeline structure.

---

## 🟡 Level 2 – Quality Gates & Feedback

**Goal:** Improve code quality and visibility.

- Unit tests with `pytest`
- Linting with `ruff`
- JUnit test reports in Jenkins UI 📊
- Artifact archiving

CI now provides **actionable feedback**, not just pass/fail.

---

## 🟠 Level 3 – Matrix Builds & Docker Delivery

**Goal:** Make CI scalable and deployment-aware.

- Python matrix testing (3.10 / 3.11 / 3.12)
- Selective execution:
  - Full linting, typing, and coverage only on Python 3.12
- Docker image build and push 🐳
- Safe tagging strategy:
  - Commit SHA (`sha-xxxxxxx`)
  - Branch + build number
  - `latest` (main branch only)
- Smoke test of the built Docker image

This level introduces **real deployment artifacts** and multi-version confidence.

---

## 🔴 Level 4 – Production-Grade CI

**Goal:** Harden the pipeline for real-world usage.

### Key Improvements

- **Concurrency safety** 🔒  
  Prevent overlapping builds with `disableConcurrentBuilds()` to avoid:
  - Workspace collisions
  - Docker tag races
  - Cache corruption

- **Deterministic Docker builds** 📦  
  - Base images pinned by digest
  - Clean `.dockerignore` to avoid leaking build artifacts

- **Cross-node Docker layer caching** ⚡  
  - Docker Buildx
  - Registry-backed cache (`--cache-from` / `--cache-to`)
  - Speeds up builds across different Jenkins nodes

- **Coverage enforcement** 📈  
  - Single source of truth via `.coveragerc`
  - Coverage reports visible **even on failed builds**

- **Workspace hygiene** 🧹  
  - Explicit artifact archiving
  - Build retention policy (`buildDiscarder`)

- **Strict image publishing rules** 🚦  
  - Docker images pushed **only from `main`**
  - Feature branches never publish images by mistake

---

## 🧱 Jenkins Agent Strategy (Pre-Baked Agents)

All jobs run on **pre-baked Jenkins agent Docker images**, not raw VMs or generic nodes.

🔗 **Agent image repository:**  
👉 https://github.com/gal-halevi/jenkins-agent-docker

### Why a pre-baked agent?

The agent image already contains:
- Docker CLI + Docker Buildx
- Required OS-level tooling

Jenkins jobs themselves run **inside containers**, while Docker is accessed via the host socket  
(Docker-in-Docker pattern).

### Benefits

- ⚡ Faster job startup
- 🔁 Deterministic environments
- 📦 No repeated installation of Docker tooling
- 🧠 Clear separation between:
  - CI infrastructure (agent image)
  - Project logic (Jenkinsfile)

Project-specific dependencies are still installed per build, ensuring isolation.

---

## 🧭 Summary

By Level 4, this CI pipeline demonstrates:

- Deterministic and reproducible builds
- Multi-version test confidence
- Safe Docker image delivery
- Cross-node caching
- Clear CI observability
- Production-grade Jenkins practices

This repository emphasizes **engineering decisions**, not just Jenkins syntax.
