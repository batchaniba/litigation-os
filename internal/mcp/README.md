# Portfolio MCP server

`server.mjs` exposes the portfolio operation catalog
(`internal/docs/API_OPERATIONS.md`) as MCP tools over stdio. Same operations
as `npm run q`, richer transport for agent clients. Dependency-free (node
builtins only). Laptop-only: it can write the working tree.

External chats (ChatGPT, Grok, Cloud Agents without the repo) do **not**
get this stdio server. They get the read-only remote MCP on the existing
document Worker:

`https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp`

That path is tools on `litigation-doc-api` (R2 + D1 bindings), not a second
Worker and not this stdio process. See `workers/doc-api/README.md`.

## Run

```sh
node internal/mcp/server.mjs
# or
npm run mcp
```

## Connect

Claude Code (`~/.claude.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "litigation-portfolio": {
      "command": "node",
      "args": ["/absolute/path/to/internal/mcp/server.mjs"],
      "cwd": "/absolute/path/to/interactive-litigation-portfolio"
    }
  }
}
```

The server resolves the repo from its own location, so `cwd` only matters
for relative `out` paths in `fetchDocument`.

## Tools

18 tools: 11 reads (`getMatter`, `listMatters`, `upcomingDeadlines`,
`getTimeline`, `getFuseBoard`, `fetchDocument`, `searchDocuments`,
`getCounselDossier`, `getJudgeDossier`, `getClusters`, `getMatterDocs`)
and 7 writes (`recordTimelineEvent`, `retireUpcomingEvent`, `setNextClock`,
`updateMatterIdentity`, `catalogDocument`, `scaffoldMatter`,
`splitMatter`). Writes validate before touching disk and land on the
working tree for review — the server never merges.

`PORTFOLIO_ROOT` redirects the server at a scratch copy, same as `npm run q`.

## Test

```sh
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getFuseBoard","arguments":{}}}' \
  | node internal/mcp/server.mjs
```
