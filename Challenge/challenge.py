import codecs
import collections
import math

class Bigram:

    def __init__(self, filename, sentence):
        self.wordlists = self._initwordlists(filename)
        self.bigramlist = self._init2gramlist()
        self.bifreq = collections.Counter(self.bigramlist)
        self.unifreq = self._initunifreq()
        self.N = collections.Counter(self.unifreq.values())
        self.N[0] = 250000 - len(self.unifreq.keys())
        self.sentence = ['<begin>', ] + sentence.split(' ')

    def _initwordlists(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            lines = ['<begin> ' + line for line in f.read().split('\n')]
        wordlists = [line.split(' ') for line in lines]
        return wordlists

    def _init2gramlist(self):
        bigram = []
        for words in self.wordlists:
            for i in range(1, len(words)):
                word = words[i - 1] + ' ' + words[i]
                bigram.append(word)
        return bigram

    def _initunifreq(self):
        list = []
        for wordlist in self.wordlists:
            list.extend(wordlist)
        dic = collections.Counter(list)
        return dic

    def setsentence(self, sentence):
        self.sentence = ['<begin>', ] + sentence.split(' ')

    def getwordcount(self):
        return len(self.unifreq.keys())

    def get2gramfreq(self):
        return self.bifreq.copy()

    def _getP(self, w1, w2):
        if self.unifreq.get(w1, 0) == 0:
            return self.unifreq.get(w2, 0) / sum(self.unifreq.values())

        if self.bifreq.get(w1+' '+w2, 0) > 0:
            c1 = self.unifreq.get(w1, 0)
            c2 = self.bifreq.get(w1 + ' ' + w2, 0)
            if self.N.get(c2, 0)!=0:
                return (c2+1)/c2 * self.N.get(c2+1, 0)/self.N.get(c2, 0) * c2/c1
            else:
                return c2/c1
        elif self.bifreq.get(w1+' '+w2, 0) == 0:
            sum1 = 0
            sum2 = 0
            for i in range(1, len(self.sentence)):
                if self.bifreq.get(self.sentence[i-1]+' '+self.sentence[i], 0) > 0:
                    c1_ = self.unifreq.get(self.sentence[i-1], 0)
                    c2_ = self.bifreq.get(self.sentence[i-1]+ ' '+self.sentence[i], 0)
                    if self.N.get(c2_, 0) != 0:
                        p1 =  (c2_ + 1) / c2_ * self.N.get(c2_ + 1, 0) / self.N.get(c2_, 0) * c2_ / c1_
                    else:
                        p1 = c2_ / c1_
                    sum1 += p1
                    sum2 += self.unifreq.get(self.sentence[i], 0)/sum(self.unifreq.values())
            return (1-sum1)/(1-sum2) * (self.unifreq.get(w2, 0)/sum(self.unifreq.values()))

    def getentropy(self):
        result = 0
        for i in range(1, len(self.sentence)):
            p2 = self._getP(self.sentence[i-1], self.sentence[i])
            # print(p2)
            result += math.log2(p2)
        return -result / (len(self.sentence)-1)

    def getperplexity(self):
        return 2 ** self.getentropy()


if __name__ == '__main__':

    wikifile = '../corpus_Wikipedia_en_abst_10p/enwiki-20150602-abstract-extracted-10.txt'
    sentences = ('Space Stories was a pulp magazine which published five issues',
                 'The Ancient Aramaic alphabet is adapted from the Phoenician alphabet',
                 'BCE It was used to write the Aramaic language',
                 'The moves over the last two days helped fuel that debate',
                 'Two other female chief executives recently stepped down',
                 'Many experts believe congestion pricing is the best way',
                 'From experience gained on this trip and on others',
                 'By the river side were men breaking up',
                 'While waiting here we experienced our first annoyance')

    wiki = Bigram(wikifile, sentences[0])
    print('a. ', wiki.getwordcount(), 'kinds of words')
    print()

    freq = wiki.get2gramfreq().most_common()
    print('b. Bigram frequency')
    for i in range(10):
        print(f'{freq[i][1]:5d} : {freq[i][0]}')
    print()

    print('c,d. Entropy, Perplexity: Sentence')
    for sentence in sentences:
        wiki.setsentence(sentence)
        print(f'{wiki.getentropy():7.4f}, {wiki.getperplexity():10.4f} : {sentence}')



