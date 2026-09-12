import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="CyberScan AI",
    page_icon="🛡️",
    layout="wide"
)
# =====================================================
# LOAD MODEL FILES
# =====================================================
rf_model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("selected_features.pkl")

X_sample = joblib.load("X_sample.pkl")
y_sample = joblib.load("y_sample.pkl")   # 🔴 REQUIRED for colors

# =====================================================
# FEATURE MEANINGS
# =====================================================
feature_info = {
    "src_bytes": ("Data sent from your device", "Web browsing: 200–3000"),
    "dst_bytes": ("Data received from server", "Web browsing: 500–8000"),
    "count": ("Rapid connection attempts", "Normal: < 20"),
    "srv_count": ("Connections to same service", "Normal: < 20"),
    "same_srv_rate": ("Same service usage ratio", "0.4 – 1.0"),
    "diff_srv_rate": ("Service switching ratio", "0 – 0.4"),
    "serror_rate": ("Connection error rate", "0 normally"),
    "srv_serror_rate": ("Service error rate", "0 normally"),
    "dst_host_count": ("Connections to server", "Normal: < 100"),
    "dst_host_srv_count": ("Connections to service", "Normal: < 100"),
    "dst_host_same_srv_rate": ("Same service ratio", "0.4 – 1.0"),
    "dst_host_diff_srv_rate": ("Different service ratio", "0 – 0.4"),
    "dst_host_serror_rate": ("Server error ratio", "0 normally"),
    "dst_host_srv_serror_rate": ("Service error ratio", "0 normally"),
    "dst_host_same_src_port_rate": ("Same port reuse", "0 – 0.8")
}

# =====================================================
# SAMPLE CASES (AUTO-FILL ALL 15 FEATURES)
# =====================================================
sample_cases = {
    "Normal – Web Browsing": dict(src_bytes=400, dst_bytes=2000, count=6, srv_count=6),
    "Normal – Streaming": dict(src_bytes=2500, dst_bytes=7200, count=10, srv_count=10),
    "Normal – Office Network": dict(src_bytes=900, dst_bytes=4000, count=12, srv_count=12),

    "Malicious – Brute Force": dict(
        src_bytes=40, dst_bytes=20, count=150, srv_count=150,
        diff_srv_rate=0.9, serror_rate=0.6
    ),
    "Malicious – DoS Flood": dict(
        src_bytes=10, dst_bytes=5, count=300, srv_count=300,
        diff_srv_rate=0.95
    ),
    "Malicious – Port Scan": dict(
        src_bytes=60, dst_bytes=30, count=180, srv_count=160,
        diff_srv_rate=0.85
    )
}

# =====================================================
# CYBER GLASS UI (UNCHANGED)
# =====================================================
st.markdown("""
<style>
html, body {
    background:
        radial-gradient(circle at top, #1b1f3b, #05060d),
        linear-gradient(120deg, rgba(124,58,237,0.15), rgba(37,99,235,0.15));
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
}
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(22px);
    border-radius: 22px;
    padding: 2rem;
    margin-bottom: 1.8rem;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.06),
        0 30px 80px rgba(0,0,0,0.7);
    transition: all 0.4s ease;
}
.glass:hover {
    transform: translateY(-6px) scale(1.01);
}
h1 {
    font-size: 3rem;
    background: linear-gradient(90deg,#a78bfa,#60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3, p, label { color: #e0e7ff; }
button {
    border-radius: 14px !important;
    background: linear-gradient(135deg,#7c3aed,#2563eb) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🧠 Model Panel")
st.sidebar.markdown("""
**Model:** Random Forest  
**Dataset:** NSL‑KDD  
**Features:** 15  
**Accuracy:** ~69%  
""")

st.sidebar.subheader("🧪 Sample Scans")
for name, vals in sample_cases.items():
    if st.sidebar.button(name):
        # 🔒 ensures ALL 15 features always exist
        st.session_state.inputs = {f: float(vals.get(f, 0)) for f in features}
        st.session_state.step = len(features) - 1
        st.rerun()

# =====================================================
# SESSION STATE
# =====================================================
if "step" not in st.session_state:
    st.session_state.step = 0
if "inputs" not in st.session_state:
    st.session_state.inputs = {}

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1>🛡️ CyberScan AI</h1>", unsafe_allow_html=True)
st.caption("A modern, interactive network security scanner")

# =====================================================
# CAROUSEL INPUT
# =====================================================
current_feature = features[st.session_state.step]
meaning, example = feature_info.get(current_feature, ("Network value", ""))

st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader(f"Step {st.session_state.step + 1} of {len(features)}")
st.write(f"**{current_feature.replace('_',' ').title()}**")
st.write(f"📘 {meaning}")
st.caption(f"💡 Example: {example}")

val = st.number_input(
    "Enter value",
    min_value=0.0,
    value=float(st.session_state.inputs.get(current_feature, 0)),
    step=1.0
)
st.session_state.inputs[current_feature] = val

c1, c2 = st.columns(2)
with c1:
    if st.button("⬅ Previous") and st.session_state.step > 0:
        st.session_state.step -= 1
        st.rerun()
with c2:
    if st.button("Next ➡") and st.session_state.step < len(features) - 1:
        st.session_state.step += 1
        st.rerun()

st.progress((st.session_state.step + 1) / len(features))
st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# RESULT + PIE + PCA
# =====================================================
if st.session_state.step == len(features) - 1:
    X_user = np.array([st.session_state.inputs[f] for f in features]).reshape(1, -1)

    if np.sum(X_user) == 0:
        st.error("❌ Invalid input: all values cannot be zero.")
    else:
        X_scaled = scaler.transform(X_user)
        prob = rf_model.predict_proba(X_scaled)[0]
        pred = np.argmax(prob)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("🔍 Scan Result")

        if pred == 1:
            st.markdown(
                f"<h2 style='color:#ff4d4d; text-shadow:0 0 30px red;'>🚨 MALICIOUS ({prob[1]*100:.1f}%)</h2>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<h2 style='color:#4ade80; text-shadow:0 0 30px #4ade80;'>✅ NORMAL ({prob[0]*100:.1f}%)</h2>",
                unsafe_allow_html=True
            )

        # PIE
        fig1, ax1 = plt.subplots(figsize=(3,3))
        ax1.pie(prob, labels=["Normal","Malicious"],
                autopct="%1.1f%%",
                colors=["#22c55e","#ef4444"])
        st.pyplot(fig1)

        # PCA WITH SEPARATE COLORS
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X_sample)
        user_2d = pca.transform(X_scaled)

        fig2, ax2 = plt.subplots(figsize=(4,4))
        ax2.scatter(X_2d[y_sample==0,0], X_2d[y_sample==0,1],
                    c="#22c55e", alpha=0.25, s=10, label="Benign")
        ax2.scatter(X_2d[y_sample==1,0], X_2d[y_sample==1,1],
                    c="#ef4444", alpha=0.25, s=10, label="Malicious")
        ax2.scatter(user_2d[:,0], user_2d[:,1],
                    c="red", s=140, edgecolors="red", linewidths=2,
                    label="Your Scan")

        ax2.set_xticks([]); ax2.set_yticks([])
        ax2.set_title("Traffic Position")
        ax2.legend(frameon=False)

        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)
