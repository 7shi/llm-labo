mkdir -p log
time uv run eval.py -m google:gemini-2.5-flash | tee log/gemini-2.5-flash.txt
time uv run eval.py -m openai:gpt-4.1-mini | tee log/gpt-4.1-mini.txt
time uv run eval.py -m openai:gpt-4.1 | tee log/gpt-4.1.txt
time uv run eval.py -m openai:gpt-4o-mini | tee log/gpt-4o-mini.txt
time uv run eval.py -m openai:gpt-4o | tee log/gpt-4o.txt
time uv run eval.py -m openai:o3 | tee log/o3.txt
time uv run eval.py -m openai:o4-mini | tee log/o4-mini.txt
time uv run eval.py -m ollama:qwen3:4b | tee log/qwen3-4b.txt
time uv run eval.py -m ollama:gemma3:4b | tee log/gemma3-4b.txt
uv run ../utils/bold.py -o log/gemini-2.5-flash.txt log/gemini-2.5-flash.txt
grep 最終結果: log/*.txt
