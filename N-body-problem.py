import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

class CelestialBody:
    def __init__(self, name, mass, position, velocity):
        self.name = name
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)

def calculate_force(body1, body2):
    r_vec = body2.position - body1.position
    r_mag = np.linalg.norm(r_vec)
    if r_mag > 0:
        f_mag = G * body1.mass * body2.mass / r_mag**2
        return f_mag * r_vec / r_mag
    else:
        return np.zeros(3)

def update_bodies(bodies, dt):
    for i in range(len(bodies)):
        total_force = np.zeros(3)
        for j in range(len(bodies)):
            if i != j:
                total_force += calculate_force(bodies[i], bodies[j])
        
        acceleration = total_force / bodies[i].mass
        bodies[i].velocity += acceleration * dt
        bodies[i].position += bodies[i].velocity * dt

# Simulation parameters
dt = 3600  # Time step in seconds (1 hour)
total_time = 31536000  # Total simulation time in seconds (1 year)

# Create celestial bodies
sun = CelestialBody("Sun", 1.989e30, [0, 0, 0], [0, 0, 0])
earth = CelestialBody("Earth", 5.972e24, [149.6e9, 0, 0], [0, 29.78e3, 0])

bodies = [sun, earth]

# Run simulation
positions = np.zeros((int(total_time/dt), len(bodies), 3))
for t in range(int(total_time/dt)):
    update_bodies(bodies, dt)
    for i, body in enumerate(bodies):
        positions[t, i] = body.position

# Plot results
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for i, body in enumerate(bodies):
    ax.plot(positions[:, i, 0], positions[:, i, 1], positions[:, i, 2], label=body.name)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
plt.legend()
plt.title('N-body Simulation')
plt.show()
