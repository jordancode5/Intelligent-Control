# ⚙️ Force Prediction on a Mass-Spring-Damper System

This project focuses on building a predictive model for estimating the **external force acting on a mass-spring-damper (MSD) system** using time-series data from the system's motion. This problem is fundamental to control theory, signal estimation, and system identification — and forms the basis for real-world applications in robotics, mechanical systems, and adaptive control.

## 🎯 Objective

Predict the **unknown input force** based on system responses such as:
- Displacement
- Velocity
- Acceleration

This inverse problem is tackled using **machine learning** and/or **observer-based estimation**, depending on the configuration.

---

## 📂 Project Structure

```bash
📁 Mass_Spring_Damper/
├── mass_spring_damper.ipynb            # Simulates MSD system and compares trained values to real (simulated) force values
