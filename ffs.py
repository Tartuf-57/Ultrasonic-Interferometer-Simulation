import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
 
# Constants
F0      = 2.0e6    # Hz
LAM0    = 0.75     # mm
RHO     = 996.458  # kg/m3
L       = 0.025    # m (25mm cell)
N       = 1000
 
x_m  = np.linspace(0, L, N)
x_mm = x_m * 1000
 
def get_params(f, lam_mm):
    lam = lam_mm * 1e-3
    v   = f * lam
    k   = 2 * np.pi / lam
    w   = 2 * np.pi * f
    b   = 1.0 / (RHO * v**2)
    return k, w, v, b
 
def get_markers(k):
    lam = 2 * np.pi / k
    anti_x = [(2*n+1)*lam/4 for n in range(int(L/(lam/4))+1) if (2*n+1)*lam/4 < L]
    node_x = [n*lam/2       for n in range(int(L/(lam/2))+1) if n*lam/2        < L]
    def snap(pts):
        return np.array([np.argmin(np.abs(x_m - p)) for p in pts], dtype=int)
    return (snap(anti_x) if anti_x else np.array([], dtype=int),
            snap(node_x) if node_x else np.array([], dtype=int))
 
# Figure
fig = plt.figure(figsize=(13, 9), facecolor="#0d0d1a")
fig.suptitle("Ultrasonic Interferometer", color="#ccccff", fontsize=14,
             fontweight="bold", y=0.995)
 
BG = "#10101e"
ax1 = fig.add_axes((0.06, 0.60, 0.78, 0.30), facecolor=BG)
ax2 = fig.add_axes((0.06, 0.31, 0.78, 0.20), facecolor=BG)
ax3 = fig.add_axes((0.06, 0.08, 0.42, 0.16), facecolor=BG)
ax4 = fig.add_axes((0.54, 0.08, 0.42, 0.16), facecolor=BG)
ax_sf = fig.add_axes((0.10, 0.045, 0.28, 0.018), facecolor="#1a1a30")
ax_sl = fig.add_axes((0.55, 0.045, 0.28, 0.018), facecolor="#1a1a30")
ax_bp = fig.add_axes((0.88, 0.038, 0.08, 0.032), facecolor="#1a1a30")
 
for ax in [ax1, ax2]:
    ax.tick_params(colors="#555577", labelsize=8)
    ax.grid(True, color="#1a1a33", lw=0.5, ls="--")
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a44")
 
for ax in [ax3, ax4]:
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_edgecolor("#2a2a44")
 
ax1.set_xlim(0, L*1000); ax1.set_ylim(-2.6, 2.6)
ax2.set_xlim(0, L*1000); ax2.set_ylim(-0.1, 2.5)
ax1.set_xlabel("Position  x  (mm)", color="#888899", fontsize=9, labelpad=0)
ax1.set_ylabel("Amplitude  u  (a.u.)", color="#888899", fontsize=9)
ax1.set_title("Incident + Reflected  =  Standing Wave", color="#aaaacc", fontsize=9, pad=10)
ax2.set_xlabel("Micrometer position  d  (mm)", color="#888899", fontsize=9, labelpad=1)
ax2.set_ylabel("|u(x)|", color="#888899", fontsize=9)
ax2.set_title("Resonance Envelope  (anode current peaks)", color="#aaaacc", fontsize=9, pad=6)
 
k0, w0, v0, b0 = get_params(F0, LAM0)
env0 = 2.0 * np.abs(np.sin(k0 * x_m))
 
ln_inc, = ax1.plot([], [], "#4fc3f7", lw=1.0, alpha=0.5, label="Incident wave")
ln_ref, = ax1.plot([], [], "#ff8a65", lw=1.0, alpha=0.5, label="Reflected wave")
ln_sum, = ax1.plot([], [], "#e8eaf6", lw=2.0,             label="Standing wave")
ln_ep,  = ax1.plot(x_mm,  env0, "#7986cb", lw=1.0, ls="--", alpha=0.6, label="Envelope")
ln_en,  = ax1.plot(x_mm, -env0, "#7986cb", lw=1.0, ls="--", alpha=0.6)
sc_node = ax1.scatter([], [], s=50, color="#ef5350", zorder=6, label="Nodes")
sc_anti = ax1.scatter([], [], s=50, color="#66bb6a", zorder=6, label="Antinodes")
ax1.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0,
           fontsize=7, facecolor="#0d0d1a", edgecolor="#2a2a44",
           labelcolor="#dddddd", framealpha=0.9)
 
ln_env,  = ax2.plot(x_mm, env0, "#ffd54f", lw=2.0, label="Anode current")
sc_peaks = ax2.scatter([], [], s=70, color="#ef5350", zorder=6, label="Resonance peaks")
arr = ax2.annotate("", xy=(0.1, 1.9), xytext=(0.5, 1.9),
                   arrowprops=dict(arrowstyle="<->", color="#80cbc4", lw=1.8))
lbl = ax2.text(0.3, 2.1, "", color="#80cbc4", fontsize=9, ha="center", fontweight="bold")
ax2.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0,
           fontsize=7.5, facecolor="#0d0d1a", edgecolor="#2a2a44",
           labelcolor="#dddddd", framealpha=0.9)
 
