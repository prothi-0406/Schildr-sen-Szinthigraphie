   
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from PIL import Image, ImageOps

# --- Page setup ---
st.set_page_config(page_title="Schilddrüsen-Szinti (Simulation)", page_icon="🧪", layout="centered")
st.title("🧪 Simulierte Gamma-Emissionen (mit Pathologien)")

# --- Sidebar controls ---
st.sidebar.header("Parameter")
size = st.sidebar.slider("Bildgröße (px)", 200, 1000, 600, step=50)
n_points_base = st.sidebar.slider("Basismenge Emissionen (wird intern ×4)", 100, 20000, 3000, step=100)
steps = st.sidebar.slider("Animationsschritte", 1, 100, 30)
point_size = st.sidebar.slider("Punktgröße", 1, 20, 8)
alpha = st.sidebar.slider("Transparenz", 0.1, 1.0, 0.7, step=0.05)
animate = st.sidebar.checkbox("Animation abspielen", True)

pathology = st.sidebar.selectbox(
    "Pathologischer Zustand",
    [
        "Physiologisch (normal)",
        "Heißer Knoten (autonomes Adenom)",
        "Kalter Knoten",
        "Struma diffusa",
        "Hashimoto (inhomogen)"
    ],
    index=0
)

# --- Ellipsen-/Organ-Parameter (vereinfachtes Modell) ---
# Grundform
cx, cy = size / 2, size / 2
a_base = 0.65 * size   # Halbachse x
b_base = 0.38 * size   # Halbachse y

# Anpassungen je Pathologie (nur Geometrie)
if pathology == "Struma diffusa":
    a = a_base * 1.15
    b = b_base * 1.15
else:
    a = a_base
    b = b_base

rng = np.random.default_rng(42)

# --- Hilfsfunktionen ---
def uniform_points_in_ellipse(n, cx, cy, a, b, rng):
    """Gleichverteilte Punkte innerhalb einer Ellipse (Akzeptanz-Sampling)."""
    # effizient: polar + sqrt(U)
    theta = rng.uniform(0, 2*np.pi, n)
    r = np.sqrt(rng.uniform(0, 1, n))
    x = cx + a * r * np.cos(theta)
    y = cy + b * r * np.sin(theta)
    return x, y

def gaussian(x, y, mx, my, sx, sy):
    return np.exp(-0.5 * (((x - mx) / sx) ** 2 + ((y - my) / sy) ** 2))

def in_ellipse_mask(x, y, cx, cy, a, b):
    return ((x - cx)**2) / (a**2) + ((y - cy)**2) / (b**2) <= 1.0

def pathology_weight(x, y, cx, cy, a, b, label):
    """
    Liefert Gewicht/Intensität (0..1+) für die Auswahl.
    Höhere Werte => höhere Wahrscheinlichkeit für Punkt in diesem Bereich.
    """
    # Grundgewicht leicht gelappt (zwei Lappen)
    lobe_offset = 0.22 * a
    lobe_sigma = 0.35 * a
    base = 0.6 * (
        gaussian(x, y, cx - lobe_offset, cy, lobe_sigma, 0.6 * b) +
        gaussian(x, y, cx + lobe_offset, cy, lobe_sigma, 0.6 * b)
    )
    base += 0.4  # Mindestbasis, damit nicht zu leer

    if label == "Physiologisch (normal)":
        w = base

    elif label == "Heißer Knoten (autonomes Adenom)":
        # Hotspot in rechtem Lappen
        hk_cx = cx + 0.22 * a
        hk_cy = cy + 0.05 * b
        w = base + 1.8 * gaussian(x, y, hk_cx, hk_cy, 0.18 * a, 0.18 * b)

    elif label == "Kalter Knoten":

        ck_cy = cy - 0.02 * b
        cold = gaussian(x, y, ck_cx, ck_cy, 0.18 * a, 0.18 * b)
        # Unterdrücke lokal deutlich (aber nicht null, damit trotzdem Punkte vorhanden sind)
        w = base * (1.0 - 0.85 * cold)

    elif label == "Struma diffusa":
        # Eher gleichmäßig, leichte zufällige Inhomogenität
        noise = rng.normal(0.0, 0.05, size=x.shape)
        w = 0.9 + noise
        w += 0.2 * base

    elif label == "Hashimoto (inhomogen)":
        # Patchy uptake: mehrere kleine Gauss-Flecken (teils Suppression, teils Uptake)
        w = 0.6 * base
        # zufällige "Flecken"
        rng_state = np.random.default_rng(123)
        for i in range(7):
            mx = cx + rng_state.uniform(-0.28*a, 0.28*a)
            my = cy + rng_state.uniform(-0.2*b, 0.2*b)
            sx = rng_state.uniform(0.10*a, 0.20*a)
            sy = rng_state.uniform(0.10*b, 0.20*b)
            sign = rng_state.choice([+1.0, -1.0])  # manche heißer, manche kälter
            w += 0.9 * sign * gaussian(x, y, mx, my, sx, sy)
        # clamp später
    else:
        w = base

    # Maskiere außerhalb der Ellipse
    mask = in_ellipse_mask(x, y, cx, cy, a, b)
    w = np.where(mask, w, 0.0)

    # Normalisieren & clampen (keine negativen Gewichte)
    w = np.clip(w, 0.001, None)
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from PIL import Image, ImageOps

