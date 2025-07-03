import json
from llm7shi.compat import generate_with_schema

# 評価基準の定義
CRITERIA = [
    "本文中で言及されている猫の数は何匹か？",
    "著者はピザとハンバーガーのどちらを好むか？",
    "物語の中の天気はどのようなものか？",
    "示されている数式の数はいくつか？",
    "本文は英語で書かれているか？"
]

def create_json_schema(schema_desc, descriptive_fields):
    """LLMに構造化出力を強制するためのJSONスキーマを生成する。"""
    properties = {}
    for i, criterion in enumerate(CRITERIA, 1):
        key = criterion if descriptive_fields else f"q{i}"
        properties[key] = (p1 := {})
        p1["type"] = "object"
        if schema_desc:
            p1["description"] = criterion
        p1["properties"] = (p2 := {})
        p2["reasoning"] = (p := {"type": "string"})
        if schema_desc:
            p["description"] = "スコア算出について検討"
        p2["score"] = {"type": "integer", "minimum": 1, "maximum": 5}
        p1["required"] = list(p2.keys())
    properties["overall_reasoning"] = (p := {"type": "string"})
    if schema_desc:
        p["description"] = "評価全体に対する総合的な理由"
    return {"type": "object", "properties": properties, "required": list(properties.keys())}

def create_prompt(essay_text, prompt_desc, descriptive_fields):
    """モデルへの指示プロンプトを作成する。"""
    if prompt_desc:
        if descriptive_fields:
            criteria_list = "\n".join([f"- {key}" for key in CRITERIA])
        else:
            criteria_list = "\n".join([f"- q{i}: {key}" for i, key in enumerate(CRITERIA, 1)])
        prompt_header = f"""評価対象の文章を、評価基準に基づいて5段階で評価してください。

### 評価基準
{criteria_list}"""
    else:
        prompt_header = "評価対象の文章を、JSONスキーマの各項目に基づいて5段階で評価してください。"
    return f"""{prompt_header}

### 指示
- 各評価基準について、スコア算出について検討（reasoning）して、1〜5点のスコア（score）を付けてください。
- スコアは評価基準への準拠度を表し、無関係なら1点、完全に準拠する場合は5点を付けてください。
- 評価全体に対する総合的な理由（overall_reasoning）も提示してください。

### 評価対象の文章
{essay_text}"""

def evaluate_essay(model_name, essay_text, prompt_desc, schema_desc, descriptive_fields):
    """指定された条件でエッセイ評価を実行し、結果を表示する。"""
    schema = create_json_schema(schema_desc, descriptive_fields)
    prompt = create_prompt(essay_text, prompt_desc, descriptive_fields)
    response = generate_with_schema([prompt], schema=schema, model=model_name, show_params=False)
    results = json.loads(response.text).values()
    scores = [r["score"] for r in results if isinstance(r, dict) and "score" in r]
    avg_score = sum(scores) / len(scores) if scores else 0
    return avg_score

# 比較実験の組み合わせを定義
# (プロンプト内解説, スキーマ解説, 詳細フィールド名)
combinations = [
    (False, False, False),  # 実験1: 指示なし（ベースライン）
    (False, True,  False),  # 実験2: スキーマのdescriptionのみで指示
    (False, False, True ),  # 実験3: フィールド名（キー）のみで指示
    (True,  False, True ),  # 実験4: プロンプトとフィールド名で二重指示
    (True,  False, False),  # 実験5: プロンプトでキーと指示を対応付け
]

def main():
    import argparse
    parser = argparse.ArgumentParser(description='LLMによるエッセイ評価の比較実験を行います。')
    parser.add_argument('-m', '--model', required=True, help='使用するLLMモデル')
    parser.add_argument('-f', '--file', default='eval.txt', help='評価対象のテキストファイル')
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as f:
        essay_text = f.read()

    print(f"評価対象ファイル: {args.file}")

    avg_scores = []
    for i, (prompt_desc, schema_desc, descriptive_fields) in enumerate(combinations, 1):
        print()
        print("=" * 30, f"実験 {i}/{len(combinations)}", "=" * 30)
        print(f"モデル: {args.model}")
        print(f"プロンプト内解説={prompt_desc}, スキーマ解説={schema_desc}, 詳細フィールド名={descriptive_fields}")
        print("=" * 70)
        print(flush=True)
        avg_score = evaluate_essay(args.model, essay_text, prompt_desc, schema_desc, descriptive_fields)
        avg_scores.append(avg_score)
        print(f"平均スコア: {avg_score:.2f}/5")

    print("\n最終結果:", ", ".join(f"{s:.2f}" for s in avg_scores))

if __name__ == "__main__":
    main()
