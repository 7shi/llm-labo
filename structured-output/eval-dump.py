import argparse
import json
import os
from eval import combinations, create_prompt, create_json_schema

# --- 引数解析 ---
# model引数は不要なので削除
parser = argparse.ArgumentParser(description='LLMに渡すプロンプトとスキーマをファイルに出力します。')
parser.add_argument('-f', '--file', default='eval.txt', help='評価対象のテキストファイル')
args = parser.parse_args()

# --- 評価対象ファイルの読み込み ---
with open(args.file, 'r', encoding='utf-8') as f:
    essay_text = f.read()

# --- メイン処理 ---
print(f"評価対象ファイル: {args.file} の内容を元に、各テストパターンのプロンプトとスキーマを生成します。")

# settingsディレクトリが存在しない場合は作成
os.makedirs('settings', exist_ok=True)

for i, (prompt_desc, schema_desc, descriptive_fields) in enumerate(combinations, 1):
    
    # プロンプトとスキーマを生成
    prompt = create_prompt(essay_text, prompt_desc, descriptive_fields)
    schema = create_json_schema(schema_desc, descriptive_fields)
    
    # ファイル名を定義
    prompt_filename = f"settings/{i}-prompt.md"
    schema_filename = f"settings/{i}-schema.json"
    
    # プロンプトをファイルに書き込み
    with open(prompt_filename, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    # スキーマをファイルに書き込み (見やすいようにインデント付き)
    with open(schema_filename, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
        
    print(f"Test {i}: {prompt_filename}, {schema_filename} を生成しました。")

print("全てのファイルの生成が完了しました。")
