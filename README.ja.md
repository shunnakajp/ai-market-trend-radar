# AI投資トレンドレーダー

**AI Market Trend Radar / AI投資トレンドレーダー** は、米国AI・テック市場まわりの「いま盛り上がっているテーマ」を毎日MarkdownレポートにするOSSツールです。

ニュース、Redditなどの公開RSS、GitHubのOSS動向を集め、OpenAI APIで英日バイリンガル要約を作ります。

> このプロジェクトは調査の入口を作るためのものです。**投資助言ではありません**。特定銘柄の売買・保有を推奨しません。

English: [README.md](README.md)

## 何を解決するか

AI/テック市場の話題は、ニュース、SNS、OSSコミュニティで同時多発的に動きます。

このツールは、それらのノイズを毎朝整理して、以下を確認できるようにします。

- 今日のトップ10トレンド
- 英語・日本語の短い要約
- なぜ今注目されているか
- 関連キーワード
- 参考ティッカー・関連テーマ
- リスク・注意点
- 元ソースへのリンク

## 特徴

- GitHub Actionsで毎日 **日本時間 朝7時** にレポート生成
- `reports/YYYY-MM-DD.md` にMarkdown保存
- 有料金融API不要。公開RSS/Atom中心
- OpenAI APIによる英日要約
- `YOU`、`DATA`、`LINK` のような汎用語が新興トレンドに混ざらないためのノイズ除外
- 銘柄ではなくテーマ中心
- MIT License

## 現在の状態

- GitHub Actionsで日次生成・手動実行ができる状態です。
- Repository Secretの `OPENAI_API_KEY` により、OpenAI要約を有効化できます。
- 生成済みサンプルレポート: [`reports/2026-06-03.md`](reports/2026-06-03.md)
- テーマスコアリングと新興トレンドのノイズ除外はテスト済みです。

## クイックスタート

```bash
git clone https://github.com/shunnakajp/ai-market-trend-radar.git
cd ai-market-trend-radar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
export OPENAI_API_KEY="your_api_key"
trend-radar
```

レポートは次に保存されます。

```text
reports/YYYY-MM-DD.md
```

`OPENAI_API_KEY` がない場合でも、基本的な非AIレポートは作れるため、コントリビューターが動作確認しやすい構成です。

## GitHub Actions設定

1. このリポジトリを作成またはForkします。
2. **Settings → Secrets and variables → Actions** を開きます。
3. `OPENAI_API_KEY` をRepository Secretとして追加します。
4. GitHub Actionsを有効にします。
5. 手動実行するか、毎日の自動実行を待ちます。

## 免責

このソフトウェアと生成レポートは、情報整理・調査補助を目的としています。金融、投資、税務、法律上の助言ではありません。投資判断は必ずご自身で調査し、必要に応じて専門家へ相談してください。
