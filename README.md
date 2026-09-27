# 📈 Rollout Causal Uplift Targeting Engine

A decision-focused direct mail targeting system designed to identify customers whose probability of conversion is **increased by receiving a marketing treatment**.

## 🚀 Overview

Traditional propensity models answer:

> **Who is most likely to convert?**

This project addresses a more useful marketing question:

> **Who is more likely to convert because we mail them?**

The system uses historical treatment and holdout observations to estimate customer-level incremental response and prioritize customers based on the expected impact of the campaign rather than response probability alone.

The result is a targeting framework that separates customers who are naturally likely to convert from customers whose behavior may actually be changed by marketing.

---

## 🧠 Problem

A high-propensity customer is not necessarily a good marketing target.

Some customers may convert whether they receive direct mail or not. Mailing those customers increases campaign cost without necessarily creating incremental conversions.

The targeting problem therefore becomes:

**Identify customers with the greatest expected incremental response to treatment.**

---

## ⚙️ Modeling Approach

The model estimates two potential outcomes for each customer:

- **P(Response | Mailed)**
- **P(Response | Not Mailed)**

Customer-level uplift is then calculated as:

```text
UPLIFT_SCORE =
P(Response | Mailed)
-
P(Response | Not Mailed)
```

Customers are ranked by this estimated treatment effect.

A customer with high response probability but little difference between the two predictions may rank below a customer whose overall response probability is lower but whose behavior appears substantially more responsive to treatment.

---

## 🌲 Model

The targeting engine uses gradient-boosted decision trees with **XGBoost**.

The modeling workflow includes:

- Historical treatment and holdout observations
- Train/test separation
- Class-imbalance handling
- `
