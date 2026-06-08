# img2nl packages

Control-plane adapters (same pattern as `vql/packages/*`):

| Package | Entry | Role |
|---------|-------|------|
| `uri2img2nl` | `uri2img2nl query` | `img2nl://analyze`, `llm-hint`, `text` |
| `dsl2img2nl` | `dsl2img2nl` | `ANALYZE`, `QUERY`, `LLM_HINT` |
| `cli2img2nl` | `cli2img2nl` | Shell wrapper over DSL bus |

Install all:

```bash
bash install-dev.sh
```
