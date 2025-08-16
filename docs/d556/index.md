---
slug: "d556"
type: implementation
authors: Steve Bate <svc-fep@stevebate.net>
status: FINAL
dateReceived: 2024-01-20
dateFinalized: 2025-03-15
trackingIssue: https://codeberg.org/fediverse/fep/issues/243
discussionsTo: https://codeberg.org/fediverse/fep/issues/243
---

# FEP-d556: WebFinger を用いたサーバーレベルのアクター発見

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時16分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/d556/fep-d556.md)から閲覧できます。

## 概要

サーバーレベルの [ActivityPub] アクターは、ユーザーやそのソフトウェア相当物（*ボット*と呼ばれることもある）を表すのではなく、サーバー全体の機能をサポートします。この提案は、[WebFinger] を使用してサーバーレベルのアクターの URI を発見する方法を記述します。

## 用語

*サーバー*という用語は明確に定義されていません。この文書の目的のために、サーバーとは同じ URL プレフィックス（スキーム、ホスト、ポート）を持つ *オリジン* [SameOriginPolicy] です。この用語は、ネットワークやソフトウェアアーキテクチャについて何も示唆しません。サーバーは、ロードバランシングリバースプロキシの背後にある多数のサーバープロセスで構成されることもあります。あるいは逆に、単一のサーバープロセスが多数のサーバーをホストすることもできます（マルチテナントアーキテクチャ）。

一部の実装では、異なるサーバーレベルの役割（モデレーション、管理など）をサポートするために複数のアクターを持つことができます。この文書では、これらの種類のアクターを記述するために *サーバーレベルのアクター* という用語が使用されます。*サーバーアクター* または *アプリケーションアクター* という用語は、単一のサーバーレベルのアクターが存在する特殊だが一般的なケースです。

*サーバー*という用語は、[ActivityPub Recommendation][ActivityPub] で広範に使用されていますが、サーバーが処理できるアクティビティ以外はほとんど定義されていません。この用語は、Mastodon が *インスタンス* という言葉を使用する方法と密接に関連していますが、これはオンラインでの議論でこの言葉が使用される唯一の方法ではありません。

> 注：サーバーレベルのアクターの標準的な役割と責任は、ここ（またはこの提出時点では他の場所）では定義されていません。いくつかの実装にはインスタンスアクターまたはアプリケーションアクターと呼ばれるものがありますが、現時点では標準的な動作が定義されていないため、相互運用可能である場合とそうでない場合があります。

## ユースケース

この FEP はサーバーレベルのアクターの具体的な使用法を定義していませんが、それらが実際にどのように使用されているか、または使用されうるかを知ることは有用です。以下にいくつかの潜在的なユースケースを示します。

*   **フェッチリクエストの署名:** これが最も一般的なユースケースであると思われます。これに必要なのは、HTTP署名（つまり「承認済みフェッチ」）を要求することでアクタープロファイルへのアクセスを制限することと、アクタープロファイルを公開鍵と密接に結合することの組み合わせです。これにより、プロファイル/鍵のフェッチループが発生します ([InstanceActor])。この望ましくない動作を軽減するための一つの手法は、サードパーティのアクター（しばしば「インスタンスアクター」と呼ばれる）にすべてのフェッチリクエストに署名させることです。このユースケースではアクターの発見は必須ではありませんが、[FEP-2677] の動機となるユースケースであるように見えるため、ここで言及されています。これは本提案といくつかの類似点があります。

*   **リレーサポート:** サーバーレベルのアクターは、リレーへの購読（しばしば [ActivityPub] の `Follow` リクエストを使用）や `inbox` メッセージの受信に使用できます。

*   **サーバーレベルの購読:** [Pleroma] のような一部の実装では、「インスタンス」からの[すべてのメッセージを受信][InstanceActorIssue]するためにフォローできるアクターを提供しています。

*   **モデレーション:** サーバーレベルのアクターは、モデレーション関連のコンテンツ（アクターまたはドメインのブロック、投稿フラグなど）を連合（フェデレート）したり、アクションを実行するモデレーターの身元を隠すための公開プロキシを提供したりするために使用できます。

*   **アナウンス:** サーバーレベルのアクターは、サーバーの公開ニュースに使用できます。例えば、新機能、メンテナンススケジュール、更新に関するアナウンスを含むコンテンツを公開できます。

*   **オブジェクトの帰属:** 一部のサーバー実装では、一部のオブジェクトを個々のユーザーやアカウントではなく、サーバーに帰属させることができます。

