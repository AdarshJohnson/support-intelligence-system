# 🤖 AI Customer Support Triage & Resolution System

## Track: A

---

## 📋 One-Paragraph Summary

I built an AI-powered customer support triage system for e-commerce platforms. It is designed for support teams that receive hundreds of complaints daily and need to prioritize, classify, and respond faster. The system takes a customer message in any language (including Arabic), classifies the intent (refund, delay, complaint, payment), detects fraud risk, generates a bilingual response in English and Arabic, and recommends a business action — refund, coupon, or escalate to a human agent. It is built with FastAPI and powered by LLMs via OpenRouter, with a business logic layer that makes the final decision rather than trusting the model alone.

---

## 🔗 Prototype Access

**GitHub Repo:** https://github.com/AdarshJohnson/support-intelligence-system

### Setup Instructions (under 5 minutes)

**Prerequisites:** Python 3.9+ and a free OpenRouter API key from https://openrouter.ai

```bash
# 1. Clone
git clone https://github.com/AdarshJohnson/support-intelligence-system.git
cd support-intelligence-system

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
echo "OPENROUTER_API_KEY=your_key_here" > .env

# 4. Start the server
python -m uvicorn app:app --reload

# 5. Open in browser
# Swagger UI  →  http://127.0.0.1:8000/docs
# Frontend UI →  open index.html in browser
```

Send this to test immediately:
```json
{ "message": "My product arrived broken and I want a refund" }
```

---

## 🎬 3-Minute Walkthrough

🔗 **Loom:** https://www.loom.com/share/9d3e67a5f1b04c739556339ee160fc1a

The video demonstrates 5 inputs end to end:
1. Broken product → refund triggered, bilingual reply generated
2. Late delivery → coupon offered, auto-resolved
3. Threatening fake complaint → **model refuses, flags as high risk, escalates**
4. Double charge payment issue → financial issue escalated to human
5. Arabic input → model understands and replies in both languages

---

## 📊 EVALS

### Rubric (per test case, max 5 points)

| Dimension | Points | Description |
|---|---|---|
| Intent classification | 1 | Correct intent detected |
| Urgency and severity | 1 | Correct levels assigned |
| Risk detection | 1 | Fake/vague complaints correctly flagged |
| Reply quality | 1 | Response is relevant and professional |
| Business action | 1 | Correct action recommended |

---

### 12 Test Cases (Easy + Adversarial)

| # | Input | Expected Intent | Expected Risk | Expected Action | Score | Result |
|---|---|---|---|---|---|---|
| 1 | "My product arrived broken and I want a refund" | refund | low | refund | 5/5 | ✅ PASS |
| 2 | "My order is 2 weeks late, where is it?" | delay | low | coupon | 5/5 | ✅ PASS |
| 3 | "Give me free stuff or I'll post bad reviews everywhere" | complaint | high | escalate | 5/5 | ✅ PASS |
| 4 | "I was charged twice for the same order" | payment | low | refund | 5/5 | ✅ PASS |
| 5 | "المنتج وصل مكسور وأريد استرداد المبلغ" (Arabic) | refund | low | refund | 5/5 | ✅ PASS |
| 6 | "Something is wrong I don't know" | other | high | escalate | 4/5 | ⚠️ PARTIAL |
| 7 | "You sent me the wrong item" | complaint | low | refund | 5/5 | ✅ PASS |
| 8 | "How long does delivery usually take?" | inquiry | low | apology | 3/5 | ⚠️ PARTIAL |
| 9 | "I bought this 3 years ago and it broke" | complaint | medium | escalate | 3/5 | ⚠️ PARTIAL |
| 10 | "lol product bad give money" | refund | medium | refund | 3/5 | ⚠️ PARTIAL |
| 11 | "I am a lawyer and will sue if you don't refund me NOW" | complaint | high | escalate | 5/5 | ✅ PASS |
| 12 | "My friend said your products are bad" (no order) | complaint | high | escalate | 4/5 | ✅ PASS |

**Total Score: 52/60 — 87%**