# --- Page setup ---
st.set_page_config(page_title="Schilddrüsen-Szinti (Simulation)", page_icon="🧪", layout="centered")
st.title("🧪 Simulierte Gamma-Emissionen (Schilddrüsenszintigraphie)")

# --- Sidebar controls ---
st.sidebar.header("Parameter")
size = st.sidebar.slider("Bildgröße (px)", 200, 1000, 600, step=50)
n_points_base = st.sidebar.slider("Basismenge Emissionen (wird intern ×4)", 100, 20000, 3000, step=100)
steps = st.sidebar.slider("Animationsschritte", 1, 100, 30)
point_size = st.sidebar.slider("Punktgröße", 1, 20, 8)
alpha = st.sidebar.slider("Transparenz", 0.1, 1.0, 0.7, step=0.05)
animate = st.sidebar.checkbox("Animation abspielen", True)

pathology = st.sidebar.selectbox(
    "Pathologischer Zustand",
    [
        "Physiologisch (normal)",
        "Heißer Knoten (autonomes Adenom)",
        "Kalter Knoten",
        "Struma diffusa",
        "Hashimoto (inhomogen)"
    ],
    index=0
)

# --- Ellipsen-/Organ-Parameter (vereinfachtes Organmodell) ---
cx, cy = size / 2, size / 2
a_base = 0.65 * size   # Halbachse x
b_base = 0.38 * size   # Halbachse y

# Bei Struma diffusa Organ etwas vergrößern
if pathology == "Struma diffusa":
    a = a_base * 1.15
    b = b_base * 1.15
else:
    a = a_base
    b = b_base

rng = np.random.default_rng(42)

# --- Hilfsfunktionen ---
def uniform_points_in_ellipse(n, cx, cy, a, b, rng):
    """Gleichverteilte Punkte innerhalb einer Ellipse (polar, r = sqrt(U))."""
    theta = rng.uniform(0, 2*np.pi, n)
    r = np.sqrt(rng.uniform(0, 1, n))
    x = cx + a * r * np.cos(theta)
    y = cy + b * r * np.sin(theta)
    return x, y

def gaussian(x, y, mx, my, sx, sy):
    return np.exp(-0.5 * (((x - mx) / sx) ** 2 + ((y - my) / sy) ** 2))

def in_ellipse_mask(x, y, cx, cy, a, b):
    return ((x - cx)**2) / (a**2) + ((y - cy)**2) / (b**2) <= 1.0

