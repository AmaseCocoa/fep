---
slug: "c16b"
authors: ilja <ilja@ilja.space>
status: DRAFT
dateReceived: 2024-08-10
discussionsTo: https://socialhub.activitypub.rocks/t/fep-c16b-formatting-mfm-functions/4448
relatedFeps: FEP-dc88
trackingIssue: https://codeberg.org/fediverse/fep/issues/383
---

# FEP-c16b: MFM関数のフォーマット

!!! Warning
    このFEPは`gemini-2.5-flash`を利用して`2025-08-17`に翻訳されました。オリジナルのFEPは[ここ](https://codeberg.org/fediverse/fep/src/branch/main/fep/c16b/c16b.md)から閲覧できます。

## 概要

このFEPは、カスタムクラスと[data-* 属性 (data-* attributes)]を持つHTMLを使用して、ActivityPubの投稿コンテンツ内のMFMをフォーマットする方法を推奨します。さらに、このFEPは、このHTML表現が使用されていることを示す新しい拡張用語を提供します。

## 要件

この文書におけるキーワード「MUST」、「MUST NOT」、「REQUIRED」、「SHALL」、「SHALL NOT」、「SHOULD」、「SHOULD NOT」、「RECOMMENDED」、「MAY」、「OPTIONAL」は、[RFC-2119]で記述されている通りに解釈されるものとします。

「Fediverse実装」または「実装」は、[ActivityPub]で記述されているActivityPub準拠クライアント、ActivityPub準拠サーバー、またはActivityPub準拠連合サーバーとして解釈されるものとします。

## 謝辞

(このセクションは非規範的です。)

このFEPの核となるアイデアは、Foundkeyの課題トラッカー[1]のJohan150に帰属します。具体的には、カスタムクラスと`data-*`属性を持つ`span`要素を使用して、HTMLでMFM関数を表現するという提案です。

## 経緯

(このセクションは非規範的です。)

Fediverseの実装では、テキストの入力としてマークアップ言語を許可するのが一般的です。このコンテンツの連合は、通常、このテキスト入力を、他の実装が容易に理解できる適切なHTML表現に変換することによって行われます。このHTML表現は、[ActivityStreams]オブジェクトの`content`プロパティを使用してActivityPub上で連合されます。一方、ActivityPubによって追加された`source`プロパティは、オプションで元の入力と入力形式を提供するために使用できます。

Misskeyは、MFM（[Markup language For Misskey]）として知られる独自のマークアップ言語を使用しています。MFMは、主にHTML、Markdown、Katex、および`$[name content]`形式のカスタムMFM関数の組み合わせで構成されています。これらのMFM関数が意図するものを適切に表示するには、一般的に複雑なCSSやJavaScriptが必要です。そのため、`content`には簡略化されたHTML表現のみが提供されます。この表現は、受信側の実装が著者の意図を常に適切に表示できないほど多くの情報を削除してしまう可能性があります。MFMを正しく表示したい受信側の実装にとって唯一の選択肢は、`source`プロパティの`mediaType`が`text/x.misskeymarkdown`の値を持つ場合に、その`source`プロパティの`content`を再解析することです。これは、不必要なオーバーヘッドを引き起こすだけでなく、特に2つの実装が異なるパーサーを使用している場合に、互換性の問題も引き起こします。

## MFM関数

(このセクションは非規範的です。)

MFM関数は、名前、オプションで1つ以上の属性（値を持つ場合と持たない場合がある）、およびコンテンツで構成されます。その形式は`$[name.attribute1,attribute2=value content]`です。

### 例

(このセクションは非規範的です。)

```
$[x2 Misskey expands the world of the Fediverse]
$[jelly.speed=2s Misskey expands the world of the Fediverse]
$[spin.x,speed=0.5s Misskey expands the world of the Fediverse]
```

## MFM関数のHTML表現

MFM関数をHTMLで表現する場合、`span`要素を使用しなければなりません（MUST）。`span`要素は、`name`がMFM関数の名前である`mfm-name`というクラスを持たなければなりません（MUST）。MFM関数が属性を持つ場合、`span`要素は、各属性に対して`data-mfm-attributename`という`data-*`属性を持たなければなりません（MUST）。ここで`attributename`は当該属性の名前です。MFM関数の属性が値を持つ場合、`data-*`属性は同じ値を持たなければなりません（MUST）。

### 例

(このセクションは非規範的です。)

これにより、以前の例は以下のように変換されます。

```
<span class="mfm-x2">Misskey expands the world of the Fediverse</span>
<span class="mfm-jelly" data-mfm-speed="2s">Misskey expands the world of the Fediverse</span>
<span class="mfm-flip" data-mfm-x data-mfm-speed="0.5s">Misskey expands the world of the Fediverse</span>
```

## その他のMFMコンポーネント

このFEPはMFM関数の表現に焦点を当てていますが、MFMはこれらのMFM関数だけから構成されているわけではありません。`content`プロパティ内のHTML表現は、受信側の実装がMFMが伝える内容を正しく表示できるように、正確かつ完全でなければなりません（MUST）。

HTMLとMarkdownは通常、`content`プロパティで正しく表現されており、どちらもFediverseで広く使用されています。そのため、これらはMFM関数と同じ意味で問題があるとは見なされません。

Katexも同様に、通常`content`プロパティで適切に表現されないという問題を抱えています。Katex入力をHTMLとして適切に表現するには、[FEP-dc88]を使用すべきです（SHOULD）。

## 発見

(このセクションは非規範的です。)

MFM対応ではあるがFEP-c16bに準拠していない実装との互換性が必要な場合、`source`は引き続き`"mediaType": "text/x.misskeymarkdown"`を使用して連合される必要があるかもしれません。一方、この実装からの受信`source`は、引き続き再解析が必要となる場合があります。そのため、FEP-c16b準拠の実装に対して、`content`を直接使用できることを通知するための発見メカニズムが必要です。

この目的のために、[FEP-888d]で記述されているように、新しい拡張用語が提案されています。

### htmlMfm

`content`がFEP-c16bに準拠していることを示すために、実装は`htmlMfm`という拡張用語を値`true`とともに使用してもよい（MAY）。`content`がFEP-c16bに準拠していない場合、実装は`htmlMfm`という拡張用語を値`true`とともに使用してはなりません（MUST NOT）が、値`false`とともに使用してもよい（MAY）。

* 説明: `content`がFEP-c16bに準拠していることを示すフラグ。
* URI: <code>https://w3id.org/fep/c16b#htmlMfm</code></li>
* ドメイン: <code>https://www.w3.org/ns/activitystreams#Object</code></li>
* 範囲: Boolean</li>

## 例

(このセクションは非規範的です。)

```json
{
	"@context": [
		"https://www.w3.org/ns/activitystreams",
		{
			"htmlMfm": "https://w3id.org/fep/c16b#htmlMfm"
		}
	],
	"content": "<span class=\"mfm-spin\" data-mfm-x data-mfm-speed=\"0.5s\">Misskey expands the world of the Fediverse</span>",
	"source": {
		"content": "$[spin.x,speed=0.5s Misskey expands the world of the Fediverse]",
		"mediaType": "text/x.misskeymarkdown"
	},
	"htmlMfm": true
}
```

## 実装

- [Akkoma](https://akkoma.dev/AkkomaGang/akkoma/src/branch/stable/FEDERATION.md#supported-feps)

## 参照

- [data-* 属性（data-* attributes）]: [HTML Living Standard](https://html.spec.whatwg.org/multipage/dom.html#embedding-custom-non-visible-data-with-the-data-*-attributes)の一部
- [RFC-2119] S. Bradner, [RFCにおける要件レベルを示すためのキーワード](https://datatracker.ietf.org/doc/html/rfc2119), 1997
- [ActivityPub] Christine Lemmer Webber, Jessica Tallon, [ActivityPub](https://www.w3.org/TR/activitypub/), 2018
- [1] Johan150, [HTMLを使用してコンテンツフィールドでMFMを連合する](https://akkoma.dev/FoundKeyGang/FoundKey/issues/343#issuecomment-7344), 2023
- [ActivityStreams] James M Snell, Evan Prodromou, [ActivityStreams 2.0](https://www.w3.org/TR/activitystreams-core), 2017
- [Markup language For Misskey], [MFM](https://misskey-hub.net/en/docs/for-users/features/mfm/)
- [FEP-dc88] Calvin Lee, [FEP-dc88: 数学のフォーマット](https://codeberg.org/ilja/fep/src/branch/main/fep/dc88/fep-dc88.md), 2023
- [FEP-888d] a, [FEP-888d: FEP固有の名前空間のベースとしてhttps://w3id.org/fepを使用する](https://codeberg.org/ilja/fep/src/branch/main/fep/888d/fep-888d.md), 2023

## 著作権

CC0 1.0 Universal (CC0 1.0) パブリックドメイン献呈

法律で許される限りにおいて、このFediverse拡張提案の著者は、この著作物に関するすべての著作権および関連する権利または隣接する権利を放棄しました。