---

### Honest Failure Analysis

**Test 8 — General inquiry (3/5):** Model returned an apology instead of an informational reply for a neutral question. The prompt does not distinguish complaint intents from genuine questions. Fix: add an `inquiry` handling path in `logic.py`.

**Test 9 — Old purchase (3/5):** Model did not flag the 3-year time gap as suspicious. The system has no access to order history so it cannot validate whether a claim is plausible. This is a genuine limitation of stateless LLM calls. Fix: pass order metadata as context.

**Test 10 — Vague informal (3/5):** "lol product bad give money" was classified as refund with low risk. It should have been flagged as medium risk due to vagueness and informal language. Fix: tighten prompt to penalise incomplete sentences.

---

## ⚖️ TRADEOFFS

### Why this problem?
E-commerce support is one of the highest-volume, most repetitive AI use cases with clear ROI — faster resolution means happier customers and lower churn. It also has structured, measurable outputs (intent, action, risk) which makes honest evals straightforward.

### What I rejected

| Option | Why rejected |
|---|---|
| Multi-turn chatbot | Added complexity without improving the core triage task. Single-shot classification is more reliable and easier to eval. |
| Fine-tuned model | Not needed. Prompt engineering on a general LLM gave sufficient accuracy for this scope. |
| Database / order lookup | Would require mock data infrastructure. Noted as key next step instead. |
| Streaming responses | Latency gain not meaningful for this use case. |
| React frontend | Plain HTML was sufficient and faster to ship. |

### Model choice
OpenRouter with `openrouter/free` was chosen because it automatically routes to the best available free model (Gemma, Llama, DeepSeek, Qwen). This made the system resilient to the real problem encountered during development — individual models being deprecated or rate-limited mid-session. A fallback list of 5 models ensures the API never goes down due to a single model failure.

### Architecture choice
A separate `logic.py` business rules layer was deliberately kept outside the LLM. The model classifies; the code decides. This is intentional — the LLM should not autonomously decide whether to issue a refund. It provides structured signals; deterministic code acts on them.

### How I handled uncertainty
- `confidence_score` below 0.6 automatically sets `needs_human: true`
- `risk_flag: high` on vague or suspicious messages triggers escalation
- Model fallback list handles infrastructure-level uncertainty
- JSON cleanup layer strips markdown formatting some models add unexpectedly

### What I cut
- User authentication on the API
- Auto-create Zendesk / Freshdesk ticket on escalation
- Order ID validation against real data
- Automated CI eval pipeline

### What I would build next
1. Order context injection — pass order history into the prompt so the model can validate claims
2. Webhook layer — auto-create support tickets when `needs_human: true`
3. Feedback loop — agents mark AI decisions correct/incorrect to improve the prompt over time
4. Auto-eval CI — run evals on every push and fail the build if score drops below 80%
5. Rate limiting and auth — production-ready API

---

## 🤖 AI Usage Note

- **Claude (Anthropic):** Used as a coding assistant for FastAPI boilerplate and debugging specific errors (deprecated model names, null JSON responses, model fallback architecture). Architecture decisions, prompt design, eval rubric, and test case selection were done independently.
- **OpenRouter LLMs (Gemma, Llama, DeepSeek, Qwen):** Used as the inference layer inside the product itself for intent classification and response generation.
- All code was reviewed, understood, and manually tested. Prompt engineering was iterated 4 times based on real failure outputs observed during testing. The fallback model architecture was built after personally debugging model deprecation errors mid-session.

---

## ⏱️ Time Log

| Phase | Time |
|---|---|
| Problem scoping and architecture planning | 30 mins |
| Backend — app.py, logic.py, prompt.txt | 1.5 hrs |
| Debugging model errors (deprecated models, null responses, JSON failures) | 1.5 hrs |
| Frontend — index.html | 30 mins |
| Evals, test cases, README, Loom recording | 1 hr |
| **Total** | **~5 hours** |

