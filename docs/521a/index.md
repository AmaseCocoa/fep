---
slug: "521a"
authors: silverpill <@silverpill@mitra.social>
type: implementation
status: FINAL
dateReceived: 2023-07-08
dateFinalized: 2025-06-14
trackingIssue: https://codeberg.org/fediverse/fep/issues/130
discussionsTo: https://socialhub.activitypub.rocks/t/fep-521a-representing-actors-public-keys/3380
---

# FEP-521a: アクターの公開鍵の表現

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時15分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/521a/fep-521a.md)から閲覧できます。

## 要約

この提案は、[ActivityPub] アクターに関連付けられた公開鍵をどのように表現するかを記述します。

## 根拠

歴史的に、Fediverse サービスはアクターの公開鍵を表現するために [publicKey](https://w3c-ccg.github.io/security-vocab/#publicKey) プロパティを使用していました。実装では通常、アクターごとに1つの鍵しか許可されていないため、追加の鍵が必要なユースケースをサポートするために新しいアプローチが必要です。

さらに、`publicKey` プロパティは非推奨と見なされており、[Security Vocabulary][SecurityVocabulary] の最新バージョンには存在しません。

## 要件

この文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119] で記述されている通りに解釈されます。

## Multikey

各公開鍵は、[Controlled Identifiers][Multikey] 仕様の *2.2.2 Multikey* セクションで定義されているように、`Multikey` 型のオブジェクトとして表現されなければなりません（MUST）。このオブジェクトは以下のプロパティを持たなければなりません（MUST）：

- `id`: 公開鍵の一意なグローバル識別子。
- `type`: このプロパティの値は文字列 `Multikey` でなければなりません（MUST）。
- `controller`: このプロパティの値はアクター ID と一致しなければなりません（MUST）。
- `publicKeyMultibase`: [Multicodec] プレフィックスと公開鍵の [Multibase] エンコードされた値。実装は `base-58-btc` アルファベットを使用しなければなりません（MUST）。

### 鍵のID

鍵の識別子は絶対 [URI][RFC-3986] でなければなりません（MUST）。

識別子は、アクター ID にフラグメント識別子を付加することによって生成されるべきです（SHOULD）。これにより、コンシューマは単一の HTTP リクエストでアクターオブジェクトと関連する鍵の両方を取得できます。アクターの鍵がフラグメント識別子を使用して識別される場合、各鍵は一意のフラグメント識別子を持たなければなりません（MUST）。

フラグメント識別子を含む URI の解決は、[Controlled Identifiers][FragmentResolution] 仕様の *3.4 Fragment Resolution* セクションで指定されたアルゴリズムを使用して実行されます。

### 鍵のタイプ

実装者は、[Multicodec] プレフィックスが登録されている任意のタイプの暗号鍵を使用できます。

## アクターオブジェクトへの鍵の追加

`Multikey` オブジェクトは、[Controlled Identifiers][ControlledIdentifiers] 仕様で記述されているように、制御された識別子ドキュメントと見なされるアクターオブジェクトに追加されます。

鍵が ActivityPub オブジェクトの署名に使用されることを意図している場合、それはアクターオブジェクト内の [`assertionMethod`][Assertion] 配列に追加されなければなりません（MUST）。

その他のユースケースは、この提案の範囲外です。

実装は、この仕様に準拠しないオブジェクトを `assertionMethod` 配列に追加することを推奨しません（discouraged）。`assertionMethod` 配列内で不適合なエントリに遭遇した実装は、それらを無視すべきです（SHOULD）。

アクターは関連する公開鍵を持たないこともあります（MAY）。

### 例

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://www.w3.org/ns/cid/v1"
    ],
    "type": "Person",
    "id": "https://server.example/users/alice",
    "inbox": "https://server.example/users/alice/inbox",
    "outbox": "https://server.example/users/alice/outbox",
    "assertionMethod": [
        {
            "id": "https://server.example/users/alice#ed25519-key",
            "type": "Multikey",
            "controller": "https://server.example/users/alice",
            "publicKeyMultibase": "z6MkrJVnaZkeFzdQyMZu1cgjg7k1pZZ6pvBQ7XJPt4swbTQ2"
        }
    ]
}
```

## テストベクトル

[fep-521a.feature](./fep-521a.feature) を参照してください。

## 実装

- Mitra
- streams
- Hubzilla
- [Fedify](https://github.com/fedify-dev/fedify/blob/1.7.5/FEDERATION.md#supported-feps)
- [tootik](https://github.com/dimkr/tootik/blob/0.18.0/FEDERATION.md#http-signatures)

## 参考文献

- Christine Lemmer-Webber, Jessica Tallon, Erin Shepherd, Amy Guy, Evan Prodromou, [ActivityPub], 2018
- Ivan Herman, Manu Sporny, Dave Longley, [Security Vocabulary][SecurityVocabulary], 2023
- S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels][RFC-2119], 1997
- Dave Longley, Manu Sporny, Markus Sabadello, Drummond Reed, Orie Steele, Christopher Allen, [Controlled Identifiers v1.0][ControlledIdentifiers], 2025
- Protocol Labs, [Multicodec][Multicodec]
- T. Berners-Lee, R. Fielding, L. Masinter, [Uniform Resource Identifier (URI): Generic Syntax][RFC-3986], 2005

[ActivityPub]: https://www.w3.org/TR/activitypub/
[SecurityVocabulary]: https://www.w3.org/2025/credentials/vcdi/vocab/v2/vocabulary.html
[RFC-2119]: https://datatracker.ietf.org/doc/html/rfc2119.html
[ControlledIdentifiers]: https://www.w3.org/TR/cid-1.0/
[Multikey]: https://www.w3.org/TR/cid-1.0/#Multikey
[Multibase]: https://www.w3.org/TR/cid-1.0/#multibase-0
[Assertion]: https://www.w3.org/TR/cid-1.0/#assertion
[FragmentResolution]: https://www.w3.org/TR/cid-1.0/#fragment-resolution
[Multicodec]: https://github.com/multiformats/multicodec/
[RFC-3986]: https://datatracker.ietf.org/doc/html/rfc3986

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法律で許される限りにおいて、この Fediverse 改善提案の著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しました。