from PrepFunctions import *


if(checkPicklefiles() == False):
    featuresets = loadDatasetFromSingleFiles("positive.txt", "negative.txt")
    training_set = featuresets[:10000]
    testing_set = featuresets[10000:]
    print("Lenght of trainingset:", len(training_set))
    print("Lenght of testingset:", len(testing_set))
    savePickle(training_set, "picklefiles_eng/trainingset.pickle")
    savePickle(testing_set, "picklefiles_eng/testingset.pickle")

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    savePickle(classifier, "picklefiles_eng/basicClassifier.pickle")
    print("Basic classifier saved")

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    savePickle(MNB_classifier, "picklefiles_eng/MNBClassifier.pickle")
    print("MNB classifier saved")

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(training_set)
    savePickle(BernoulliNB_classifier, "picklefiles_eng/BNBClassifier.pickle")
    print("BNB classifier saved")

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression(solver='liblinear'))
    LogisticRegression_classifier.train(training_set)
    savePickle(LogisticRegression_classifier, "picklefiles_eng/LRClassifier.pickle")
    print("LRC classifier saved")

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)
    savePickle(SGDClassifier_classifier, "picklefiles_eng/SGDClassifier.pickle")
    print("SGD classifier saved")

    LinearSVC_classifier = SklearnClassifier(LinearSVC(max_iter=10000))
    LinearSVC_classifier.train(training_set)
    savePickle(LinearSVC_classifier, "picklefiles_eng/LinearSVCClassifier.pickle")
    print("LinearSVC classifier saved")

    NuSVC_classifier = SklearnClassifier(NuSVC(gamma='auto'))
    NuSVC_classifier.train(training_set)
    savePickle(NuSVC_classifier, "picklefiles_eng/NUSVCClassifier.pickle")
    print("NuSVC classifier saved")

#Code to print accuracy of each classifier, outcommented due to consuming a lot of time.
"""
#print("Naive Bayes accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
#print("Multinomial Naive Bayes accuracy:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
#print("BernoulliNB accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
#print("LogisticRegression accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
#print("SGDClassifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
#print("LinearSVC accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
#print("NuSVC accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
#print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)
"""

def prepareAnalysis(swe):
    messageList = loadMultipleDirectoriesToOneList("outputEmails")
    if(swe):
        translatedMessageList = translateMessageListToEnglish(messageList)
        savePickle(translatedMessageList, "picklefiles_eng/translatedmessages.pickle")
    else:
        savePickle(messageList, "picklefiles_eng/messages.pickle")