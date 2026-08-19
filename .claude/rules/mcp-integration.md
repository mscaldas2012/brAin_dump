---
name: mcp-integration
description: How to scope and configure MCP servers, and when to expose something as a resource instead of a tool
paths:
  - "**/*mcp*.*"
  - "**/mcp/**"
  - "**/*.mcp.json"
  - "**/*tool*.*"
---

# MCP integration

## Roles, briefly

MCP is a client-server protocol, not a library. A host (the app the user
interacts with) runs a separate client for every server it's configured
with — one 1:1 connection per server, each completing its own capability
handshake independently. A host with three configured servers runs three
separate client instances; there's no fan-out or shared connection across
them, and no bottleneck from one connection on another's setup.

## Project scope vs. user scope

Same hierarchy logic as CLAUDE.md's own scoping — this isn't a coincidence,
it's the same underlying "shared vs. personal" axis applied to a different
config surface:

| Scope | Shared via VCS? | Use for |
|---|---|---|
| Project-level config | Yes | Team-wide tooling everyone needs, credentials referenced via `${VAR}` expansion rather than committed literally |
| User-level config | No | Personal or experimental servers not ready for (or not relevant to) the whole team |

Never hardcode a literal secret into a project-scoped config file — use
environment-variable expansion so the shared file references a credential
without committing it. And don't put an experimental personal server into
the project-scoped file just because it's convenient — wrong scope, it'll
show up for every teammate whether they want it or not.

Tools from every configured server (project and user, however many) are
discovered at connection time and are simultaneously available in the
session — there's no manual merging or selection step, and no assumption
that only one server's tools are "active" at once.

## Resources vs. tools — who decides, and why it matters

| Primitive | Who decides to use it | Purpose |
|---|---|---|
| **Tool** | The model, mid-reasoning | An action with a side effect or computation |
| **Resource** | The host/user, ahead of time or on demand | Read-only content the model can be given without a tool round-trip |

A resource is the more efficient design whenever the content is genuinely
static and known ahead of time — a schema, a document catalog, an
enumerable reference list. Exposing something as a resource means the model
never has to spend a tool-call round-trip just to check something that
could already be sitting in context. Using tool calls to let the model
"explore" available data when a resource would do is strictly more
expensive for no benefit — check whether what you're building is actually
an action (tool) or a lookup against something that doesn't change within
the session (resource) before defaulting to a tool.

## Build vs. buy

Prefer an existing community MCP server for standard integrations (issue
trackers, source control, common SaaS platforms) over writing a custom one.
Reserve custom servers for genuinely team-specific workflows that no
existing server covers. Building a custom server for a standard integration
is effort spent reinventing something that already exists and is
maintained elsewhere.

## Thin descriptions cause fallback to a trusted built-in

If an MCP tool's description is thin, a model can default to a built-in
tool it already "trusts" for a similar-sounding job (e.g. falling back to a
generic search/grep tool instead of a more capable MCP-provided one) — even
when the MCP tool would do a better job. This is the same fix as any other
tool-selection problem: enrich the description (see
`tool-interface-design.md`'s fix hierarchy) rather than trying to suppress
the built-in tool or work around the model's preference some other way.

## Traps

| Trap | Why it's wrong |
|---|---|
| Hardcoding a literal secret into a project-scoped/shared config file | Should use environment-variable expansion instead — a shared file shouldn't carry a committed credential |
| Putting an experimental personal server into project scope | Wrong scope — belongs in the user-level config until it's ready for the whole team |
| Assuming only one configured server's tools are "active" at a time | All configured servers' tools are available simultaneously once connected |
| Building a custom MCP server for a standard, already-covered integration | Default to an existing community server; reserve custom builds for team-specific workflows |
| Using tool calls for the model to "explore" data that's actually static and known ahead of time | A resource is the more efficient design when one fits — no need to spend a round-trip on it |
| A thin MCP tool description causing fallback to a built-in tool | Fix per `tool-interface-design.md`: enrich the description, don't work around the symptom |
