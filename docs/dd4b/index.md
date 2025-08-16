---
slug: "dd4b"
authors: Evan Prodromou <evan@socialwebfoundation.org>
status: DRAFT
discussionsTo: https://codeberg.org/evanp/fep/issues
dateReceived: 2025-02-21
trackingIssue: https://codeberg.org/fediverse/fep/issues/511
---

# FEP-dd4b: 引用投稿

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/dd4b/fep-dd4b.md)から閲覧できます。

## 概要

この FEP は、[Activity Streams 2.0][AS2] および [Activity Vocabulary][Vocabulary] で定義されている、引用投稿、すなわち追加のコメントを伴う [Announce](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-announce) アクティビティを作成するためのメカニズムを記述します。

## 動機

他のアクターによって作成されたコンテンツやアクティビティを再配布することは、ソーシャルウェブにおける主要な活動です。[Announce](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-announce) アクティビティタイプは、この活動を表すために Activity Streams 2.0 ("AS2") で定義されています。`Announce` は ActivityPub で共有機能を提供するために使用されます。詳細については、[7.11 Announce Activity (sharing)](https://www.w3.org/TR/activitypub/#announce-activity-inbox) を参照してください。

AS2 の [Activity](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-activity) オブジェクトタイプは、[Object](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-activity) タイプのすべてのプロパティを継承します。これは、**すべて**のアクティビティタイプが、ソーシャルウェブ上の第一級コンテンツとして表現するための豊富なプロパティセットを持っていることを意味します。`Announce` タイプも例外ではありません。

しかし、ActivityPub 仕様は、共有コンテンツに追加のコメント、メタデータ、およびファイルを提供するためにこれらのプロパティを使用する方法を記述していません。「引用ツイート（["quote Tweets"](https://en.wikipedia.org/wiki/Tweet_(social_media)#Quote_tweets)）」、「コメント付きリポスト」、「引用投稿（["quote posts"](https://help.instagram.com/279780184399513)）」と呼ばれるこの種の拡張された共有は、共有オブジェクトに追加のコンテキストを与えます。

この FEP は、このコメントを提供するために `content` プロパティを使用する方法、およびこのコンテキストで役立つ可能性のある他のプロパティについて記述します。これは Activity Streams 2.0 の一般的な使用に適用されます。ActivityPub に適用される箇所は明記されています。

## 仕様

- `Announce` アクティビティの `object` プロパティは、共有コンテンツへの参照でなければなりません（MUST）。これは、JSON オブジェクトまたは URL のいずれかとして、AS2 の `Object` または `Link` であっても構いません（MAY）。
- `Announce` アクティビティの `content` プロパティは、共有コンテンツに関する追加のコメントを提供するために使用されても構いません（MAY）。
- `Announce` アクティビティの `attachment` プロパティは、共有コンテンツまたはコメントに関連する追加のメディアコンテンツを提供するために使用されても構いません（MAY）。
- `Announce` アクティビティの `tag` プロパティは、共有コンテンツまたはコメントに関する、[Mention](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-mention) オブジェクトや [Hashtag][Miscellany] オブジェクトなどの追加のメタデータを提供するために使用されても構いません（MAY）。
- `Announce` アクティビティの `inReplyTo` プロパティは、`Announce` アクティビティを返信として別のオブジェクトに接続するために使用されても構いません（MAY）。返信先のオブジェクトは共有コンテンツであっても構いませんが、これは一般的ではありません。また、別の会話の一部である場合もあります。
- `inReplyTo` プロパティを持つ `Announce` アクティビティは、返信先のオブジェクトの `replies` コレクションに含まれるべきです（SHOULD）。
- `Announce` アクティビティは、[7.11 Announce Activity (sharing)](https://www.w3.org/TR/activitypub/#announce-activity-inbox) で定義されているように、追加のプロパティに関わらず、共有コンテンツの `shares` コレクションの一部として数えられるべきです（SHOULD）。

## 例

### 基本的な引用投稿

これは、アクターが別のノートをコメント付きで共有する、シンプルな引用投稿を表します。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/aaabbbccc",
  "type": "Announce",
  "actor": "https://example.com/users/evan",
  "to": "https://example.com/users/evan/followers",
  "object": {
    "id": "https://example.com/notes/1234",
    "type": "Note",
    "attributedTo": "https://example.com/users/franklin"
  },
  "content": "I think that this is a good point and should be shared."
}
```

### 添付ファイル付き引用投稿

これは、アクターが別のノートをコメントと画像付きで共有する、添付ファイル付き引用投稿を表します。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/dddeeefff",
  "type": "Announce",
  "actor": "https://example.com/users/evan",
  "to": "https://example.com/users/evan/followers",
  "object": {
    "id": "https://example.com/notes/1234",
    "type": "Note",
    "attributedTo": "https://example.com/users/franklin"
  },
  "content": "The author describes the rock formations of Crete; here's an example from my recent visit.",
  "attachment": {
    "type": "Link",
    "mediaType": "image/jpeg",
    "url": "https://example.com/images/1234.jpg"
  }
}
```

### ハッシュタグ付き引用投稿

これは、アクターが別のノートをコメントとハッシュタグ付きで共有する、ハッシュタグ付き引用投稿を表します。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/ghhiijjkk",
  "type": "Announce",
  "actor": "https://example.com/users/evan",
  "to": "https://example.com/users/evan/followers",
  "object": {
    "id": "https://example.com/notes/1234",
    "type": "Note",
    "attributedTo": "https://example.com/users/franklin"
  },
  "content": "Great description of Cretan geology; saving it for my next trip. <a href='https://example.com/tags/evanstriptocrete'>#evanstriptocrete</a>",
  "tag": {
    "type": "Hashtag",
    "href": "https://example.com/tags/evanstriptocrete",
    "name": "evanstriptocrete"
  }
}
```

### メンション付き引用投稿

これは、アクターが別のノートをコメントとメンション付きで共有する、メンション付き引用投稿を表します。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/lllmmnnoo",
  "type": "Announce",
  "actor": "https://example.com/users/evan",
  "to": ["https://example.com/users/evan/followers", "https://example.com/users/jeff"],
  "object": {
    "id": "https://example.com/notes/1234",
    "type": "Note",
    "attributedTo": "https://example.com/users/franklin"
  },
  "content": "<a href='https://example.com/users/jeff'>@jeff</a> you might like this Cretan geology article.",
  "tag": {
    "type": "Mention",
    "href": "https://example.com/users/jeff",
    "name": "jeff"
  }
}
```

引用されたコンテンツの作者もメンションできます。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/pppqqqrrr",
  "type": "Announce",
  "actor": "https://example.com/users/evan",
  "to": ["https://example.com/users/evan/followers", "https://example.com/users/franklin"],
  "object": {
    "id": "https://example.com/notes/1234",
    "type": "Note",
    "attributedTo": "https://example.com/users/franklin"
  },
  "content": "<a href='https://example.com/users/franklin'>@franklin</a> wrote this great Cretan geology article.",
  "tag": {
    "type": "Mention",
    "href": "https://example.com/users/franklin",
    "name": "franklin"
  }
}
```

### 返信としての引用投稿

引用投稿は、多くの場合、別の情報源からの証拠や情報を共有するために、返信として使用できます。

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "id": "https://example.com/activities/rrrsssttt",
  "type": "Note",
  "actor": "https://example.com/users/jeff",
  "to": "https://example.com/users/jeff/followers",
  "content": "Does anyone know where I can find a good article on Cretan geology?",
  "replies": {
    "id": "https://example.com/activities/rrrsssttt/replies",
    "type": "Collection",
    "totalItems": 1,
    "items": [
      {
        "id": "https://example.com/activities/lllmmnnoo",
        "type": "Announce",
        "actor": "https://example.com/users/evan",
        "object": {
          "id": "https://example.com/notes/1234",
          "type": "Note",
          "attributedTo": "https://example.com/users/franklin"
        },
        "content": "<a href='https://example.com/users/jeff'>@jeff</a> you might like this Cretan geology article.",
        "tag": {
          "type": "Mention",
          "href": "https://example.com/users/jeff",
          "name": "jeff"
        },
        "inReplyTo": "https://example.com/activities/rrrsssttt"
      }
    ]
  }
}
```

