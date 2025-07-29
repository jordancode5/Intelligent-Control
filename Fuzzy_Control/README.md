# 🤖 Fuzzy_Rover: Obstacle-Avoiding Goal-Seeking Navigation with Fuzzy Logic

This project implements a fuzzy logic-based navigation system for a 2D autonomous rover operating in an environment with static and/or dynamic obstacles. The rover intelligently balances **goal-seeking** and **obstacle avoidance** behaviors to reach its target while navigating uncertain environments — all without hardcoded rules or optimal planning algorithms.

---

## 🎯 Project Objective

To design a fuzzy inference system (FIS) that drives a simulated rover from a start position to a defined goal while avoiding obstacles, based solely on sensor-like inputs (e.g., distances and angles).

---

## 🧠 Key Features

- 🚗 **Fuzzy logic controller** for steering and movement decisions  
- 📡 **Sensor-inspired input model** using relative angle and obstacle distance  
- 🧭 Continuous position and heading updates  
- 🎯 Goal-directed motion  
- ⛔ Dynamic obstacle proximity response  
- 🎥 **GIF animation** of the rover's full path over time

---

## 🗺️ Environment Setup

- 2D Cartesian plane
- Static goal position
- Initial rover position and heading
- Obstacles randomly placed or manually defined

---

## 📂 Project Structure

```bash
📁 Fuzzy_Rover/
├── fuzzy_navigation.ipynb         # Main simulation and fuzzy controller
├── robot_navigation.gif              # GIF output of the simulation run
├── README.md
