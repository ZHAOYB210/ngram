
class Ngram(object):
    def __init__(self, lm, order):
        self.order = order
        self.lm = self.readlm(lm)

    def readlm(self, filepath):
        f = open(filepath)
        lines = f.readlines()
        dict = {}
        for line in lines:
            line = line.strip().split('\t')
            if len(line) >= 2 and line[0] != 'ngram':
                if len(line) == 2:
                    line.append('0')
                dict[line[1]] = [float(line[0]), float(line[2])]
        return dict

    def pa_z(self, str):
        index = " ".join(str)
        try:
            ret = self.lm[index][0]
            return ret
        except:
            if len(str) == 1:
                return float("-Inf")
            i = " ".join(str[:-1])
            try:
                bow = self.lm[i][1]
                return bow + self.pa_z(str[1:])
            except:
                return self.pa_z(str[1:])

    def getppl(self, test_string):
        total = 0.0
        OOVs = 0
        logprobs = []
        test_string = test_string.strip().split(' ')
        test_string.append('</s>')
        test_string.insert(0, '<s>')
        for index in xrange(1, len(test_string)):
            a = 0 if index < self.order else index+1-self.order
            p = self.pa_z(test_string[a:index+1])
            if p != float("-Inf"):
                total += p
            else:
                OOVs += 1
            logprobs.append(p)
        d_ppl = len(test_string)-1 - OOVs
        d_ppl1 = len(test_string)-2 - OOVs
        ppl = pow(10, (-total) / d_ppl) if d_ppl > 0 else "undefined"
        ppl1 = pow(10, (-total) / d_ppl1) if d_ppl1 > 0 else "undefined"
        return logprobs, total, ppl, ppl1