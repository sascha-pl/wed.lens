# WedLens

## Project Overview

WedLens is a private, AI-powered wedding photo platform.

The initial real-world use case is a wedding: guests can upload photos, the system processes them, and users can search and discover photos based on people, metadata, and eventually semantic/image understanding.

The long-term goal is to turn the project into a technically serious, production-like application that demonstrates:

* Modern Python backend development
* AI/LLM integration
* Computer vision
* Face detection and optional face identification
* Vector similarity search
* PostgreSQL
* RDF / semantic knowledge representation
* CI/CD
* Docker
* Kubernetes
* OpenShift
* Monitoring and observability
* Kubeflow Pipelines
* Scalable application architecture

The project should remain a real, usable product rather than becoming a technology showcase with unnecessary complexity.

---

# Product Vision

## Core Concept

WedLens connects:

* Photos
* People
* Events
* Metadata
* AI-generated information
* Relationships between people and photos

The central user experience is:

> "Help me find the photos I care about."

Examples:

* Show me photos of Anna.
* Show me photos of Anna and Markus together.
* Show me photos from the ceremony.
* Show me photos taken around 22:00.
* Show me all photos I uploaded.
* Show me photos containing Anna from the reception.
* Eventually: "Show me photos of Anna and Markus dancing."

The application should provide source/context information for AI-generated results where possible.

---

# Product Principles

1. **Useful before clever**

   * Build a genuinely usable photo application before adding advanced AI functionality.

2. **Incremental complexity**

   * Do not introduce Kubernetes, OpenShift, Kubeflow, or other infrastructure until the local application works.

3. **Real engineering**

   * Prefer production-like patterns over toy implementations.
   * Handle errors, authentication, validation, logging, storage, background processing, and security properly.

4. **Privacy first**

   * Wedding photos and facial information are personal data.
   * Avoid collecting unnecessary personal information.
   * Face identification must be opt-in.
   * Do not expose uploaded photos publicly by default.

5. **No fake expertise**

   * Technologies should only be listed as project experience once they are actually implemented and understood.
   * Do not add technologies merely because they are on the roadmap.

6. **Keep the architecture explainable**

   * Every major component should have a clear reason to exist.

---

# Initial MVP

The first milestone is intentionally small.

## MVP 0.1

A user must be able to:

1. Authenticate
2. Upload a photo
3. See uploaded photos in a gallery
4. View photo metadata
5. Delete photos
6. Create/manage people
7. Associate people with photos manually
8. Search photos by people and metadata

Do NOT implement advanced face recognition, semantic search, Kubernetes, OpenShift, or Kubeflow in the first MVP.

The first goal is a reliable photo management application.

---

# MVP 0.2 — AI Photo Processing

After the basic application works:

1. Detect faces in uploaded photos.
2. Store detected face information.
3. Generate face embeddings using a pretrained model.
4. Allow users to associate a detected face with a person.
5. Use embeddings to suggest possible person matches.
6. Require confirmation for uncertain matches.

Example:

```text
Photo
  ├── Face 1 → Anna (94% similarity)
  ├── Face 2 → Markus (88% similarity)
  └── Face 3 → Unknown
```

The system must never silently assume a person's identity when confidence is insufficient.

---

# MVP 0.3 — Semantic/Image Search

Add richer search capabilities.

Examples:

```text
Anna
Anna + Markus
Ceremony
Reception
22:00
Anna during the ceremony
Anna and Markus together
```

Eventually support natural-language queries such as:

> "Show me photos of Anna and Markus dancing."

The system may combine:

* Structured database filtering
* Face/person matching
* Image embeddings
* Metadata
* LLM query interpretation

Do not make the LLM the authoritative source of truth.

---

# Future Semantic Knowledge Layer

A later project phase should explore a semantic representation of relationships between:

* People
* Photos
* Events
* Locations
* Activities
* Albums

Potential technologies:

* RDF
* OWL
* SPARQL
* Triplestore

Example conceptual graph:

```text
Anna
  └── appearsIn → Photo123

Markus
  └── appearsIn → Photo123

Photo123
  └── partOf → WeddingReception

Anna
  └── relatedTo → Markus
```

The semantic layer should be introduced only after the conventional application and database model are stable.

