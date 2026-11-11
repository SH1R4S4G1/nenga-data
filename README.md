# nenga-data

iPhone アプリ「年賀当選チェック」が読み込む、お年玉付年賀はがき・寄付金付お年玉付年賀切手の当選番号データです（個人制作・非公式）。
番号や日付は日本郵便株式会社の発表にもとづきます。最終確認は日本郵便の発表で行ってください。

配信URL: https://sh1r4s4g1.github.io/nenga-data/v1/seasons.json

## 抽せん日の更新手順

1. 日本郵便の当せん番号の発表を確認する。
2. GitHub の画面で `docs/v1/seasons.json` を開いて編集する（スマホのブラウザでも可）。
   - `"announced": false` → `true`
   - 各賞の `"numbers"` に番号を入れる（**半角数字、`matchDigits` と同じけた数**）
   - `"revision"` を 1 増やす。`"updatedAt"` を今の日時にする
   - `"officialURL"` を当せん番号のお知らせページにする
3. コミットすると GitHub Actions が自動で検証する（✓ になればOK。✗ なら理由が表示される）。
4. 1〜2分で GitHub Pages に反映される。アプリは起動時・画面に戻ったとき・抽せん日以降は3分ごとに取りに来る。
5. **もう1人が日本郵便の発表と照合する。**

```json
{ "rank": 1, "title": "1等", "name": "現金30万円", "matchDigits": 6, "count": 1, "numbers": ["123456"], "requiresID": true },
{ "rank": 2, "title": "2等", "name": "賞品カタログギフト", "matchDigits": 5, "count": 1, "numbers": ["12345"], "requiresID": true },
{ "rank": 3, "title": "3等", "name": "お年玉切手シート", "matchDigits": 2, "count": 3, "numbers": ["12", "34", "56"], "requiresID": false }
```

データに誤り（けた数違い・本数違い・未発表なのに番号あり など）があると、アプリはその内容を使わず判定を止めます。

## 毎年の準備（8〜11月）

日本郵便の「年賀はがき等の発行概要」と「お年玉賞品」の資料で、抽せん日・引換期間・**各賞の当選けた数**を確認し、`seasons` に新しい年を追加して `revision` を増やす（2027年用から 2等が下4けた → **下5けた** に変わった）。
アプリに同梱しているデータ（アプリ側の `Resources/seasons.json`）も同じ内容にそろえ、アプリを更新する。

## 手元での検証

```bash
python3 scripts/validate_seasons.py docs/v1/seasons.json
```
