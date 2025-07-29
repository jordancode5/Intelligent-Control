import pygame
import numpy as np
import csv
import random

# ---------------------- Pendulum Dynamics ----------------------
class InvertedPendulum:
    def __init__(self, m=0.2, M=0.5, l=0.3, b=0.1, g=9.81, dt=0.01):
        self.m = m
        self.M = M
        self.l = l
        self.b = b
        self.g = g
        self.dt = dt
        self.state = np.zeros(4)  # [x, x_dot, theta, theta_dot]

    def reset(self, state=None):
        if state is None:
            self.state = np.zeros(4)
        else:
            self.state = np.array(state, dtype=float)
        return self.state.copy()

    def step(self, u):
        x, x_dot, theta, theta_dot = self.state
        m, M, l, b, g, dt = self.m, self.M, self.l, self.b, self.g, self.dt

        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        total_mass = m + M

        temp = (u + m * l * theta_dot ** 2 * sin_theta - b * x_dot) / total_mass
        theta_acc = (g * sin_theta - cos_theta * temp) / (l * (4/3 - m * cos_theta ** 2 / total_mass))
        x_acc = temp - m * l * theta_acc * cos_theta / total_mass

        x_dot += x_acc * dt
        x += x_dot * dt
        theta_dot += theta_acc * dt
        theta += theta_dot * dt

        self.state = np.array([x, x_dot, theta, theta_dot])
        return self.state

    def get_state(self):
        return self.state.copy()

# ---------------------- Q-learning Setup ----------------------
x_bins = np.linspace(-2.4, 2.4, 10)
x_dot_bins = np.linspace(-3.0, 3.0, 10)
theta_bins = np.linspace(-np.pi, np.pi, 20)
theta_dot_bins = np.linspace(-4.0, 4.0, 10)
actions = [-10.0, 0.0, 10.0]

def discretize(state):
    x, x_dot, theta, theta_dot = state
    bins = [x_bins, x_dot_bins, theta_bins, theta_dot_bins]
    indices = []
    for val, b in zip([x, x_dot, theta, theta_dot], bins):
        idx = np.digitize(val, b) - 1
        idx = np.clip(idx, 0, len(b) - 1)
        indices.append(idx)
    return tuple(indices)

def reward_function(state):
    x, x_dot, theta, theta_dot = state

    # Quadratic penalties (harshly punishes further deviation)
    theta_penalty = (theta)**2
    theta_dot_penalty = 0.1 * (theta_dot)**2
    x_penalty = 0.05 * (x)**2
    x_dot_penalty = 0.01 * (x_dot)**2

    # Total reward: high when upright and centered, sharply negative when off
    reward = - (theta_penalty + theta_dot_penalty + x_penalty + x_dot_penalty)

    # Optional: bonus if very close to upright
    if abs(theta) < 0.1 and abs(theta_dot) < 0.5 and abs(x) < 0.2:
        reward += 5

    return reward

# def reward_function(state):
#     upright_bonus = 1.0 - abs(state[2]) / np.pi  # 1 when upright, 0 when upside-down
#     centered_bonus = 1.0 - abs(state[0]) / 2.4   # centered on track
#     return upright_bonus + 0.1 * centered_bonus

# def reward_function(state):
#     return - (abs(state[0]) + abs(state[1]) + abs(state[2]) + abs(state[3]))

# ---------------------- Q-learning Training Loop ----------------------
episodes = 2000
alpha_max = 0.125
alpha = alpha_max
gamma = 0.99
epsilon_max = 0.2
epsilon_i = epsilon_max
Q = np.zeros((len(x_bins), len(x_dot_bins), len(theta_bins), len(theta_dot_bins), len(actions)))
sim = InvertedPendulum()

for episode in range(episodes):
    sim.reset([0, 0, 0.05, 0])
    epsilon_i = epsilon_max - (episode/episodes) * epsilon_max + 0.01
    alpha = alpha_max - (episode/episodes) * alpha_max + 0.05
    # epsilon *= 0.995
    print("Epsilon =", epsilon_i, "Alpha =", alpha)
    for t in range(500):
        state = sim.get_state()
        s = discretize(state)

        if random.random() < epsilon_i:
            action_idx = random.randint(0, len(actions) - 1)
        else:
            action_idx = np.argmax(Q[s])

        u = actions[action_idx]
        next_state = sim.step(u)
        ns = discretize(next_state)
        r = reward_function(next_state)

        Q[s][action_idx] = (1 - alpha) * Q[s][action_idx] + alpha * (r + gamma * np.max(Q[ns]))
        
        if abs(next_state[0]) > 2.4 or abs(next_state[2]) > np.pi / 2:
            break

# ---------------------- Save Q-table to CSV ----------------------
with open("q_table.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    for index, q_vals in np.ndenumerate(Q[..., 0]):
        q_list = [Q[index][a] for a in range(len(actions))]
        writer.writerow(list(index) + q_list)

# ---------------------- Pygame Visualization ----------------------
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Inverted Pendulum")
clock = pygame.time.Clock()
pixels_per_meter = 80
cart_w, cart_h = 60, 30
pendulum_length = 1.0

sim.reset([0, 0, 0.05, 0])
running = True
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = sim.get_state()
    s = discretize(state)
    action_idx = np.argmax(Q[s])
    u = actions[action_idx]
    sim.step(u)

    x_cart = state[0]
    phi = state[2]

    cart_x_screen = int(WIDTH // 2 + x_cart * pixels_per_meter)
    cart_y_screen = HEIGHT // 2
    pygame.draw.line(screen, (0, 0, 0), (0, cart_y_screen), (WIDTH, cart_y_screen), 2)

    pygame.draw.rect(screen, (0, 100, 200),
                     pygame.Rect(int(cart_x_screen - cart_w // 2),
                                 int(cart_y_screen - cart_h // 2),
                                 cart_w, cart_h))

    pend_x = x_cart + pendulum_length * np.sin(phi)
    pend_y = -pendulum_length * np.cos(phi)
    pend_x_screen = int(WIDTH // 2 + pend_x * pixels_per_meter)
    pend_y_screen = int(cart_y_screen + pend_y * pixels_per_meter)

    pygame.draw.line(screen, (200, 0, 0), (cart_x_screen, cart_y_screen), (pend_x_screen, pend_y_screen), 4)
    pygame.draw.circle(screen, (0, 0, 0), (pend_x_screen, pend_y_screen), 5)

    pygame.display.flip()

pygame.quit()