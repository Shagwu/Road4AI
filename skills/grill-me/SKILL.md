---
name: grill-me
description: User-invoked. Get relentlessly interviewed about a plan, architecture change, or tool evaluation until every branch is resolved. Type /grill-me before committing to something — the agent won't reach for this on its own.
disable-model-invocation: true
---

Run a `grilling` session on whatever the user brings.

Stateless: writes nothing to disk by itself. If the user wants the outcome persisted, the `grilling` primitive's closing step handles that via a Hermes checkpoint — this wrapper doesn't need its own logic beyond invoking the primitive.
