# DocuGeniusAI: AI-Driven Document Engineering Platform

> [!WARNING]
> **Under Construction** > This application is currently under development.

**DocuGeniusAI** is a professional-grade platform designed to bridge the gap between unstructured business descriptions and structured document lifecycles. It leverages Large Language Models (LLMs) to dynamically architect business requirements into database-backed entities and production-ready documents.

---

## The Core Engineering Concept

Unlike generic AI chat interfaces, DocuGeniusAI treats AI as a **Schema Architect**. The system follows a rigorous three-stage pipeline:

1. **Discovery & Schema Generation:** The AI analyzes a business description and proposes a structured list of `Document Types`. These are not just text; they are entities to be managed and persisted.
2. **Dynamic Form Mapping:** For a selected document type, the AI generates essential data fields. These fields are automatically mapped to validated HTML tags (e.g., date, select, text) and stored as a relational schema.
3. **Final Generation:** A high-fidelity document is generated based on the previously defined and populated schema, ensuring consistency and business alignment.

## Tech Stack & Implementation Details

The project is built with a focus on **asynchronous performance**, **type safety**, and **domain-driven design**:

* **Core Framework:** `FastAPI` with `Uvicorn` for high-performance, asynchronous API execution.
* **Data Integrity:** `Pydantic v2` for strict schema validation and `pydantic[email]` for robust identity verification.
* **Database & ORM:** `SQLAlchemy 2.0` (Modern 2.0 style) using `aiomysql` for fully asynchronous database operations.
* **AI Integration:** Dual integration via `huggingface_hub` and `openai` (v2.9.0) to ensure flexibility in LLM orchestration.
* **Security:** `bcrypt` for secure credential hashing and `python-dotenv` for environment-based configuration management.

## Architectural Highlights

* **Asynchronous First:** Every layer, from API entry points to database persistence, is designed to be non-blocking.
* **Strict Typing:** Deep integration of Pydantic models to bridge the gap between AI-generated JSON and Relational Database records.
* **Zero Hallucination Pipeline:** AI outputs are treated as "proposals" that pass through a validation layer before becoming persistent business entities.
* **RBAC Ready:** Separate Administrative and User environments built to handle secure document lifecycles.

---

## 👤 Maintained By

This project is developed and maintained by **Fernando Antunes de Magalhães Desenvolvimento de Software Ltda.**

**Fernando Magalhães** CEO – FM ByteShift Software

📞 (21) 97250-1546

✉️ [contact@fmbyteshiftsoftware.com](mailto:contact@fmbyteshiftsoftware.com)

🌐 [fmbyteshiftsoftware.com](https://fmbyteshiftsoftware.com)

🏢 CNPJ: 62.145.022/0001-05 (Brazil)