*   **管理:** サーバーレベルのアクターは、ソフトウェアの問題（ユーザーからの報告を含む）、利用可能な更新、セキュリティの脆弱性とその軽減策に関する情報を共有するために使用できます。

## 発見

サーバーレベルのアクターの URI を発見するには、サーバープレフィックスをリソースクエリパラメータとして [WebFinger] にクエリします。

リクエスト例:
```
GET /.well-known/webfinger?resource=https://server.example/
```
レスポンス:
```json
{
    "subject": "https://server.example/",
    "links": [
        {
            "rel": "https://www.w3.org/ns/activitystreams#Service",
            "type": "application/activity+json",
            "href": "https://server.example/actor"
        }
    ]
}
```
`subject` は通常、リソース URI になります。この提案は `subject` の特定の URI に依存しませんが、ActivityPub アクター URI が推奨されます。

サーバーレベルのアクターの URI は、`rel`（リレーションタイプ）プロパティが `https://www.w3.org/ns/activitystreams#Service` である `link` の `href` プロパティになります（[W3C AS2 Service Primer][ActivityPubService]）。サーバーレベルのアクター自体のタイプは、リレーションタイプと同じである必要はありません。

単一アクターサーバーにおいて、サーバーレベルのアクターとユーザーのアクターとの間に曖昧さがない場合、`https://www.w3.org/ns/activitystreams#Service` の `rel` 値は `self` に置き換えられることがあります（[単一アクターサーバー](#単一アクターサーバー)の議論を参照）。

`http://webfinger.net/rel/profile-page` の `rel` ([WebFinger Relations][WebFingerRels]) は、サーバーのメタデータ（複数のコンテンツタイプを持つ可能性あり）へのリンクに使用できます。ただし、ターゲットとなるメタデータの構造は現時点では定義されていません。例えば、以下のリンクは HTML および JSON-LD 形式のプロファイルデータを参照しています。

```json
{
    "subject": "https://server.example/",
    "links": [
        {
            "rel": "https://www.w3.org/ns/activitystreams#Service",
            "type": "application/activity+json",
            "href": "https://server.example/actor"
        },
        {
            "rel": "http://webfinger.net/rel/profile-page",
            "type": "text/html",
            "href": "https://server.example/profile"
        },
        {
            "rel": "http://webfinger.net/rel/profile-page",
            "type": "application/ld+json",
            "href": "https://server.example/profile"
        }
    ]
}
```

複数のサーバーレベルのアクターリンクが返された場合、標準の [WebFinger] プロパティを使用してリンクにメタデータを追加することで、リンクを明確に区別できます。例えば、実装によっては異なる目的を果たす異なるサーバーレベルのアクターを持つことができます。

また、別の FEP が一般的な役割のための標準的な `rel` URI を定義する可能性もあります。その場合、それらの FEP の役割 URI が優先されるべきです（SHOULD）。

> 注：標準的なサーバーレベルのアクターの役割の定義は、この FEP の範囲外です。

```json
{
    "subject": "https://server.example/",
    "links": [
        {
            "rel": "https://www.w3.org/ns/activitystreams#Service",
            "type": "application/activity+json",
            "href": "https://server.example/actor",
            "properties": {
              "http://schema.org/roleName": "administration"
            }
        },
        {
            "rel": "https://www.w3.org/ns/activitystreams#Service",
            "type": "application/activity+json",
            "href": "https://server.example/actor",
            "properties": {
              "http://schema.org/roleName": "moderation"
            }
        }
    ]
}
```

この例では、同じアクターが管理とモデレーションに使用されています。しかし、アクターが異なる場合でもこの例は有効です。一部のユースケースでは、役割がさらに細分化される可能性があります。例えば、追加のプロパティが役割の地理的地域を指定するかもしれません。

## <a id="single-actor-servers"></a> 単一アクターサーバー

単一アクター（ユーザーアクター）サーバーの開発者は、サーバーレベルのアクターとして意図されていないにもかかわらず、そのユーザーがサーバープレフィックスに対応する URI を持つことを望むかもしれません。このシナリオは一般的であるとは予想されませんが、[WebFinger] レスポンスで複数のリンクを返すことでサポートできます。

```json
{
    "subject": "https://server.example/",
    "links": [
        {
            "rel": "https://www.w3.org/ns/activitystreams#Service",
            "type": "application/activity+json",
            "href": "https://server.example/server-actor"
        },
        {
            "rel": "self",
            "type": "application/activity+json",
            "href": "https://server.example/user-actor"
        }
    ]
}
```

アプリケーションがサーバーアクターまたはユーザーアクターのみに特に関心がある場合、[WebFinger] 仕様で説明されているように（[Webfinger] サービス実装によってサポートされている場合）、`rel` クエリパラメータを使用してリンクをフィルタリングできます。

例えば、ユーザーアクター URI のみをクエリするには、クエリは次のようになります。

```
GET /.well-known/webfinger?resource=https://server.example/&rel=self
```

```json
{
    "subject": "https://server.example/",
    "links": [
        {
            "rel": "self",
            "type": "application/activity+json",
            "href": "https://server.example/user-actor"
        }
    ]
}
```

# 実装

既知の実装には以下が含まれます。

*   FIRM
*   [Mastodon] はこの提案と類似したものを実装しています。
*   Streams
*   Mitra

## Mastodon の例

```
GET /.well-known/webfinger?resource=https://mastodon.social/
Host: https://mastodon.social
```
または Mastodon のアカウントベース URI を使用する場合：
```
GET /.well-known/webfinger?resource=acct:mastodon.social@mastodon.social
Host: https://mastodon.social
```

```json
{
  "subject": "acct:mastodon.social@mastodon.social",
  "aliases": [
    "https://mastodon.social/actor"
  ],
  "links": [
    {
      "rel": "http://webfinger.net/rel/profile-page",
      "type": "text/html",
      "href": "https://mastodon.social/about/more?instance_actor=true"
    },
    {
      "rel": "self",
      "type": "application/activity+json",
      "href": "https://mastodon.social/actor"
    },
    {
      "rel": "http://ostatus.org/schema/1.0/subscribe",
      "template": "https://mastodon.social/authorize_interaction?uri={uri}"
    }
  ]
}
```

Mastodon の実装とこの提案のいくつかの違いは以下の通りです。

*   標準の [WebFinger] の `rel` によるフィルタリングをサポートしていません。

*   `subject` は、推奨される [ActivityPub] アクター URI ではなく、サーバーレベルのアクターに対する Mastodon 固有のアカウント URI です。

サーバーリソースに対してユーザー関連のアクターリンクが提供されていないため、`self` の `rel` 値は曖昧さなく使用できます。

## 関連する提案

[FEP-2677] は、同様の目的で [NodeInfo] を使用することを提案しています。[WebFinger] を使用する場合と比較して、いくつかの欠点があります。

*   [WebFinger] は [ActivityPub] Recommendation によって必須ではありませんが、ほとんどの ActivityPub ベースの実装（例：Mastodon および互換性のある実装）との連合（フェデレーション）には必須です。[NodeInfo] は連合に必須ではないため、この目的での使用を要求すると、何のメリットもなく連合の複雑さが増します。
*   [WebFinger] は Internet Engineering Task Force (IETF) によって標準化されています。[NodeInfo] は非公式に定義されています。
*   [WebFinger] は、リソース識別子を解決し、サーバーレベルのメタデータ（例：プロファイルページの URL）へのリンクを提供するために既に使用されています。[NodeInfo] は主にサーバーメタデータの収集と集約に使用されます。
*   [FEP-2677] は、新しい非標準の `rel` リレーションを [NodeInfo] インデックスドキュメントに追加します。これは、一部の利用側実装に予期せぬ影響を与える可能性があります。この提案は、標準的な方法で [WebFinger] を使用しています。
*   [ActivityVocabulary] アクタータイプが WebFinger の `rel` 値に使用されていることを考えると、W3C ActivityStreams Primers がこの種のリソースに対して推奨するタイプは `as:Application` ([Primer][ActivityPubApp]) ではなく `as:Service` ([Primer][ActivityPubService]) です。（これは WebFinger からリンクされるサーバーレベルのアクターリソースで指定されるタイプとは異なることに注意してください。）
*   [FEP-2677] は単一のサーバーレベルアクターのみを定義しています。この提案はそのユースケースを許可しますが、高度な実装に対してより柔軟性があります。
*   [FEP-2677] はアクターが `as:Application` タイプを持つことを要求します。この提案はアクタータイプに制約を設けません。`as:Service` URI はリンクのリレーションタイプにのみ使用されます。

定義は明確ではありませんが、[FEP-2677] の「アプリケーションアクター」は、ソフトウェアの「アプリケーション」（定義されていませんが、この提案における「サーバー」と類似の概念のようです）のプロキシであるように見えます。例えば、アプリケーションのメタデータをアクターに付加することについての議論があります。この提案では、サーバープロキシアクターは存在しません（ただし、禁止されているわけではありません）。リンクされたサーバーレベルのサービスアクターを持つサーバー WebFinger リソースは存在しますが、サーバーリソース自体が必ずしもアクターであるとは限りません。

[FEP-2c59] は、[ActivityPub] アクターリソースから [WebFinger] リソース URI を発見する方法について議論しています。これはサーバーレベルのアクター発見とは関係ありません。

[FEP-4adb] は、WebFinger を用いた識別子の逆参照について議論しています。これはこの提案と類似していますが、サーバーレベルのアクターの発見に特に関連するものではありません。

## 参照

- Christine Lemmer Webber, Jessica Tallon, [ActivityPub], 2018
- James M Snell, Evan Prodromou, [ActivityStreams Vocabulary][ActivityVocabulary], 2017
- W3C ActivityStreams Primer - [Application type][ActivityPubApp]
- W3C ActivityStreams Primer - [Service type][ActivityPubService]
- Eugen Rochko, [Mastodon], 2016
- Jonne Haß, [NodeInfo 2.1][NodeInfo]
- MDN, [Same-origin Policy][SameOriginPolicy]
- Brad Fitzpatrick, [WebFinger], 2013
- WebFinger\.net [Link Relations][WebFingerRels]

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法的に可能な限り、この Fediverse Enhancement Proposal の著者は、この著作物に関するすべての著作権および関連する権利または隣接する権利を放棄しました。

[ActivityPub]: https://www.w3.org/TR/activitypub/ "ActivityPub プロトコルは、ActivityStreams 2.0 データ形式に基づいた分散型ソーシャルネットワーキングプロトコルです。コンテンツの作成、更新、削除のためのクライアントからサーバーへの API と、通知およびコンテンツを配信するための連合型サーバーからサーバーへの API を提供します。"
[ActivityVocabulary]: https://www.w3.org/TR/activitystreams-vocabulary "この仕様は Activity 語彙を記述しています。ActivityStreams 2.0 形式のコンテキストで使用されることを意図しており、アクティビティ構造と特定のアクティビティタイプのための基礎的な語彙を提供します。"
[ActivityPubApp]: https://www.w3.org/wiki/Activity_Streams/Primer/Application_type "Application タイプに関する W3C AS2 Primer"
[ActivityPubService]: https://www.w3.org/wiki/Activity_Streams/Primer/Service_type "Service タイプに関する W3C AS2 Primer"
[InstanceActor]: https://seb.jambor.dev/posts/understanding-activitypub-part-4-threads/#the-instance-actor "この記事は、承認済みフェッチループのいくつかのリクエストシーケンスを文書化しています。この記事は、この動作を誤って ActivityPub と関連付けていますが、これは主に Mastodon の実装設計に基づいた ActivityPub ではない特異な動作です。"
[InstanceActorIssue]: https://github.com/mastodon/mastodon/issues/10453 "Mastodon にインスタンス全体のアクターを追加することに関連する元の GitHub イシュー。"
[Mastodon]: https://joinmastodon.org/ "セルフホスト型で、グローバルに相互接続されたマイクロブログソフトウェア"
[NodeInfo]: http://nodeinfo.diaspora.software/protocol.html "NodeInfo は、分散型ソーシャルネットワークのインストールに関するメタデータを公開するための標準化された方法を定義します。"
[Pleroma]: https://pleroma.social/ "Pleroma は、同じ連合標準（OStatus および ActivityPub）をサポートする他のサーバーと連合（つまりメッセージを交換）できるマイクロブログサーバーソフトウェアです。"
[SameOriginPolicy]: https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy "同一オリジンポリシーは、あるオリジンによってロードされたドキュメントやスクリプトが、別のオリジンからのリソースとどのように相互作用できるかを制限する重要なセキュリティメカニズムです。"
[WebFinger]: https://tools.ietf.org/html/rfc7033 "標準的な HTTP メソッドを使用してインターネット上の人物やその他のエンティティに関する情報を発見するためのプロトコル"
[WebFingerRels]: https://webfinger.net/rel "webfinger.net で定義されている WebFinger リンクリレーション"
[FEP-2677]: ../2677/fep-2677.md "FEP-2677: アプリケーションアクターの識別"
[FEP-2c59]: ../2c59/fep-2c59.md "FEP-2c59: ActivityPub アクターからの Webfinger アドレスの発見"
[FEP-4adb]: ../4adb/fep-4adb.md "FEP-4adb: Webfinger を用いた識別子の逆参照"