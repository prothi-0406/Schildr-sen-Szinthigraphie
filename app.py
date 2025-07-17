# Schildr-sen-Szinthigraphie
import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt 
import time 
st.set_page_config(page_title="Schilddrüsenszintigraphie-Simulation", layout="wide") 
st.title("Schilddrüsenszintigraphie – Physikalische Prozesse (Simulation)") 
st.markdown(""" 
Diese interaktive Simulation zeigt die physikalischen Abläufe einer 
Schilddrüsenszintigraphie: - **Aufnahme des Radiopharmakons** - **Radioaktiver Zerfall und Gamma-Emission** - **Bildentstehung durch eine Gamma-Kamera** 
""") 
# Auswahl des Radiopharmakons 
pharmakon = st.selectbox("Radiopharmakon auswählen:", ["Technetium-99m", "Jod123"]) 
halbwertszeit = {"Technetium-99m": 6.01, "Jod-123": 13.2}[pharmakon] 
st.write(f"Halbwertszeit von **{pharmakon}**: {halbwertszeit} Stunden") 
# Zerfallskurve 
st.subheader("Zerfall des Radiopharmakons") 
t = np.linspace(0, 24, 100) 
NO = 1000 
N = NO * np.exp(-np.log(2) * t / halbwertszeit) 

 fig1, ax1 = plt.subplots() 
ax1.plot(t, N, label="Anzahl radioaktiver Atome") 
ax1.set_xlabel("Zeit (h)") 
ax1.set_ylabel("Restaktivität") 
ax1.set_title("Exponentieller Zerfall") 
ax1.grid(True) 
st.pyplot(fig1) 
# Schilddrüsengewebe: Aktivitätsverteilung 
st.subheader("Verteilung im Schilddrüsengewebe") 
size = 100 
activity = np.random.normal(loc=20, scale=5, size=(size, size)) 
# Heiße Region (autonomes Adenom) 
activity[40:60, 40:60] += 100 
# Kalte Region (kalter Knoten) 
activity[20:30, 70:80] -= 15 
# Simuliere Detektion 
detected = np.clip(activity + np.random.normal(0, 5, (size, size)), 0, None) 
f
 ig2, ax2 = plt.subplots() 
im = ax2.imshow(detected, cmap="hot", interpolation="nearest") 
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung") 
ax2.set_title("Simuliertes Szintigramm") 
st.pyplot(fig2) 
# Animation: Gamma-Emissionen (vereinfacht) 
st.subheader(" Animation: Gamma-Emissionen") 
 
if st.button(" Emissionen starten"): 
    emission_fig, emission_ax = plt.subplots() 
    emission_ax.set_xlim(0, size) 
    emission_ax.set_ylim(0, size) 
    emission_ax.set_title("Gamma-Emissionen (vereinfachte Darstellung)") 
 
    # Plot-Container für Animation 
    plot_placeholder = st.empty() 
 
    for i in range(100): 
        x, y = np.random.randint(0, size, 2) 
        if np.random.rand() < activity[x, y] / np.max(activity): 
            emission_ax.plot(y, x, 'bo', alpha=0.4) 
        if i % 5 == 0: 
            plot_placeholder.pyplot(emission_fig) 
        time.sleep(0.01) 
 
    # Finales Bild anzeigen 
    plot_placeholder.pyplot(emission_fig) 
 
st.markdown("---") 
st.info("Diese Simulation dient der Lehre und veranschaulicht vereinfacht die Abläufe 
einer Schilddrüsenszintigraphie.")
