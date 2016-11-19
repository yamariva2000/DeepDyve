import json

import pandas as pd

with open("../Downloads/DeepDyve.json") as fileobject:
    str = fileobject.next()
    deepid = str[:11]
    rest = str[11:]

    d = json.loads(rest)
    d["permdld"] = deepid
    b = d['body']

    # print json.dumps(d['body'])
for k, i in d.iteritems():
    p = pd.Series(d[k])
    df = pd.DataFrame(p)
    print df

assert False
# generate some data to play with
X, y = samples_generator.make_classification(
    n_informative=5, n_redundant=0, random_state=42)
# ANOVA SVM-C
anova_filter = SelectKBest(f_regression, k=5)
clf = svm.SVC(kernel='linear')
anova_svm = Pipeline([('anova', anova_filter), ('svc', clf)])
# You can set the parameters using the names issued
# For instance, fit using a k of 10 in the SelectKBest
# and a parameter 'C' of the svm
anova_svm.set_params(anova__k=10, svc__C=.1).fit(X, y)

prediction = anova_svm.predict(X)
anova_svm.score(X, y)

# getting the selected features chosen by anova_filter
anova_svm.named_steps['anova'].get_support()