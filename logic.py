import re
import os
import json
from typing import Tuple, Dict, List
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATA_FILE = "data.json"

# -----------------------------
# Load stored data
# -----------------------------
try:
    with open(DATA_FILE, "r") as f:
        raw = json.load(f)
        _conversation_entities = {
            k: {kk: set(vv) for kk, vv in v.items()}
            for k, v in raw.items()
        }
except:
    _conversation_entities = {}

_conversation_states = {}
_conversation_history = {}

# -----------------------------
# Scam detection keywords
# -----------------------------
SCAM_KEYWORDS = [
    "account", "blocked", "suspended", "verify",
    "fraud", "security", "alert", "urgent",
    "lottery", "winner", "won", "prize",
    "selected", "congratulations", "reward"
]

URGENCY_KEYWORDS = ["urgent", "immediately", "now", "asap"]
PAYMENT_KEYWORDS = ["pay", "payment", "transfer", "upi", "bank"]
NEGATIONS = ["not", "no", "never"]

# -----------------------------
# Regex patterns (UPDATED)
# -----------------------------
UPI_PATTERN = r"\b[a-zA-Z0-9._-]+@[a-zA-Z0-9]+\b"
BANK_ACCOUNT_PATTERN = r"\b\d{9,18}\b"
IFSC_PATTERN = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
URL_PATTERN = r"https?://\S+|www\.\S+"

# -----------------------------
# Ensure clean conversation
# -----------------------------
def initialize_conversation(conversation_id: str):
    if conversation_id not in _conversation_states:
        _conversation_states[conversation_id] = "idle"

    if conversation_id not in _conversation_history:
        _conversation_history[conversation_id] = []

    if conversation_id not in _conversation_entities:
        _conversation_entities[conversation_id] = {
            "upi_ids": set(),
            "bank_accounts": set(),
            "ifsc_codes": set(),
            "phishing_links": set()
        }

# -----------------------------
# Save data
# -----------------------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(
            {k: {kk: list(vv) for kk, vv in v.items()} for k, v in _conversation_entities.items()},
            f
        )

# -----------------------------
# Scam Detection
# -----------------------------
def detect_scam(message: str) -> Tuple[bool, float]:
    if not isinstance(message, str) or not message.strip():
        return False, 0.0

    msg = message.lower()
    score = 0.0

    keyword_hits = sum(0.15 for w in SCAM_KEYWORDS if re.search(rf"\b{w}\b", msg))
    score += min(0.5, keyword_hits)

    score += 0.2 if any(re.search(rf"\b{w}\b", msg) for w in URGENCY_KEYWORDS) else 0.0
    score += 0.2 if any(re.search(rf"\b{w}\b", msg) for w in PAYMENT_KEYWORDS) else 0.0

    score += 0.2 if re.search(URL_PATTERN, msg) else 0.0
    score += 0.3 if re.search(UPI_PATTERN, msg) else 0.0
    score += 0.3 if re.search(BANK_ACCOUNT_PATTERN, msg) else 0.0

    if any(re.search(rf"\b{neg}\b", msg) for neg in NEGATIONS):
        score *= 0.7

    confidence = min(round(score, 2), 1.0)
    return confidence >= 0.6, confidence

# -----------------------------
# Entity Extraction (FIXED)
# -----------------------------
def extract_entities(message: str) -> Dict[str, List[str]]:
    # normalize input
    message = message.lower()
    message = re.sub(r"[,\n;]", " ", message)

    upi_ids = set(re.findall(UPI_PATTERN, message))
    bank_accounts = set(re.findall(BANK_ACCOUNT_PATTERN, message))
    ifsc_codes = set(re.findall(IFSC_PATTERN, message.upper()))
    phishing_links = set(re.findall(URL_PATTERN, message))

    # remove overlap
    bank_accounts = {
        acc for acc in bank_accounts
        if not any(acc in upi for upi in upi_ids)
    }

    return {
        "upi_ids": list(upi_ids),
        "bank_accounts": list(bank_accounts),
        "ifsc_codes": list(ifsc_codes),
        "phishing_links": list(phishing_links)
    }

# -----------------------------
# LLM REPLY
# -----------------------------
def generate_llm_reply(conversation_id: str) -> str:
    try:
        history = _conversation_history.get(conversation_id, [])

        system_prompt = {
            "role": "system",
            "content": """
You are a normal, slightly naive person talking to a scammer.
Keep replies short, curious, and natural.
Do not act suspicious.
"""
        }

        messages = [system_prompt] + history

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content.strip()

        _conversation_history[conversation_id].append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:
        print("Groq error:", e)
        return "Hmm okay… what should I do next?"

# -----------------------------
# Honeypot Engine
# -----------------------------
def honeypot_response(conversation_id: str, message: str) -> dict:

    initialize_conversation(conversation_id)

    current_state = _conversation_states[conversation_id]
    next_state = "confused" if current_state == "idle" else "extracting"
    _conversation_states[conversation_id] = next_state

    _conversation_history[conversation_id].append({
        "role": "user",
        "content": message
    })

    is_scam, confidence = detect_scam(message)
    entities = extract_entities(message)

    for key in ["upi_ids", "bank_accounts", "ifsc_codes", "phishing_links"]:
        _conversation_entities[conversation_id][key].update(entities.get(key, []))

    save_data()

    reply = generate_llm_reply(conversation_id)

    stored = {
        k: list(v) for k, v in _conversation_entities[conversation_id].items()
    }

    return {
        "is_scam": is_scam,
        "confidence": confidence,
        "persona_state": next_state,
        "reply": reply,
        "extracted_entities": stored
    }

# -----------------------------
# Data retrieval
# -----------------------------
def get_conversation_data(conversation_id: str):
    data = _conversation_entities.get(conversation_id, {
        "upi_ids": set(),
        "bank_accounts": set(),
        "ifsc_codes": set(),
        "phishing_links": set()
    })

    return {k: list(v) for k, v in data.items()}