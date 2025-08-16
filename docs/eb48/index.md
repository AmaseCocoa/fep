---
slug: "eb48"
title: Hashtags
dateReceived: 2024-07-16
discussionsTo: https://socialhub.activitypub.rocks/t/4369
title: Timeline Preferences
authors: AvidSeeker <avidseeker7@protonmail.com>
status: DRAFT
trackingIssue: https://codeberg.org/fediverse/fep/issues/373
---

# FEP-eb48: ハッシュタグ

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/eb48/eb48.md)から閲覧できます。

## 概要

この提案は、Fediverse 全体の投稿におけるハッシュタグの識別と表示のための標準化された方法を導入します。このルールは、ハッシュタグが何で構成され、どのように解析および表示されるべきかを定義し、異なるプラットフォームやクライアント間での一貫性と予測可能性を保証します。

## ハッシュタグのルール

文字列は、以下の基準を満たす場合にハッシュタグと見なされます。

1.  `#` 記号で始まること。
2.  1つ以上の英数字（A-Z、a-z、または0-9の数字）が続くこと。
3.  アンダーバー（`_`）を含めることはできますが、ハッシュタグ自体の中に他の特殊文字、スペース、句読点を含めてはなりません。

## 例

以下の例は、ハッシュタグがどのように識別され、強調表示されるべきかを示しています。

-   `#hashtag`
-   "`#hashtag`"
-   " `#hashtag`"
-   (`#hashtag`/#hashtag)
-   ( `#hashtag`/#hashtag)
-   ( `#hashtag` /#hashtag)
-   ( `#hashtag` / `#hashtag`)
-   -`#hashtag`
-   \_`#hashtag`
-   !`#hashtag`
-   ?`#hashtag`
-   @`#hashtag`
-   ;`#hashtag`
-   ,`#hashtag`
-   .'`#hashtag`
-   [`#hashtag`
-   &`#hashtag`
-   ^`#hashtag`

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法律で可能な限り、このFediverse拡張提案の著者は、この著作物に対するすべての著作権および関連する権利または隣接する権利を放棄しました。