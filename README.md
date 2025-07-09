# Themis – Human-Centered HR Intelligence System

**Themis** is an advanced HR management system engineered to go beyond standard data tracking. It is a fusion of structured database design, RESTful APIs, deep learning predictions, and practical interface logic — created to serve not just as a management tool, but as a decision-support system built on transparency, accountability, and human insight.

---

##  The Journey Behind Themis

Themis was born out of a core realization: modern HR systems often collect data but fail to understand it. This project started with the goal of transforming an HR system from a passive database into an active reasoning engine — one that predicts, explains, and adapts.

What began as a backend system handling salaries and attendance grew into a full-stack application with AI-driven insights, role-based access control, real-time behavioral monitoring, and predictive logic. It was never about writing code — it was about designing accountability.

---

##  System Architecture Overview

Themis is composed of three interconnected layers:

### 1.  Backend (FastAPI + SQLAlchemy)
- Modular routing system with controller-based architecture
- Role-based access (Employee, HR, Admin) using JWT token handling
- MySQL relational database with full normalization and foreign key integrity
- Core modules: Users, Payroll, Attendance, Benefits, Sick Notes, Appraisals, Raise Requests, Comments, News

### 2. AI Engine (TRACE Models + Custom Architectures)
- **Sentiment Score Prediction**: Dual-branch model (structured + text) for emotional analysis
- **Attrition Risk**: Predicts employee resignation probability (4-class)
- **Performance Score**: Predicts continuous performance levels
- **Benefit-to-Cost Ratio (BCR)**: Regression-based cost-efficiency analysis
- **Role Fitting**: Collaborative filtering + skill gap analyzer for department suitability

### 3.  Frontend (HTML/CSS/JS)
- Role-separated interfaces for Admin, HR, and Employee
- Real-time dashboards and modal-based interaction
- Modular forms for updates, raise requests, benefit assignment
- Visualization support (chart toggles, filterable tables)

---

##  Security & Design Patterns

- Password hashing (Bcrypt) and token management (JWT)
- Clean controller separation (business logic away from route calls)
- Core utilities and in a centralized `/core` layer
- Custom permissions, role enforcement, and user logging (dependencies)

---

##  AI Model Pipeline

Each prediction model is trained and integrated into FastAPI without loading it at startup — instead, models load on-demand for scalability and performance.

### Example Flow:

User Input → Preprocessing  
→ Transformer + Autoencoder OR LSTM → Latent Representation  
→ Fusion MLP → Softmax/Regression → Prediction

> All models are version-controlled and connected to the database via their own schemas and tables.

---

##  Why TRACE Architecture?

The **TRACE** model (Transformer-Reduced Autoencoder for Classification and Estimation) was developed to overcome the challenges of gradient instability, overfitting, and unstructured learning in HR data.

When extended to **TRACE++**, it allowed for multimodal inputs (e.g., behavioral logs + comments) to be processed together — improving prediction accuracy and real-world usability.

---

##  Modules Overview

| Module              | Purpose                                                | AI Support          |
|---------------------|--------------------------------------------------------|---------------------|
| Users               | Login, registration, token auth                        | ✅ Role-based logic |
| Attendance          | Live sheet + permanent history tracking                | ✅ Absence analysis |
| Payroll             | Fixed + dynamic payroll, raise requests                | ✅ Raise impact eval|
| Sick Notes          | Logging, status review, HR approval                    | ❌                  |
| Appraisals          | Periodic performance-based scoring                     | ✅ Performance input|
| Penalties           | Disciplinary log linked to payroll                     | ✅ Attrition factor |
| Benefits            | Catalog + per-user benefit mapping                     | ✅ Cost analysis     |
| Sentiment           | Emotional profile generation                           | ✅ Core sentiment model |
| AI Predictions      | 7 integrated prediction models                         | ✅ All               |

---

## 🚀 Key Features

- Dynamic attendance management with historical logging
- Raise requests linked directly to payroll
- Real-time sentiment tracking based on behavior and language
- Predictive dashboards for HR and Admin
- Fusion-based decision engine: behavioral + emotional + structural

---
