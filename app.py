# Schilddrüsen-Szintigraphie Simulation
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# Seiteneinstellungen
st.set_page_config(page_title="Schilddrüsen-Szintigraphie-Simulation", layout="wide")
st.title("Schilddrüsen-Szintigraphie – Physikalische Prozesse (Simulation)")

st.markdown("""
Diese interaktive Simulation zeigt die physikalischen Abläufe einer Schilddrüsen-Szintigraphie:
- **Aufnahme des Radiopharmakons**
- **Radioaktiver Zerfall und Gamma-Emission**
- **Bildentstehung durch eine Gamma-Kamera**
""")

# Auswahl Radiopharmakon
pharmakon = st.selectbox("Radiopharmakon auswählen:", ["Technetium-99m", "Jod-123"])
halbwertszeit = {"Technetium-99m": 6.01, "Jod-123": 13.2}[pharmakon]
st.write(f"Halbwertszeit von **{pharmakon}**: {halbwertszeit} Stunden")

# Auswahl Anfangsaktivität
A0_MBq = st.slider("Anfangsaktivität auswählen (MBq):", 70, 150, 100, 10)
A0_Bq = A0_MBq * 1e6

# Zerfallskurve (in Bq)
st.subheader("Zerfall des Radiopharmakons (Aktivität in Bq)")
t = np.linspace(0, 24, 100)
A = A0_Bq * np.exp(-np.log(2) * t / halbwertszeit)

fig1, ax1 = plt.subplots()
ax1.plot(t, A / 1e6, label="Aktivität")
ax1.set_xlabel("Zeit (h)")
ax1.set_ylabel("Aktivität (MBq)")
ax1.set_title("Exponentieller Zerfall")
ax1.grid(True)
ax1.set_ylim(0, 150)  # Skala konstant halten
st.pyplot(fig1)

# Pathologie-Auswahl
st.subheader("Verteilung im Schilddrüsengewebe")
pathologie = st.selectbox("Pathologisches Muster auswählen:", ["Normal", "Autonomes Adenom", "Kalter Knoten", "Morbus Basedow"])

# Schilddrüsengewebe initialisieren
size = 100
activity = np.random.normal(loc=20, scale=5, size=(size, size))

# Pathologiespezifische Modifikationen
if pathologie == "Autonomes Adenom":
    activity[40:60, 40:60] += 100
elif pathologie == "Kalter Knoten":
    xx, yy = np.meshgrid(np.arange(size), np.arange(size))
    ellipse = ((xx - 75)**2) / (8**2) + ((yy - 25)**2) / (10**2) < 1
    activity[ellipse] = np.random.normal(loc=2, scale=0.5, size=activity[ellipse].shape)
elif pathologie == "Morbus Basedow":
    activity += 40

# Simulierte Detektion
st.subheader("Simuliertes Szintigramm")
detected = np.clip(activity + np.random.normal(0, 5, (size, size)), 0, None)

fig2, ax2 = plt.subplots()
im = ax2.imshow(detected, cmap="hot", interpolation="nearest", vmin=0, vmax=A0_MBq)
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung (rel. Einheiten)")
ax2.set_title(f"Simuliertes Szintigramm – {pathologie}")
st.pyplot(fig2)

# Animation: Gamma-Emissionen (vereinfacht)
st.subheader("Animation: Gamma-Emissionen")

if st.button("Emissionen starten"):
    emission_fig, emission_ax = plt.subplots()
    emission_ax.set_xlim(0, size)
    emission_ax.set_ylim(0, size)
    emission_ax.set_title("Simulierte Gamma-Emissionen (vereinfachte Darstellung)")
    emission_ax.set_aspect('equal')

    # Schilddrüsen-Ellipse zeichnen (kleiner)
    ellipse_center = (size // 2, size // 2)
    ellipse_width = 60
    ellipse_height = 40

    ellipse_patch = patches.Ellipse(
        ellipse_center,
        width=ellipse_width,
        height=ellipse_height,
        edgecolor='black',
        facecolor='none',
        linewidth=2
    )
    emission_ax.add_patch(ellipse_patch)

    # Platzhalter für die Animation
    plot_placeholder = st.empty()

    for i in range(300):
        x, y = np.random.randint(0, size, 2)
        if np.random.rand() < activity[x, y] / np.max(activity):
            emission_ax.plot(y, x, 'o', color='dodgerblue', alpha=0.5, markersize=4)

        if i % 10 == 0:
            plot_placeholder.pyplot(emission_fig)
        time.sleep(0.01)

    # Finale Darstellung
    plot_placeholder.pyplot(emission_fig)

st.markdown("---")
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe einer Schilddrüsen-Szintigraphie.")
