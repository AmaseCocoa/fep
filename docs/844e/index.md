---
slug: "844e"
authors: silverpill <@silverpill@mitra.social>
type: implementation
status: DRAFT
discussionsTo: https://codeberg.org/silverpill/feps/issues
dateReceived: 2025-06-14
trackingIssue: https://codeberg.org/fediverse/fep/issues/624
---

# FEP-844e: 機能発見

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時15分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/844e/fep-844e.md)から閲覧できます。

## 概要

[ActivityPub]アプリケーションのための機能発見（Capability discovery）。

この文書は、[FEP-aaa3: アプリケーションアクターに実装された仕様をリストする][FEP-aaa3]で記述されたアイデアに基づいています。

## 要件

この文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119]で記述されている通りに解釈されるものとします。

## アプリケーションオブジェクト

アプリケーションは、`Application` オブジェクトの `implements` プロパティを使用して、その機能（capabilities）を広告できます。

このオブジェクトはアクターではない場合があります。`implements` プロパティの値は、以下のプロパティを含む `Link` オブジェクトの配列でなければなりません（MUST）。

- `href` (必須 - REQUIRED): 機能の一意な識別子。値はURIでなければなりません（MUST）。
- `name` (推奨 - RECOMMENDED): 機能の短い説明。

例：

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/fep/844e"
  ],
  "type": "Application",
  "id": "https://social.example/server",
  "implements": [
    {
      "href": "https://datatracker.ietf.org/doc/html/rfc9421",
      "name": "RFC-9421: HTTP Message Signatures"
    }
  ]
}
```

## アクターを介した発見

[`generator`][generator]プロパティを使用して、`Application` オブジェクトをアクターにリンクできます。このプロパティの値は、`implements` プロパティを含む部分的なオブジェクトであるべきです（SHOULD）。そのオブジェクトは匿名（識別子なし）であっても構いません（MAY）。

例：

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/fep/844e"
  ],
  "id": "https://social.example/actors/1",
  "type": "Person",
  "inbox": "https://social.example/actors/1/inbox",
  "outbox": "https://social.example/actors/1/outbox",
  "generator": {
    "type": "Application",
    "implements": [
      "href": "https://datatracker.ietf.org/doc/html/rfc9421",
      "name": "RFC-9421: HTTP Message Signatures"
    ]
  }
}
```

## well-knownエンドポイントを介した発見

WebFinger を使用して `Application` オブジェクトを発見するメカニズムは、[FEP-d556]で記述されています。

NodeInfo エンドポイントを介した機能発見は推奨されません。

## 意図された使用法

この文書で記述されているメカニズムへの依存は、実装の複雑さを増し、相互運用性を妨げる可能性があります。

実装者は、オブジェクトのプロパティや型から機能が推測できる場合には、これを使用してはなりません（MUST NOT）。

## ソフトウェア機能のレジストリ

(このセクションは非規範的です。)

| 名前 | 識別子 |
| ---  | ---        |
| RFC-9421: HTTP Message Signatures | https://datatracker.ietf.org/doc/html/rfc9421 |
| RFC-9421 signatures using the Ed25519 algorithm | https://datatracker.ietf.org/doc/html/rfc9421#name-eddsa-using-curve-edwards25 |

## 実装

- Streams
- Forte
- Mitra
- [ActivityPub for WordPress](https://activitypub.blog/2025/07/09/7-0-0-i-will-follow-you/)

## 参照

- Christine Lemmer-Webber, Jessica Tallon, Erin Shepherd, Amy Guy, Evan Prodromou, [ActivityPub], 2018
- S. Bradner, [RFCで要求レベルを示すためのキーワード][RFC-2119], 1997
- Helge, [FEP-aaa3: アプリケーションアクターに実装された仕様をリストする][FEP-aaa3], 2024
- Steve Bate, [FEP-d556: WebFinger を使用したサーバーレベルのアクター発見][FEP-d556], 2024

[ActivityPub]: https://www.w3.org/TR/activitypub/
[RFC-2119]: https://datatracker.ietf.org/doc/html/rfc2119.html
[FEP-aaa3]: https://codeberg.org/helge/fep/src/commit/e1b2a16707b542ea5ea0cfb390ac1abce89f05bb/fep/aaa3/fep-aaa3.md
[FEP-d556]: https://codeberg.org/fediverse/fep/src/branch/main/fep/d556/fep-d556.md
[generator]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-generator

## 著作権

CC0 1.0 ユニバーサル (CC0 1.0) パブリックドメイン献呈

法的に可能な限り、このFediverse強化提案の著者は、この著作物に関するすべての著作権および関連する権利または隣接する権利を放棄しました。