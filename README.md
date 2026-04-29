# 🤖 AI Customer Support Triage & Resolution System

An intelligent backend that automatically classifies customer complaints, detects fraud risk, generates bilingual responses (English + Arabic), and recommends business actions — powered by LLMs via OpenRouter and built with FastAPI.

**Live demo:** Clone → install → run in under 5 minutes.

---

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

## 🧪 Evals — Rubric, Test Cases & Scores

### Scoring Rubric (per test case, max 5 points)

| Dimension | Points | Description |
|---|---|---|
| Intent Classification | 1 | Correct intent detected (refund, delay, complaint, etc.) |
| Urgency / Severity | 1 | Correct urgency and severity level |
| Risk Detection | 1 | Correctly flags fake/vague complaints |
| Response Quality | 1 | Suggested reply is relevant and professional |
| Business Action | 1 | Correct recommended action (refund/coupon/escalate) |

---

### Test Cases & Results

| # | Input | Expected Intent | Expected Risk | Expected Action | Score | Notes |
|---|---|---|---|---|---|---|
| 1 | "My product arrived broken and I want a refund" | refund | low | refund | ✅ 5/5 | Clear case, model handles perfectly |
| 2 | "My order is 2 weeks late, where is it?" | delay | low | coupon | ✅ 5/5 | Delay detected, coupon offered |
| 3 | "Give me free stuff or I'll leave bad reviews everywhere" | complaint | high | escalate | ✅ 5/5 | Correctly flagged as manipulative |
| 4 | "I was charged twice for the same order" | payment | low | refund | ✅ 5/5 | Payment issue escalated correctly |
| 5 | "المنتج وصل مكسور وأريد استرداد المبلغ" (Arabic) | refund | low | refund | ✅ 5/5 | Arabic input handled, bilingual reply generated |
| 6 | "Something is wrong I don't know" | other | high | escalate | ✅ 4/5 | Risk flagged correctly; action was escalate but reasoning was thin |
| 7 | "You sent the wrong item" | complaint | low | refund | ✅ 5/5 | Straightforward, handled well |
| 8 | "How long does delivery usually take?" | inquiry | low | apology | ⚠️ 3/5 | Model classified as inquiry correctly but suggested "apology" instead of an informational reply |
| 9 | "I bought this 3 years ago and it broke" (old purchase) | complaint | medium | escalate | ⚠️ 3/5 | Model did not flag time gap as risk; overconfident refund recommendation |
| 10 | "lol product bad give money" (vague/informal) | refund | medium | refund | ⚠️ 3/5 | Classified as refund but risk score was low; should be medium given vagueness |
| 11 | "I am a lawyer and will sue if you don't refund NOW" | complaint | high | escalate | ✅ 5/5 | Correctly identified legal threat; high urgency, escalated |
| 12 | "My friend said your products are bad" (hearsay, no order) | complaint | high | escalate | ✅ 4/5 | No order context flagged as high risk; good refusal to auto-resolve |

**Overall Score: 52/60 (87%)**

---

### Honest Failure Analysis

**Test 8 — General inquiry:** The model apologized instead of answering informationally. The prompt does not distinguish between complaint-type intents and genuine questions. Fix: add an `inquiry` handling path in `logic.py` that returns an informational reply instead of an apology.

**Test 9 — Old purchase:** The model missed the 3-year time gap entirely. It has no access to order history, so it cannot validate whether a claim is plausible. This is a genuine limitation of stateless LLM calls. Fix: pass order metadata as context if available.

**Test 10 — Vague/informal message:** The model was too lenient with informal language. It parsed "give money" as a refund intent without flagging uncertainty. The confidence score was 0.7 when it should have been lower. Fix: tighten the prompt to lower confidence on incomplete sentences.

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

### AI Assistants used
| Tool | How it was used |
|---|---|
| **Claude (Anthropic)** | Primary development assistant — architecture design, debugging FastAPI errors, writing and iterating the system prompt, generating test cases, writing this README |
| **OpenRouter** | LLM gateway — used to access multiple free models via a single API |

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

## 📁 Project Structure

```
support-intelligence-system/
├── app.py              # FastAPI backend + model fallback logic
├── logic.py            # Business rules (refund, coupon, escalate)
├── prompt.txt          # System prompt for the LLM
├── index.html          # Frontend UI
├── requirements.txt    # Python dependencies
├── test_cases.json     # 12 test cases with expected outputs
├── .gitignore          # Excludes .env and cache files
└── README.md           # This file
```

---

## 📊 Example Output

**Input:**
```json
{ "message": "My product arrived broken and I want a refund" }
```

**Output:**
```json
{
  "intent": "refund",
  "urgency": "high",
  "category": "product",
  "issue_severity": "high",
  "confidence_score": 1.0,
  "reasoning": "Customer clearly states product arrived broken and explicitly requests a refund.",
  "risk_flag": "low",
  "risk_reason": "Specific, legitimate complaint with no signs of manipulation.",
  "suggested_reply_en": "We sincerely apologize that your product arrived damaged. Please share your order number and a photo, and we will process your refund within 1-2 business days.",
  "suggested_reply_ar": "نعتذر بصدق. يرجى مشاركة رقم طلبك وصورة للمنتج التالف وسنعالج طلب الاسترداد خلال 1-2 يوم عمل.",
  "recommended_action": "refund",
  "goodwill_token": { "type": "coupon", "value": "10%" },
  "needs_human": true,
  "model_used": "openrouter/free"
}
```