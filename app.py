# Schilddrüsenszintigraphie – Überarbeitete Version nach Wunsch

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from PIL import Image

# App-Konfiguration
st.set_page_config(page_title="Schilddrüsenszintigraphie-Simulation", layout="wide")
st.title("🧪 Schilddrüsenszintigraphie – Physikalische Prozesse (Simulation)")

st.markdown("""
Diese interaktive Simulation zeigt die grundlegenden physikalischen Abläufe einer Schilddrüsenszintigraphie:

- 💊 **Aufnahme des Radiopharmakons**
- 🧬 **Radioaktiver Zerfall**
- 📸 **Bildentstehung durch Gamma-Kamera**
""")

# Radiopharmakon-Auswahl
pharmakon = st.selectbox("Radiopharmakon auswählen:", ["Technetium-99m", "Jod-123"])
halbwertszeit = {"Technetium-99m": 6.01, "Jod-123": 13.2}[pharmakon]
st.info(f"Halbwertszeit von **{pharmakon}**: **{halbwertszeit} Stunden**")

# Zerfall in MBq
st.subheader("🧬 Exponentieller Zerfall des Radiopharmakons")
A0_MBq = st.slider("Anfangsaktivität (in MBq)", 70, 150, 100, step=10)
A0_Bq = A0_MBq * 1e6
zeit = np.linspace(0, 24, 200)
A = A0_Bq * np.exp(-np.log(2) * zeit / halbwertszeit)

fig1, ax1 = plt.subplots()
ax1.plot(zeit, A / 1e6, color='darkred', label="Aktivität")
ax1.set_xlabel("Zeit [h]")
ax1.set_ylabel("Aktivität [MBq]")
ax1.set_title("Zerfallskurve")
ax1.set_ylim(0, 150)  # konstante y-Achse
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

# Pathologie-Auswahl
st.subheader("🧠 Pathologisches Muster auswählen")
pathologie = st.selectbox("Pathologischer Zustand:", [
    "Normale Schilddrüse",
    "Autonomes Adenom (heißer Knoten)",
    "Kalter Knoten",
    "M. Basedow (diffus heiß)"
])

# Schilddrüsenform und Aktivitätsmatrix
size = 100
X, Y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
ellipse_mask = ((X**2)/(0.7**2) + (Y**2)/(0.4**2)) < 1

activity = np.zeros((size, size))
activity[ellipse_mask] = np.random.normal(loc=20, scale=4, size=np.sum(ellipse_mask))

if pathologie == "Autonomes Adenom (heißer Knoten)":
    activity[45:55, 40:60] += 80
elif pathologie == "Kalter Knoten":
    activity[25:35, 65:75] = 0
elif pathologie == "M. Basedow (diffus heiß)":
    activity[ellipse_mask] += 30

activity = np.clip(activity, 0, None)

# Szintigramm mit fester Farbskala
st.subheader("📍 Simuliertes Szintigramm")
detected = np.clip(activity + np.random.normal(0, 4, (size, size)), 0, None)

fig2, ax2 = plt.subplots()
im = ax2.imshow(detected, cmap="plasma", interpolation="nearest", vmin=0, vmax=120)
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung (a.u.)")
ax2.set_title(f"Simuliertes Szintigramm – {pathologie}")
ax2.axis("off")
st.pyplot(fig2)

# Gamma-Emission mit gleichfarbigen Punkten und kleinerer Ellipse
st.subheader("💥 Simulierte Gamma-Emissionen (Punktverteilung)")

if st.button("Emissionen anzeigen"):
    fig3, ax3 = plt.subplots()
    ax3.set_xlim(0, size)
    ax3.set_ylim(0, size)
    ax3.set_title("Simulierte Gamma-Emissionen")
    ax3.axis("off")
    placeholder = st.empty()

    xs, ys = [], []

    for i in range(500):
        x, y = np.random.randint(0, size, 2)
        if ellipse_mask[x, y] and np.random.rand() < activity[x, y] / np.max(activity):
            xs.append(y)
            ys.append(x)

        if i % 20 == 0:
            ax3.clear()
            ax3.set_xlim(0, size)
            ax3.set_ylim(0, size)
            ax3.axis("off")
            ax3.set_title("Simulierte Gamma-Emissionen")
            ax3.scatter(xs, ys, color='deepskyblue', s=8, alpha=0.8)
            ellipse = patches.Ellipse(
                (size / 2, size / 2),
                width=0.65 * size * 2,
                height=0.35 * size * 2,
                edgecolor='black',
                facecolor='none',
                linewidth=1.2,
                linestyle='--'
            )
            ax3.add_patch(ellipse)
            placeholder.pyplot(fig3)
            time.sleep(0.01)

    ax3.clear()
    ax3.set_xlim(0, size)
    ax3.set_ylim(0, size)
    ax3.axis("off")
    ax3.set_title("Simulierte Gamma-Emissionen – final")
    ax3.scatter(xs, ys, color='deepskyblue', s=8, alpha=0.8)
    ellipse = patches.Ellipse(
        (size / 2, size / 2),
        width=0.65 * size * 2,
        height=0.35 * size * 2,
        edgecolor='black',
        facecolor='none',
        linewidth=1.2,
        linestyle='--'
    )
    ax3.add_patch(ellipse)
    placeholder.pyplot(fig3)

    st.markdown("**🟦 Mehr Punkte = heißer Bereich, weniger Punkte = kalter Bereich**")

# Echte Bilddaten hochladen
st.subheader("🖼️ Echtes Szintigramm hochladen (optional)")
uploaded_file = st.file_uploader("Bilddatei (PNG, JPG) auswählen", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Hochgeladenes echtes Szintigramm", use_column_width=True)

st.markdown("---")
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe einer Schilddrüsenszintigraphie. Keine diagnostische Anwendung.")
