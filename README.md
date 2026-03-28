# DocuGeniusAI: AI-Driven Document Engineering Platform

<p align="center">
  <img src="https://assets.zyrosite.com/AQEZkE43zXtgRjLB/docugenius-ai-logo-kteCwjiZWTiZ6Rey.png" alt="DocuGenius AI Logo" width="300">
</p>

**DocuGeniusAI** transforms how businesses create personalized documents. It bridges the gap between unstructured business requirements and structured, AI-powered document generation. Administrators define document schemas, and users fill dynamic forms to generate professional, compliant documents instantly.

## Why DocuGeniusAI?

- **Streamline Document Creation:** Move away from manual, repetitive document drafting.
- **Increase Accuracy & Consistency:** Reduce human error by standardizing document structures.
- **Boost Efficiency:** Save time for professionals by automating routine document tasks.
- **Enhance User Experience:** Provide an intuitive form-based interface for non-technical users.
- **Leverage AI Responsibly:** Utilize generative models for high-fidelity output while maintaining control and validation.
- **Built for Scalability:** Robust, secure architecture designed to grow with your business needs.

Perfect for: Legal, Financial, Consulting, Healthcare, Insurance, Government Agencies, or any organization requiring consistent, personalized document output at scale.

## Core Features

- **Admin Schema Configuration:** Define `Document Types` and their required/optional `Fields` via an admin panel.
- **User-Friendly Generation:** Common users select a document type and fill a dynamic form tailored to that type.
- **AI-Powered Generation:** Generate high-quality, formatted documents (e.g., contracts, reports, proposals) based on user input and AI models.
- **Role-Based Access Control (RBAC):** Separate environments and permissions for administrators and common users.
- **Secure & Scalable:** Built with security best practices and designed for horizontal scaling.

### Default User Credentials (For Testing)

After the initial application startup, two default users are created automatically:

**Admin User:**
*   **Username:** `admin`
*   **Password:** `UniqueSecretSuperPaSSword92!37`

**Common User:**
*   **Username:** `common`
*   **Password:** `PaSSword92!37`

Use these credentials to log in and explore the admin and user functionalities respectively.

## Experience the Flow

