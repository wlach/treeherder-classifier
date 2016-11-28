This is a simple test of using scikit-learn on treeherder data. To try it out,
install scikit-learn (and its dependencies) in a virtualenv, then run:

    # extract test data
    tar jxf training.tar.bz2
    tar jxf testing.tar.bz2
    python classify-and-test.py

You should get a bunch of output as the script creates a classifier based on
the training data and attempts to use it on the test set of data.
