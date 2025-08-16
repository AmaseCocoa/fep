---
slug: "67ff"
authors: silverpill <@silverpill@mitra.social>
status: FINAL
dateReceived: 2023-09-05
dateFinalized: 2024-09-22
trackingIssue: https://codeberg.org/fediverse/fep/issues/157
discussionsTo: https://socialhub.activitypub.rocks/t/fep-67ff-federation-md/3555
---

# FEP-67ff: FEDERATION.md

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025年08月16日 23時15分`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/67ff/fep-67ff.md)から閲覧できます。

## 概要

`FEDERATION.md` は、連合型サービスとの相互運用性を実現するために必要な情報を含むファイルです。これは元々、Darius Kazemi 氏によって SocialHub フォーラムの [半標準的な方法での連合動作の文書化？] というトピックで提案されました。

## 要件

本文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119] で記述されている通りに解釈されるものとします。

## 構造

`FEDERATION.md` ファイルは任意の構造と内容を持つことができます。唯一の要件は以下の通りです。

- 有効な Markdown ドキュメントであること。
- プロジェクトのコードリポジトリのルートに配置されていること。プロジェクトのドキュメントが別の場所にある場合、`FEDERATION.md` ファイルはその場所へのリンクを含むことができます。
- 実装されている連合プロトコルのリストを含むべきです。
- サポートされている Fediverse Enhancement Proposals (FEP) のリストを含むべきです。

## テンプレート

(このセクションは規範的ではありません。)

```markdown
# Federation

## Supported federation protocols and standards

- [ActivityPub](https://www.w3.org/TR/activitypub/) (Server-to-Server)
- [WebFinger](https://webfinger.net/)
- [Http Signatures](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures)
- [NodeInfo](https://nodeinfo.diaspora.software/)

## Supported FEPs

- [FEP-f1d5: NodeInfo in Fediverse Software](https://codeberg.org/fediverse/fep/src/branch/main/fep/f1d5/fep-f1d5.md)

## ActivityPub

<!-- Describe activities and extensions. -->

## Additional documentation

<!-- Add links to documentation pages. -->
```

## 実装例

- [gathio](https://github.com/lowercasename/gathio/blob/main/FEDERATION.md)
- [Streams](https://codeberg.org/streams/streams/src/branch/dev/FEDERATION.md)
- [Smithereen](https://github.com/grishka/Smithereen/blob/master/FEDERATION.md)
- [Mastodon](https://github.com/mastodon/mastodon/blob/main/FEDERATION.md)
- [Hometown](https://github.com/hometown-fork/hometown/blob/hometown-dev/FEDERATION.md)
- [Mitra](https://codeberg.org/silverpill/mitra/src/branch/main/FEDERATION.md)
- [Emissary](https://github.com/EmissarySocial/emissary/blob/main/FEDERATION.md)
- [Vervis](https://codeberg.org/ForgeFed/Vervis/src/branch/main/FEDERATION.md)
- [WordPress](https://github.com/Automattic/wordpress-activitypub/blob/master/FEDERATION.md)
- [Postmarks](https://github.com/ckolderup/postmarks/blob/main/FEDERATION.md)
- [Bovine](https://bovine-herd.readthedocs.io/en/latest/FEDERATION/) in [repo](https://codeberg.org/bovine/bovine/src/branch/main/bovine_herd/docs/docs/FEDERATION.md) and the [symlink](https://codeberg.org/bovine/bovine/src/branch/main/FEDERATION.md)
- [BookWyrm](https://github.com/bookwyrm-social/bookwyrm/blob/main/FEDERATION.md)
- [Hatsu](https://github.com/importantimport/hatsu/blob/main/FEDERATION.md)
- [tootik](https://github.com/dimkr/tootik/blob/main/FEDERATION.md)
- [Bridgy Fed](https://github.com/snarfed/bridgy-fed/blob/main/FEDERATION.md)
- [Friendica](https://git.friendi.ca/friendica/friendica/src/branch/develop/FEDERATION.md)
- [PieFed](https://codeberg.org/rimu/pyfedi/src/branch/main/FEDERATION.md)
- [Akkoma](https://akkoma.dev/AkkomaGang/akkoma/src/branch/stable/FEDERATION.md)
- [Iceshrimp.NET](https://iceshrimp.dev/iceshrimp/Iceshrimp.NET/src/branch/dev/FEDERATION.md)
- [Forte](https://codeberg.org/fortified/forte/src/branch/dev/FEDERATION.md)
- [NeoDB](https://github.com/neodb-social/neodb/blob/main/FEDERATION.md)
- [FIRM](https://github.com/steve-bate/firm/blob/main/FEDERATION.md)
- [Vernissage](https://github.com/VernissageApp/VernissageServer/blob/main/FEDERATION.md)
- [apkit](https://github.com/fedi-libs/apkit/blob/main/FEDERATION.md)
- [Tvmarks](https://github.com/stefanhayden/tvmarks/blob/main/FEDERATION.md)
- [Manyfold](https://github.com/manyfold3d/manyfold/blob/main/FEDERATION.md)

## 参照

- Darius Kazemi, [半標準的な方法での連合動作の文書化？][半標準的な方法での連合動作の文書化？], 2020
- S. Bradner, [Key words for use in RFCs to Indicate Requirement Levels][RFC-2119], 1997

[半標準的な方法での連合動作の文書化？]: https://socialhub.activitypub.rocks/t/documenting-federation-behavior-in-a-semi-standard-way/453
[RFC-2119]: https://tools.ietf.org/html/rfc2119.html

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法的に可能な限り、この Fediverse Enhancement Proposal の著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しています。