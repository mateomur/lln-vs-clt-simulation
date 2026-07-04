import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

np.random.seed(123)

# --- distribution: exponential (skewed, makes CLT effect dramatic) ---
def draw_samples(n):
    return np.random.exponential(scale=1.0, size=n)

TRUE_MEAN = 1.0
N_PER_SAMPLE = 30

# --- LLN data ---
max_n = 1000
cumulative = np.cumsum(draw_samples(max_n)) / np.arange(1, max_n + 1)

# --- CLT data ---
means_10   = [draw_samples(N_PER_SAMPLE).mean() for _ in range(10)]
means_100  = [draw_samples(N_PER_SAMPLE).mean() for _ in range(100)]
means_1000 = [draw_samples(N_PER_SAMPLE).mean() for _ in range(1000)]

# --- style ---
BLUE   = "#2a78d6"
RED    = "#e34948"
GREEN  = "#1baf7a"
GRAY   = "#898781"
BG     = "#ffffff"
LIGHT  = "#f5f5f3"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.facecolor": LIGHT,
    "figure.facecolor": BG,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.labelsize": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlepad": 10,
})

fig = plt.figure(figsize=(12, 7))
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(
    2, 4,
    figure=fig,
    hspace=0.55,
    wspace=0.35,
    left=0.06, right=0.97,
    top=0.88, bottom=0.10
)

# ── section labels ──────────────────────────────────────────────────────────
fig.text(0.01, 0.96, "Law of Large Numbers", fontsize=13, fontweight="bold", color="#0b0b0b")
fig.text(0.01, 0.91, "One sample, growing n  →  mean stabilises to μ  →  about accuracy",
         fontsize=10, color=GRAY)

fig.text(0.52, 0.96, "Central Limit Theorem", fontsize=13, fontweight="bold", color="#0b0b0b")
fig.text(0.52, 0.91, "Many samples, fixed n  →  distribution of means → normal  →  about shape",
         fontsize=10, color=GRAY)

# ── LLN plot ────────────────────────────────────────────────────────────────
ax_lln = fig.add_subplot(gs[:, :2])
ax_lln.set_facecolor(LIGHT)

ax_lln.plot(np.arange(1, max_n + 1), cumulative,
            color=BLUE, lw=1.8, label="running sample mean")
ax_lln.axhline(TRUE_MEAN, color=RED, lw=1.5, ls="--", label=f"true mean μ = {TRUE_MEAN}")

ax_lln.fill_between(np.arange(1, max_n + 1), cumulative, TRUE_MEAN,
                    alpha=0.08, color=BLUE)

ax_lln.set_xlabel("sample size  (n)", labelpad=6)
ax_lln.set_ylabel("sample mean", labelpad=6)
ax_lln.tick_params(length=0)
ax_lln.grid(axis="y", color="#ddddd8", lw=0.7)

leg = ax_lln.legend(fontsize=9, frameon=False, loc="upper right")
for text in leg.get_texts():
    text.set_color(GRAY)

# annotation
ax_lln.annotate(
    f"converges to μ = {TRUE_MEAN}",
    xy=(max_n, cumulative[-1]),
    xytext=(700, TRUE_MEAN + 0.25),
    fontsize=9, color=BLUE,
    arrowprops=dict(arrowstyle="->", color=BLUE, lw=1),
)

# ── CLT histograms ───────────────────────────────────────────────────────────
clt_configs = [
    (gs[0, 2], means_10,   "10 sample means",   7),
    (gs[0, 3], means_100,  "100 sample means",  12),
    (gs[1, 2], means_1000, "1000 sample means", 22),
]

for spec, data, title, bins in clt_configs:
    ax = fig.add_subplot(spec)
    ax.set_facecolor(LIGHT)
    ax.hist(data, bins=bins, color=BLUE, edgecolor=BG, linewidth=0.4)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
    ax.tick_params(length=0)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.grid(axis="y", color="#ddddd8", lw=0.5)

# normal curve overlay on 1000 means
from scipy.stats import norm as sp_norm
ax_1000 = fig.axes[-1]
mu_m, std_m = np.mean(means_1000), np.std(means_1000)
x_norm = np.linspace(min(means_1000), max(means_1000), 200)
y_norm = sp_norm.pdf(x_norm, mu_m, std_m)
ax_1000_twin = ax_1000.twinx()
ax_1000_twin.plot(x_norm, y_norm, color=GREEN, lw=2)
ax_1000_twin.set_yticks([])
ax_1000_twin.spines[:].set_visible(False)

# ── "shape converges" label in bottom-right ──────────────────────────────────
ax_note = fig.add_subplot(gs[1, 3])
ax_note.set_facecolor(BG)
ax_note.axis("off")
ax_note.text(0.5, 0.65, "shape →", ha="center", va="center",
             fontsize=11, fontweight="bold", color="#0b0b0b")
ax_note.text(0.5, 0.42, "normal", ha="center", va="center",
             fontsize=18, fontweight="bold", color=GREEN)
ax_note.text(0.5, 0.20,
             "regardless of the\noriginal distribution",
             ha="center", va="center", fontsize=9, color=GRAY)

# ── footer ───────────────────────────────────────────────────────────────────
fig.text(
    0.5, 0.02,
    "Distribution: Exponential(λ=1)  |  n = 30 per sample  |  simulation by @mateomur",
    ha="center", fontsize=9, color=GRAY
)

plt.savefig("lln_vs_clt.png", dpi=180, bbox_inches="tight")
print("saved.")