Ready to automate your document generation process?  
**[Watch Demo Video](https://youtu.be/E6lHLd9oYAs)** *(Demonstrates the application flow)*<br>
**[https://fmbyteshiftsoftware.com](https://fmbyteshiftsoftware.com/)**<br>
**[Contact for Setup](mailto:contact@fmbyteshiftsoftware.com)** *(Schedule a quick setup call)*<br>

## Technical Excellence

Built with modern, reliable technologies: Python, FastAPI, React, MySQL, Generative AI.

---

*DocuGeniusAI: Where intelligent automation meets professional document standards.*

---

## Architecture & Deployment

### Application Architecture

This diagram illustrates the high-level structure of the DocuGeniusAI system, showing the relationship between the Frontend Application (React), API interfaces, Backend application logic, Core Domain, Infrastructure components, and External services.

![DocuGeniusAI Architecture](docs/diagrams/architecture/docugenius-ai-architecture-diagram.png) <!-- Caminho relativo à raiz do repo -->

---

### ▶ Try It Locally

Want to run the full DocuGeniusAI application (frontend and backend) locally? Choose your preferred setup method.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (for Option 1)
- [Python 3.13+](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) (for Option 2 - Backend)
- [Node.js](https://nodejs.org/en/download/) and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) (for Option 2 - Frontend)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

#### Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/python-projects-fernando/docugenius-ai.git
cd docugenius-ai
```

#### Environment Configuration (.env file)

Create a `.env` file in the **root directory** of the project (`docugenius-ai/.env`) based on the `.env.example` file located there.

1.  **Copy the Example File:**
    ```bash
    # From the docugenius-ai root directory
    cp .env.example .env
    ```
2.  **Edit the `.env` File:**
    *   Open the newly created `.env` file in a text editor.
    *   Replace the placeholder values (like `fakeRootPassword123!`, `your-super-secret-jwt-key-change-this-in-production`, `hf_fakeTokenForExampleAbCdEfGhIjKlMnOpQrStUvWxYz`, etc.) with your actual credentials and settings.
    *   **For Option 1 (Docker Compose):** Ensure the values are appropriate for the services running inside Docker (e.g., database passwords should match those in `docker-compose.yml`).
    *   **For Option 2 (Local Execution):** Ensure `DATABASE_URL` points to your local/host MySQL instance (e.g., `mysql+aiomysql://user:your_local_password@localhost:3306/docugenius_ai`).

#### Option 1 Compose (Recommended)

This is the easiest way to run the entire application stack (frontend, backend, MySQL, Redis) with a single command.

**Important:** Ensure your **root** `.env` file contains the environment variables required for the Docker Compose setup (especially `DATABASE_URL` pointing to the internal `db` service, and other secrets/tokens).

1.  **Copy the Example Compose File:**
    *   Locate the `docker-compose.example.yml` file in the repository root.
    *   **Rename** it to `docker-compose.yml` in the root directory (`docugenius-ai/`).
    *   **Review** the newly renamed `docker-compose.yml` file. Ensure the service names, build contexts, ports, and environment variable references are correct and match your setup.

2.  **Run the Application Stack:**
    ```bash
    # Build images (if needed) and run the full application stack (frontend, backend, db, redis)
    # Docker Compose will automatically load environment variables from the .env file in the current directory
    docker-compose up --build
    ```

*   The **Backend API** will be available at **http://localhost:8000**
*   The **Backend API Documentation** will be accessible at **http://localhost:8000/docs**
*   The **Frontend** will be available at **http://localhost:5173** (or the port you mapped in `docker-compose.yml`)
*   The **Database** (MySQL) will be accessible internally within the Docker network as `db:3306` and externally on your host machine as `localhost:3306` (mapped by the compose file).
*   The **Cache** (Redis) will be accessible internally as `redis:6379`.

> **Note:** The initial build might take a few minutes as it downloads dependencies, builds the frontend bundle, and sets up the backend environment.

#### Option 2: Run Services Separately (Local Execution)

If you prefer to run the backend and frontend services directly on your host machine (outside of Docker), follow these steps.

**Important:** Ensure your **root** `.env` file contains the environment variables required for local execution (especially `DATABASE_URL` pointing to your local MySQL instance).

1.  **Set up the Backend:**
    *   **Navigate to the Backend Directory (Optional but Recommended):** While `uvicorn backend.main:app` can run from the root, ensure the `.env` is accessible and the `backend` package can be resolved (e.g., by installing it in editable mode or setting `PYTHONPATH`). For simplicity here, we'll run from root.
    *   **Set up Virtual Environment (Recommended):**
        ```bash
        # Create a virtual environment named .venv in the root directory
        python -m venv .venv

        # Activate the virtual environment
        # On Windows:
        .venv\Scripts\activate
        # On macOS/Linux:
        source .venv/bin/activate
        ```
    *   **Install Backend Dependencies:**
        ```bash
        # Navigate to the backend directory
        cd backend
        # Install the backend package and its dependencies in editable mode
        pip install -e .
        # Install runtime dependencies
        pip install -r requirements.txt
        # Install development dependencies (optional, for tests/linting)
        # pip install -r requirements-dev.txt
        # Navigate back to the root directory
        cd ..
        ```
    *   **Ensure your root `.env` file is configured correctly for local DB access.**
    *   **Ensure your local MySQL instance is running and the `docugenius_ai` database exists.**
    *   **Run the Backend Application (from the root project directory `docugenius-ai/`):**
        ```bash
        # Run the application using uvicorn
        uvicorn backend.main:app --reload
        ```
        The **Backend API** will be running at **http://localhost:8000**  
        Access the interactive API documentation at **http://localhost:8000/docs**.

2.  **Set up the Frontend (in a new terminal):**
    *   **Navigate to the Frontend Directory:**
        ```bash
        cd frontend # From the root directory docugenius-ai/
        ```
    *   **Install Frontend Dependencies (only needed once or after package.json changes):**
        ```bash
        npm install
        ```
    *   **Ensure your `frontend/.env` file (if it exists) or the root `.env` is configured for local backend access (e.g., `VITE_API_BASE_URL=http://localhost:8000/api/v1`).**
    *   **Run the Frontend Development Server:**
        ```bash
        npm run dev
        ```
        The **Frontend** will be available at **http://localhost:5173** (or another port if 5173 is taken, Vite will show the correct number in the terminal).

---

### Running Tests

To ensure code quality and functionality, DocuGenius-AI includes unit tests. You can run them using `pytest`.

1. **Run the tests from the root `docugenius-ai` directory** (where `docugenius-ai/backend/` and `docugenius-ai/frontend/` are located):
    *   **On Windows using PowerShell:**
        ```powershell
        # From the docugenius-ai root directory (not the backend subdirectory)
        $env:PYTHONPATH = ".\backend"; python -m pytest .\backend\tests\unit\test_core\test_models\
        ```
    *   **On Windows using Command Prompt (cmd):**
        ```cmd
        # From the docugenius-ai root directory (not the backend subdirectory)
        set PYTHONPATH=.\\backend && python -m pytest .\\backend\\tests\\unit\\test_core\\test_models\\
        ```
    *   **On macOS/Linux/WSL using Git Bash:**
        ```bash
        # From the docugenius-ai root directory (not the backend subdirectory)
        PYTHONPATH="./backend" python -m pytest ./backend/tests/unit/test_core/test_models/
        ```
    *   **Alternatively, if your environment is set up correctly (e.g., backend package installed in editable mode):**
        ```bash
        pytest backend/tests/unit/test_core/test_models/
        ```

This command will discover and run all unit tests located in the `backend/tests/unit/test_core/test_models/` directory.

---

> ⚠ **Note**: This is a focused, production-grade reference implementation for document generation—not a full SaaS. It demonstrates how Clean Architecture and modern Python & React practices can deliver real business value.

---

**DocuGeniusAI: Because creating documents shouldn't be a bottleneck.**

---

## 👤 Maintained By
This project is developed and maintained by **FM ByteShift Software**

**Fernando Magalhães**  
CEO – FM ByteShift Software  
📞 (21) 97250-1546  
✉️ [contact@fmbyteshiftsoftware.com](mailto:contact@fmbyteshiftsoftware.com)  
🌐 [fmbyteshiftsoftware.com](https://fmbyteshiftsoftware.com)  
🏢 CNPJ: 62.145.022/0001-05 (Brazil)
