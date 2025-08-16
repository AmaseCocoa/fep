---
slug: "c0e0"
authors: silverpill <@silverpill@mitra.social>
type: implementation
status: DRAFT
dateReceived: 2024-08-08
discussionsTo: https://socialhub.activitypub.rocks/t/fep-c0e0-emoji-reactions/4443
trackingIssue: https://codeberg.org/fediverse/fep/issues/384
---

# FEP-c0e0: 絵文字リアクション

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/c0e0/c0e0.md)から閲覧できます。

## 概要

このドキュメントでは、[ActivityPub] ネットワークにおける絵文字リアクションの実装方法について説明します。

## 履歴

Misskey はバージョン [10.97.0](https://github.com/misskey-dev/misskey/releases/tag/10.97.0) (2019年) 以降、絵文字リアクションをサポートしています。
Pleroma はバージョン [2.0.0](https://pleroma.social/announcements/2020/03/08/pleroma-major-release-2-0-0/) (2020年) 以降、絵文字リアクションをサポートしています。

## 要件

このドキュメントにおけるキーワード「MUST (必須)」、「MUST NOT (してはならない)」、「REQUIRED (必須)」、「SHALL (するものとする)」、「SHALL NOT (しないものとする)」、「SHOULD (すべきである)」、「SHOULD NOT (すべきではない)」、「RECOMMENDED (推奨)」、「MAY (してもよい)」、「OPTIONAL (任意)」は、[RFC-2119] に記述されている通りに解釈されます。

## EmojiReact アクティビティ

`EmojiReact` アクティビティタイプは、[LitePub] ボキャブラリーの一部と見なされます。その完全な IRI は `http://litepub.social/ns#EmojiReact` です。

このアクティビティは `Like` アクティビティに似ています。`Like` アクティビティの標準プロパティに加えて、`EmojiReact` アクティビティは `content` プロパティを**必須**とします。リアクションのコンテンツは、単一のユニコード書記素（unicode grapheme）であるか、コロンで囲まれたカスタム絵文字の名前（[ショートコード][Shortcode]）のいずれかで**なければなりません**。

カスタム絵文字が使用される場合、`EmojiReact` アクティビティは、単一の [`Emoji`][FEP-9098] オブジェクトを含む `tag` プロパティを**必須**とします。その `name` プロパティの値はカスタム絵文字の名前を含んで**いなければならず**、コロンで囲まれて**いるべきです**。埋め込まれた `Emoji` は、アクターのサーバーとは異なるサーバーから発信されることがあります。

アクターは、単一の `object` に対して複数の `EmojiReact` アクティビティを生成できます。ただし、実装者は、同じ絵文字によるリアクションを複数許可しない、またはオブジェクトごとに複数のリアクションを許可しないことを**選択してもよい**です。

ユニコード絵文字の例：

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "litepub": "http://litepub.social/ns#",
      "EmojiReact": "litepub:EmojiReact"
    }
  ],
  "actor": "https://alice.social/users/alice",
  "content": "🔥",
  "id": "https://alice.social/activities/65379d47-b7aa-4ef6-8e4f-41149dda1d2c",
  "object": "https://bob.social/objects/57caeb99-424c-4692-b74f-0a6682050932",
  "to": [
    "https://alice.social/users/alice/followers",
    "https://bob.social/users/bob"
  ],
  "type": "EmojiReact"
}
```

カスタム絵文字の例：

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    {
      "toot": "http://joinmastodon.org/ns#",
      "Emoji": "toot:Emoji",
      "litepub": "http://litepub.social/ns#",
      "EmojiReact": "litepub:EmojiReact"
    }
  ],
  "actor": "https://alice.social/users/alice",
  "content": ":blobwtfnotlikethis:",
  "id": "https://alice.social/activities/65379d47-b7aa-4ef6-8e4f-41149dda1d2c",
  "object": "https://bob.social/objects/57caeb99-424c-4692-b74f-0a6682050932",
  "tag": [
    {
      "icon": {
        "mediaType": "image/png",
        "type": "Image",
        "url": "https://alice.social/files/1b0510f2-1fb4-43f5-a399-10053bbd8f0f"
      },
      "id": "https://alice.social/emojis/blobwtfnotlikethis",
      "name": ":blobwtfnotlikethis:",
      "type": "Emoji",
      "updated": "2024-02-07T02:21:46.497Z"
    }
  ],
  "to": [
    "https://alice.social/users/alice/followers",
    "https://bob.social/users/bob"
  ],
  "type": "EmojiReact"
}
```

## content を持つ Like

絵文字リアクションは、`Like` アクティビティとして表現することもできます。この絵文字リアクションのバリアントは、非対応の実装によって通常の「いいね」として処理され、それが望ましい場合には、実装者は `EmojiReact` タイプではなく `Like` タイプを**使用してもよい**です。

実装は、`content` を持つ `Like` を `EmojiReact` アクティビティと**同じ方法で処理しなければなりません**。

## リアクションの取り消し

絵文字リアクションは、標準の `Undo` アクティビティを使用して取り消すことができます：

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams"
  ],
  "actor": "https://alice.social/users/alice",
  "id": "https://alice.social/activities/99b8f47b-f3a9-4cf5-94a2-95352e7462d6",
  "object": "https://alice.social/activities/65379d47-b7aa-4ef6-8e4f-41149dda1d2c",
  "to": [
    "https://alice.social/users/alice/followers",
    "https://bob.social/users/bob"
  ],
  "type": "Undo"
}
```

## `emojiReactions` コレクション

オブジェクトに対する絵文字リアクションのリストは、`emojiReactions` プロパティを使用して公開できます。その完全な IRI は `http://fedibird.com/ns#emojiReactions` です。

このプロパティによって指定される URL は、`Like`（`content` を持つ）および `EmojiReact` アクティビティを含むコレクションに解決され**なければなりません**。

## 実装

このドキュメントは、Misskey、Pleroma、Fedibird における絵文字リアクションの実装に基づいています。

この FEP が公開された後、他のいくつかのプロジェクトがそのサポートを発表しました：

- [Hollo](https://hollo.social/@hollo/0192479d-cbcc-7e4d-b2f1-1e0f8de61ea7)
- [Mitra](https://codeberg.org/silverpill/mitra/src/commit/3458b584bdb649f32cccac0e55ad10844debd397/FEDERATION.md#supported-feps)
- [PieFed](https://codeberg.org/rimu/pyfedi/src/commit/7ea1930b0601c4a0521da6e37e0a732b38c98c3b/FEDERATION.md#partially-supported-feps)
- [Iceshrimp.NET](https://iceshrimp.dev/iceshrimp/Iceshrimp.NET/src/commit/65d6edf799169a0dc88d895f52a8a32071b5f0c4/FEDERATION.md#supported-feps)

## 参照

- Christine Lemmer Webber, Jessica Tallon, [ActivityPub][ActivityPub], 2018
- S. Bradner, [RFCs で要件レベルを示すためのキーワード][RFC-2119], 1997
- LitePub contributors, [LitePub プロトコルスイート][LitePub], 2019
- silverpill, [FEP-9098: カスタム絵文字][FEP-9098], 2025

[ActivityPub]: https://www.w3.org/TR/activitypub/
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html
[LitePub]: https://litepub.social/
[Shortcode]: https://emojipedia.org/shortcodes
[FEP-9098]: https://codeberg.org/fediverse/fep/src/branch/main/fep/9098/fep-9098.md

## 著作権

CC0 1.0 ユニバーサル (CC0 1.0) パブリックドメイン献呈

法的に可能な限り、この Fediverse Enhancement Proposal の著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しました。