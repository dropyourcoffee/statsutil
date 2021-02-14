from collections import Counter
from pathlib import Path
import pandas


class BayesSuite(object):
    def __init__(self, obj=None):
        self.d = {}

        if obj is None:
            return

        if "likelihood" not in dir(self):
            raise NoLikelihoodError()

        if isinstance(obj, dict):
            self.d.update(obj.items())
        elif isinstance(obj, pandas.Series):
            self.d.update(obj.value_counts().iteritems())
        else:
            self.d.update(Counter(obj))

        if len(self) > 0:
            self.normalize()

    def __hash__(self):
        return id(self)

    def __str__(self):
        cls = self.__class__.__name__
        return '%s(%s)' % (cls, str(self.d))

    __repr__ = __str__

    def __eq__(self, other):
        return self.d == other.d

    def __len__(self):
        return len(self.d)

    def __iter__(self):
        return iter(self.d)

    def iterkeys(self):
        return iter(self.d)

    def __contains__(self, value):
        return value in self.d

    def __getitem__(self, value):
        return self.d.get(value, 0)

    def __setitem__(self, value, prob):
        self.d[value] = prob

    def print(self):
        """ 확률순으로 출력하기. """
        for val, prob in sorted(self.d.items()):
            print(val, prob)

    @property
    def values(self):
        return self.d.keys()

    @property
    def total(self):
        return sum(self.d.values())

    def update(self, data):
        for hypo in self.values:
            like = self.likelihood(data, hypo)
            self.multiply(hypo, like)
        return self.normalize()

    def normalize(self, fraction = 1.0):
        total = self.total
        if total == 0.0:
            raise ValueError("확률의 총 합이 0 :: (hypothesis 범위에서 나올 수 없는 데이터를 update 한게 아닌지 확인 필요)")

        factor = fraction / total
        for x in self.d:
            self.d[x] *= factor

        return total

    def multiply(self, x, factor):
        """
            likelihood, hypothesis 두 벡터 곱하기.
        :param x:
        :param factor:
        :return:
        """
        self.d[x] = self.d.get(x, 0) * factor


class NoLikelihoodError(Exception):
    def __init__(self):
        super().__init__("likelihood 함수 정의가 되지 않음.")


if __name__ == "__main__":
    print(f":: {Path(__file__).name}  ::\n BayesSuite(obj=None)")