ax3.text(0.02, 0.95, "Wave Parameters", transform=ax3.transAxes,
         color="#80cbc4", fontsize=9, va="top", fontweight="bold")
txt_p = ax3.text(0.02, 0.75, "", transform=ax3.transAxes,
                 color="#e0e0e0", fontsize=8.5, va="top", family="monospace")
 
ax4.text(0.02, 0.95, "Micrometer Readings (first 5 antinodes)",
         transform=ax4.transAxes, color="#ffd54f", fontsize=9, va="top", fontweight="bold")
txt_m = ax4.text(0.02, 0.75, "", transform=ax4.transAxes,
                 color="#e0e0e0", fontsize=8.5, va="top", family="monospace")
 
sl_f = Slider(ax_sf, "f (MHz)", 0.5, 5.0, valinit=F0/1e6, color="#4fc3f7", valstep=0.05)
sl_l = Slider(ax_sl, "λ (mm)",  0.10, 3.0, valinit=LAM0,   color="#ffd54f", valstep=0.01)
btn  = Button(ax_bp, "PAUSE", color="#1a1a30", hovercolor="#2a2a50")
 
for sl in [sl_f, sl_l]:
    sl.label.set_color("#dddddd"); sl.label.set_fontsize(8.5)
    sl.valtext.set_color("#aaaaff"); sl.valtext.set_fontsize(8.5)
btn.label.set_color("#dddddd"); btn.label.set_fontsize(8)
 
state = {"f": F0, "lam": LAM0, "paused": False, "t": 0}
 
def update():
    k, w, v, b = get_params(state["f"], state["lam"])
    lam_mm = state["lam"]
    env = 2.0 * np.abs(np.sin(k * x_m))
    antinodes, nodes = get_markers(k)
 
    ln_ep.set_ydata(env)
    ln_en.set_ydata(-env)
    ln_env.set_ydata(env)
 
    sc_node.set_offsets(np.c_[x_mm[nodes], np.zeros(len(nodes))] if len(nodes)
                        else np.empty((0, 2)))
 
    if len(antinodes):
        ax = x_mm[antinodes]
        sc_anti.set_offsets(np.vstack([np.c_[ax, np.full(len(ax),  2.0)],
                                        np.c_[ax, np.full(len(ax), -2.0)]]))
        sc_peaks.set_offsets(np.c_[ax, np.full(len(ax), 2.0)])
        if len(antinodes) >= 2:
            x1, x2 = float(x_mm[antinodes[0]]), float(x_mm[antinodes[1]])
            xm = (x1 + x2) / 2
            arr.xy     = (x2, 1.9)
            arr.set_position((x1, 1.9))
            lbl.set_position((xm, 2.1))
            lbl.set_text(f"λ/2 = {lam_mm/2:.4f} mm")
    else:
        sc_anti.set_offsets(np.empty((0, 2)))
        sc_peaks.set_offsets(np.empty((0, 2)))
 
    txt_p.set_text(f"  f   = {state['f']/1e6:.3f} MHz\n"
                   f"  λ   = {lam_mm:.4f} mm\n"
                   f"  λ/2 = {lam_mm/2:.4f} mm\n"
                   f"  v   = {v:.1f} m/s\n"
                   f"  β   = {b:.3e} m²/N\n"
                   f"  ρ   = {RHO} kg/m³")
 
    if len(antinodes):
        rows = ["  N    d (mm)    Δd (mm)"]
        for i, idx in enumerate(antinodes[:5]):
            d = x_mm[idx]
            dd = f"{d - x_mm[antinodes[i-1]]:.4f}" if i > 0 else "  —"
            rows.append(f"  {i+1}   {d:7.4f}   {dd}")
        txt_m.set_text("\n".join(rows))
 
    fig.canvas.draw_idle()
 
def animate(frame):
    if state["paused"]:
        return ln_inc, ln_ref, ln_sum
    state["t"] += 1
    k, w, v, b = get_params(state["f"], state["lam"])
    t = state["t"] / (state["f"] * 60)
    ln_inc.set_data(x_mm, np.sin(k*x_m - w*t))
    ln_ref.set_data(x_mm, np.sin(k*x_m + w*t))
    ln_sum.set_data(x_mm, np.sin(k*x_m - w*t) + np.sin(k*x_m + w*t))
    return ln_inc, ln_ref, ln_sum
 
sl_f.on_changed(lambda v: (state.update({"f": v * 1e6}), update()))
sl_l.on_changed(lambda v: (state.update({"lam": v}),     update()))
btn.on_clicked(lambda e: (state.update({"paused": not state["paused"]}),
                           btn.label.set_text("RESUME" if state["paused"] else "PAUSE"),
                           fig.canvas.draw_idle()))
 
plt.figtext(0.06, 0.005,
    "Red ● = Nodes (zero amplitude)   Green ● = Antinodes (max amplitude)   "
    "Consecutive antinodes separated by λ/2",
    color="#555566", fontsize=7.5)
 
update()
ani = animation.FuncAnimation(fig, animate, frames=10000, interval=40, blit=False)
plt.show()
 