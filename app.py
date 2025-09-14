# Schilddrüsenszintigraphie

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from PIL import Image

# App-Konfiguration
st.set_page_config(page_title="Schilddrüsenszintigraphie", layout="wide")
st.title("🧪 Schilddrüsenszintigraphie – Simulation")

st.markdown("""
Diese Simulation zeigt wichtige Abläufe einer Schilddrüsenszintigraphie:

- 💊 Aufnahme des Radiopharmakons
- 🧬 Radioaktiver Zerfall
- 📸 Bildentstehung durch Gamma-Kamera
""")

# Radiopharmakon-Auswahl
pharmakon = st.selectbox("Radiopharmakon auswählen:", ["Technetium-99m", "Iod-123"])
halbwertszeit = {"Technetium-99m": 6.01, "Iod-123": 13.2}[pharmakon]
st.info(f"Halbwertszeit von **{pharmakon}**: **{halbwertszeit} Stunden**")

# Zerfallskurve – in MBq
st.subheader("🧬 Zerfall des Radiopharmakons in MBq")
A0 = st.slider("Anfangsaktivität [MBq]", 70, 150, 100, step=10)
zeit = st.slider("Simulationszeitraum (h)", 6, 48, 24, step=6)
t = np.linspace(0, zeit, 200)
A = A0 * np.exp(-np.log(2) * t / halbwertszeit)

fig1, ax1 = plt.subplots()
ax1.plot(t, A, color='darkgreen', label="Aktivität [MBq]")
ax1.set_xlabel("Zeit [h]")
ax1.set_ylabel("Aktivität [MBq]")
ax1.set_ylim(0, 150)  # Fixe Y-Achse
ax1.set_title("Exponentialzerfall")
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

# Pathologie-Auswahl
st.subheader("🧠 Pathologisches Muster")
pathologie = st.selectbox("Pathologischer Zustand:", [
    "Normale Schilddrüse",
    "Autonomes Adenom (heißer Knoten)",
    "Kalter Knoten",
    "M. Basedow (diffus heiß)"
])

# Schilddrüsenform und Aktivität
size = 100
X, Y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
ellipse_mask = ((X**2)/(0.7**2) + (Y**2)/(0.4**2)) < 1

activity = np.zeros((size, size))
activity[ellipse_mask] = np.random.normal(loc=20, scale=4, size=np.sum(ellipse_mask))

# Pathologie-Simulation
if pathologie == "Autonomes Adenom (heißer Knoten)":
    activity[45:55, 40:60] += 60
elif pathologie == "Kalter Knoten":
    activity[45:55, 40:60] -= 18
elif pathologie == "M. Basedow (diffus heiß)":
    activity[ellipse_mask] += 25

activity = np.clip(activity, 0, None)

# Szintigramm-Darstellung
st.subheader("📍 Simuliertes Szintigramm")
detected = np.clip(activity + np.random.normal(0, 4, (size, size)), 0, None)

fig2, ax2 = plt.subplots()
im = ax2.imshow(detected, cmap="plasma", interpolation="nearest", vmin=0, vmax=60)  # Feste Skala
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung (a.u.)")
ax2.set_title(f"Simuliertes Szintigramm – {pathologie}")
ax2.axis("off")
st.pyplot(fig2)

# Gamma-Emissionen
st.subheader("💥 Simulierte Gamma-Emissionen")

if st.button("Emissionen anzeigen"):
    emission_fig, emission_ax = plt.subplots()
    emission_ax.set_xlim(0, size)
    emission_ax.set_ylim(0, size)
    emission_ax.axis("off")
    plot_placeholder = st.empty()

    xs = []
    ys = []

    for i in range(500):
        x, y = np.random.randint(0, size, 2)
        if ellipse_mask[x, y] and np.random.rand() < activity[x, y] / 80:
            xs.append(y)
            ys.append(x)

        if i % 20 == 0:
            emission_ax.clear()
            emission_ax.set_xlim(0, size)
            emission_ax.set_ylim(0, size)
            emission_ax.axis("off")
            emission_ax.set_title("Simulierte Gamma-Emissionen")
            emission_ax.scatter(xs, ys, color='cyan', s=10, alpha=0.7)

            ellipse = patches.Ellipse(
                (size / 2, size / 2),
                width=0.65 * size * 2,
                height=0.38 * size * 2,
                edgecolor='black',
                facecolor='none',
                linewidth=1.2,
                linestyle='--'
            )
            emission_ax.add_patch(ellipse)
            plot_placeholder.pyplot(emission_fig)
            time.sleep(0.01)

    # Finales Bild
    emission_ax.clear()
    emission_ax.set_xlim(0, size)
    emission_ax.set_ylim(0, size)
    emission_ax.axis("off")
    emission_ax.set_title("Simulierte Gamma-Emissionen – final")
    emission_ax.scatter(xs, ys, color='cyan', s=10, alpha=0.7)

    ellipse = patches.Ellipse(
        (size / 2, size / 2),
        width=0.65 * size * 2,
        height=0.38 * size * 2,
        edgecolor='black',
        facecolor='none',
        linewidth=1.2,
        linestyle='--'
    )
    emission_ax.add_patch(ellipse)
    plot_placeholder.pyplot(emission_fig)

# Bild-Upload
st.subheader("🖼️ Echtes Szintigramm hochladen")
uploaded_file = st.file_uploader("Bilddatei (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Hochgeladenes Szintigramm", use_column_width=True)

st.markdown("---")
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe einer Schilddrüsenszintigraphie. Keine diagnostische Anwendung.")
