# Deployment

Agent Trust Lab includes a static browser demo under `web/`.

## Local Demo

```powershell
python -m http.server 8765
```

Open:

```text
http://localhost:8765/web/
```

## GitHub Pages

The repository includes `.github/workflows/pages.yml`.

After pushing to `main`, enable GitHub Pages with GitHub Actions as the source if it is not enabled automatically.

The deployed site should serve the contents of `web/`.

## Safety Note

The static demo uses embedded synthetic case summaries only. It does not contain private data, credentials, or patent claim text.

