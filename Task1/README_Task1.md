 Task 1 — Ecosystem Simulator

An agent-based predator-prey simulation demonstrating OOP concepts in Python, with a tkinter GUI.

---

## How to Run

**Requirements:** Python 3.11 or later

```bash
# run the simulator
python main.py
```

Adjust parameters in the control panel on the right side of the window, then press **Start**. Press **Pause** to suspend the simulation without losing state. Press **Reset** to return all parameters to their defaults and clear the canvas.

---

## Module Structure

```
task1/
├── main.py        # entry point
├── app.py         # GUI (EcosystemApp, colour palette)
├── ecosystem.py   # simulation engine (Ecosystem)
├── grid.py        # spatial container (Grid)
├── organisms.py   # Plant, Sheep, Wolf
└── base.py        # abstract bases: Entity, Organism, Animal
```

The import direction is strictly one-way: `main` -> `app` -> `ecosystem` -> `grid` / `organisms` -> `base`. There are no circular imports.

---

## Parameters

| Section         | Parameter                 | Default | Effect                                          |
| --------------- | ------------------------- | ------- | ----------------------------------------------- |
| Reproducibility | random seed               | 42      | fixed seed for repeatable runs                  |
| Grid            | width                     | 60      | grid columns                                    |
| Grid            | height                    | 50      | grid rows                                       |
| Population      | grass coverage %          | 40      | initial grass density                           |
| Population      | sheep                     | 60      | initial sheep count                             |
| Population      | wolves                    | 10      | initial wolf count                              |
| Grass           | growth rate / cell / step | 0.05    | probability of regrowth per empty cell per step |
| Grass           | energy given to sheep     | 5       | energy restored when sheep eats grass           |
| Sheep           | initial energy            | 20      | starting energy                                 |
| Sheep           | reproduction threshold    | 100     | energy required to spawn offspring              |
| Wolf            | initial energy            | 15      | starting energy                                 |
| Wolf            | reproduction threshold    | 500     | energy required to spawn offspring              |
| Wolf            | energy from eating sheep  | 10      | energy restored when wolf kills sheep           |
| Speed           | steps / second            | 15      | simulation rate                                 |

## Presentation Video
https://youtu.be/uK9JV0BkDc4?si=TmrMItZSfTM2Tx6n
