[Vigilant Pay]
>   A high-performing real-time api protection tool.
>   The application uses MVC architecture because velocity was important for the development. MVC
    increased the development speed, ease of test and deployment.


![Success Badge](https://github.com/Timi-Jegede/vigilant-pay/actions/workflows/ci.yml/badge.svg)
[![Python Version](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python)](https://python.org)
[![Django Version](https://img.shields.io/badge/Django-5.2+-092e20?logo=django&logoColor=white)](https://djangoproject.com)

## 🚀 Highlights
*   **Scalable Architecture**:  Monolithic architecture using Django Framework for server-side rendered
                                appplication to enable rapid development and simplified state management.
                                
                                Full-stack integration by integrating fraud scoring logic directly into the request-response lifecycle using Django signals and middleware.
*   **Security First**:         Implements MFA authentication.

## 🛠 Tech Stack
*   **Backend**:    Django, PostgreSQL
*   **Frontend**:   TypeScript, Django-Plotly Dash

## ⚙️ Local Development
### Prerequisites
*   Docker & Docker Compose (Recommended)
*   Python 3.13+

### Setup
1.  **Clone & Environment**:
    ```bash
    git clone [repo-url]
    cp .env.example .env # configure your secrets here
    ```

2.  **Run with Docker (Standard for Senior Profiles)**:
    ```bash
    docker-compose up --build
    ```

3.  **Database Setup**:
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

The application will be live at `http://localhost:8000

## 🏗 Sytem Architecture
```mermaid
graph TD
    %% Define System Actors and Entry
    Client[🏦 Fintech Client App] -->|1. POST Request + JSON Payload| Gateway[🌐 API Gateway App]
    
    %% Middleware Processing Layers
    subgraph Django Middleware Pipeline
        Gateway -->|2. Authenticate Token| Auth[🔒 Client Auth Middleware]
        Auth -->|3. Enrich GeoData / IP Lookup| Geo[🌍 Geo Data Enrichment]
    end

    %% Internal Processing Logic
    subgraph Fraud Detection Engine Core
        Geo -->|4. Pass Formatted Payload| View[📄 EvaluateTransactionView]
        View -->|5. Clean & Validate Data| Serializer[📋 TransactionSerializer]
        Serializer -->|6. Validated Fields| FeatureService[⚙️ MLFeatureService]
        FeatureService -->|7. Extracted Vectors| Model[🧠 PredictMLModel XGBoost]
    end

    %% Testing Isolation Framework (The Mocks)
    subgraph GitHub Actions / Pytest Mock Layer
        M_Auth[🚫 Bypassed in CI] -.->|Override Settings| Auth
        M_Geo[🚫 Bypassed in CI] -.->|Mock Request Attrs| Geo
        M_Feat[📦 Returns Dummy Vectors] -.->|@patch| FeatureService
        M_Model[💾 Returns Fake Probabilities] -.->|@patch / sys.modules| Model
    end

    %% Return Data Flow
    Model -->|8. Raw Score Details| View
    View -->|9. JSON Response: BLOCK / APPROVE| Client

    %% Stylings
    style Client fill:#f9f,stroke:#333,stroke-width:2px
    style View fill:#bbf,stroke:#333,stroke-width:2px
    style Model fill:#bfb,stroke:#333,stroke-width:2px
    style GitHub Actions / Pytest Mock Layer fill:#fff2cc,stroke:#d6b656,stroke-width:1px,stroke-dasharray: 5 5

```

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