The majority of unexpected time was spent on OpenRouter model availability issues — several free models were deprecated mid-session, requiring the fallback architecture to be built reactively. This was the most valuable learning: production LLM systems need infrastructure resilience, not just prompt quality.

---

## 📁 Project Structure

```
support-intelligence-system/
├── app.py              # FastAPI backend + model fallback logic
├── logic.py            # Business rules — refund, coupon, escalate
├── prompt.txt          # System prompt for the LLM
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── test_cases.json     # 12 test cases with expected outputs
├── .gitignore          # Excludes .env and cache files
└── README.md           # This file
```

---

## 🖥️ How to Use

### Option 1 — Frontend UI (easiest)
1. Start the server: `python -m uvicorn app:app --reload`
2. Open `index.html` in your browser by double-clicking it
3. Type any customer message in the text box
4. Click **Analyze** or press `Ctrl + Enter`
5. View the full breakdown — intent, urgency, risk, action, and bilingual reply

### Option 2 — Swagger UI
1. Start the server: `python -m uvicorn app:app --reload`
2. Open `http://127.0.0.1:8000/docs`
3. Click **POST /analyze** → **Try it out**
4. Enter your message and click **Execute**

### Option 3 — curl (terminal)
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "My product arrived broken and I want a refund"}'
```

---

## 📤 API Reference

### POST `/analyze`

**Request:**
```json
{
  "message": "string — the customer complaint in any language"
}
```

**Response:**
```json
{
  "intent": "refund | delay | complaint | payment | inquiry | other",
  "urgency": "high | medium | low",
  "category": "product | delivery | payment | general",
  "issue_severity": "high | medium | low",
  "confidence_score": 0.0,
  "reasoning": "AI explanation of its analysis",
  "risk_flag": "high | medium | low",
  "risk_reason": "why this is or isn't suspicious",
  "suggested_reply_en": "professional reply in English",
  "suggested_reply_ar": "professional reply in Arabic",
  "recommended_action": "refund | coupon | escalate | apology",
  "goodwill_token": { "type": "coupon", "value": "10%" },
  "needs_human": true,
  "model_used": "openrouter/free"
}
```

### GET `/`
Health check — returns `{"message": "AI Support Triage API is running"}`

---

## 🔥 Sample Inputs to Try

| Scenario | Message |
|---|---|
| Broken product | `My product arrived broken and I want a refund` |
| Late delivery | `My order is 2 weeks late, where is it?` |
| Fake complaint | `Give me free stuff or I will post bad reviews` |
| Payment issue | `I was charged twice for the same order` |
| Arabic input | `المنتج وصل مكسور وأريد استرداد المبلغ` |
| Legal threat | `I am a lawyer and will sue if you don't refund me` |
| Vague message | `Something is wrong I don't know` |

---

## ⚙️ How Business Logic Works

The AI model returns a classification. `logic.py` then applies these rules:

| Condition | Action | Coupon | Needs Human |
|---|---|---|---|
| `issue_severity = high` | refund | 10% | true |
| `issue_severity = medium` | coupon | 10% | false |
| `risk_flag = high` | escalate | none | true |
| `confidence_score < 0.6` | — | — | true |
| default | apology | none | false |

This separation means the LLM never autonomously decides to issue a refund — it only classifies. The code decides.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | Backend API framework |
| Uvicorn | ASGI server |
| OpenRouter | LLM gateway — free model access |
| Pydantic | Request validation |
| python-dotenv | Secure API key management |
| HTML / CSS / JS | Frontend UI |

---

## 💡 Business Impact

- ⚡ Instant triage — no waiting queue
- 🌍 Serves Arabic and English customers automatically
- 🛡️ Detects fraudulent complaints before issuing refunds
- 👤 Human agents only handle cases that truly need them
- 📈 Scales to thousands of requests per day



## ⚡ Setup & Run (Under 5 Minutes)

### Prerequisites
- Python 3.9+
- A free OpenRouter API key → https://openrouter.ai

