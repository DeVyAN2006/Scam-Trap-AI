# ScamTrap AI 🪤

> A honeypot system that turns scammers into data.

---

## The Problem

A family member of mine was targeted by a scammer. That incident pushed me to look deeper into the scale of this issue — and the numbers were staggering.

> 🇮🇳 In 2025 alone, India recorded **28 lakh phishing cases** resulting in **₹22,495 crore in losses.**

Yet despite this scale, there is almost **no structured data** on how scammers actually operate — what language they use, how they respond to pushback, what psychological tactics they deploy, and how conversations evolve over time.

ScamTrap AI is my attempt to change that.

---

## What Is ScamTrap AI?

ScamTrap AI is an intelligent honeypot system that **simulates realistic user interactions with scammers**, engages them in conversation using an LLM, and extracts structured signals from their responses — building a dataset of real fraudulent communication patterns.

It doesn't just block scams. It **studies them.**

---

## What It Does

- 🤖 Simulates believable human conversations with scammers
- 💬 Generates context-aware replies to keep scammers engaged
- 🔍 Extracts key fraud signals from conversations:
  - UPI IDs
  - Bank account numbers
  - IFSC codes
  - Phishing links
- 📊 Applies keyword heuristics and regex-based pattern matching with **confidence scoring**
- 🗄️ Stores all interactions as **structured data** for analysis and research

---

## How It Works

```
Incoming Scam Message
        ↓
LLM generates a context-aware reply
        ↓
Conversation continues to simulate human behavior
        ↓
Responses analyzed via Regex + Heuristic Rules
        ↓
Sensitive entities extracted (UPI, IFSC, links, etc.)
        ↓
Structured data stored for analysis
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI (deployed on Render) |
| **Frontend** | Netlify Dashboard |
| **Core Logic** | Python, Regex, Heuristics |
| **AI Layer** | LLM-based response generation |

---

## Current Progress

- ✅ Built and deployed an initial working prototype
- ✅ Tested on **20+ real scam messages**
- 🔄 Actively collecting and structuring interaction data

---

## Future Work

- [ ] Improve scam classification accuracy with ML models
- [ ] Expand the dataset of scam interactions across categories (banking, KYC, lottery, etc.)
- [ ] Identify and map recurring scam strategies and conversation flows
- [ ] Build detection and prevention tools powered by collected data
- [ ] Publish anonymized dataset for open research

---

## Why This Matters

Most anti-scam tools focus on **blocking** known threats. ScamTrap AI focuses on **understanding** them — because you can't build better defenses without knowing how attackers actually behave.

Every conversation ScamTrap engages in is a data point. Over time, that data becomes a resource for researchers, policymakers, and developers building the next generation of fraud detection systems.

---

## Status

🟢 **Actively being developed**

---

## Author

**Devyan Nitharwal**
[@DeVyAN2006](https://github.com/DeVyAN2006)
