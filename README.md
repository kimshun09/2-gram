# 2-gram(Bi-gram) Model

言語モデルであるN-gramの例として，2-gramモデルを実装した．

`Challenge/challenge.py`では，Wikipediaのコーパス`corpus_Wikipedia_en_abst_10p/nwiki-20150602-abstract-extracted-10.txt`を用いて以下を実行する．

1. コーパス中に出現する単語の種類数を表示．
2. コーパス中の2単語組の出現回数の上位10個を表示．バックオフスムージングを用いる．
3. 2をもとに2-gramを計算し与えられた文のテストセットエントロピーとテストセットパープレキシティを表示する．

このエントロピーが低いほど単語確率に偏りがあり，良い言語モデルであると言える．

また，パープレキシティは平均次単語数であるため，低いほどよい言語モデルであると言える．

実行例は以下の通り．

```
$ python3 challenge.py
a.  191295 kinds of words

b. Bigram frequency
67084 : is a
43362 : of the
43154 : in the
31142 : <begin> The
15323 : is an
12975 : was a
11824 : It is
10435 : is the
 9823 : It was
 9695 : species of

c,d. Entropy, Perplexity: Sentence
 8.3141,   318.2598 : Space Stories was a pulp magazine which published five issues
 6.7879,   110.4973 : The Ancient Aramaic alphabet is adapted from the Phoenician alphabet
 7.9173,   241.7375 : BCE It was used to write the Aramaic language
10.5267,  1475.2196 : The moves over the last two days helped fuel that debate
10.2444,  1213.0251 : Two other female chief executives recently stepped down
12.2709,  4942.1900 : Many experts believe congestion pricing is the best way
11.6140,  3134.3585 : From experience gained on this trip and on others
10.1877,  1166.2599 : By the river side were men breaking up
16.0135, 66151.5667 : While waiting here we experienced our first annoyance
```

c,dにおいて，1-3文目は英語版Wikipedia，4-6文目は英語ニュース，7-9文目は英語文学から適当に取ってきたものである．

英語版Wikipediaの方が他の種類の文よりもエントロピー・パープレキシティが低くなっていた．
これは，コーパスの中に含まれている文章であり，出現確率の大小がはっきりついているからであるといえる．
また，英語文学では英語ニュースと比べると比較的パープレキシティが高く，極端に大きなものも存在している．
英語版Wikipediaと英語ニュースは説明文である一方英語文学は物語文であるので文章の種類も大きく異なっている．
ゆえに英語文学のほうが曖昧性が高くなっているのだと考えられる．