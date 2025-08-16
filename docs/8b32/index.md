---
slug: "8b32"
authors: silverpill <@silverpill@mitra.social>
type: implementation
status: DRAFT
dateReceived: 2022-11-12
trackingIssue: https://codeberg.org/fediverse/fep/issues/29
discussionsTo: https://socialhub.activitypub.rocks/t/fep-8b32-object-integrity-proofs/2725
---

# FEP-8b32: オブジェクトの完全性証明

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時14分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/8b32/fep-8b32.md)から閲覧できます。

## 概要

この提案は、[ActivityPub][ActivityPub]サーバーとクライアントが自己認証可能なアクティビティとオブジェクトを作成する方法を記述します。

HTTP署名（HTTP signatures）は、サーバー間インタラクションにおける認証によく使用されます。しかし、これは認証をアクティビティの配信に結びつけ、プロトコルの柔軟性を制限します。

完全性証明（Integrity proofs）は、デジタル署名とそれらを検証するために必要なパラメータを表す属性のセットです。これらの証明は任意のアクティビティまたはオブジェクトに追加でき、受信者がアクターの身元とデータの完全性を検証することを可能にします。これにより、認証がトランスポートから切り離され、アクティビティのリレー、埋め込みオブジェクト、クライアントサイド署名など、さまざまなプロトコルの改善が可能になります。

## 履歴

Mastodon は[2017年以来](https://github.com/mastodon/mastodon/pull/4687)Linked Data signaturesをサポートしており、その後他の多くのプラットフォームがそれらをサポートしました。これらの署名は完全性証明に似ていますが、他の標準に置き換えられた古い[Linked Data Signatures 1.0](https://github.com/w3c-ccg/ld-signatures/)仕様に基づいています。

## 要件

この文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119][RFC-2119]で記述されている通りに解釈されます。

## 完全性証明

提案される認証メカニズムは、[Data Integrity][DataIntegrity]仕様に基づいています。

### 証明の生成

証明は、*Data Integrity*仕様のセクション[4.2 Add Proof][DI-AddProof]に従って作成されなければなりません（MUST）。

証明の生成プロセスは、以下のステップで構成されます。

- **正規化（Canonicalization）**は、JSONオブジェクトを、ある決定論的アルゴリズムに従ってハッシュ化に適した形式に変換することです。
- **ハッシュ化（Hashing）**は、暗号学的ハッシュ関数を使用して、変換されたデータに対する識別子を計算するプロセスです。
- **署名生成（Signature generation）**は、入力データの完全性を改ざんから保護する値を計算するプロセスです。

結果として得られる証明は、元のJSONオブジェクトの`proof`キーの下に追加されます。オブジェクトは複数の証明を含むことができます（MAY）。

完全性証明で使用される属性のリストは、*Data Integrity*仕様のセクション[2.1 Proofs][DI-Proofs]で定義されています。証明タイプは、セクション[3.1 DataIntegrityProof][DI-DataIntegrityProof]で指定されているように、`DataIntegrityProof`であるべきです（SHOULD）。`proofPurpose`属性の値は`assertionMethod`でなければなりません（MUST）。

証明の`verificationMethod`属性の値は、公開鍵のHTTP(S) URLまたは[DID URL][DID-URL]であることができます。検証メソッドの識別子は、保護されたドキュメントの識別子と[同一オリジン][FEP-fe34-SameOrigin]であるか、異なるオリジンであっても、保護されたドキュメントの識別子との間に確立された[クロスオリジントラスト関係][FEP-fe34-CrossOrigin]を持っていなければなりません（MUST）。

検証メソッドが表現される[制御識別子ドキュメント][ControlledIdentifiers]は、アクターオブジェクト、または[ActivityPub]アクターと証明可能に関連付けられる別のドキュメント（例：[DID][DIDs]ドキュメント）でなければなりません（MUST）。検証メソッドは、制御識別子ドキュメントの`assertionMethod`プロパティに関連付けられなければなりません（MUST）。制御識別子ドキュメントがアクターオブジェクトである場合、実装者は[FEP-521a]で記述されている`assertionMethod`プロパティを使用すべきです（SHOULD）。

### 証明の検証

