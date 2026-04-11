"""tkinter GUI: canvas renderer and parameter controls."""

import tkinter as tk
from ecosystem import Ecosystem
from organisms import Sheep, Wolf

# ── colour palette ─────────────────────────────────────────────────────────────

CELL = {
    "empty": "#000000",
    "grass": "#28BC79",
    "sheep": "#E8E8D0",
    "wolf":  "#CCA403",
}
_BG     = "#000000"
_PANEL  = "#000000"
_FG     = "#CBD5E0"
_ACC    = "#A0C4FF"
_MONO   = ("Consolas", 9)
_MONO_B = ("Consolas", 9, "bold")


# ── main application window ────────────────────────────────────────────────────

class EcosystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ecosystem Simulator")
        self.configure(bg=_BG)
        self.resizable(False, False)

        self.eco     = None
        self.running = False
        self._job    = None
        self._items  = []   # canvas rect ids [y][x]

        self._build()

    # ── layout ─────────────────────────────────────────────────────────────────

    def _build(self):
        cf = tk.Frame(self, bg=_BG)
        cf.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        self.canvas = tk.Canvas(cf, bg=CELL["empty"], highlightthickness=0,
                                width=600, height=500)
        self.canvas.pack()

        panel = tk.Frame(self, bg=_PANEL, padx=10, pady=8)
        panel.grid(row=0, column=1, sticky="ns", padx=(0, 6), pady=6)
        self._fill_panel(panel)

    def _sep(self, p):
        tk.Frame(p, bg="#2A3F5F", height=1).pack(fill="x", pady=5)

    def _section(self, p, title):
        tk.Label(p, text=title, bg=_PANEL, fg=_ACC,
                 font=_MONO_B, anchor="w").pack(fill="x", pady=(4, 1))

    def _spin_row(self, p, label, var, lo, hi, step=1):
        row = tk.Frame(p, bg=_PANEL)
        row.pack(fill="x", pady=1)
        tk.Label(row, text=label, bg=_PANEL, fg=_FG, font=_MONO,
                 width=26, anchor="w").pack(side="left")
        tk.Spinbox(row, from_=lo, to=hi, increment=step, textvariable=var,
                   width=7, bg="#0F3460", fg="#E2E8F0",
                   insertbackground="white", font=_MONO, relief="flat").pack(side="left")

    def _fill_panel(self, p):
        tk.Label(p, text="ECOSYSTEM SIMULATOR", bg=_PANEL, fg=_ACC,
                 font=("Consolas", 11, "bold"), anchor="w").pack(fill="x")
        tk.Label(p, text="Grass · Sheep · Wolf",
                 bg=_PANEL, fg="#5A7FA0", font=_MONO, anchor="w").pack(fill="x")
        self._sep(p)

        self.v = {
            "seed":         tk.IntVar(value=42),
            "gw":           tk.IntVar(value=60),
            "gh":           tk.IntVar(value=50),
            "grass_pct":    tk.IntVar(value=40),
            "n_sheep":      tk.IntVar(value=60),
            "n_wolves":     tk.IntVar(value=10),
            "grass_rate":   tk.DoubleVar(value=0.05),
            "grass_energy": tk.IntVar(value=5),
            "sheep_e":      tk.IntVar(value=20),
            "sheep_repr":   tk.IntVar(value=100),
            "wolf_e":       tk.IntVar(value=15),
            "wolf_repr":    tk.IntVar(value=500),
            "wolf_sheep_e": tk.IntVar(value=10),
            "speed":        tk.IntVar(value=15),
        }

        self._section(p, "Reproducibility")
        self._spin_row(p, "random seed", self.v["seed"], 0, 99999)

        self._section(p, "Grid")
        self._spin_row(p, "width",  self.v["gw"],  10, 150)
        self._spin_row(p, "height", self.v["gh"],  10, 100)

        self._section(p, "Initial population")
        self._spin_row(p, "grass coverage %", self.v["grass_pct"], 0, 95)
        self._spin_row(p, "sheep",             self.v["n_sheep"],  0, 500)
        self._spin_row(p, "wolves",            self.v["n_wolves"], 0, 200)

        self._section(p, "Grass")
        self._spin_row(p, "growth rate / cell / step", self.v["grass_rate"],  0.001, 1.0, 0.001)
        self._spin_row(p, "energy given to sheep",     self.v["grass_energy"], 1, 100)

        self._section(p, "Sheep")
        self._spin_row(p, "initial energy",        self.v["sheep_e"],    1, 200)
        self._spin_row(p, "reproduction threshold", self.v["sheep_repr"], 2, 300)

        self._section(p, "Wolf")
        self._spin_row(p, "initial energy",          self.v["wolf_e"],      1, 200)
        self._spin_row(p, "reproduction threshold",  self.v["wolf_repr"],   2, 300)
        self._spin_row(p, "energy from eating sheep", self.v["wolf_sheep_e"], 1, 200)

        self._section(p, "Simulation speed")
        self._spin_row(p, "steps / second", self.v["speed"], 1, 120)

        self._sep(p)

        bf = tk.Frame(p, bg=_PANEL)
        bf.pack(fill="x", pady=(0, 4))
        kw = dict(font=_MONO_B, relief="flat", padx=6, pady=5, cursor="hand2", bd=0)
        self.btn_run   = tk.Button(bf, text="▶  Start",  bg="#2D6A4F", fg="white",
                                   command=self._start, **kw)
        self.btn_pause = tk.Button(bf, text="⏸  Pause",  bg="#4A4E69", fg="white",
                                   command=self._pause, state="disabled", **kw)
        self.btn_reset = tk.Button(bf, text="↺  Reset",  bg="#7B2D2D", fg="white",
                                   command=self._reset, **kw)
        for b in (self.btn_run, self.btn_pause, self.btn_reset):
            b.pack(side="left", padx=2, expand=True, fill="x")

        self._sep(p)

        self._section(p, "Stats")
        self.sv_step   = tk.StringVar(value="step:    0")
        self.sv_grass  = tk.StringVar(value="grass:   0")
        self.sv_sheep  = tk.StringVar(value="sheep:   0")
        self.sv_wolves = tk.StringVar(value="wolves:  0")

        # step row (no swatch)
        tk.Label(p, textvariable=self.sv_step, bg=_PANEL, fg=_FG,
                 font=_MONO, anchor="w").pack(fill="x")

        for cell_key, var, fg in (
            ("grass", self.sv_grass,  CELL["grass"]),
            ("sheep", self.sv_sheep,  CELL["sheep"]),
            ("wolf",  self.sv_wolves, CELL["wolf"]),
        ):
            row = tk.Frame(p, bg=_PANEL)
            row.pack(fill="x", pady=1)
            tk.Label(row, bg=CELL[cell_key], width=2, relief="flat").pack(side="left", padx=(0, 5))
            tk.Label(row, textvariable=var, bg=_PANEL, fg=fg,
                     font=_MONO, anchor="w").pack(side="left")

    # ── simulation control ─────────────────────────────────────────────────────

    def _get_cfg(self):
        v = self.v
        return {
            "seed":             v["seed"].get(),
            "grid_w":           v["gw"].get(),
            "grid_h":           v["gh"].get(),
            "grass_pct":        v["grass_pct"].get(),
            "n_sheep":          v["n_sheep"].get(),
            "n_wolves":         v["n_wolves"].get(),
            "grass_rate":       v["grass_rate"].get(),
            "grass_energy":     v["grass_energy"].get(),
            "sheep_energy":     v["sheep_e"].get(),
            "sheep_repr":       v["sheep_repr"].get(),
            "wolf_energy":      v["wolf_e"].get(),
            "wolf_repr":        v["wolf_repr"].get(),
            "sheep_energy_val": v["wolf_sheep_e"].get(),
        }

    def _init_canvas(self, gw, gh):
        cell = max(3, min(14, 700 // max(gw, gh)))
        self._cell = cell
        self.canvas.config(width=gw * cell, height=gh * cell)
        self.canvas.delete("all")
        self._items = []
        for y in range(gh):
            row = []
            for x in range(gw):
                item = self.canvas.create_rectangle(
                    x * cell, y * cell,
                    x * cell + cell, y * cell + cell,
                    fill=CELL["empty"], outline="", width=0,
                )
                row.append(item)
            self._items.append(row)

    def _start(self):
        cfg = self._get_cfg()
        self._init_canvas(cfg["grid_w"], cfg["grid_h"])
        self.eco     = Ecosystem(cfg)
        self.running = True
        self.btn_run.config(state="disabled")
        self.btn_pause.config(state="normal", text="⏸  Pause")
        self._schedule()

    def _pause(self):
        if self.running:
            self.running = False
            self.btn_pause.config(text="▶  Resume")
            if self._job:
                self.after_cancel(self._job)
                self._job = None
        else:
            self.running = True
            self.btn_pause.config(text="⏸  Pause")
            self._schedule()

    def _reset(self):
        self.running = False
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.eco     = None
        self._items  = []
        self.canvas.delete("all")
        self.canvas.config(width=600, height=500)
        self.btn_run.config(state="normal")
        self.btn_pause.config(state="disabled", text="⏸  Pause")
        self.sv_step.set("step:    0")
        self.sv_grass.set("grass:   0")
        self.sv_sheep.set("sheep:   0")
        self.sv_wolves.set("wolves:  0")

    def _schedule(self):
        if not self.running:
            return
        delay     = max(16, 1000 // self.v["speed"].get())
        self._job = self.after(delay, self._tick)

    def _tick(self):
        if not self.running or not self.eco:
            return
        self.eco.step()
        self._render()
        self._schedule()

    def _render(self):
        eco   = self.eco
        items = self._items
        for x, y, has_grass, animal in eco.grid.iter_cells():
            if isinstance(animal, Wolf):
                c = CELL["wolf"]
            elif isinstance(animal, Sheep):
                c = CELL["sheep"]
            elif has_grass:
                c = CELL["grass"]
            else:
                c = CELL["empty"]
            self.canvas.itemconfig(items[y][x], fill=c)

        g, s, w = eco.counts()
        self.sv_step.set(  f"step:    {eco.step_count}")
        self.sv_grass.set( f"grass:   {g}")
        self.sv_sheep.set( f"sheep:   {s}")
        self.sv_wolves.set(f"wolves:  {w}")
