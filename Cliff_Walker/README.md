# 🧠 Cliff Walking with Q-Learning

This repository contains a Q-learning agent implementation for solving the **Cliff Walking problem**, a classic example in reinforcement learning. The environment challenges the agent to learn an optimal path from a start point to a goal while avoiding the "cliff" — high-penalty states that reset progress.

The project demonstrates value-based learning, exploration vs exploitation, and convergence behavior in a discrete, stochastic gridworld.

Check out some of the supporting files or a youtube file to get more of a sense what the cliffwalker game is

---

## 🎯 Objectives

- Learn an optimal policy using Q-learning
- Explore trade-offs between exploration rate (ε), learning rate (α), and discount factor (γ)
- Visualize agent behavior, reward progression, and Q-table convergence

---

## 🗺️ Environment Overview

- Gridworld of size **4×12**
- Start at bottom-left corner (S), goal at bottom-right (G)
- The "cliff" lies between S and G along the bottom row
- If the agent steps into the cliff, it receives a **large negative reward** and returns to the start