Do not force RDF/OWL into every part of the application.

---

# Planned Architecture

The long-term architecture is approximately:

```text
                         Web Frontend
                              |
                              v
                         FastAPI API
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
     PostgreSQL          Object Storage       AI Workers
          |                   |                   |
          |                   |          +--------+--------+
          |                   |          |        |        |
          |                   |          v        v        v
          |                   |       Face AI   Vision    LLM
          |                   |          |
          |                   |          v
          |                   |      Embeddings
          |                   |          |
          +-------------------+----------+
                              |
                              v
                       Search / Retrieval
                              |
                              v
                    Optional Semantic Layer
                              |
                              v
                         RDF / SPARQL
```

---

# Recommended Technology Stack

## Frontend

Preferred:

* Vue
* TypeScript
* modern component-based architecture

Use the user's existing Vue knowledge where practical.

Do not introduce React unless there is a strong technical reason.

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy or another well-supported ORM/database layer

## Database

Primary:

* PostgreSQL

Potential extensions:

* pgvector for vector similarity search

## Object Storage

Use an S3-compatible abstraction.

For local development, a local storage implementation or MinIO may be used.

Do not couple application logic directly to a specific cloud provider.

## AI

Potential components:

* pretrained face detection model
* pretrained face embedding model
* image embedding model
* OpenAI-compatible LLM API

Do not train a facial recognition model from scratch.

Do not make external LLM calls for operations that can be done deterministically.

---

# Data Model

The initial conceptual entities are:

```text
User
Person
Photo
PhotoPerson
Album
Event
Upload
ProcessingJob
FaceDetection
Embedding
```

Possible relationships:

```text
User
 └── uploads → Photo

Photo
 ├── contains → FaceDetection
 ├── associatedWith → Person
 ├── belongsTo → Album
 └── belongsTo → Event

Person
 └── appearsIn → Photo
```

The exact relational schema should be designed during implementation rather than blindly copying this conceptual model.

---

# Photo Processing Pipeline

Image processing should eventually run asynchronously.

Conceptually:

```text
Upload
   |
   v
Validate
   |
   v
Store Original
   |
   v
Create Processing Job
   |
   v
Generate Thumbnail
   |
   v
Extract Metadata
   |
   v
Detect Faces
   |
   v
Generate Face Embeddings
   |
   v
Generate Image Embedding
   |
   v
Persist Results
   |
   v
Available for Search
```

Processing must not block the HTTP request for expensive operations.

Use background jobs/workers once the basic synchronous implementation is proven.

---

# Face Recognition / Identification

Face detection and face identification are separate concepts.

## Face detection

Determine where faces exist in an image.

## Face identification

Determine whether a detected face belongs to a known person.

Identification must be opt-in.

Users should explicitly provide a reference photo and consent to being identifiable.

The application should support:

* Unknown person
* Suggested match
* Confirmed match

Never automatically label a person with low confidence.

Do not expose facial embeddings publicly.

---

# Privacy and Security

This is a private wedding application.

Security is a core feature, not an afterthought.

Requirements:

* Authentication
* Authorization
* Private-by-default photos
* Secure upload handling
* File type validation
* File size limits
* Rate limiting
* Protection against path traversal
* Safe image processing
* No arbitrary file execution
* No API keys in frontend code
* Secrets stored through environment/configuration mechanisms
* No sensitive data in Git
* Avoid unnecessary retention of uploaded images
* Audit sensitive operations where appropriate

For public demos, use synthetic/test data or explicitly consented data.

Never publish real wedding photos without explicit permission.

---

# API Design

The backend should expose clear REST endpoints.

Potential structure:

```text
/api/auth/...

/api/photos
/api/photos/{id}

/api/people
/api/people/{id}

/api/albums
/api/albums/{id}

/api/search

/api/jobs/{id}
```

Use consistent:

* HTTP status codes
* validation
* error responses
* pagination
* filtering
* API documentation

FastAPI's generated OpenAPI documentation should remain usable.

---

# Frontend Views

Initial views:

## Login

Authentication.

## Gallery

Browse photos.

Features:

* thumbnails
* pagination/infinite scrolling
* filters
* upload
* photo selection

## Photo Detail

Display:

