---
slug: "e232"
authors: silverpill <@silverpill@mitra.social>
status: FINAL
dateReceived: 2022-08-01
dateFinalized: 2023-12-03
trackingIssue: https://codeberg.org/fediverse/fep/issues/14
discussionsTo: https://socialhub.activitypub.rocks/t/fep-e232-object-links/2722
---

# FEP-e232: オブジェクトリンク

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時14分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/e232/fep-e232.md)から閲覧できます。

## 概要

この文書は、メンションに類似した、[ActivityPub][ActivityPub]オブジェクトへのテキストベースのリンクを表現する方法を提案します。そのようなリンクの一例として、`content`プロパティの値内のインライン引用が挙げられますが、この提案は特定のユースケースに限定されるものではありません。

## 要件

この文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119][RFC-2119]で記述されている通りに解釈されるものとします。

## オブジェクトリンク

ソフトウェアは、`@mention`や`#hashtag`のようなマイクロシンタックス（microsyntax）を用いて、ユーザーがオブジェクトリンクを定義できるようにすることが期待されます。オブジェクトリンクを定義する正確な方法はユースケースによって異なる可能性があり、この文書の範囲外です。

オブジェクトの`name`、`summary`、または`content`が他のオブジェクトへの修飾されたリンクを持つ場合、そのオブジェクトは[Activity Vocabulary][ActivityVocabulary]によって提案されているように、各オブジェクトリンクが`Link`オブジェクトとして表現される`tag`プロパティを持つべき（SHOULD）です。この`Link`オブジェクトのプロパティは以下の通りです。

- `type` (必須): タイプは`Link`またはそのサブタイプである必要があります（MUST）。
- `mediaType` (必須): メディアタイプは`application/ld+json; profile="https://www.w3.org/ns/activitystreams"`である必要があります（MUST）。この仕様はActivityPubオブジェクトのみを扱いますが、実際にはメディアタイプが異なる場合があり、サーバーは要件に準拠しないオブジェクトリンクを受け入れてもよい（MAY）です。例えば、`application/activity+json`のメディアタイプは同等として扱われるべき（SHOULD）です。
- `href` (必須): `href`プロパティは参照されるオブジェクトのURIを含む必要があります（MUST）。
- `name` (任意): `name`はオブジェクトのコンテンツで使用されるマイクロシンタックスと一致すべき（SHOULD）です。
- `rel` (任意): 関連する場合、`rel`はリンクが現在のリソースとどのように関連しているかを指定すべき（SHOULD）です。`rel`を使用することで、特定の意図されたユースケースを示すことにより、オブジェクトリンクに追加の目的を提供できます。

## 例

(このセクションは非規範的です。)

バグトラッカー内のイシューへのリンク:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "The bug was reported in #1374",
    "tag": [
        {
            "type": "Link",
            "mediaType": "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"",
            "href": "https://forge.example/tickets/1374",
            "name": "#1374"
        }
    ]
}
```

インライン引用:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "content": "This is a quote:<br>RE: https://server.example/objects/123",
    "tag": [
        {
            "type": "Link",
            "mediaType": "application/ld+json; profile=\"https://www.w3.org/ns/activitystreams\"",
            "href": "https://server.example/objects/123",
            "name": "RE: https://server.example/objects/123"
        }
    ]
}
```

なお、`content`には`RE: <url>`マイクロシンタックスが含まれていますが、消費する実装は適切な関連付けを行うためにそれをパースする必要はありません。

## 実装

- (streams)
- FoundKey
- Mitra
- Pleroma ([MRF経由](https://git.pleroma.social/pleroma/pleroma/-/blob/v2.6.0/lib/pleroma/web/activity_pub/mrf/quote_to_link_tag_policy.ex))
- Threads ([発表](https://engineering.fb.com/2024/03/21/networking-traffic/threads-has-entered-the-fediverse/))
- [Friendica](https://github.com/friendica/friendica/pull/14032)
- Bridgy Fed
- [Hollo](https://hollo.social/@hollo/01920132-739e-7eff-9f5f-424282884eee)
- [Iceshrimp.NET](https://iceshrimp.dev/iceshrimp/Iceshrimp.NET/src/commit/bdfd3a8d4e788ef3bdec06f32f444ed7fcffc3c7/FEDERATION.md#supported-feps)

## 参照

- Christine Lemmer Webber, Jessica Tallon, [ActivityPub][ActivityPub], 2018
- S. Bradner, [RFCにおける要件レベルを示すためのキーワード][RFC-2119], 1997
- James M Snell, Evan Prodromou, [Activity Vocabulary][ActivityVocabulary], 2017

[ActivityPub]: https://www.w3.org/TR/activitypub/
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html
[ActivityVocabulary]: https://www.w3.org/TR/activitystreams-vocabulary/

## 著作権

CC0 1.0 ユニバーサル (CC0 1.0) パブリックドメイン献呈

法が許す限りにおいて、このFediverse Enhancement Proposalの著者は、この著作物に対するすべての著作権および関連する権利、または隣接する権利を放棄しました。