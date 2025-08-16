---
slug: "9098"
authors: silverpill <@silverpill@mitra.social>
type: implementation
status: DRAFT
discussionsTo: https://codeberg.org/silverpill/feps/issues
dateReceived: 2025-07-06
trackingIssue: https://codeberg.org/fediverse/fep/issues/648
---

# FEP-9098: カスタム絵文字

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/9098/9098.md)から閲覧できます。

## 概要

カスタム絵文字は、アイデアや感情を表現するために使用される小さな画像です。カスタム絵文字は、文字のシーケンスであるUnicode絵文字とは異なります。

このドキュメントでは、[ActivityPub] ネットワークでカスタム絵文字がどのように実装されているかを説明します。

## 歴史

カスタム絵文字は、2017年にPleroma ([コミット](https://gitgud.io/lambadalambda/pleroma/-/compare/c17c8ce36d35db03a007a264cc2e507afa9b803e...7c82b8219734102ff24d9dc24226c08351e608cc)) と Mastodon ([PR](https://github.com/mastodon/mastodon/pull/4988)) によって導入されました。

## 要件

このドキュメントにおけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119] に記述されている通りに解釈されるものとします。

## Emoji オブジェクト

カスタム絵文字は `Emoji` オブジェクトとして表現されます（完全な型 IRI は `http://joinmastodon.org/ns#Emoji` です）。`Emoji` オブジェクトには以下のプロパティがあります。

- `id` (推奨): カスタム絵文字の一意な識別子。一部の実装ではこのプロパティを省略します（つまり、オブジェクトは匿名です）。
- `type` (必須): リテラル文字列 `Emoji`。
- `name` (必須): カスタム絵文字の [ショートコード][Shortcode]（コロンで囲まれた絵文字の名前。 [マイクロシンタックス](#マイクロシンタックス) セクションを参照）。
- `updated` (任意): カスタム絵文字が更新された日付で、[RFC-3339] の日付と時刻の文字列形式です。
- `icon` (必須): 絵文字画像を記述する `Image` オブジェクト。
  - `type` (必須): リテラル文字列 `Image`。
  - `url` (必須): 絵文字として使用する画像の URI。

> [!NOTE]
> ActivityStreams Vocabulary における `icon` プロパティの定義では、アスペクト比を1対1にすることを推奨していますが、実際にはカスタム絵文字は様々なアスペクト比を持っています。

例:

```json
{
  "id": "https://social.example/emoji/blobcat",
  "type": "Emoji",
  "name": ":blobcat:",
  "updated": "1970-01-01T00:00:00Z",
  "icon": {
    "type": "Image",
    "url": "https://social.example/media/blobcat.png"
  }
}
```

### 一意性

カスタム絵文字の主要な一意な識別子は、その名前とドメイン名の組み合わせです。ドメイン名は、`Emoji` オブジェクトの `id` から、またはそれが埋め込まれているオブジェクトの `id` から抽出できます。

発行者が絵文字の `id` がグローバルに一意であることを保証しない場合、このプロパティを追加してはなりません（MUST NOT）。

### アクセシビリティ

カスタム絵文字の短い説明は、`alternateName` プロパティで指定できます（完全な IRI は `http://schema.org/alternateName` です）。

## カスタム絵文字の使用

### マイクロシンタックス

テキストでは、カスタム絵文字は [ショートコード][Shortcode] で表現されます。これはコロンで囲まれた絵文字の名前です（例: `:blobcat:`）。これは `Emoji` オブジェクトの `name` プロパティの値でもあります。

これらのテキスト表現は、カスタム絵文字を埋め込むオブジェクトの `name`、`summary`、`content` プロパティの値に挿入されることがよくあります。例えば、`Note` の `content` や `Actor` の `name` などです。

対応する `Emoji` オブジェクトは、オブジェクトの `tag` 配列に追加されます。その配列内では、カスタム絵文字は任意の順序で出現できます。

例:

```json
{
  "type": "Note",
  "id": "https://social.example/notes/1234",
  "content": "<p>:blobcat:</p>",
  "tag": [
    {
      "id": "https://social.example/emoji/blobcat",
      "type": "Emoji",
      "name": ":blobcat:",
      "icon": {
        "type": "Image",
        "url": "https://social.example/media/blobcat.png"
      }
    }
  ]
}
```

### 右から左へのテキスト

カスタム絵文字のショートコードは、右から左へのテキストであっても、常に左から右に記述されます。

### レンダリング

#### 一般的なクライアントの考慮事項

画像の縦横比は維持されるべきです（SHOULD）。画像の最大幅は制限される場合があります（MAY）。

`<code>` および `<pre>` HTML 要素内のショートコードは置換されてはなりません（MUST NOT）。

#### Webクライアントの考慮事項

Webアプリケーションは通常、カスタム絵文字のショートコードを `<img>` HTMLタグに置き換え、出力をHTMLとしてレンダリングします。

[クロスサイトスクリプティング (XSS)][XSS] 攻撃を防ぐため、実装者は以下を保証しなければなりません（MUST）：

- 絵文字の名前、説明、URL、および置換に使用されるその他の文字列に、予約済みのHTML文字（`&<>"'`）が含まれていないこと。
- HTMLコンテンツ（例: `summary`、`content`）が処理される際、ショートコードは [Text][DOM-Text] ノード内でのみ置換されること。
- テキスト内の予約済みHTML文字は、ショートコードを置換する前にエスケープされること。

## 互換性

可能な限り多くのサーバーと互換性を持たせるため、実装は以下の追加要件に準拠すべきです（SHOULD）：

- 名前は少なくとも2文字を含むこと ([Mastodon](https://github.com/mastodon/mastodon/blob/v4.3.7/app/models/custom_emoji.rb#L28))。
- 名前は `[a-zA-Z0-9_]` セットの文字のみを含むこと ([Mastodon](https://github.com/mastodon/mastodon/blob/v4.3.7/app/models/custom_emoji.rb#L30))。
- 画像メディアタイプは `image/png`、`image/gif`、または `image/webp` であること ([Mastodon](https://github.com/mastodon/mastodon/blob/v4.3.7/app/models/custom_emoji.rb#L37))。
- 画像サイズは 256 KB を超えないこと ([Mastodon](https://github.com/mastodon/mastodon/blob/v4.3.7/app/models/custom_emoji.rb#L27))。
- 画像は正方形であること（一部のクライアントでは、正方形でない絵文字が誤ったアスペクト比で表示される場合があります）。
- ショートコードは、Unicodeの英数字、コロン、または行末ではない2つの文字の間に配置されること ([Mastodon](https://github.com/mastodon/mastodon/blob/v4.4.2/app/models/custom_emoji.rb#L32-L34)、また issue [#7364](https://github.com/mastodon/mastodon/issues/7364) も参照)。

## 実装

このドキュメントは、Pleroma、Mastodon、Misskey、Fedibird におけるカスタム絵文字の実装に基づいています。

## 参考文献

- Christine Lemmer-Webber, Jessica Tallon, Erin Shepherd, Amy Guy, Evan Prodromou, [ActivityPub], 2018
- S. Bradner, [RFCにおける要件レベルを示すためのキーワード][RFC-2119], 1997
- G. Klyne, C. Newman, [インターネット上の日付と時刻: タイムスタンプ][RFC-3339], 2002

[ActivityPub]: https://www.w3.org/TR/activitypub/
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html
[RFC-3339]: https://www.rfc-editor.org/rfc/rfc3339
[Shortcode]: https://emojipedia.org/shortcodes
[XSS]: https://owasp.org/www-community/attacks/xss/
[DOM-Text]: https://developer.mozilla.org/en-US/docs/Web/API/Text

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法律で許される限りにおいて、この Fediverse Enhancement Proposal の著者は、この著作物に関するすべての著作権および関連する権利または隣接する権利を放棄しました。