* original/optimized image
* metadata
* detected people
* associated event
* uploader
* processing state

## People

List known people.

Person detail:

```text
Anna

Reference photo

Photos:
[ ... ]
```

## Search

Structured and eventually natural-language search.

## Admin/Event Management

Potential later functionality for:

* managing guests
* managing event configuration
* reviewing face suggestions
* reviewing processing failures

---

# Background Processing

Expensive operations should eventually use a job queue.

Examples:

```text
photo.uploaded
     |
     v
processing job
     |
     +--> thumbnail
     +--> metadata
     +--> face detection
     +--> embeddings
     +--> indexing
```

Potential technologies can be evaluated later.

Do not introduce Kafka or other heavyweight infrastructure unless there is a real need.

---

# CI/CD Roadmap

Once the application works locally:

```text
Git Push
   |
   v
Automated Tests
   |
   v
Lint / Type Checks
   |
   v
Build Docker Image
   |
   v
Security Scan
   |
   v
Push Image
   |
   v
Deploy
   |
   v
Health Check
```

Potential technology:

* GitHub Actions
* Docker
* container registry

---

# Containerization Roadmap

Eventually create separate containers for major services.

Potential services:

```text
frontend
api
worker
postgres
object-storage
```

Local development should initially use Docker Compose.

Do not containerize every trivial component unnecessarily.

---

# Kubernetes Roadmap

After Docker-based local deployment works:

Learn and use:

* Pods
* Deployments
* Services
* ConfigMaps
* Secrets
* Persistent Volumes
* Resource Requests/Limits
* Health Checks
* Horizontal Pod Autoscaling

Example:

```text
API
 ├── replica 1
 ├── replica 2
 └── replica 3
```

The project should be capable of explaining why replicas and resource limits exist.

---

# OpenShift Roadmap

After Kubernetes fundamentals are understood:

Deploy the application to OpenShift/OKD or an appropriate learning environment.

Explore:

* Projects
* Routes
* Deployments
* Secrets
* ConfigMaps
* Resource management
* Build/deployment workflows
* Application operations

Do not claim professional OpenShift experience based solely on this project.

Use accurate CV wording such as:

> Hands-on OpenShift experience through personal project.

---

# Monitoring and Observability

Later introduce:

* Prometheus
* Grafana
* structured application logging
* health endpoints
* metrics
* error tracking

Useful metrics:

```text
HTTP request count
HTTP error rate
HTTP response latency
Photo upload rate
Processing queue length
Processing duration
Face detection duration
LLM request count
LLM latency
Worker failures
CPU usage
Memory usage
```

Create a useful dashboard rather than collecting metrics without purpose.

---

# Scalability / Performance

The project should eventually demonstrate:

* horizontal API scaling
* background workers
* rate limiting
* caching where useful
* efficient image processing
* resource limits
* database indexing
* pagination
* asynchronous processing

Load testing can be used to demonstrate behavior under increasing traffic.

Do not optimize prematurely.

Measure first.

---

# Kubeflow Roadmap

Kubeflow should be introduced only once image processing is already working.

The pipeline could become:

```text
Input Images
     |
     v
Preprocessing
     |
     v
Face Detection
     |
     v
Face Embedding
     |
     v
Image Embedding
     |
     v
Metadata Extraction
     |
     v
Indexing
     |
     v
Evaluation
```

The purpose is to demonstrate practical pipeline orchestration rather than simply installing Kubeflow.

---

# Project Development Phases

## Phase 0 — Project Setup

* Repository
* README
* Architecture documentation
* Development environment
* Frontend skeleton
* Backend skeleton
* PostgreSQL
* Basic Docker Compose

## Phase 1 — Core Product

* Authentication
* Photo upload
* Photo storage
* Gallery
* Photo details
* Metadata
* Delete photos
* Basic search/filtering

## Phase 2 — People

* People management
* Person reference photos
* Manual photo/person associations
* Person-based search

## Phase 3 — AI

* Face detection
* Face embeddings
* Suggested person matching
* Image embeddings
* Async processing

## Phase 4 — Advanced Search

* Vector search
* Combined structured/vector search
* Natural-language queries
* LLM query interpretation
* Search result explanations

## Phase 5 — Semantic Knowledge

