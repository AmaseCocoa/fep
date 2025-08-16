---
slug: "ae0c"
authors: Steve Bate <svc-fep@stevebate.net>
status: FINAL
category: informational
dateReceived: 2024-10-19
dateFinalized: 2025-03-14
trackingIssue: https://codeberg.org/fediverse/fep/issues/424
discussionsTo: https://socialhub.activitypub.rocks/t/fediverse-relays/4626
---

# FEP-ae0c: Fediverseリレープロトコル：MastodonとLitePub

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/ae0c/fep-ae0c.md)から閲覧できます。



## 概要

リレー（Relay）は、分散型Fediverseアーキテクチャにおける重要なコンポーネントです。これらは異なるインスタンス間の通信を促進する仲介サーバーとして機能し、Fediverseプラットフォームのユーザーがアクターのフォロー関係を必要とせずに公開コンテンツを共有できるようにします。

これらのリレーは、小規模なインスタンスがFediverseコンテンツの消費者としても生産者としても、連合型ソーシャルネットワークに効果的に参加できるようにすることで、利益をもたらします。

Activity Fediverseにはいくつかのスタイルのリレーが存在します。このFEPは、2つの一般的なリレーのスタイルを記述します。

* [Mastodonスタイルリレー](#Mastodonスタイルリレー)
* [LitePubスタイルリレー](#LitePubスタイルリレー)

*注：これは現状を文書化した情報提供FEPです。[RFC-2119]の要件キーワードは便宜上使用しているに過ぎません。また、これらは標準化されたプロトコルではありません。ActivityPub標準のいくつかの概念を使用していますが、一般的にはActivityPub標準に準拠していません。*

## 用語

このドキュメントでは、以下の用語を使用します。

| 用語 | 説明 |
|------|-------------|
| **リレークライアントアクター** | リレーサーバーの購読者であるサーバー内のアクター。*クライアントアクター*とも呼ばれます。 |
| **リレークライアントサーバー** | 1つ以上のリレークライアントアクターをホストするサーバー。*クライアントサーバー*とも呼ばれます。 |
| **リレー購読** | リレークライアントアクターとリレーサーバーの間で、[ActivityPub]の`Follow`アクティビティを使用して確立される関係。 |
| **リレーサーバーアクター** | リレークライアントアクター間でメッセージのリレーを提供するサーバー内のアクター。*リレーアクター*とも呼ばれます。 |
| **リレーサーバー** | 1つ以上のリレーサーバーアクターをホストするサーバー。*リレーサーバー*または*リレー*とも呼ばれます。 |
| **[HTTP署名][Mastodon HTTP Signatures]** | メッセージの送信者と内容を検証するために使用されるHTTPベースの署名（Cavage）。 |
| **[LD署名][Mastodon LD Signatures]** | トランスポートに関係なくメッセージを検証するために使用されるJSON-LD署名。 |

## Mastodonリレープロトコル

Mastodonリレープロトコルは、リレーされたメッセージを検証するためにLD署名（LD Signatures）に依存しています。これにより、Mastodonは、異なるアクター（リレーサーバーアクター）によって送信されたメッセージであっても、リレーされたメッセージを検証できます。

### リレークライアントアクター

リレークライアントアクターは、リレーサーバーアクターとのフォロー関係を確立し、その後、アクターの[ActivityPub] `inbox`に送信されたリレーメッセージを処理します。リレークライアントサーバーは、公開可視性を持つコンテンツの配信ターゲットにリレーインボックスを追加します。

#### リレー購読

Mastodonは、リレーのActivityPub `inbox` URIにActivityPub `Follow`リクエストをPOSTします。`Follow`リクエストの`object`は、Public擬似コレクション（`https://www.w3.org/ns/activitystreams#Public`）の完全に展開されたURIでなければなりません（MUST）。リレーはその後、`Accept`または`Reject`アクティビティで`Follow`リクエストに応答します。購読には手動承認が必要な場合があるため、承認の応答時間は任意に長くなる可能性があります。

リクエストは、MastodonがActivityPub連合（federation）に使用するのと同じ[HTTP署名][Mastodon HTTP Signatures]（Cavage）アルゴリズムを使用して署名されなければなりません（MUST）。リレーは、アクターの公開鍵を取得するためにリレークライアントアクターのドキュメントをフェッチします。最高の相互運用性のためには、アクターのActivityPubドキュメントはMastodon互換であるべきです（SHOULD）。例えば、[ActivityPub]で要求されるすべてのアクターフィールドに加えて`preferredUsername`が提供されるべきであり（SHOULD）、アクターは`sharedInbox`エンドポイントURLを提供するべきです（SHOULD）。

リレークライアントアクターのタイプは、アクターのタイプを正確に反映するべきです（SHOULD）。ただし、一部のリレーサーバー実装では、クライアントアクターのActivityPubタイプを制約していることに注意してください。例えば、リレーサーバー実装は、クライアントアクターが`Application`タイプであることを要求し、他のタイプを拒否する場合があります。

**Followリクエストの例**

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://client.example/6ae15297",
    "type": "Follow",
    "actor": "https://client.example/actor",
    "object": "https://www.w3.org/ns/activitystreams#Public"
}
```

**Follow承認応答の例**

`Accept`アクティビティは、承認された`Follow`アクティビティURIを`object`として応答してもよいし（MAY）、元の`Follow`アクティビティのコピーを埋め込んでもよいです。`Reject`アクティビティも同様の構造になります。

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://relay.example/15c0b99f-23d4-4488-ba9d-d0c7bc2876a5",
    "type": "Accept",
    "actor": "https://relay.example/actor",
    "object": {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "https://client.example/6ae15297",
        "type": "Follow",
        "actor": "https://client.example/actor",
        "object": "https://www.w3.org/ns/activitystreams#Public"
    }
}
```

#### リレー購読解除

リレーの購読を解除するには、元の`Follow`アクティビティ（埋め込み、またはURI）を`object`として`Undo`を送信します。通常、`Undo`に対する応答はありません。

**Undo/Followリクエストの例**

```json
{
    "@context": "https: //www.w3.org/ns/activitystreams",
    "id": "https://client.example/3f5ebd6d",
    "type": "Undo",
    "actor": "https://client.example/actor",
    "published": "2024-10-14T14:42:17.650139+00:00",
    "object": "https://client.example/6ae15297"
}
```

#### リレーへのメッセージ公開

Mastodonスタイルリレーにアクティビティを公開するには、発行者はMastodon固有の[LD署名][Mastodon LD Signatures]アルゴリズムを使用してメッセージに署名しなければなりません（MUST）。LD署名を使用する利点は、受信サーバーがクライアントサーバーから再フェッチすることなくメッセージの内容を検証できることです。これにより、クライアントサーバーのサーバー負荷が軽減されます。

欠点は、LD署名の実装が容易ではなく、Mastodonがアルゴリズムの古い非標準形式を使用していることです。Mastodonのドキュメントでは、これらの理由からLD署名をサポートしないことを推奨しています。
さらに、Mastodonのドキュメントは、それが実装するLD署名アルゴリズムを正確に記述していません。詳細については、このドキュメントの[Mastodon LD署名](#Mastodon-LD署名)に関する追加情報を参照してください。

投稿されたアクティビティは、Mastodon互換の[HTTP署名][Mastodon HTTP Signatures]で署名されなければなりません（MUST）。

Mastodonは、以下の種類のアクティビティをリレーします：`Create`、`Update`、`Delete`、`Move`。リレーアクターはこれらのタイプのみを転送してもよいですが（MAY）、MastodonはLD署名なしで`Announce`などの他のリレーアクティビティを*受け入れます*。`Announce`の場合、アナウンスされた`object`をフェッチします。

#### リレーからのメッセージ受信

リレーされたメッセージは、リレークライアントアクターの`inbox`に投稿されます。リレーされたメッセージは、リレーアクターによって署名されたHTTP署名を持たなければなりません（MUST）。

リレーサーバーアクターから受信したメッセージは、LD署名を持っていてもよいです（MAY）。HTTP署名とLD署名の両方が存在する場合、LD署名検証後、アクティビティの`actor`が実質的な送信者となります。

LD署名が存在せず、受信したメッセージが`Announce`アクティビティである場合、リレークライアントはコンテンツが正当であること（なりすましではないこと）を確認しなければなりません（MUST）。これは、発信元サーバーからアナウンスされたアクティビティをフェッチするか、ローカルキャッシュからリモートコンテンツを使用することで行われます。ただし、アナウンスされたアクティビティがすでにローカルにキャッシュされている場合、クライアントサーバーにはすでに認識されているため、通常はそれに対して行うべき処理はありません。

リレーされたメッセージを受信するクライアントサーバーは、ActivityPubのオーディエンスターゲティングプロパティに基づいて、ローカルの受信者にもメッセージを配信してもよいです（MAY）。

### リレーサーバーアクター

以下の動作は、Mastodonスタイルリレーサーバーアクターの典型的な実装を記述しています。

#### フォロー

`https://www.w3.org/ns/activitystreams#Public`が`object`プロパティに含まれていることを確認します。`actor`をリレークライアントアクターURIとして使用し、購読者に関する情報を保存します。リレーサーバーは、署名者のドメインなどの要因に基づいてアクセスを拒否することを決定してもよいです（MAY）。

#### Undo/フォロー

`actor`が既知のリレークライアントであることを確認し、そうであれば、リレーアクターのフォロワーのセットからクライアントアクターを削除します。

#### アクティビティのリレー

クライアントアクターからメッセージを受信した場合、リレーはアクティビティのHTTP署名を検証し、発信元のアクターを特定しなければなりません（MUST）。メッセージが有効であれば、その後（リレーアクターのHTTP署名とともに）リレーのフォロワーのインボックスに投稿されます。ActivityPubのオーディエンスターゲティングプロパティに基づく配信は行われません。リレーは、リレーされたメッセージを発信元のリレークライアントアクターに送信してはなりません（MUST not）。

通常、メッセージは変更されずに転送されます。ただし、リレーはメッセージに対して他の処理を行ってもよいです（MAY）。例えば、LD署名のないメッセージをActivityPub `Announce`アクティビティでラップしてから転送する（[pub-relay]を参照）などです。このような拡張された動作は、このFEPでは記述されていません。

リレーアクターは、フォロワーからのメッセージのみをリレーするべきです（SHOULD）。リレーアクターは、すでにリレーしていないアクティビティのみをリレーするべきです（SHOULD）。`to`のようなアドレス指定プロパティは、単一のURIであってもリストでなければなりません（MUST）。

### Mastodon LD署名

*注：MastodonのLD署名に関する[Mastodonドキュメント][Mastodon LD Signatures]は不完全かつ不正確です。このセクションでは詳細を提供しますが、さらなる明確化のためにMastodonのソースコードを確認する必要があるかもしれません。*

Mastodon LD署名で署名されたアクティビティには、アクティビティ内に署名ドキュメント（`signature`プロパティを使用）が含まれます。

**署名ドキュメントの例**

```json
{
  "@context": [
    "https: //www.w3.org/ns/activitystreams",
    "https://w3id.org/security/v1"
  ],
  "id": "https://client.example/3f5ebd6d",
  # ...
  "signature": {
      "type": "RsaSignature2017",
      "creator": "https://client.example/actor#main-key",
      "created": "2024-12-08T03:48:33.901Z",
      "signatureValue": "s69F3mfddd99dGjmvjdjjs81e12jn121Gkm1"
  }
}
```

`https://w3id.org/security/v1` JSON-LDコンテキストは`signature`および関連プロパティを定義しますが、MastodonではLD署名処理には使用されません。

署名操作を実行する際、署名ドキュメントとアクティビティ（署名ドキュメントなし）は最初に個別に処理（ハッシュ化）されます。SHA256ハッシュダイジェストが連結され、その文字列が署名されます。

#### JSON-LDアクティビティの署名

1. `creator`と`created`プロパティのみを持つ署名ドキュメントを作成します。`@context`を`https://w3id.org/identity/v1`に設定します。（注：このコンテキストはもはやウェブ上でアクセスできないようです。カスタムJSON-LDコンテキストローダーを備えたローカルコピーが必要になる場合があります。）
2. 署名ドキュメントの正規RDF表現を作成します。これには、標準アルゴリズム（[JSON-LD-ALGO]）を使用したJSON-LD展開と、**Universal RDF Dataset Canonicalization Algorithm 2015**（[RDF-CANON]）を使用したRDFへの変換が必要です。シリアライズされたRDFは、その後[SHA256]を使用してハッシュ化され、ヘックスダイジェストが作成されます。
3. 同様の手順を使用して、アクティビティドキュメント（署名ドキュメントなし）のSHA256ヘックスダイジェストを作成します。
4. 署名ドキュメントとアクティビティドキュメントのSHA256ヘックスダイジェストを連結し、SHA256とクライアントアクターの秘密鍵を使用して結果に署名します。
5. [Base64]を使用して署名をエンコードし、署名ドキュメントの`signatureValue`に結果を設定します。
6. 署名ドキュメントの`type`を"RsaSignature2017"に設定します。
7. アクティビティの`signature`プロパティを署名ドキュメントに設定します。

#### JSON-LD署名の検証

1. 署名ドキュメントがアクティビティから取得され、タイプが非標準の"RsaSignature2017"であるかどうかがチェックされます。そうでない場合、検証は失敗します。
2. 署名ドキュメントから`signatureValue`を保存します。
3. 署名ドキュメントから`type`、`id`、`signatureValue`プロパティを削除し、ドキュメントの署名について記述された手順を使用して、変更された署名ドキュメントのSHA256ヘックスダイジェストを生成します。
4. アクティビティから`signature`を削除し、そのSHA256ヘックスダイジェストを生成します。
5. 変更された署名ドキュメントとアクティビティドキュメントのヘックスダイジェストを連結します。
6. クライアントの公開鍵を使用して、SHA256で署名を検証します。

## LitePubリレープロトコル

[LitePub][litepub]プロトコルは[ActivityPub]に基づいており、Pleroma互換サーバーで使用されています。参照実装は[Pleroma Relay][pleroma-relay]です。

### リレークライアント

LitePubリレークライアントアクターは、`Application`タイプであり、アクターIDが`/relay`で終わる必要があります。最高の相互運用性のためには、Mastodonアクタードキュメントと互換性があり、WebFingerサポートを持つべきです。他の実装では異なるアクターID構造を使用する場合があります（例：AodeRelayは`/actor`を使用し、Pleromaで動作するようです）。これらのLitePubバリアントの一般的なリレー相互運用性は不明です。

#### リレー購読

クライアントリレーアクターは、リレーサーバーに`Follow`を送信します。`Follow`の`object`はリレーサーバーアクターURIです。

リレーサーバーは、`Follow`リクエストに`Accept`または`Reject`で応答しなければなりません（MUST）。承認された場合、リレーサーバーはLitePubクライアントアクターに対して相互の`Follow`リクエストを送信します。クライアントサーバーは`Accept`または`Reject`アクティビティで応答するべきです（SHOULD）。リレーサーバーは、妥当な時間間隔内に承認が受信されない場合、購読を無視することを決定してもよいです（MAY）。

**リレーFollowリクエストの例**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://pleroma.example/schemas/litepub-0.1.jsonld",
        {
            "@language": "und"
        }
    ],
    "actor": "https://pleroma.example/relay",
    "bcc": [],
    "bto": [],
    "cc": [],
    "id": "https://pleroma.example/activities/3fe13910-73f4-4cdc-9c84-ec7013a3e764",
    "object": "https://relay.example/actor",
    "state": "pending",
    "to": [
        "https://relay.example/actor"
    ],
    "type": "Follow"
}
```

注：
1. JSON-LDコンテキストはJSON-LD処理に対して有効ではありません。litepub-0.1.jsonldドキュメントには、無効なWebFinger関連のコンテキストURLが含まれています。
2. `state`プロパティはJSON-LDコンテキストで定義されていません。

#### リレー購読解除

リレーの購読を解除するには、元の`Follow`アクティビティを`object`として`Undo`を送信します。通常、`Undo`に対する応答はありません。

**Undo/Followリクエストの例**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://pleroma.example/schemas/litepub-0.1.jsonld",
        {
            "@language": "und"
        }
    ],
    "id": "https://pleroma.example/activities/cf9c85e9-f83f-4a02-b598-880f15423f68",
    "object": {
        "actor": "https://pleroma.example/relay",
        "bcc": [],
        "bto": [],
        "cc": [],
        "context": "https://pleroma.example/contexts/d493d02b-7cc9-49dc-995c-d949af0b5417",
        "id": "https://pleroma.example/activities/3fe13910-73f4-4cdc-9c84-ec7013a3e764",
        "object": "https://relay.example/actor",
        "published": "2024-10-18T14:04:11.029802Z",
        "state": "cancelled",
        "to": [
            "https://relay.example/actor"
        ],
        "type": "Follow"
    },
    "published": "2024-10-18T14:04:11.029791Z",
    "to": [ "https://relay.example/actor" ],
    "cc": [],
    "type": "Undo",
    "actor": "https://pleroma.example/relay",
    "context": "https://pleroma.example/contexts/d493d02b-7cc9-49dc-995c-d949af0b5417"
}
```