オブジェクトの受信者は、完全性証明が含まれている場合、証明の検証を実行すべきです（SHOULD）。検証プロセスは、*Data Integrity*仕様のセクション[4.4 Verify Proof][DI-VerifyProof]に従わなければなりません（MUST）。これは、JSONオブジェクトから`proof`値を削除することから始まります。次に、*Controlled Identifiers*仕様のセクション[3.3 Retrieve Verification Method][CI-RetrieveMethod]で記述されているように、制御識別子ドキュメントから検証メソッドが取得されます。その後、オブジェクトは正規化され、ハッシュ化され、証明で指定されたパラメータに従って署名検証が実行されます。

HTTP署名と完全性証明の両方が使用される場合、完全性証明はHTTP署名よりも優先されなければなりません（MUST）。HTTP署名は無視されることがあります（MAY）。

### アルゴリズム

実装者は、完全性証明のためのアルゴリズムを選択する際に、広範な相互運用性を追求することが期待されます。

[eddsa-jcs-2022][eddsa-jcs-2022]暗号スイートが推奨されます（RECOMMENDED）：

- 正規化（Canonicalization）：[JCS][JCS]
- ハッシュ化（Hashing）：SHA-256
- 署名：EdDSA

>[!WARNING]
>`eddsa-jcs-2022`暗号スイートの仕様は安定しておらず、W3C勧告になる前に変更される可能性があります。

### 後方互換性

完全性証明とLinked Data signaturesは、それぞれ異なるプロパティ（`proof`と`signature`）に依存しているため、一緒に使用できます。

レガシーシステムとの互換性が必要な場合、完全性証明はLinked Data signatureの生成前に作成され、挿入されなければなりません（MUST）。

受信したオブジェクトに`proof`と`signature`の両方が存在する場合、完全性証明の検証前にLinked Data signatureを削除しなければなりません（MUST）。

## 例

### 署名されたオブジェクト

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/data-integrity/v1"
  ],
  "id": "https://server.example/objects/1",
  "type": "Note",
  "attributedTo": "https://server.example/users/alice",
  "content": "Hello world",
  "proof": {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://w3id.org/security/data-integrity/v1"
    ],
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-jcs-2022",
    "verificationMethod": "https://server.example/users/alice#ed25519-key",
    "proofPurpose": "assertionMethod",
    "proofValue": "...",
    "created": "2023-02-24T23:36:38Z"
  }
}
```

### 署名されたアクティビティ

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/data-integrity/v1"
  ],
  "id": "https://server.example/activities/1",
  "type": "Create",
  "actor": "https://server.example/users/alice",
  "object": {
    "id": "https://server.example/objects/1",
    "type": "Note",
    "attributedTo": "https://server.example/users/alice",
    "content": "Hello world"
  },
  "proof": {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://w3id.org/security/data-integrity/v1"
    ],
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-jcs-2022",
    "verificationMethod": "https://server.example/users/alice#ed25519-key",
    "proofPurpose": "assertionMethod",
    "proofValue": "...",
    "created": "2023-02-24T23:36:38Z"
  }
}
```

### 埋め込み署名付きオブジェクトを含む署名されたアクティビティ

```json
{
  "@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://w3id.org/security/data-integrity/v1"
  ],
  "id": "https://server.example/activities/1",
  "type": "Create",
  "actor": "https://server.example/users/alice",
  "object": {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://w3id.org/security/data-integrity/v1"
    ],
    "id": "https://server.example/objects/1",
    "type": "Note",
    "attributedTo": "https://server.example/users/alice",
    "content": "Hello world",
    "proof": {
      "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/data-integrity/v1"
      ],
      "type": "DataIntegrityProof",
      "cryptosuite": "eddsa-jcs-2022",
      "verificationMethod": "https://server.example/users/alice#ed25519-key",
      "proofPurpose": "assertionMethod",
      "proofValue": "...",
      "created": "2023-02-24T23:36:38Z"
    }
  },
  "proof": {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      "https://w3id.org/security/data-integrity/v1"
    ],
    "type": "DataIntegrityProof",
    "cryptosuite": "eddsa-jcs-2022",
    "verificationMethod": "https://server.example/users/alice#ed25519-key",
    "proofPurpose": "assertionMethod",
    "proofValue": "...",
    "created": "2023-02-24T23:36:38Z"
  }
}
```

## テストベクトル

[fep-8b32.feature](./fep-8b32.feature)を参照してください。

## 実装

