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

## PREVIEW : 
<img width="672" alt="Screenshot 2025-07-08 000224" src="https://github.com/user-attachments/assets/a6344179-d7e2-46f1-8c09-ff9a80543086" />
<img width="947" alt="Screenshot 2025-07-08 000340" src="https://github.com/user-attachments/assets/06c415a5-503c-46fd-ba6c-0dbebf134df4" />
<img width="957" alt="Screenshot 2025-07-08 000453" src="https://github.com/user-attachments/assets/ad4a9a50-9d61-4fa9-b55b-c672753716a4" />
<img width="947" alt="Screenshot 2025-07-08 000521" src="https://github.com/user-attachments/assets/fab295f4-9c0f-4ccd-a0c2-41f03e0bce0f" />
<img width="946" alt="Screenshot 2025-07-08 000545" src="https://github.com/user-attachments/assets/da40b5e4-eb37-48cf-bd43-7c915c976088" />
<img width="953" alt="Screenshot 2025-07-08 000602" src="https://github.com/user-attachments/assets/ed389e38-4640-40dc-9f88-6994d9b8d0f6" />
<img width="947" alt="Screenshot 2025-07-08 000619" src="https://github.com/user-attachments/assets/afbefa5c-5d5b-4712-ac20-a108e2c82dc3" />
<img width="946" alt="Screenshot 2025-07-08 000640" src="https://github.com/user-attachments/assets/97809947-1673-4e2e-bcd0-5374bee9a0bf" />
<img width="950" alt="Screenshot 2025-07-08 000656" src="https://github.com/user-attachments/assets/192f553a-4e4b-4d0c-8dfc-9bfbfad3646b" />
<img width="950" alt="Screenshot 2025-07-08 000731" src="https://github.com/user-attachments/assets/fa66dc05-d49e-4f5a-a107-c9b57a53ab1e" />
<img width="947" alt="Screenshot 2025-07-08 000759" src="https://github.com/user-attachments/assets/36383cff-5ffa-477c-b46b-6478952b8708" />
<img width="949" alt="Screenshot 2025-07-08 001114" src="https://github.com/user-attachments/assets/fa22b810-1aab-42b0-8dbd-276c2f8f1d7b" />
<img width="945" alt="Screenshot 2025-07-08 001125" src="https://github.com/user-attachments/assets/478ef384-25b7-49c2-b024-8042ba805378" />
<img width="946" alt="Screenshot 2025-07-08 001145" src="https://github.com/user-attachments/assets/f4f3c228-052c-41e2-a0f2-9e00da1e1b2a" />
<img width="944" alt="Screenshot 2025-07-08 001201" src="https://github.com/user-attachments/assets/0121339a-644e-41e0-b230-0e08dd8e6717" />
<img width="944" alt="Screenshot 2025-07-08 001412" src="https://github.com/user-attachments/assets/b25d542d-07aa-4084-a3f3-16a80cb70bac" />
<img width="668" alt="Screenshot 2025-07-08 001436" src="https://github.com/user-attachments/assets/fbfde79a-98ed-4fad-9253-1d4ee0b44750" />
<img width="662" alt="Screenshot 2025-07-08 001501" src="https://github.com/user-attachments/assets/f04658db-453a-4e41-bf6c-ff06ffc6eb82" />
<img width="715" alt="Screenshot 2025-07-08 001511" src="https://github.com/user-attachments/assets/983adde7-2891-4e1d-a26d-d060e000eeed" />
<img width="777" alt="Screenshot 2025-07-08 001530" src="https://github.com/user-attachments/assets/642d8056-3b87-47d7-8047-b460ef6bf8a5" />
<img width="737" alt="Screenshot 2025-07-08 001544" src="https://github.com/user-attachments/assets/46fb2b2c-a312-4d84-87c9-d06425fad03a" />
<img width="755" alt="Screenshot 2025-07-08 001612" src="https://github.com/user-attachments/assets/93382188-5707-48b6-b6bf-23d31ce39971" />
<img width="673" alt="Screenshot 2025-07-08 001621" src="https://github.com/user-attachments/assets/096d5993-a2d3-4fbf-ae66-c169a225646c" />
<img width="673" alt="Screenshot 2025-07-08 001646" src="https://github.com/user-attachments/assets/0cbf1ad3-ccee-44b4-b24e-9dd95845caf3" />
<img width="860" alt="Screenshot 2025-07-08 001707" src="https://github.com/user-attachments/assets/0ea31927-d792-4de5-b549-c88d0cfd978a" />
<img width="741" alt="Screenshot 2025-07-08 001725" src="https://github.com/user-attachments/assets/a484211a-27e8-4536-b4a3-b746edf33368" />
<img width="707" alt="Screenshot 2025-07-08 001744" src="https://github.com/user-attachments/assets/655ff765-2c16-46e6-8807-c4ef3b4b4958" />
<img width="686" alt="Screenshot 2025-07-08 001802" src="https://github.com/user-attachments/assets/df6c7d35-1bca-4395-95fa-5125dd6686e7" />
<img width="680" alt="Screenshot 2025-07-08 001822" src="https://github.com/user-attachments/assets/49cba07b-4cbf-4113-8823-09d0ca9e98f2" />
<img width="767" alt="Screenshot 2025-07-08 001840" src="https://github.com/user-attachments/assets/8396a523-7873-4714-9cc5-6ed4096f4cda" />
<img width="652" alt="Screenshot 2025-07-08 001849" src="https://github.com/user-attachments/assets/8fd0d2e5-e65b-47c1-b160-e86b2fcc1f3a" />











