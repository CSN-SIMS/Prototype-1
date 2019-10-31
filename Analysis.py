#Lukas and Jenjira

from Functions import *
import datetime, time
#Att göra: Skapa ett relativt enkelt sätt att byta mellan svenska och engelska och ändra andra inställningar (GUI).
#Lägg till neutral klassifiering när testning är klar, Motverka neg klassifiering av texter som är neutrala,
#Error hantering när t.ex nätverket är frånkopplat för översättning.

newFile = False

training_set = loadPickleFile("picklefiles_eng/trainingset.pickle")
testing_set = loadPickleFile("picklefiles_eng/testingset.pickle")
document = loadPickleFile("picklefiles_eng/trainingset.pickle")
word_features = loadPickleFile("picklefiles_eng/word_features.pickle")

classifier = loadPickleFile("picklefiles_eng/basicClassifier.pickle")
NuSVC_classifier = loadPickleFile("picklefiles_eng/NUSVCClassifier.pickle")
BernoulliNB_classifier = loadPickleFile("picklefiles_eng/BNBClassifier.pickle")
LinearSVC_classifier = loadPickleFile("picklefiles_eng/LinearSVCClassifier.pickle")
SGDClassifier_classifier = loadPickleFile("picklefiles_eng/SGDClassifier.pickle")
MNB_classifier = loadPickleFile("picklefiles_eng/MNBClassifier.pickle")
LogisticRegression_classifier = loadPickleFile("picklefiles_eng/LRClassifier.pickle")


voted_classifier = VoteClassifier(classifier,
                                      NuSVC_classifier,
                                      BernoulliNB_classifier,
                                      LinearSVC_classifier,
                                      SGDClassifier_classifier,
                                      MNB_classifier,
                                      LogisticRegression_classifier)
#print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)

def startAnalysis(excelFilename, noExcel, noAppend):
    translatedMessageList = loadPickleFile("picklefiles_eng/translatedmessages.pickle")
    judgementList = analyseListOfMessages(translatedMessageList, word_features, voted_classifier)
    percentages = calculatePercentagesOfList(judgementList)
    if(noExcel == False):
        if(noAppend):
            saveToNewExcelfile(judgementList, "Data", percentages, excelFilename + ".xlsx")
        else:
            saveExcelFormat(judgementList, "Data", percentages, excelFilename + ".xlsx", append=True)
    print("Done")
    return judgementList