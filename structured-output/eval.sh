mkdir -p log
time uv run eval.py -m google:gemini-2.5-flash | tee log/gemini-2.5-flash.md
time uv run eval.py -m openai:gpt-4.1-mini | tee log/gpt-4.1-mini.md
time uv run eval.py -m openai:gpt-4.1 | tee log/gpt-4.1.md
time uv run eval.py -m openai:gpt-4o-mini | tee log/gpt-4o-mini.md
time uv run eval.py -m openai:gpt-4o | tee log/gpt-4o.md
time uv run eval.py -m openai:o3 | tee log/o3.md
time uv run eval.py -m openai:o4-mini | tee log/o4-mini.md
time uv run eval.py -m ollama:qwen3:4b | tee log/qwen3-4b.md
time uv run eval.py -m ollama:gemma3:4b | tee log/gemma3-4b.md
grep 最終結果: log/*.md
