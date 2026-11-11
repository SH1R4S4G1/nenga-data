#!/usr/bin/env python3
"""当選番号データ（seasons.json）の検証。アプリ側の検証（Season.swift）と同じ規則。

使い方: python3 scripts/validate_seasons.py docs/v1/seasons.json [他のファイル ...]
誤りがあれば内容を表示して終了コード 1 で終わる。
"""
import json
import sys
from datetime import date

SUPPORTED_SCHEMA = 1
NUMBER_LENGTH = 6


def parse_date(value, where, errors):
    try:
        y, m, d = value.split("-")
        assert len(y) == 4 and len(m) == 2 and len(d) == 2
        return date(int(y), int(m), int(d))
    except Exception:
        errors.append(f"{where}: 日付「{value}」は YYYY-MM-DD 形式で書いてください")
        return None


def validate(path):
    errors = []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # JSON の書き間違い（カンマ忘れなど）
        return [f"JSON として読めません: {e}"]

    if data.get("schemaVersion") != SUPPORTED_SCHEMA:
        errors.append(f"schemaVersion は {SUPPORTED_SCHEMA} にしてください")
    if not isinstance(data.get("revision"), int):
        errors.append("revision は整数にしてください（更新のたびに 1 増やす）")
    seasons = data.get("seasons") or []
    if not seasons:
        errors.append("seasons が空です")

    seen = set()
    for s in seasons:
        sid = s.get("id", "?")
        where = f"シーズン {sid}"
        if sid in seen:
            errors.append(f"{where} が重複しています")
        seen.add(sid)
        d = {k: parse_date(s.get(k, ""), f"{where} の {k}", errors)
             for k in ("salesStart", "drawDate", "exchangeStart", "exchangeEnd")}
        if all(d.values()) and not (d["salesStart"] < d["drawDate"] < d["exchangeStart"] <= d["exchangeEnd"]):
            errors.append(f"{where}: 日付の順序が正しくありません（販売開始 < 抽せん日 < 引換開始 <= 引換終了）")
        announced = s.get("announced")
        if not isinstance(announced, bool):
            errors.append(f"{where}: announced は true か false にしてください")
        prizes = s.get("prizes") or []
        if not prizes:
            errors.append(f"{where}: prizes が空です")
        ranks = set()
        for p in prizes:
            rank = p.get("rank")
            pw = f"{where} の {p.get('title', rank)}"
            if rank in ranks:
                errors.append(f"{pw}: rank が重複しています")
            ranks.add(rank)
            digits = p.get("matchDigits")
            count = p.get("count")
            numbers = p.get("numbers") or []
            if not isinstance(digits, int) or not 1 <= digits <= NUMBER_LENGTH:
                errors.append(f"{pw}: matchDigits は 1〜6 にしてください")
                continue
            if not isinstance(count, int) or count < 1:
                errors.append(f"{pw}: count は 1 以上にしてください")
                continue
            if not announced:
                if numbers:
                    errors.append(f"{pw}: 未発表（announced: false）なのに番号が入っています")
                continue
            if len(numbers) != count:
                errors.append(f"{pw}: 番号は {count} 本のはずが {len(numbers)} 本です")
            for n in numbers:
                if not (isinstance(n, str) and n.isascii() and n.isdigit() and len(n) == digits):
                    errors.append(f"{pw}: 番号「{n}」は半角数字 {digits} けたで書いてください")
            if len(set(numbers)) != len(numbers):
                errors.append(f"{pw}: 同じ番号が2回入っています")
    return errors


def main(paths):
    failed = False
    for path in paths:
        errors = validate(path)
        if errors:
            failed = True
            print(f"✗ {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"✓ {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["docs/v1/seasons.json"]))
