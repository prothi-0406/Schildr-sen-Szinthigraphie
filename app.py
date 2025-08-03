# Schilddrüsenszintigraphie – Finalversion
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from PIL import Image

# Streamlit-Konfiguration
st.set_page_config(page_title="Schilddrüsenszintigraphie-Simulation", layout="wide")
st.title("🧪 Schilddrüsenszintigraphie – Physikalische Prozesse (Simulation)")

st.markdown("""
Diese interaktive Simulation zeigt die grundlegenden physikalischen Abläufe einer Schilddrüsenszintigraphie:

- 💊 **Aufnahme des Radiopharmakons**
- 🧬 **Radioaktiver Zerfall**
- 📸 **Bildentstehung in der Gamma-Kamera**
""")

# Radiopharmakon-Auswahl
pharmakon = st.selectbox("Radiopharmakon auswählen:", ["Technetium-99m", "Jod-123"])
halbwertszeit = {"Technetium-99m": 6.01, "Jod-123": 13.2}[pharmakon]
st.info(f"Halbwertszeit von **{pharmakon}**: **{halbwertszeit} Stunden**")

# Zerfallskurve
st.subheader("🧬 Exponentieller Zerfall des Radiopharmakons")
NO = st.slider("Anfangsaktivität (z. B. Anzahl radioaktiver Atome)", 100, 5000, 1000, step=100)
zeit = st.slider("Simulationszeitraum (Stunden)", 6, 48, 24, step=6)
t = np.linspace(0, zeit, 200)
N = NO * np.exp(-np.log(2) * t / halbwertszeit)

fig1, ax1 = plt.subplots()
ax1.plot(t, N, color='darkred', label="Restaktivität")
ax1.set_xlabel("Zeit [h]")
ax1.set_ylabel("Anzahl aktiver Atome")
ax1.set_title("Zerfallskurve")
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

# Schilddrüsengewebe – Pathologie-Auswahl
st.subheader("🧠 Pathologisches Muster auswählen")
pathologie = st.selectbox("Pathologischer Zustand:", [
    "Normale Schilddrüse",
    "Autonomes Adenom (heißer Knoten)",
    "Kalter Knoten",
    "M. Basedow (diffus heiß)"
])

# Schilddrüsenform & Aktivität
size = 100
X, Y = np.meshgrid(np.linspace(-1, 1, size), np.linspace(-1, 1, size))
ellipse_mask = ((X**2)/(0.7**2) + (Y**2)/(0.4**2)) < 1

activity = np.zeros((size, size))
activity[ellipse_mask] = np.random.normal(loc=20, scale=4, size=np.sum(ellipse_mask))

# Pathologie anwenden
if pathologie == "Autonomes Adenom (heißer Knoten)":
    activity[45:55, 40:60] += 80
elif pathologie == "Kalter Knoten":
    activity[25:35, 65:75] -= 18
elif pathologie == "M. Basedow (diffus heiß)":
    activity[ellipse_mask] += 30

activity = np.clip(activity, 0, None)

# Simulierte Detektion (Szintigramm)
st.subheader("📍 Simuliertes Szintigramm")

detected = np.clip(activity + np.random.normal(0, 4, (size, size)), 0, None)

fig2, ax2 = plt.subplots()
im = ax2.imshow(detected, cmap="plasma", interpolation="nearest")
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung (a.u.)")
ax2.set_title(f"Simuliertes Szintigramm – {pathologie}")
ax2.axis("off")
st.pyplot(fig2)

# Gamma-Emission mit Farblegende
st.subheader("💥 Gamma-Emissionen mit Farbbedeutung")

if st.button("Emissionen anzeigen"):
    emission_fig, emission_ax = plt.subplots()
    emission_ax.set_xlim(0, size)
    emission_ax.set_ylim(0, size)
    emission_ax.set_title("Simulierte Gamma-Emissionen")
    emission_ax.axis("off")
    plot_placeholder = st.empty()

    for i in range(200):
        x, y = np.random.randint(0, size, 2)
        if ellipse_mask[x, y] and np.random.rand() < activity[x, y] / np.max(activity):
            val = activity[x, y]
            norm_val = val / np.max(activity)

            if norm_val > 0.8:
                color = 'red'      # heiß
            elif norm_val > 0.4:
                color = 'orange'   # mittel
            else:
                color = 'blue'     # kalt

            circ = patches.Circle((y, x), radius=1.5, edgecolor=color, facecolor='none', linewidth=1)
            emission_ax.add_patch(circ)

        if i % 5 == 0:
            plot_placeholder.pyplot(emission_fig)
        time.sleep(0.01)

    plot_placeholder.pyplot(emission_fig)

    # 🔍 LEGENDE
    st.markdown("**🔎 Legende der Emissionsfarben:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 **Heißer Bereich** (z. B. Adenom)")
    with col2:
        st.markdown("🟠 **Normale Aktivität**")
    with col3:
        st.markdown("🔵 **Kalter Bereich** (z. B. Zyste)")

# Echte Bilddaten hochladen
st.subheader("🖼️ Echtes Szintigramm hochladen (optional)")
uploaded_file = st.file_uploader("Bilddatei (PNG, JPG) auswählen", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Hochgeladenes echtes Szintigramm", use_column_width=True)

st.markdown("---")
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe einer Schilddrüsenszintigraphie. Keine diagnostische Anwendung.")