#### リレーへのメッセージ公開

LitePubリレークライアントアクターは、リレーされたオブジェクト（`Note`など）に対して`Announce`を送信します。最高の相互運用性のためには、`Announce`はアナウンスされたオブジェクトをURIで参照するべきです（オブジェクトを埋め込むのではなく）。

`Announce`アクティビティは、リレーサーバーアクターのフォロワーコレクションにアドレス指定されなければなりません（MUST）。（TODO：管理者アドレス指定も必要かどうかは不明です）。一部のリレーサーバーは`published`プロパティがないアクティビティを拒否するため、このプロパティは含めるべきです。

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://pleroma.example/schemas/litepub-0.1.jsonld",
        {
            "@language": "und"
        }
    ],
    "actor": "https://pleroma.example/relay",
    "to": [
        "https://pleroma.example/relay/followers",
        "https://pleroma.example/users/admin"
    ],
    "bto": [],
    "cc": [],
    "context": "https://pleroma.example/contexts/a59117d9-7f7c-48ec-83b4-5e183e7179b5",
    "id": "https://pleroma.example/activities/e24e46a2-8926-4a20-9f5f-638e06102159",
    "object": "https://pleroma.example/objects/c13bba3c-e7c1-45ac-939f-aa292d23ee8c",
    "published": "2024-10-18T14:06:37.736295Z",
    "type": "Announce"
}
```

#### リレーからのメッセージ受信

リレーから受信したメッセージは、通常`Announce`アクティビティにラップされています。アナウンスの`object`がフェッチされ検証された後、連合タイムラインに表示されます。`Pleroma`はリレーされた`Create`アクティビティ（Mastodon互換性のため）を受け入れるようですが、LD署名が処理されないため、`Create`の`object`を再フェッチします。（TODO：この動作を確認する。）

## その他のリレーサーバーに関する考慮事項

リレーアクターをホストするリレーサーバーは、アクティビティのリレー以外の機能も持ちます。

### WebFinger

リレーサーバーは、リレーアクターに対する[WebFinger]サポートを実装しなければなりません（MUST）。これはMastodonのアクターフェッチ実装のために必要です。LitePub専用のリレーサーバーでは必要ない可能性があります。

### NodeInfo

リレーサーバーは、サーバーのアクティビティとメタデータを宣伝するために[NodeInfo]を実装してもよいです（MAY）。

### オプションのリレーサーバーの動作

リレーサーバーは複数のリレープロトコルをサポートしてもよいです（MAY）。ただし、それらの機能を宣伝する標準的な方法はありません。

リレーサーバーは通常、単一のアクターをホストしますが、任意数のリレーアクターをホストすることもできます。例えば、リレーサーバーは特定のトピック、ハッシュタグ、またはモデレーションカテゴリごとにリレーアクターを持つことができます。リレークライアントは、特定のサーバー内の任意数のリレーアクターを購読できます。

一部のサーバーは動的なリレーアクター作成を実装しています。リレーアクターの`inbox` URIは、ハッシュタグやトピック名に基づいている場合があります。クライアントアクターがこの種のインボックスURIを購読すると、リレーアクターが自動的に作成されます。明らかに、不正なクライアントによって使用された場合、このアプローチにはリスクがあります。

## 参照

- Christine Lemmer Webber, Jessica Tallon, [ActivityPub][ActivityPub], 2018
- James M Snell, Evan Prodromou, [Activity Vocabulary][AS2-Vocab], 2017
- Mastodon Documentation, [LD Signatures][Mastodon LD Signatures], [HTTP Signatures][Mastodon HTTP Signatures]
- S. Bradner, Key words for use in RFCs to Indicate Requirement Levels, [RFC-2119], 1997
- Matthew Sporny, Dave Longley, JSON-LD 1.1, [JSON-LD], 2020
- Dave Longley, Gregg Kellogg, JSON-LD 1.1 Processing Algorithms and API, [JSON-LD-ALGO], 2018
- Graham Klyne, Jeremy J. Carroll, RDF 1.1 Concepts and Abstract Syntax, [RDF], 2014
- Dave Longley, RDF Dataset Canonicalization, (URDNA2015) [RDF-CANON], 2022
- NIST, Secure Hash Standard (SHS), [SHA256], 2015
- Wikipedia, [Base64]
- P. Jones, WebFinger, RFC-7033 [WebFinger], 2013
- Jonne Haß, [NodeInfo], GitHub
- Pleroma Relay, [pleroma-relay]
- LitePub Protocol Suite, [litepub]
- Takeshi Umeda, pub-relay [pub-relay]

[ActivityPub]: https://www.w3.org/TR/activitypub/
[Mastodon LD Signatures]: https://docs.joinmastodon.org/spec/security/#ld
[Mastodon HTTP Signatures]: https://docs.joinmastodon.org/spec/security/#http
[AS2-Vocab]: https://www.w3.org/TR/activitystreams-vocabulary
[RFC-2119]: https://datatracker.ietf.org/doc/html/rfc2119
[JSON-LD]: https://www.w3.org/TR/json-ld11/
[JSON-LD-ALGO]: https://www.w3.org/2018/jsonld-cg-reports/json-ld-api/
[RDF]: https://www.w3.org/TR/rdf11-concepts/
[RDF-CANON]: https://www.w3.org/community/reports/credentials/CG-FINAL-rdf-dataset-canonicalization-20221009/#canonicalization
[SHA256]: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
[Base64]: https://en.wikipedia.org/wiki/Base64
[WebFinger]: https://www.rfc-editor.org/rfc/rfc7033
[NodeInfo]: https://github.com/jhass/nodeinfo
[pleroma-relay]: https://git.pleroma.social/pleroma/relay
[litepub]: https://litepub.social/
[pub-relay]: https://github.com/noellabo/pub-relay

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法律で許される限りにおいて、このFediverse Enhancement Proposalの著者は、この著作物に関するすべての著作権および関連する、または隣接する権利を放棄しました。
```