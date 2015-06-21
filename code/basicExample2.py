import numpy as np
import scipy.stats as stats

x = np.array([[1,2,3,4,5]])
y = x + stats.norm(0, 1).rvs(5)

x = x.T; y = y.T

train = x[:3], y[:3]
valid = x[3:], y[3:]

exp = theanets.Experiment(theanets.Regressor, layers = (1, 1))
exp.train(train, valid, algorithm='sgd', learning_rate=1e-4, momentum=0.9)
 
exp.network.predict(x)