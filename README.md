## Stats Util 모음.

### Bayesian Suite

likelihood 로 posterior 확률을 update 하는 기본적인 bayesian model

```python
class MyModel(BayesianSuite):
    def likelihood(self, data, hypo):
        
        return 1 ## P(D|H) 를 리턴

MyModel([1,2,3]) ## hypothesis
MyModel.update[2]
MyModel.print()

```