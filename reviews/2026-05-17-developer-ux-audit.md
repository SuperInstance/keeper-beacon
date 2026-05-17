# keeper-beacon Developer UX Audit
**Date:** 2026-05-17
**Auditor:** External Developer Agent
**Scope:** keeper-beacon repo + keeper service (port 8900)

---

## Keeper Service (localhost:8900)

### Endpoint Quality

| Endpoint | Response Quality | Notes |
|----------|-----------------|-------|
| `GET /` | ✅ Perfect | Lists all available endpoints. Best landing page possible. |
| `GET /status` | ✅ Excellent | Full status: agents, pools, bottles, uptime |
| `GET /agents` | ✅ Excellent | Agent list with capabilities, trust scores, status |
| `GET /agents/active` | ✅ Works | Returns active subset |
| `GET /agent/oracle1` | ✅ Works | Single agent details |
| `GET /match?capabilities=...` | ✅ Clean | Returns matches or `[]` |
| `GET /bottles/inbox` | ✅ Works | Inbox state |
| Auth missing (POST) | ✅ **Excellent** | `{"error": "KEEPER_API_KEY required", "hint": "..."}` + 401 |
| Auth bad key (POST) | ✅ Good | `{"error": "invalid KEEPER_API_KEY"}` + 403 |
| Nonexistent endpoint | ✅ Good | `{"error": "not found"}` — consistent pattern |

**Verdict: Keeper is the best-documented service in the fleet.**

- CORS: `Access-Control-Allow-Origin: *` ✅
- Content-Type: Always `application/json` ✅
- Auth: Required for writes, reads are open. Sensible default.
- Error messages: Universally helpful. Auth hint with exact header format is best-in-class.

---

## Repo README Quality

**Current README:** 313 lines, Rust library. Sections:
- What it does (discovery, registry, proximity, matcher)
- Lighthouse metaphor (Cocapn brand integration)
- Installation (`pip install keeper-beacon`)
- "Part of the Cocapn Fleet" (links to Keeper service on port 8900)
- MIT License

**What's missing:**

| Gap | Severity | Detail |
|-----|----------|--------|
| **No API code examples** | P1 | No usage examples for `AgentRegistry`, `CapabilityMatcher`, `ProximityScorer` in code |
| **No service URL** | P1 | Says "port 8900" but doesn't say if there's a public URL |
| **No feature flags** | P2 | What can be disabled/enabled? |
| **No architecture diagram** | P2 | A simple ASCII diagram showing keeper → beacon → agents would help |
| **No changelog** | P2 | No history of what changed between versions |

---

## Package Ecosystem

| Registry | Package | Quality |
|----------|---------|---------|
| **PyPI** | keeper-beacon v0.2.0 | ✅ Has README. Description matches repo. |
| **crates.io** | keeper-beacon (Rust) | Unknown — not checked |

---

## Live Services Map (from keeper audit)

| Port | Service | Listen | Auth | Docs |
|------|---------|--------|------|------|
| 8900 | Keeper v2 | 127.0.0.1 | Read: open, Write: API key | ✅ Self-documenting |
| 8847 | PLATO server | 127.0.0.1 | Unknown | README on platoclaw (404) |
| 8300 | PLATO MCP | 127.0.0.1 | None | ✅ Great README |
| 9438 | Seed MCP v2 | **0.0.0.0** | Configured | Self-describing at root |

**Security note:** Only port 9438 is externally exposed. Rest are local-only. Good default.

---

## Priority Fixes

1. **Add code examples** to README — show `AgentRegistry`, `CapabilityMatcher`, `ProximityScorer` usage
2. **Add architecture diagram** — keeper-beacon → keeper service → agents
3. **Add feature flag documentation** — what's configurable?
4. **Add changelog** — track v0.1.0 → v0.2.0 changes
5. **Check crates.io rust package** — is it complete and documented?

---

*Keeper service UX is excellent. Repo README just needs code examples and an architecture diagram to be top-tier.*