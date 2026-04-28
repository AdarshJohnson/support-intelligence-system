# 🤖 AI Customer Support Triage & Resolution System

An intelligent backend system that automatically analyzes customer complaints, classifies issues, detects fraud risk, generates bilingual responses, and recommends business actions — powered by LLMs via OpenRouter and built with FastAPI.

---

## 🎯 Problem Statement

E-commerce platforms receive thousands of customer queries daily. Manual support is slow, expensive, and struggles to prioritize urgent cases like damaged products or payment failures.

This system solves that by:
- Automatically understanding customer intent
- Detecting urgency and severity
- Flagging suspicious or fake complaints
- Generating instant responses in **English and Arabic**
- Recommending actions: refund, coupon, or escalate

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🧠 Intent Classification | Detects refund, delay, complaint, payment, inquiry |
| 🔥 Urgency Detection | Rates urgency as high / medium / low |
| 🚨 Risk Flagging | Identifies fake or vague complaints |
| 🌍 Bilingual Responses | Replies in both English and Arabic |
| ⚙️ Business Logic | Auto-assigns refund, coupon, or escalation |
| 👤 Human-in-the-loop | Escalates critical cases to human agents |
| 🔄 Model Fallback | Tries multiple free LLMs automatically |

---

## 🏗️ System Architecture

```
Customer Message
      ↓
FastAPI Backend (app.py)
      ↓
OpenRouter API (LLM)
      ↓
AI JSON Response
      ↓
Business Logic Layer (logic.py)
      ↓
Final Decision + Bilingual Reply
```

---

## 🤖 AI Model

This project uses **OpenRouter** as the LLM gateway with automatic model fallback:

| Priority | Model |
|---|---|
| 1st | `openrouter/free` (auto-selects best available) |
| 2nd | `google/gemma-3-12b-it:free` |
| 3rd | `meta-llama/llama-3.1-8b-instruct:free` |
| 4th | `deepseek/deepseek-chat-v3-0324:free` |
| 5th | `qwen/qwen3-8b:free` |

If one model is rate-limited or unavailable, the system automatically tries the next one.

---

## 📁 Project Structure

```
support-intelligence-system/
├── app.py              # FastAPI backend + model fallback logic
├── logic.py            # Business rules (refund, coupon, escalate)
├── prompt.txt          # System prompt for the AI model
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed to git)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/support-intelligence-system.git
cd support-intelligence-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your free API key at: https://openrouter.ai

### 4. Run the server
```bash
python -m uvicorn app:app --reload
```

### 5. Open API docs
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Test Cases

### Input
```json
{ "message": "My product arrived broken and I want a refund" }
```

### Output
```json
{
  "intent": "refund",
  "urgency": "high",
  "category": "product",
  "issue_severity": "high",
  "confidence_score": 1.0,
  "reasoning": "Customer clearly states product is broken and requests refund.",
  "risk_flag": "low",
  "risk_reason": "Specific, legitimate complaint with no signs of manipulation.",
  "suggested_reply_en": "We sincerely apologize. Please share your order number and a photo of the damaged product, and we will process your refund within 1-2 business days.",
  "suggested_reply_ar": "نعتذر بصدق. يرجى مشاركة رقم طلبك وصورة للمنتج التالف وسنعالج طلب الاسترداد خلال 1-2 يوم عمل.",
  "recommended_action": "refund",
  "goodwill_token": { "type": "coupon", "value": "10%" },
  "needs_human": true,
  "model_used": "openrouter/free"
}
```

---

## 🔥 More Test Cases

| Message | Expected Action |
|---|---|
| "Product arrived broken" | Refund + escalate |
| "My order is 2 weeks late" | Coupon + apology |
| "Give me free stuff or I'll leave a bad review" | Escalate (high risk) |
| "المنتج وصل مكسور" | Refund (Arabic input) |
| "I don't know something is wrong" | High risk (vague) |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **AI Gateway:** OpenRouter (free LLMs)
- **Language Models:** Gemma, Llama, DeepSeek, Qwen (auto-selected)
- **Environment:** python-dotenv
- **API Testing:** FastAPI Swagger UI

---

## 💡 Business Impact

- ⚡ Reduces manual support workload
- 🕐 Instant response — no waiting queue
- 🌍 Serves Arabic and English customers
- 🛡️ Detects fraudulent complaints automatically
- 📈 Scalable to thousands of requests per day

---

## 👤 Author

Built as an AI engineering project demonstrating real-world LLM integration, prompt engineering, and backend API design.