# Utils ユーティリティ

このディレクトリには、プロジェクトで使用するユーティリティスクリプトが含まれています。

## bold.py

TTY太字制御シーケンスをMarkdown太字マーカーに変換するツールです。

### 機能

- TTY太字制御シーケンス（`\x1b[1m`と`\x1b[22m`）をMarkdown太字マーカー（`**`）に変換
- ファイルまたは標準入力からの入力をサポート
- 出力ファイルへの書き込み

### 使用方法

```bash
# ファイルを変換
python3 bold.py -o output.md input.txt

# 標準入力から変換
cat input.txt | python3 bold.py -o output.md
```

### オプション

- `-o`, `--output`: 出力ファイルパス（必須）
- `input`: 入力ファイルパス（オプション、指定しない場合は標準入力を使用）

### 使用例

```bash
# 太字制御シーケンスを含むファイルを変換
python3 bold.py -o converted.md log.txt

# パイプを使用した変換
command_with_bold_output | python3 bold.py -o output.md
```