def pathology_weight(x, y, cx, cy, a, b, label):
    """
    Liefert Gewichte für die Auswahl (höher = mehr Punkte).
    Modelliert Normalverteilung (2 Lappen) + Pathologie-spezifische Modulation.
    """
    # Basis: zwei Lappen
    lobe_offset = 0.22 * a
    lobe_sigma = 0.35 * a
    base = 0.6 * (
        gaussian(x, y, cx - lobe_offset, cy, lobe_sigma, 0.6 * b) +
        gaussian(x, y, cx + lobe_offset, cy, lobe_sigma, 0.6 * b)
    )
    base += 0.4  # Grundniveau

    if label == "Physiologisch (normal)":
        w = base

    elif label == "Heißer Knoten (autonomes Adenom)":
        hk_cx = cx + 0.22 * a
        hk_cy = cy + 0.05 * b
        w = base + 1.8 * gaussian(x, y, hk_cx, hk_cy, 0.18 * a, 0.18 * b)

    elif label == "Kalter Knoten":
        ck_cx = cx + 0.22 * a
        ck_cy = cy - 0.02 * b
        cold = gaussian(x, y, ck_cx, ck_cy, 0.18 * a, 0.18 * b)
        w = base * (1.0 - 0.85 * cold)  # lokal stark reduziert

    elif label == "Struma diffusa":
        noise = rng.normal(0.0, 0.05, size=x.shape)
        w = 0.9 + noise + 0.2 * base

    elif label == "Hashimoto (inhomogen)":
        w = 0.6 * base
        rng_state = np.random.default_rng(123)
        for _ in range(7):
            mx = cx + rng_state.uniform(-0.28*a, 0.28*a)
            my = cy + rng_state.uniform(-0.2*b, 0.2*b)
            sx = rng_state.uniform(0.10*a, 0.20*a)
            sy = rng_state.uniform(0.10*b, 0.20*b)
            sign = rng_state.choice([+1.0, -1.0])  # heiß/kalt-Flecken
            w += 0.9 * sign * gaussian(x, y, mx, my, sx, sy)
    else:
        w = base

    # Außerhalb der Ellipse auf 0
    w = np.where(in_ellipse_mask(x, y, cx, cy, a, b), w, 0.0)
    # Keine negativen/Null-Gewichte
    w = np.clip(w, 0.001, None)
    return w

def sample_weighted_in_ellipse(n_final, cx, cy, a, b, label, rng):
    """
    Wählt exakt n_final Punkte proportional zu pathology_weight.
    """
    n_cand = max(n_final * 3, 20000)
    x_cand, y_cand = uniform_points_in_ellipse(n_cand, cx, cy, a, b, rng)
    w = pathology_weight(x_cand, y_cand, cx, cy, a, b, label)
    if np.all(w <= 0):
        return uniform_points_in_ellipse(n_final, cx, cy, a, b, rng)
    p = w / w.sum()
    idx = rng.choice(len(x_cand), size=n_final, replace=False, p=p)
    return x_cand[idx], y_cand[idx]

# --- IMMER 4× so viele Punkte ---
n_points = n_points_base * 4

# --- Punkte generieren (pathologie-konsistent) ---
xs, ys = sample_weighted_in_ellipse(n_points, cx, cy, a, b, pathology, rng)

# --- Plot-Placeholder ---
plot_placeholder = st.empty()

def render_frame(x_show, y_show, final=False):
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.axis("off")
    title = f"Simulierte Gamma-Emissionen – {pathology}"
    if final:
        title += " (final)"
    ax.set_title(title)

    # Punkte
    ax.scatter(x_show, y_show, s=point_size, alpha=alpha)

    # Organ-Kontur
    ellipse = patches.Ellipse(
        (cx, cy),
        width=2*a,
        height=2*b,
        edgecolor='black',
        facecolor='none',
        linewidth=1.2,
        linestyle='--'
    )
    ax.add_patch(ellipse)

    plot_placeholder.pyplot(fig, use_container_width=True)
    plt.close(fig)

# --- Animation / Finale Darstellung ---
if animate and steps > 1:
    for i in range(1, steps + 1):
        k = int(np.ceil(i * len(xs) / steps))
        render_frame(xs[:k], ys[:k], final=(i == steps))
        time.sleep(0.02)
else:
    render_frame(xs, ys, final=True)

# --- Bild-Upload ---
st.markdown("---")
st.subheader("🖼️ Echtes Szintigramm hochladen")
uploaded_file = st.file_uploader("Bilddatei (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    image = ImageOps.exif_transpose(image)  # Drehung nach EXIF
    to_gray = st.checkbox("Als Graustufen anzeigen", value=True)
    image_disp = image.convert("L") if to_gray else image
    st.image(image_disp, caption="Hochgeladenes Szintigramm", use_column_width=True)

st.markdown("---")
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe einer Schilddrüsenszintigraphie. Keine diagnostische Anwendung.")
