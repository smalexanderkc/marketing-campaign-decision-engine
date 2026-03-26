📈 Rollout Targeting Engine

A decision-focused targeting system for optimizing direct mail campaigns using lift, incremental impact, and ROI modeling.

🚀 Overview

This project transforms a traditional predictive model into a business decision engine.

Instead of optimizing for accuracy alone, it enables marketers to:

Concentrate conversions into a smaller audience
Reduce wasted mail spend
Optimize targeting strategy based on ROI
🧠 Problem

Direct mail campaigns often:

Target too broadly
Have low precision
Waste budget on low-probability customers

👉 The goal:
Identify and prioritize high-conversion customers while minimizing cost.

⚙️ Solution

This app:

Scores the full population using a predictive model
Ranks customers by likelihood to convert
Simulates selection strategies (top 5%, 10%, 20%, etc.)
Evaluates performance using business-focused metrics
📊 Key Metrics

The system focuses on decision metrics, not just model metrics:

Lift vs Baseline
Conversion Capture (%)
Cost per Acquisition (CPQ)
Incremental Impact (vs random / holdout)
Revenue & ROI
💡 Example Insight

Selecting the top 20% of customers captures ~40% of conversions
with ~2x lift, while significantly reducing mail volume.

🔬 Incremental Measurement

To avoid misleading results:

Uses random / holdout groups as baseline
Estimates true incremental lift
Separates correlation vs causal impact
💰 Decision Engine

The app includes:

Mail cost modeling (~$0.47 per piece)
Revenue assumptions (premium per policy)
ROI optimization across selection thresholds

👉 Output:
Recommended targeting % that maximizes ROI

🖥️ App Features
Interactive selection threshold (slider)
Lift curve visualization
Decile performance table
ROI optimization engine
Real-time business impact metrics
🛠️ Tech Stack
Python
Streamlit
Pandas / NumPy
SQL Server (ODBC)
Matplotlib
▶️ Run Locally
cd C:\Users\xxxxx
streamlit run app.py
🎯 90-Second Walkthrough (Interview Ready)

Problem
“We were sending large volumes of direct mail with low precision, so I built a targeting system to concentrate conversions into a smaller, higher-performing segment.”

Approach
“I score the population, rank customers, and simulate different selection thresholds like top 10% or 20%.”

Metrics
“I focus on business impact — lift, capture rate, cost per acquisition, and incremental performance.”

Insight
“For example, selecting the top 20% captures ~40% of conversions with ~2x lift while reducing mail volume.”

Incrementality
“I compare against random and holdout groups to estimate true incremental lift.”

Decision Layer
“I added cost and revenue modeling to optimize for ROI, not just model accuracy.”

Close
“This turns the model into a decision engine where the business can choose the optimal strategy based on budget and goals.”

🔥 Why This Matters

This project demonstrates:

Transition from modeling → decision science
Focus on incremental impact (causal thinking)
Alignment with real business outcomes (ROI)

📌 Future Enhancements
A/B test simulation
Budget-constrained optimization
Multi-channel attribution
Automated campaign recommendations

👤 Author
Shawn Alexander
Senior Data Scientist | Marketing Analytics | Decision Science
