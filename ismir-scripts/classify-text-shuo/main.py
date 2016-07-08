# -*- coding: utf-8 -*-



import util
import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sklearn.svm
import sklearn.naive_bayes
import sklearn.neighbors
from colorama import init
from termcolor import colored
import sys
import os
import glob,codecs,re

def main():
    init()

    # get the dataset 
    #print colored("Where is the dataset?", 'cyan', attrs=['bold'])
    #print colored('warning: files might get deleted if they are incompatible with utf8', 'yellow')
    ans = sys.argv[1]
    # remove any newlines or spaces at the end of the input
    path = ans.strip('\n')
    if path.endswith(' '):
        path = path.rstrip(' ')

    # preprocess data into two folders instead of 6
    print colored("Reorganizing folders, into two classes", 'cyan', attrs=['bold'])
    #reorganize_dataset(path)


    print '\n\n'

    # do the main test, permutating the feature representations, and classification algorithms
    feature_rep = ['bow','tfidf']
    classification_algorithms = ['knn', 'svm', 'nb']
    
    for feat in feature_rep:
        for clalgo in classification_algorithms:
            main_test(path, feat, clalgo)





def main_test(path = None, feature_rep = 'tfidf', classification_algorithm = 'knn' ):
    dir_path = path or 'dataset'
    stop_ori='的 一 不 在 人 有 是 为 以 于 上 他 而 后 之 来 及 了 因 下 可 到 由 这 与 也 此 但 并 个 其 已 无 小 我 们 起 最 再 今 去 好 只 又 或 很 亦 某 把 那 你 乃 它 吧 被 比 别 趁 当 从 到 得 打 凡 儿 尔 该 各 给 跟 和 何 还 即 几 既 看 据 距 靠 啦 了 另 么 每 们 嘛 拿 哪 那 您 凭 且 却 让 仍 啥 如 若 使 谁 虽 随 同 所 她 哇 嗡 往 哪 些 向 沿 哟 用 于 咱 则 怎 曾 至 致 着 诸 自'

    frwords=codecs.decode(stop_ori,'utf-8')
    stoplist=set(frwords.split())


    #remove_incompatible_files(dir_path)

    print '\n\n'

    # load data
    print colored('Loading files into memory', 'green', attrs=['bold'])
    files = sklearn.datasets.load_files(dir_path)

    # calculate the BOW representation
    print colored('Calculating BOW', 'green', attrs=['bold'])
    word_counts,vocab_list = util.bagOfWords(files.data)

    count=0
    for i in vocab_list:
        if len(i)==1:
            count+=1
    print "len ==1 words:",count

    # TFIDF
    print colored('Calculating TFIDF', 'green', attrs=['bold'])
    tf_transformer = sklearn.feature_extraction.text.TfidfTransformer(use_idf=True).fit(word_counts)
    X = tf_transformer.transform(word_counts)

    if feature_rep == 'bow':
        X = word_counts
    print X.shape


    print '\n\n'

    # create classifier

    if classification_algorithm == 'nb':
        clf = sklearn.naive_bayes.MultinomialNB()
    elif classification_algorithm == 'svm':
        clf = sklearn.svm.LinearSVC()
    elif classification_algorithm == 'knn':
        n_neighbors = 11
        weights = 'uniform'
        weights = 'distance'
        clf = sklearn.neighbors.KNeighborsClassifier(n_neighbors, weights=weights)

    # test the classifier
    print '\n\n'
    print feature_rep, classification_algorithm
    print colored('Testing classifier with train-test split', 'magenta', attrs=['bold'])
    test_classifier(X, files.target, clf, test_size=0.1, y_names=files.target_names, confusion=False)

def remove_incompatible_files(dir_path):
    # find incompatible files
    print colored('Finding files incompatible with utf8: ', 'green', attrs=['bold'])
    incompatible_files = util.find_incompatible_files(dir_path)
    print colored(len(incompatible_files), 'yellow'), 'files found'

    # delete them
    if(len(incompatible_files) > 0):
        print colored('Deleting incompatible files', 'red', attrs=['bold'])
        util.delete_incompatible_files(incompatible_files)

def test_classifier(X, y, clf, test_size=0.4, y_names=None, confusion=False):
    #train-test split
    print 'test size is: %2.0f%%' % (test_size*100)
    X_train, X_test, y_train, y_test = sklearn.cross_validation.train_test_split(X, y, test_size=test_size)

    clf.fit(X_train, y_train)
    y_predicted = clf.predict(X_test)

    if not confusion:
        print colored('Classification report:', 'magenta', attrs=['bold'])
        print sklearn.metrics.classification_report(y_test, y_predicted, target_names=y_names)
    else:
        print colored('Confusion Matrix:', 'magenta', attrs=['bold'])
        print sklearn.metrics.confusion_matrix(y_test, y_predicted)

if __name__ == '__main__':
    main()