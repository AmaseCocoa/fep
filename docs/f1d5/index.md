---
slug: "f1d5"
authors: CJ <cjslep@gmail.com>, silverpill <@silverpill@mitra.social>
status: FINAL
dateReceived: 2020-12-13
dateFinalized: 2023-06-02
trackingIssue: https://codeberg.org/fediverse/fep/issues/50
discussionsTo: https://codeberg.org/fediverse/fep/issues/50
---

# FEP-f1d5: フェディバースソフトウェアにおけるNodeInfo

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時13分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/f1d5/fep-f1d5.md)から閲覧できます。

## 概要

NodeInfo は、サーバーレベルのメタデータを公開するための標準的な方法を確立することを目的としたプロトコルです。これにより、ツールやクライアントは、このメタデータを利用してサーバーの健全性を評価したり、エンドユーザーがフェディバース上で使用するサーバーやソフトウェアを選択するのを容易にしたりすることができます。

## 履歴

NodeInfo は、diaspora、friendica、redmatrix ソフトウェアでの使用を目的とした [ActivityPub] プロトコルよりも前に開発されました。NodeInfo がカプセル化した元のプロトコルには、diaspora、pumpio、gnusocial が含まれます。

NodeInfo の仕様は、そのスキーマにおいて非常に厳格であり、しばしば正規表現検証（regex-validation）や、列挙された可能な値の閉じたセットを要求します。これに対する異議として、一部のフィールドの検証を削除し、メタデータの論理的な再構築を行うことで、批判の形として NodeInfo2 フォークが作成されました。NodeInfo と NodeInfo2 を基盤として、[ServiceInfo][ServiceInfo] が一時的に検討されました。

この FEP は、特定のプロトコルの詳細を文書化しようとするものでは**ありません**。詳細については、[NodeInfo][NodeInfoRepository] および [NodeInfo2][NodeInfo2Repository] を参照してください。この FEP は、現在のFediverseソフトウェア開発者に文脈を提供するために、その歴史を明確にし、現在の手法の欠点を特定しようとするものです。

## 要件

この仕様におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119] で記述されている通りに解釈されるものとします。

フェディバースソフトウェアは [NodeInfo][NodeInfoRepository] を実装**すべき**です（SHOULD）。

## 注意事項

この FEP の執筆時点において、コミュニティによって特定された NodeInfo の現状に対する現在の異議は以下の通りです。特定された技術的な代替案は、例示を目的としたものであり、規定するものではないことに注意してください。

*   `software.name` の正規表現（regex）は不必要に厳格です。例えば、大文字、スペース、英字以外の文字、ハイフン以外の特殊文字は許可されていません。
*   `software.version` フィールドが必須であることは、不必要に厳格です。ソフトウェアにバージョン情報の開示を強制することは、潜在的なセキュリティ問題となる可能性があります。
*   `inbound` および `outbound` 要素は、単純な文字列ではなく、列挙型（enums）の閉じたセットとして指定されています。プロトコルのバージョン管理は、名前の変更や新しい列挙型の追加として現れ、不明瞭なバージョン管理につながります。
*   フェディバースソフトウェアは、`openRegistrations` の概念を**持たなければなりません**（MUST）。これは必須であるためです。
*   HTTP Signatures、webfinger、OAuth などの他の機能を識別し、バージョン管理するための拡張可能な方法が欠けています。仕様が非常に厳格である一方で、`metadata` はあまりにも緩すぎます。
*   `usage.users` は非正規化（denormalized）されておらず、実装がソフトウェアにとって意味のある `(アクティビティ数, 日数での期間)` のカスタムペアを提供できません。
*   `usage.users` は、ユーザーIDが実行中のソフトウェアの特定のインスタンスに紐付けられていると仮定しています。ユーザーIDが複数のサーバーにまたがっていたり、複数のグループにまたがっていたり、複数のユーザーコレクション内に存在したりする場合に、`total` ユーザーをどのようにカウントするのか不明確です。複数のソフトウェアインスタンスがそれぞれ、そのユーザーを「自社のソフトウェアを使用している」と合理的に主張する可能性があり、その結果、グローバルにユーザーが複数回カウントされることになります。
*   `usage.users` のアクティビティカウントも同様に、ユーザーIDが実行中のソフトウェアの特定のインスタンスに紐付けられていると仮定しています。上記の理由と同様に、`total` ユーザーカウントがすべての実行中のソフトウェアで同じユーザーの重複カウントにつながる可能性があるのと同様に、アクティビティカウントの `activeHalfYear` および `activeMonth` もグローバルに水増しされたカウントにつながる可能性があります。
*   `activeHalfyear` と `activeMonth` は、それぞれ180日と30日の期間を記述するプロパティとしては不適切な名前です。「半年のうち半分」が180日であることは0%の確率であり、約182.5日であるのは約75%の確率に過ぎません。1ヶ月が30日であるのは約33%の確率に過ぎません。
*   `localPosts` と `localComments` は、例えばオーディオファイルをホストするソフトウェア、ビデオをホストするソフトウェア、またはコメントや投稿を持たないソフトウェアのために、`(種類, カウント)` のペアに非正規化されていません。
*   `localPosts` と `localComments` は必須であり、コメントや投稿を持たないソフトウェアにとっては問題となります。

## 実装

### サーバー

このリストは網羅的ではありません：

*   Mastodon
*   Matrix
*   Pleroma
*   PeerTube
*   WriteFreely
*   Friendica
*   Diaspora
*   PixelFed
*   Misskey
*   Funkwhale
*   Smithereen
*   Plume
*   GNU Social
*   lemmy
*   zap
*   Socialhome
*   epicyon
*   apcore
*   FIRM

### クライアント

*   [The-Federation.Info](https://the-federation.info/)
*   [Hello Matrix Public Servers](https://www.hello-matrix.net/public_servers.php)

## 参考文献

-   Christine Lemmer Webber, Jessica Tallon, [ActivityPub][ActivityPub], 2018
-   Jonne Haß, [jhass/nodeinfo][NodeInfoRepository], 2014
-   Jason Robinson, [jaywink/nodeinfo2][NodeInfo2Repository], 2016
-   Jason Robinson, [ServiceInfo - specification for service metadata][ServiceInfo], 2019
-   S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels][RFC-2119], 1997

[ActivityPub]: https://www.w3.org/TR/activitypub/
[NodeInfoRepository]: https://github.com/jhass/nodeinfo
[NodeInfo2Repository]: https://github.com/jaywink/nodeinfo2
[ServiceInfo]: https://web.archive.org/web/20220201002230/https://talk.feneas.org/t/serviceinfo-specification-for-service-metadata/99
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html

## 著作権

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

法的に可能な限り、このフェディバース拡張提案の著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しました。