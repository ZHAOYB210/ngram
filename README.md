LM -> ppl

example

from ngram import Ngram

a = Ngram("example.lm", order=3)
a.getppl(test_string)


return value is a quadruple

([words_prob], sentence_logprob, sentence_ppl, sentence_ppl1)