## ユーザーインターフェースのガイダンス

引用投稿の一般的な表現は、`Announce` の `object` を埋め込みカードまたは他の表現として含め、`Announce` オブジェクトの `content` を導入テキストとして使用することです。

![マイクロブログインターフェースでの引用投稿の例](quote-post.png)

## セキュリティに関する考慮事項

すべての `Announce` アクティビティにおいて、共有コンテンツのどの程度を `Announce` アクティビティの受信者に公開するかを考慮することが重要です。URL を参照として使用したり、この FEP の例のように限られたメタデータを含めたりすることで、共有コンテンツの公開サーバーがコンテンツへのアクセスを制御できるようになります。詳細については、[ActivityPub Primer][Primer] の [共有オブジェクトの包含（Inclusion of the shared object）](https://www.w3.org/wiki/ActivityPub/Primer/Announce_activity#Inclusion_of_the_shared_object) を参照してください。

## プライバシーに関する考慮事項

### 共有されることへの同意

引用されたコンテンツの作成者は、`shares` コレクションを使用して、引用されることへの同意を示すことができます。作成者が引用されることに同意する場合、引用投稿を `shares` コレクションに追加できます。同意しない場合、引用投稿を省略するか、削除できます。

サーバーは、作成者が `shares` コレクションに追加したり削除したりできる機能（affordances）を提供するべきです（SHOULD）。サーバーは、元の作者が明示的に追加しない限り `Announce` アクティビティが `shares` コレクションに追加されないオプトイン同意を提供しても構いません（MAY）。サーバーは、`Announce` アクティビティが受信時に自動的に `shares` コレクションに追加されるが、元の作者によって削除できるオプトアウト同意を提供しても構いません（MAY）。

引用投稿の消費者は、発行者が同意を表明しているかどうかを判断するために、いつでも `shares` コレクションを参照できます。同意はいつでも延長または撤回できます。

消費者は、元の作者が引用投稿に同意しているかどうかを示すべきです（SHOULD）。また、元の作者の同意がない引用投稿を不明瞭にしたり、非表示にしたりしても構いません（MAY）。

## 参照

- James Snell, Evan Prodromou, et al. [Activity Streams 2.0][AS2]. W3C勧告。2018年5月8日。
- James Snell, Evan Prodromou, et al. [Activity Streams Vocabulary][Vocabulary]. W3C勧告。2018年5月8日。
- Christine Lemmer-Webber, Jessica Tallon, et al. [ActivityPub][ActivityPub]. W3C勧告。2018年1月23日。
- Evan Prodromou. [ActivityPub Miscellaneous Terms][Miscellany]. W3Cソーシャルウェブコミュニティグループドラフトレポート。2024年10月3日。
- W3Cメンバーおよび貢献者。[ActivityPub Primer][Primer]. W3C Wiki. 2023年以降。

[ActivityPub]: https://www.w3.org/TR/activitypub/
[AS2]: https://www.w3.org/TR/activitystreams-core/
[Vocabulary]: https://www.w3.org/TR/activitystreams-vocabulary/
[Miscellany]: https://swicg.github.io/miscellany/
[Primer]: https://www.w3.org/wiki/ActivityPub/Primer

## 著作権

CC0 1.0 ユニバーサル (CC0 1.0) パブリックドメイン献呈

法律で許される限り、このFediverse Enhancement Proposalの著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しました。