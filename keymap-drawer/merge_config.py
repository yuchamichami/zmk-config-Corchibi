#!/usr/bin/env python3
"""
merge_config.py
テーマファイルの色変数をテンプレートconfigに適用して、
keymap-drawerが読み込める最終的なconfigファイルを生成します。

使い方:
    python merge_config.py \
        --base   keymap-drawer/keymap_drawer.config.template.yaml \
        --theme  keymap-drawer/themes/black.yaml \
        --output /tmp/keymap_drawer.config.yaml
"""

import argparse
import re
import sys
from pathlib import Path


def load_theme(theme_path: Path) -> dict[str, str]:
    """
    テーマYAMLを読み込んで {変数名: 値} の辞書を返します。
    コメント行（#）と空行は無視します。
    値はダブルクォートで囲まれていても囲まれていなくても両方対応します。
    """
    theme = {}
    for line in theme_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, raw_value = line.partition(":")
        key = key.strip()
        raw_value = raw_value.strip()
        # クォートで囲まれた値の場合はクォート内を取り出す（# を含む色コードを保護）
        if raw_value.startswith('"') and '"' in raw_value[1:]:
            value = raw_value[1:raw_value.index('"', 1)]
        elif raw_value.startswith("'") and "'" in raw_value[1:]:
            value = raw_value[1:raw_value.index("'", 1)]
        else:
            # クォートなしの場合のみインラインコメントを除去
            value = raw_value.split("#")[0].strip()
        theme[key] = value
    return theme


def apply_theme(template: str, theme: dict[str, str]) -> str:
    """
    テンプレート文字列内のプレースホルダーを theme 辞書の値で置換します。
    対応する書き方:
      - ${THEME_FOO}  : svg_extra_style などで使われる形式
      - THEME_FOO     : glyphs 内 SVG 属性値などで使われる裸の形式
    未定義の変数が残っていた場合はエラーを出して終了します。
    """
    result = template

    # 長いキー名から先に置換して部分一致の誤替えを防ぐ
    sorted_keys = sorted(theme.keys(), key=len, reverse=True)

    for key in sorted_keys:
        value = theme[key]
        # ${THEME_FOO} 形式
        result = result.replace(f"${{{key}}}", value)
        # 裸の THEME_FOO 形式（ただし THEME_ で始まるキーのみ対象）
        if key.startswith("THEME_"):
            result = result.replace(key, value)

    # 未置換の ${...} プレースホルダーを検出
    remaining_braced = re.findall(r"\$\{[^}]+\}", result)
    if remaining_braced:
        print(f"エラー: テーマファイルに未定義の変数があります: {set(remaining_braced)}", file=sys.stderr)
        sys.exit(1)

    # 未置換の裸の THEME_* を検出
    remaining_bare = re.findall(r"\bTHEME_\w+", result)
    if remaining_bare:
        print(f"エラー: テーマファイルに未定義の変数があります: {set(remaining_bare)}", file=sys.stderr)
        sys.exit(1)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="テーマファイルをテンプレートconfigに適用してconfigファイルを生成します"
    )
    parser.add_argument("--base",   required=True, help="テンプレートconfigファイルのパス")
    parser.add_argument("--theme",  required=True, help="テーマYAMLファイルのパス")
    parser.add_argument("--output", required=True, help="出力configファイルのパス")
    args = parser.parse_args()

    base_path   = Path(args.base)
    theme_path  = Path(args.theme)
    output_path = Path(args.output)

    if not base_path.exists():
        print(f"エラー: テンプレートファイルが見つかりません: {base_path}", file=sys.stderr)
        sys.exit(1)
    if not theme_path.exists():
        print(f"エラー: テーマファイルが見つかりません: {theme_path}", file=sys.stderr)
        sys.exit(1)

    template = base_path.read_text(encoding="utf-8")
    theme    = load_theme(theme_path)

    print(f"テーマ '{theme_path.stem}' を適用中...")
    result = apply_theme(template, theme)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8")
    print(f"生成完了: {output_path}")


if __name__ == "__main__":
    main()
