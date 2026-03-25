import numpy as np
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ------------------------
# Quantum Setup
# ------------------------

qc = QuantumCircuit(1)
states = [Statevector.from_label('0')]

# ------------------------
# Tkinter Setup
# ------------------------

root = tk.Tk()
root.title("Quantum Glasses - Smooth Bloch Simulator")
root.geometry("600x700")

background = "#091413"

# Display
display_frame = tk.Frame(root, bg=background)
display_frame.pack(fill="x")

display = tk.Entry(
    display_frame,
    font=("Arial", 18),
    bg=background,
    fg="white",
    justify="left"
)
display.pack(fill="x", padx=5, pady=5)

# Visualization Frame
visual_frame = tk.Frame(root)
visual_frame.pack(fill="both", expand=True)

# Matplotlib Figure (ONLY ONE)
fig = plt.figure(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=visual_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# ------------------------
# Bloch Drawing (SMOOTH)
# ------------------------

def draw_bloch(state):
    fig.clf()
    ax = fig.add_subplot(111, projection='3d')

    vec = state.data
    alpha = vec[0]
    beta = vec[1]

    # Bloch vector
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.abs(alpha)**2 - np.abs(beta)**2

    # Sphere (SOLID + CLEAR)
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    xs = np.cos(u) * np.sin(v)
    ys = np.sin(u) * np.sin(v)
    zs = np.cos(v)

    ax.plot_surface(xs, ys, zs, alpha=0.15)  # soft solid sphere
    ax.plot_wireframe(xs, ys, zs, linewidth=0.5)  # grid

    # Axis lines
    ax.quiver(0, 0, 0, 1, 0, 0)  # X
    ax.quiver(0, 0, 0, 0, 1, 0)  # Y
    ax.quiver(0, 0, 0, 0, 0, 1)  # Z

    # Labels
    ax.text(1.2, 0, 0, "X")
    ax.text(0, 1.2, 0, "Y")
    ax.text(0, 0, 1.2, "Z")

    # State vector (BOLD)
    ax.quiver(0, 0, 0, x, y, z, linewidth=3)

    # Limits
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    # Clean look
    ax.set_box_aspect([1,1,1])
    ax.set_axis_off()

    ax.set_title("Bloch Sphere", fontsize=14)

    canvas.draw()
# ------------------------
# Animation
# ------------------------

def animate_transition(state1, state2, steps=25):
    vec1 = state1.data
    vec2 = state2.data

    def update_frame(i):
        t = i / steps
        interp = (1 - t) * vec1 + t * vec2
        interp = interp / np.linalg.norm(interp)

        temp_state = Statevector(interp)

        draw_bloch(temp_state)

        if i < steps:
            root.after(15, update_frame, i + 1)

    update_frame(0)

# ------------------------
# Gate Logic
# ------------------------

def apply_gate(gate_name):
    global qc, states
# go thourh vector x to state
    if gate_name == "x":
        qc.x(0)
# go thourh vector y to state
    elif gate_name == "y":
        qc.y(0)
    elif gate_name == "z":
        qc.z(0)
    elif gate_name == "h":
        qc.h(0)
# 90' with vector x , y
    elif gate_name == "rx":
        qc.rx(pi/2, 0)
    elif gate_name == "ry":
        qc.ry(pi/2, 0)
    elif gate_name == "rz":
        qc.rz(pi/2, 0)

    elif gate_name == "s":
        qc.s(0)
    elif gate_name == "sd":
        qc.sdg(0)

    elif gate_name == "t":
        qc.t(0)
    elif gate_name == "td":
        qc.tdg(0)

    # Save state
    state = Statevector.from_instruction(qc)
    states.append(state)

    # Display
    display.insert(tk.END, gate_name.upper() + " ")

    # Animate transition
    animate_transition(states[-2], states[-1])

    print(f"Applied: {gate_name.upper()}")

# ------------------------
# Controls
# ------------------------

def clear():
    global qc, states
    qc = QuantumCircuit(1)
    states = [Statevector.from_label('0')]
    display.delete(0, tk.END)
    draw_bloch(states[0])

def quit_app():
    root.destroy()

# ------------------------
# Buttons
# ------------------------

button_frame = tk.Frame(root)
button_frame.pack(fill="both", expand=True)

for i in range(4):
    button_frame.rowconfigure(i, weight=1)

for j in range(3):
    button_frame.columnconfigure(j, weight=1)

btn_style = {"bg": "#285A48", "fg": "white", "font": ("Arial", 12)}

buttons = [
    ("X", "x"), ("Y", "y"), ("Z", "z"),
    ("RX", "rx"), ("RY", "ry"), ("RZ", "rz"),
    ("S", "s"), ("SD", "sd"), ("H", "h"),
    ("T", "t"), ("TD", "td")
]

row, col = 0, 0
for text, gate in buttons:
    tk.Button(
        button_frame,
        text=text,
        command=lambda g=gate: apply_gate(g),
        **btn_style
    ).grid(row=row, column=col, sticky="nsew")

    col += 1
    if col == 3:
        col = 0
        row += 1

# Controls
tk.Button(root, text="Clear", command=clear, bg="orange").pack(fill="x")
tk.Button(root, text="Quit", command=quit_app, bg="red", fg="white").pack(fill="x")

# Initial draw
draw_bloch(states[0])

# Run
root.mainloop()