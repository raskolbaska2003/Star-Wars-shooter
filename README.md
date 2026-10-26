# Star Wars Shooter

A Star Wars-inspired 2D shooter built with Python and Pygame. Aim with the mouse, dodge enemy fire, defeat bosses, and collect temporary power-ups.

## Features

- Mouse aiming and keyboard movement.
- Bosses with random health and projectile attacks.
- Triple-shot and support-drone power-ups.
- A radial projectile attack and teleport ability.
- Particle effects when a boss is defeated.
- Survival timer, defeated-boss counter, and final score.
- Window dimensions based on the desktop resolution.

## Setup and run

Use Python 3.11 and Pygame 2.5.2. From the project directory:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the dependency and launch the game:

```bash
python -m pip install -r requirements.txt
python main.py
```

Run from the project directory because image paths are relative to it. A graphical desktop is required.

## Controls

| Input | Action |
| --- | --- |
| W / A / S / D | Move |
| Mouse | Aim |
| Hold left mouse button | Shoot |
| Space | Teleport to the cursor |
| G | Emit projectiles from the cursor toward the screen edges |
| Close the window | Exit |

## Gameplay

Enemy bullets end the current round on contact. After the game-over screen, another round starts automatically. The score is elapsed survival time multiplied by the number of defeated bosses, rounded down.

Bosses can drop a power-up when no other power-up is active or waiting on the map. Blue pickups activate support drones; cyan pickups activate triple shot. Collected power-ups last 20 seconds. The first round starts with five seconds of support-drone assistance.

A boss can take damage only while the player is within its attack range; red health text indicates that it can be damaged, while gray text indicates that the player is too far away.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Game loop, controls, collisions, rendering, and round handling |
| `Values.py` | Display setup, settings, and initial game state |
| `Player.py` | Player movement and shooting |
| `Boss.py` | Boss state and shooting |
| `Bullet.py` | Projectile movement and drawing |
| `Bonus.py` | Power-up generation and duration |
| `Particles.py` | Explosion particle effects |
| `test.py` | Standalone rotation experiment, not an automated test suite |

Keep the image files alongside the Python files.

## Current limitations

This is a learning project. Projectile creation does not yet handle identical start and target positions. Some lists are modified during iteration, which can cause elements to be skipped. The boss-spawn distance check can also keep searching indefinitely on a small display if no valid position is available.

## Artwork

The project includes Star Wars-themed images. Their source and licensing are not documented in this repository; no ownership or redistribution rights for third-party artwork are claimed here.
