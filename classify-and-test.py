import os
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier


training_set = load_files('training')
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(training_set.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, training_set.target)

num_correct = 0
num_missed = 0

for (subdir, _, fnames) in os.walk('testing/'):
    if fnames:
        bugnum = os.path.basename(subdir)
        print bugnum, fnames
        for fname in fnames:
            doc = open(os.path.join(subdir, fname)).read()
            if not len(doc):
                print "--> (skipping, empty)"
            X_new_counts = count_vect.transform([doc])
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)
            predicted_bugnum = training_set.target_names[clf.predict(X_new_tfidf)[0]]
            if bugnum == predicted_bugnum:
                num_correct += 1
                print "--> correct"
            else:
                num_missed += 1
                print "--> missed (%s)" % predicted_bugnum
print "Correct: %s Missed: %s Ratio: %s" % (num_correct, num_missed, num_correct / float(num_correct + num_missed))
