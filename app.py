# Schilddrüsenszintigraphie – Finalversion

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

# Pathologie-Auswahl
st.subheader("🧠 Pathologisches Muster auswählen")
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

if pathologie == "Autonomes Adenom (heißer Knoten)":
    activity[45:55, 40:60] += 80
elif pathologie == "Kalter Knoten":
    activity[25:35, 65:75] -= 18
elif pathologie == "M. Basedow (diffus heiß)":
    activity[ellipse_mask] += 30

activity = np.clip(activity, 0, None)

# Szintigramm-Darstellung
st.subheader("📍 Simuliertes Szintigramm")

detected = np.clip(activity + np.random.normal(0, 4, (size, size)), 0, None)

fig2, ax2 = plt.subplots()
im = ax2.imshow(detected, cmap="plasma", interpolation="nearest")
plt.colorbar(im, ax=ax2, label="Detektierte Strahlung (a.u.)")
ax2.set_title(f"Simuliertes Szintigramm – {pathologie}")
ax2.axis("off")
st.pyplot(fig2)

# Gamma-Emission mit Punkten + Rahmenellipse
st.subheader("💥 Gamma-Emissionen mit Punkt + Schilddrüsenrahmen")

if st.button("Emissionen anzeigen"):
    emission_fig, emission_ax = plt.subplots()
    emission_ax.set_xlim(0, size)
    emission_ax.set_ylim(0, size)
    emission_ax.set_title("Simulierte Gamma-Emissionen (farbige Punkte mit Ellipsen-Rahmen)")
    emission_ax.axis("off")
    plot_placeholder = st.empty()

    xs = []
    ys = []
    colors = []

    for i in range(300):
        x, y = np.random.randint(0, size, 2)
        if ellipse_mask[x, y] and np.random.rand() < activity[x, y] / np.max(activity):
            val = activity[x, y]
            norm_val = val / np.max(activity)

            if norm_val > 0.8:
                color = 'red'
            elif norm_val > 0.4:
                color = 'orange'
            else:
                color = 'blue'

            xs.append(y)
            ys.append(x)
            colors.append(color)

        if i % 10 == 0:
            emission_ax.clear()
            emission_ax.set_xlim(0, size)
            emission_ax.set_ylim(0, size)
            emission_ax.axis("off")
            emission_ax.set_title("Simulierte Gamma-Emissionen")
            emission_ax.scatter(xs, ys, color=colors, s=10, alpha=0.8)

            ellipse = patches.Ellipse(
                (size / 2, size / 2),
                width=0.7 * size * 2,
                height=0.4 * size * 2,
                edgecolor='black',
                facecolor='none',
                linewidth=1.5,
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
    emission_ax.scatter(xs, ys, color=colors, s=10, alpha=0.8)

    ellipse = patches.Ellipse(
        (size / 2, size / 2),
        width=0.7 * size * 2,
        height=0.4 * size * 2,
        edgecolor='black',
        facecolor='none',
        linewidth=1.5,
        linestyle='--'
    )
    emission_ax.add_patch(ellipse)

    plot_placeholder.pyplot(emission_fig)

    # Farblegende
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
