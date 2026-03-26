import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data_loader import load_rollout_data

st.set_page_config(layout="wide")
st.title("📈 Rollout Targeting Decision Engine")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data(ttl=600)
def load_data():
    return load_rollout_data()

df = load_data()

st.write(f"Rows loaded: {len(df):,}")

# -----------------------------
# Controls
# -----------------------------
selected_pct = st.slider("Select Top % of File", 5, 50, 20, 5)
avg_premium = st.slider("Avg Premium ($)", 200, 1200, 600, 50)
MAIL_COST = 0.47

# -----------------------------
# Ranking
# -----------------------------
df = df.sort_values("SCORE", ascending=False).copy()
df["RANK"] = np.arange(1, len(df)+1)
df["PCT_RANK"] = df["RANK"] / len(df)

df["IS_SELECTED"] = df["PCT_RANK"] <= (selected_pct / 100)
selected_df = df[df["IS_SELECTED"]]

# -----------------------------
# Baseline (robust)
# -----------------------------
baseline_df = df[df["MAILTYPE"].isin(["Mailed-Random", "Holdout-Random"])]

if len(baseline_df) > 100:
    baseline_rate = baseline_df["DIR_FP_QT"].mean()
else:
    baseline_rate = df["DIR_FP_QT"].mean()

# -----------------------------
# Direct Metrics
# -----------------------------
selected_rate = selected_df["DIR_FP_QT"].mean()
lift = selected_rate / baseline_rate if baseline_rate > 0 else 0

total_quotes = df["DIR_FP_QT"].sum()
selected_quotes = selected_df["DIR_FP_QT"].sum()

capture = selected_quotes / total_quotes if total_quotes > 0 else 0

# -----------------------------
# Mail + Cost
# -----------------------------
mailed = selected_df[selected_df["MAILTYPE"].isin(["Mailed-Selected", "Mailed-Random"])]

mail_volume = len(mailed)
mail_quotes = mailed["DIR_FP_QT"].sum()

cost = mail_volume * MAIL_COST

direct_cpq = cost / mail_quotes if mail_quotes > 0 else 0

# -----------------------------
# Incremental Metrics
# -----------------------------
expected = mail_volume * baseline_rate
incremental = mail_quotes - expected
incremental = max(incremental, 0)

incremental_rate = incremental / mail_volume if mail_volume > 0 else 0
incremental_cpq = cost / incremental if incremental > 0 else 0

# -----------------------------
# Revenue
# -----------------------------
direct_rev = mail_quotes * avg_premium
incremental_rev = incremental * avg_premium

roi = incremental_rev / cost if cost > 0 else 0

# -----------------------------
# Executive Summary
# -----------------------------
st.markdown("## 📌 Executive Summary")

st.markdown(f"""
Selecting **{selected_pct}%** of the file:

- Captures **{capture:.1%}** of total direct quotes  
- Produces **{lift:.2f}x lift vs baseline**  
- Direct Cost per Quote = **${direct_cpq:,.0f}**  
- Incremental Cost per Quote = **${incremental_cpq:,.0f}**  

👉 The model is concentrating conversions into a smaller, higher-performing segment.
""")

# -----------------------------
# Metrics
# -----------------------------
st.markdown("## 🎯 Performance")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Selected %", f"{selected_pct}%")
c2.metric("Capture %", f"{capture:.1%}")
c3.metric("Lift", f"{lift:.2f}x")
c4.metric("Direct Quotes", f"{int(selected_quotes):,}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Baseline Rate", f"{baseline_rate:.2%}")
c6.metric("Selected Rate", f"{selected_rate:.2%}")
c7.metric("Mail Cost", f"${cost:,.0f}")
c8.metric("Direct CPQ", f"${direct_cpq:,.0f}")

st.markdown("## 💡 Incremental Impact")

c9, c10, c11, c12 = st.columns(4)
c9.metric("Expected Quotes", f"{expected:,.1f}")
c10.metric("Incremental Quotes", f"{incremental:,.1f}")
c11.metric("Incremental Rate", f"{incremental_rate:.2%}")
c12.metric("Incremental CPQ", f"${incremental_cpq:,.0f}" if incremental > 0 else "N/A")

c13, c14, c15 = st.columns(3)
c13.metric("Direct Revenue", f"${direct_rev:,.0f}")
c14.metric("Incremental Revenue", f"${incremental_rev:,.0f}")
c15.metric("ROI", f"{roi:.2f}x")

# -----------------------------
# Decile Table
# -----------------------------
df["DECILE"] = pd.qcut(df["SCORE"], 10, labels=False, duplicates="drop") + 1

decile = (
    df.groupby("DECILE")
    .agg(
        COUNT=("IID_TXT", "count"),
        RATE=("DIR_FP_QT", "mean")
    )
    .reset_index()
    .sort_values("DECILE", ascending=False)
)

decile["LIFT"] = decile["RATE"] / baseline_rate

st.subheader("📊 Decile Performance")
st.dataframe(decile, use_container_width=True)

# -----------------------------
# Lift Curve
# -----------------------------
curve = df.sort_values("SCORE", ascending=False).copy()

curve["CUM_QT"] = curve["DIR_FP_QT"].cumsum()
curve["CUM_CAPTURE"] = curve["CUM_QT"] / curve["DIR_FP_QT"].sum()
curve["PCT_FILE"] = np.arange(1, len(curve)+1) / len(curve)

fig, ax = plt.subplots()
ax.plot(curve["PCT_FILE"], curve["CUM_CAPTURE"])
ax.axvline(x=selected_pct/100, linestyle="--")
ax.set_xlabel("File %")
ax.set_ylabel("Capture %")

st.pyplot(fig)

# -----------------------------
# Optimization + Recommendation
# -----------------------------
opt = []

for pct in range(5, 55, 5):
    cutoff = df["SCORE"].quantile(1 - pct/100)
    tmp = df[df["SCORE"] >= cutoff]

    mailed_tmp = tmp[tmp["MAILTYPE"].isin(["Mailed-Selected", "Mailed-Random"])]
    vol = len(mailed_tmp)
    qt = mailed_tmp["DIR_FP_QT"].sum()

    c = vol * MAIL_COST
    exp = vol * baseline_rate
    incr = max(qt - exp, 0)

    roi_val = (incr * avg_premium) / c if c > 0 else 0

    opt.append((pct, vol, qt, incr, roi_val))

opt_df = pd.DataFrame(opt, columns=["Pct", "Volume", "Quotes", "Incremental", "ROI"])

best = opt_df.loc[opt_df["ROI"].idxmax()]

# 🔥 Recommendation Banner
st.success(
    f"Recommended Selection: {int(best['Pct'])}% "
    f"(Max ROI = {best['ROI']:.2f}x)"
)

# Optional detail table
st.subheader("📊 ROI by Selection %")
st.dataframe(opt_df, use_container_width=True)