## Question
Should Road4AI adopt OmniRoute as a multi-provider AI gateway?

## Type
grilling

## Status
resolved

## Resolution
Deferred. Self-hosted local proxy with 230+ LLM providers, MIT license, no cloud in request path. Ollama already solves local-first inference for Road4AI's current needs. OmniRoute adds a large attack surface for no active benefit. Revisit if a future phase requires cloud-provider fallback that Ollama/MiMo can't cover.