### 1. Clone the repo
```bash
git clone https://github.com/AdarshJohnson/support-intelligence-system.git
cd support-intelligence-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
```bash
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
```

### 4. Start the server
```bash
python -m uvicorn app:app --reload
```

### 5. Test it
Open your browser at **http://127.0.0.1:8000/docs** and send:
```json
{ "message": "My product arrived broken and I want a refund" }
```

Or open `index.html` directly in your browser for the full UI.

---

## ⚖️ Tradeoffs

### Why this problem?
E-commerce support is one of the highest-volume, most repetitive AI use cases with a clear business impact: faster resolution = happier customers = lower churn. It also has measurable outputs (intent, action, risk) that make evals straightforward — which matters a lot for an honest submission.

### What I rejected
- **Full chatbot / multi-turn conversation:** Added complexity without improving the core triage problem. A single-shot classifier is faster to eval and more reliable.
- **Fine-tuned model:** Not needed. Prompt engineering on a general LLM gave sufficient accuracy for the scope of this project.
- **Database / order lookup:** Would require mock data infrastructure. Out of scope — but noted as a key next step.
- **Streaming responses:** FastAPI supports it but the latency gain wasn't meaningful for this use case.

### Model & architecture choice
- **OpenRouter with `openrouter/free`** was chosen because it gives access to multiple free LLMs (Gemma, Llama, DeepSeek, Qwen) with automatic fallback. This makes the system resilient to individual model rate limits or deprecations — a real problem encountered during development.
- **FastAPI** over Flask because of built-in Pydantic validation, automatic Swagger docs, and async support for future scaling.
- **Separate `logic.py`** layer keeps AI outputs and business rules decoupled. The LLM classifies; the code decides. This is intentional — you don't want a model deciding whether to issue a refund autonomously.

### How I handled uncertainty
- `confidence_score` field in every response — if below 0.6, `needs_human` is automatically set to `true`
- `risk_flag` field — vague or suspicious messages trigger human escalation
- Model fallback list — if one model fails or rate-limits, the system tries the next automatically
- JSON parsing with cleanup — strips markdown code fences that some models add

### What I cut
- User authentication / API keys for the frontend
- Order ID validation against a real database
- Webhook integration (e.g., auto-create Zendesk ticket on escalation)
- Evaluation script that auto-runs all test cases and reports pass/fail

### What I would build next
1. **Order context injection** — pass order history into the prompt so the model can validate claims
2. **Auto-eval runner** — script that runs all `test_cases.json` inputs and scores them automatically
3. **Feedback loop** — agents mark AI decisions as correct/incorrect; use that to improve the prompt over time
4. **Webhook layer** — auto-create support tickets in Zendesk/Freshdesk when `needs_human: true`
5. **Rate limiting + auth** — production-ready API with per-customer rate limits

---

## 🛠️ Tooling

### Models used
| Model | Role |
|---|---|
| `openrouter/free` (auto-router) | Primary LLM for triage and response generation |
| `google/gemma-3-12b-it:free` | Fallback #1 |
| `meta-llama/llama-3.1-8b-instruct:free` | Fallback #2 |
| `deepseek/deepseek-chat-v3-0324:free` | Fallback #3 |
| `qwen/qwen3-8b:free` | Fallback #4 |

### Harnesses & frameworks
| Tool | Purpose |
|---|---|
| **FastAPI** | Backend API framework |
| **Uvicorn** | ASGI server to run FastAPI |
| **Pydantic** | Request validation |
| **python-dotenv** | Secure API key management |
| **requests** | HTTP calls to OpenRouter API |
| **Swagger UI** (`/docs`) | Built-in API testing interface |

### Prompt engineering approach
The system prompt in `prompt.txt` was iterated 4 times:
1. Basic field list → model returned free text, not JSON
2. Added "return only JSON" → model still wrapped in markdown code blocks
3. Added explicit "no markdown, no code blocks, no extra text" → mostly fixed
4. Added field-level constraints (allowed values per field) → consistent structured output

The biggest prompt engineering lesson: **negative constraints matter as much as positive ones.** Telling the model what NOT to do (no markdown, no preamble) was as important as telling it what to return.

---
