#!/usr/bin/env python3
"""Build the deployable app: inject data/*.json into src/index.template.html -> public/index.html.
Run after regenerating the data (see pipeline/). Netlify/Render can also run this as the build command."""
import pathlib
root=pathlib.Path(__file__).parent
tpl=(root/"src/index.template.html").read_text(encoding="utf-8")
nat=(root/"data/national.json").read_text(encoding="utf-8")
peer=(root/"data/peer.json").read_text(encoding="utf-8")
out=tpl.replace("__NATIONAL__",nat).replace("__PEER__",peer)
(root/"public").mkdir(exist_ok=True)
(root/"public/index.html").write_text(out,encoding="utf-8")
print(f"built public/index.html ({len(out):,} bytes)")