- [Mitra](https://codeberg.org/silverpill/mitra/src/commit/f096ed54e350f4a0121289bcc0d1d5f83b5bbf8b/FEDERATION.md#object-integrity-proofs)
- Vervis
  （[生成](https://codeberg.org/ForgeFed/Vervis/commit/e8e587af26944d3ea8d91f5c47cc3058cf261387)、
  [検証](https://codeberg.org/ForgeFed/Vervis/commit/621275e25762a1c1e5860d07a6ff87b147deed4f)）
- Streams
- [Hubzilla](https://hub.somaton.com/channel/mario?mid=4214a375-3a18-4acb-b546-75c6c4818e2f)
- [Fedify](https://todon.eu/users/hongminhee/statuses/112638238338153870)
- [apsig](https://github.com/AmaseCocoa/apsig/blob/af7af0e106132a51356fc92ed034b11252a1caea8/docs/proof.md)

## ユースケース

- [受信トレイからの転送](https://www.w3.org/TR/activitypub/#inbox-forwarding)
- [会話コンテナ](https://fediversity.site/help/develop/en/Containers)
- [FEP-ef61: ポータブルオブジェクト](https://codeberg.org/fediverse/fep/src/branch/main/fep/ef61/fep-ef61.md)
- [FEP-ae97: クライアントサイドのアクティビティ署名](https://codeberg.org/fediverse/fep/src/branch/main/fep/ae97/fep-ae97.md)

## 参照

- Christine Lemmer Webber, Jessica Tallon, [アクティビティパブ][ActivityPub], 2018
- S. Bradner, [RFCにおける要件レベルを示すためのキーワード][RFC-2119], 1997
- Dave Longley, Manu Sporny, [検証可能なクレデンシャルデータ完全性 1.0][DataIntegrity], 2024
- Manu Sporny, Dave Longley, Markus Sabadello, Drummond Reed, Orie Steele, Christopher Allen, [分散型識別子 (DIDs) v1.0][DIDs], 2022
- Dave Longley, Manu Sporny, Markus Sabadello, Drummond Reed, Orie Steele, Christopher Allen, [制御識別子 v1.0][ControlledIdentifiers], 2025
- silverpill, [FEP-521a: アクターの公開鍵の表現][FEP-521a], 2023
- Dave Longley, Manu Sporny, [データ完全性 EdDSA 暗号スイート v1.0][eddsa-jcs-2022], 2025
- A. Rundgren, B. Jordan, S. Erdtman, [JSON正規化スキーム (JCS)][JCS], 2020
- silverpill, [FEP-fe34: オリジンベースのセキュリティモデル][FEP-fe34], 2024

[ActivityPub]: https://www.w3.org/TR/activitypub/
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html
[DataIntegrity]: https://www.w3.org/TR/vc-data-integrity/
[DI-Proofs]: https://www.w3.org/TR/vc-data-integrity/#proofs
[DI-AddProof]: https://www.w3.org/TR/vc-data-integrity/#add-proof
[DI-DataIntegrityProof]: https://www.w3.org/TR/vc-data-integrity/#dataintegrityproof
[DI-VerifyProof]: https://www.w3.org/TR/vc-data-integrity/#verify-proof
[DIDs]: https://www.w3.org/TR/did-core/
[DID-URL]: https://www.w3.org/TR/did-core/#did-url-syntax
[ControlledIdentifiers]: https://www.w3.org/TR/cid/
[CI-RetrieveMethod]: https://www.w3.org/TR/cid/#retrieve-verification-method
[FEP-521a]: https://codeberg.org/fediverse/fep/src/branch/main/fep/521a/fep-521a.md
[eddsa-jcs-2022]: https://www.w3.org/TR/vc-di-eddsa/#eddsa-jcs-2022
[JCS]: https://www.rfc-editor.org/rfc/rfc8785
[FEP-fe34]: https://codeberg.org/fediverse/fep/src/branch/main/fep/fe34/fep-fe34.md
[FEP-fe34-SameOrigin]: https://codeberg.org/silverpill/feps/src/branch/main/fe34/fep-fe34.md#origin
[FEP-fe34-CrossOrigin]: https://codeberg.org/silverpill/feps/src/branch/main/fe34/fep-fe34.md#cross-origin-relationships

## 著作権

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

法律で許される限りにおいて、このFediverse Enhancement Proposalの著者は、この著作物に関するすべての著作権および関連する権利または隣接する権利を放棄しました。