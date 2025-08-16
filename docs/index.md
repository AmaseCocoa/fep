# Fediverse 機能強化提案

これは、Fediverse 拡張提案 (FEP)の日本語訳です。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep)にあります。

Fediverse拡張提案（FEP）は、Fediverseコミュニティに情報を提供する文書です。FEPの目的は、Fediverseを構成する多様なサービス、アプリケーション、コミュニティの相互運用性と健全性を向上させることです。

FEPプロセスは、 [W3Cソーシャルウェブインキュベータコミュニティグループ](https://www.w3.org/community/SocialCG/)のリエゾンである[SocialHub](https://socialhub.activitypub.rocks)開発者コミュニティのイニシアチブです。現在進行中および過去の議論については、SocialHub FEPカテゴリをご覧ください。

## FEPの提出

Fediverseコミュニティ全体と共有したいアイデア、意見、情報をお持ちですか？ Fediverse Enhancement Proposal（FEP）をご利用ください。

FEP を作成して提出するには:

1. このリポジトリをフォークし、ローカルマシンにクローンしてください。プルリクエストの作成方法については、 Codebergの[チートシート](https://docs.codeberg.org/collaborating/pull-requests-and-git-flow/#cheat-sheet)をご覧ください。
2. 提出したい FEP のタイトルを考えます。
3. タイトルのハッシュを計算して、FEPの識別子を計算します。これは以下のUnixコマンドで実行できます。

```
$ echo -n "The title of my proposal" | sha256sum | cut -c-4
b3f0
```

4. 計算した識別子を使用して`fep/`のサブディレクトリを作成します。
5. FEP テンプレート ([fep-xxxx-template.md](https://codeberg.org/fediverse/fep/src/branch/main/fep-xxxx-template.md)) をこのサブディレクトリにコピーし、ファイル名を適切に変更します。
6. フロントマターを入力するときに、識別子を「slug」として使用します。
    - たとえば、計算された識別子が`abcd`の場合、ファイルは`fep/abcd/fep-abcd.md`に配置され、フロントマターには`slug: "abcd"`が含まれます。
7. 新しく作成されたファイルにアイデアを書き留め、リポジトリ内の新しいブランチ (例: fep-xxxx) にコミットします。
8. FEP を送信する準備ができたら、フロントマターの`dateReceived`フィールドの値を現在の日付に変更します。
9. FEPに関するディスカッショントピックを作成してください。SocialHubフォーラムの[ActivityPubカテゴリ](https://socialhub.activitypub.rocks/c/activitypub/5)を利用できます。
10. ディスカッショントピックのURLを含む`discussionsTo`フィールドをFEPのフロントマターに追加します。
11. [FEP-a4ed: Fediverse拡張提案プロセス](a4ed)のステップ1を完了するには、プルリクエストを作成してください。以降のプロセスについては、FEP-a4edに記載されています。


手順3～6の代わりに、以下を実行することもできます。

```bash
./scripts/new_proposal.py TITLE OF YOUR PROPOSAL
```

これにより、事前に入力されたテンプレートが作成されます。

## ファシリテーター
FEPのリストは、[FACILITATORS.md](FACILITATORS.md)ファイルに記載されているファシリテーターによって管理されます。ファシリテーターはFEPプロセスにおける中立的な管理者であり、PRをマージし、追跡問題を作成します。

## 貢献する

FEPプロセスを改善するためのアイデアをお持ちですか？課題トラッカーまたは[SocialHub](https://socialhub.activitypub.rocks)フォーラムにご提案を投稿してください。SocialHub開発者コミュニティは「DoOcracy（ドゥーオクラシー）」です。これは「好きなタスクを選び、最後までやり遂げる」という意味です。皆様の貢献を心よりお待ちしておりますので、ぜひご参加いただき、ご自身の力量に合った方法を見つけてください。


## ライセンス

CC0 1.0 ユニバーサル (CC0 1.0) パブリックドメイン

法律で認められる範囲において、この文書の著者はこの作品に対するすべての著作権および関連する権利または隣接する権利を放棄します。