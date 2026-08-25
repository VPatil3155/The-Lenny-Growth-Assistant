# Session 05 – Runtime Provider Switching

## Objective

Allow switching between Ollama and OpenAI without restarting the application.

---

## Prompt

Implement runtime model switching using a provider abstraction.

Requirements:

- OpenAI
- Ollama
- Runtime switching
- Availability indicator

---

## Result

Implemented:

- Provider API
- Provider selector
- Runtime override
- Availability status

---

## Issue Encountered

Provider selection needed to update immediately without restarting the backend.

---

## Resolution

Introduced a provider factory with runtime override.

The frontend updates the selected provider immediately.

---

## Outcome

✓ OpenAI works

✓ Ollama works

✓ Switching works without restart

✓ Provider status displayed