* RDF
* OWL
* Triplestore
* SPARQL
* Model relationships between people/photos/events

Only introduce this where it provides actual value.

## Phase 6 — Production Engineering

* Docker
* CI/CD
* Automated tests
* Security scanning
* Deployment automation

## Phase 7 — Kubernetes

* Kubernetes deployment
* Scaling
* Resource limits
* Health checks
* Persistent storage

## Phase 8 — Observability

* Prometheus
* Grafana
* Logs
* Metrics
* Alerts

## Phase 9 — OpenShift

* OpenShift deployment
* OpenShift-specific configuration
* Operations

## Phase 10 — Kubeflow

* Pipeline orchestration
* AI processing workflow
* Pipeline monitoring/evaluation

---

# Current Priority

The current priority is **Phase 0 and Phase 1 only**.

Do NOT start implementing:

* Kubernetes
* OpenShift
* Kubeflow
* Prometheus
* Grafana
* RDF
* OWL
* SPARQL
* complex vector search

until the basic photo application works.

The immediate target is:

```text
User
  ↓
Login
  ↓
Upload photo
  ↓
Photo stored
  ↓
Photo appears in gallery
  ↓
Photo metadata visible
  ↓
Photo searchable
```

Once this works reliably, begin adding AI functionality.

---

# Development Guidelines for Codex

## General

* Prefer simple, maintainable solutions.
* Avoid premature abstraction.
* Avoid unnecessary dependencies.
* Follow established conventions of the selected frameworks.
* Keep components modular.
* Write tests for meaningful business logic.
* Update documentation when architecture changes.
* Do not silently introduce major architectural changes.

## Before adding a dependency

Ask:

1. Is this actually necessary?
2. Can the standard library/framework already solve it?
3. Does it materially improve the project?
4. Will it complicate deployment?

Prefer fewer dependencies.

## API

* Validate all external input.
* Return useful errors.
* Do not leak internal exceptions.
* Keep business logic out of route handlers where practical.

## Database

* Use migrations.
* Never modify production schema manually.
* Add indexes based on actual query requirements.
* Use transactions appropriately.

## Files

Treat uploaded files as untrusted input.

Validate:

* size
* MIME type
* file extension
* image decoding
* storage path

Never trust filenames supplied by users.

## AI

* Keep model/provider integrations behind service interfaces.
* Do not hard-code API keys.
* Make AI operations observable.
* Store model/version information where useful.
* Handle API failures and rate limits.
* Do not use LLMs for deterministic tasks.

## Privacy

* Assume all wedding data is private.
* Minimize data collection.
* Keep authorization checks close to data access.
* Do not expose private photo URLs accidentally.
* Do not commit real wedding photos to the repository.

---

# Repository Structure

Initial target:

```text
wed.lens/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   └── privacy.md
│
└── infrastructure/
    └── # added later
```

Do not create Kubernetes/OpenShift directories until those phases actually begin.

---

# Definition of Done

A feature is not complete merely because it works locally once.

For meaningful features, consider:

* implementation
* validation
* error handling
* tests
* documentation
* security implications
* migration if schema changes
* reasonable UI behavior

The project should remain runnable from a clean checkout using documented instructions.

---

# Portfolio Goal

The finished project should eventually demonstrate that the developer can:

* design a real application
* build a Python backend
* build a modern frontend
* work with PostgreSQL
* integrate AI services
* process images asynchronously
* use vector search
* model semantic relationships
* containerize applications
* implement CI/CD
* deploy to Kubernetes/OpenShift
* monitor production-like workloads
* reason about scalability and performance
* orchestrate AI pipelines

The final GitHub repository should contain:

* clear README
* architecture diagram
* setup instructions
* screenshots
* API documentation
* testing instructions
* deployment documentation
* technology rationale
* examples of monitoring
* performance/load-test results where appropriate

The project should tell a coherent story:

> A real wedding photo product was built first, then progressively evolved into a production-like AI platform.

---

# Naming

Current project name:

**WedLens**

Possible tagline:

> Private, AI-powered discovery for your wedding memories.

Repository name:

```text
wed.lens
```

The architecture should remain general enough that WedLens could eventually become a broader private photo-memory platform rather than being permanently tied to weddings.
