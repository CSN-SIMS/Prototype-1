# Rosen
# GUI with functionality connecting the two parts of the program - keyword-search Categorization and Sentiment Analysis
# Tkinter is free software released under a Python license.

from tkinter import Tk, Button, Frame, PhotoImage, Message, Canvas, Label, Listbox, Scrollbar, IntVar, \
    RIGHT, X, Y, END, BOTTOM, HORIZONTAL, VERTICAL, Entry, Checkbutton, OptionMenu, Toplevel, filedialog, StringVar
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from KeywordSearch import *
from Functions import *
from Preperation import *
from PrepFunctions import *
from Analysis import *

FontStyle = "Helvetica"

# Page frame for switching between the three different pages of the application
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# Background of the application
def backgroundSet(self):
    self.canvas = Canvas(self)
    self.background_label = Label(self, bg='#3C1E5F')
    self.background_label.place(relwidth=1, relheight=1)
    self.canvas.pack()

# Using global variables for saving selected folder from File Explorer
selectedFolderInputFiles = ''
errorTextFolderSelect = ''

def inputFolderDialog():
    global selectedFolderInputFiles
    global errorTextFolderSelect
    try:
        # Ask for directory with input files
        selectedFolderInputFiles = filedialog.askdirectory()
    except FileNotFoundError:
        errorTextFolderSelect = "The system cannot find the path specified."

# Popup message with result from page 1
# Gets the selected folder by the user and uses keywordSearch in txt files, then presents categories and file names
# Sentiment analysis of the output sub-directories and saving the result in excel
def popupWindowInputFiles(selectLanguageVar, checkVar, entryContentExcelFilename, selectedFolderInputFiles, errorTextFolderSelect, checkVarAppend):
    print("Language value " + str(selectLanguageVar))
    print("Check value " + str(checkVar))
    print("Check value Append " + str(checkVarAppend))
    print("Entry excel name " + str(entryContentExcelFilename))
    print("Input folder " + str(selectedFolderInputFiles))
    errorText = errorTextFolderSelect
    amountOfFiles = 0
    mapCategorizedFiles = {}
    messageSavingExcelFile = ""
    noExcel = True
    noAppend = True
    judgementList = []
    try:
        # Ask for directory with input files
        categorizer = Categorizer()
        # Amount of analyzed Emails
        amountOfFiles = categorizer.amountOfFiles(selectedFolderInputFiles)
        # Map of categories with their emails
        mapCategorizedFiles = categorizer.categorizeFilesFromDirectoryInMapAndSubDirectory(selectedFolderInputFiles)
        # Preparation of Sentiment analysis
        if (selectLanguageVar == 'Swedish'):
            try:
                prepareAnalysis(True)
            except:
                errorText = "Problem occurred when translating the message."
        else:
            prepareAnalysis(False)
        # Start of Sentiment analysis and print the result as well as save it to a new excel file or to an existing one
        if (checkVarAppend == 1 and entryContentExcelFilename != ''):
            noExcel = False
            noAppend = False
            judgementList = startAnalysis(entryContentExcelFilename, noExcel, noAppend)
            messageSavingExcelFile = "The result is append to " + str(entryContentExcelFilename) + ".xlsx on Desktop"
        elif (checkVarAppend == 1 and entryContentExcelFilename == ''):
            judgementList = startAnalysis(entryContentExcelFilename, noExcel, noAppend)
            messageSavingExcelFile = "Enter a name to the excel file which you would like to append the result."
        elif(checkVar==1 and entryContentExcelFilename != ''):
            noExcel = False
            noAppend = True
            judgementList = startAnalysis(entryContentExcelFilename, noExcel, noAppend)
            messageSavingExcelFile = "The result is saved as " + str(entryContentExcelFilename) + ".xlsx on Desktop"
        elif(checkVar==1 and entryContentExcelFilename == ''):
            judgementList = startAnalysis(entryContentExcelFilename, noExcel, noAppend)
            messageSavingExcelFile = "Enter a name to the new excel file."
        elif (checkVar == 0 and checkVarAppend == 0):
            judgementList = startAnalysis(entryContentExcelFilename, noExcel, noAppend)
    except UnicodeDecodeError:
        errorText = "Selected folder does not contain txt files."
    except FileNotFoundError:
        errorText = "The system cannot find the path specified."
    popupWindowInputFiles = Toplevel()
    popupWindowInputFiles.wm_title("Result")
    popupWindowInputFiles.wm_geometry("800x450")
    # container with results from Categorization and Sentiment analysis of the given input folder
    results = Listbox(popupWindowInputFiles, font=("Courier", 12), bg='white', fg='#3C1E5F', justify='left', bd=3)
    results.grid(column=1, row=1, padx=10, ipady=10)
    results.place(relwidth=1, relheight=0.85)
    scrollbar_vertical = Scrollbar(results, orient=VERTICAL)
    scrollbar_vertical.pack(side=RIGHT, fill=Y)
    scrollbar_vertical.configure(command=results.yview)
    scrollbar_horizontal = Scrollbar(results, orient=HORIZONTAL)
    scrollbar_horizontal.pack(side=BOTTOM, fill=X)
    scrollbar_horizontal.configure(command=results.xview)
    results.configure(yscrollcommand=scrollbar_vertical.set)
    results.configure(xscrollcommand=scrollbar_horizontal.set)

    # Shows if there is an error occurred when opening the input folder
    if(errorText != ""):
        results.insert(END, "Error occured: " + errorText)
        results.insert(END, "Try again.")
        results.insert(END, "\n")
    else:
        # Shows the amount of analyzed Emails
        results.insert(END, "Amount of analysed Emails: " + str(amountOfFiles))
        results.insert(END, "\n")

        # Shows a map of categories with their emails
        results.insert(END, "List of categories with their emails: ")
        results.insert(END, "Category".ljust(20, ' ') + "File name")
        for key, val in mapCategorizedFiles.items():
            results.insert(END, str(key).ljust(20, ' ') + str(val))

        # Shows the message about saving the result as excel file
        results.insert(END, "\n")
        results.insert(END, messageSavingExcelFile)
        results.insert(END, "\n")

        # Shows the result from judgementList with Filename, Category, Judgement from Sentiment analysis in %, Confidence
        results.insert(END, "The categorization and sentiment analysis shows: \n")
        results.insert(END, "Filename".ljust(30, ' ') + "Category".ljust(20, ' ')
                       + "Judgement %".ljust(15, ' ') + "Confidence")
        for fn, judgement in judgementList:
            results.insert(END, str(fn[0]).ljust(30, ' ') + str(fn[1]).ljust(20, ' ')
                           + str(judgement[0]).ljust(15, ' ') + str(judgement[1]))

    # Button to close the popup window
    buttonPopup = Button(popupWindowInputFiles, text="OK", bd=5, command=popupWindowInputFiles.destroy)
    buttonPopup.place(relx=0.45, rely=0.87, relwidth=0.15, relheight=0.10)

# Popup message with result from Sentiment analysis of direct input by the user
def popupWindowDirectInput(selectLanguageVar, entryString):
    print("Language " + selectLanguageVar)
    print("Entry " + entryString)
    # Popup message with result from Sentiment analysis of direct input by the user (displays positive, negative or neutral sentiment)
    popupWindowDirectIput = Toplevel()
    popupWindowDirectIput.wm_title("Result")
    popupWindowDirectIput.wm_geometry("800x450")
    # container with results from Sentiment analysis of the given direct input
    results = Listbox(popupWindowDirectIput, font=("Courier", 12), bg='white', fg='#3C1E5F', justify='center', bd=3)
    results.grid(column=1, row=1, padx=10, ipady=10)
    results.place(rely=0.2, relwidth=1, relheight=0.65)
    scrollbar_vertical = Scrollbar(results, orient=VERTICAL)
    scrollbar_vertical.pack(side=RIGHT, fill=Y)
    scrollbar_vertical.configure(command=results.yview)
    scrollbar_horizontal = Scrollbar(results, orient=HORIZONTAL)
    scrollbar_horizontal.pack(side=BOTTOM, fill=X)
    scrollbar_horizontal.configure(command=results.xview)
    results.configure(yscrollcommand=scrollbar_vertical.set)
    results.configure(xscrollcommand=scrollbar_horizontal.set)
    errorText = ''
    # Check if the direct input by the user is empty
    if(str(entryString) != ''):
        # Preparation of Sentiment analysis of an entry by the user
        if (selectLanguageVar == 'Swedish'):
            try:
                entryString = translateSingleMessageToEng(entryString)
            except:
                errorText = "Problem occurred when translating the message."
        # Start of Sentiment analysis of an entry by the user
        resultSentimentAndConfidence = sentiment(entryString, voted_classifier, word_features)
        print(resultSentimentAndConfidence)
        resultSentiment = StringVar()
        # Shows if there is an error occurred when opening the input folder
        if (errorText != ""):
            results.insert(END, "Error occured: " + errorText)
            results.insert(END, "Try again.")
            results.insert(END, "\n")
        else:

            if(str(resultSentimentAndConfidence[0]) == "pos"):
                resultSentiment = "Positive"
                colorResultDirectInput = "#00FF00"
            elif (str(resultSentimentAndConfidence[0]) == "neg"):
                resultSentiment = "Negative"
                colorResultDirectInput = "#FF0000"
            else:
                resultSentiment = "Neutral"
                colorResultDirectInput = "#0000ff"
            # displays positive, negative or neutral sentiment
            popupLabel = Label(popupWindowDirectIput, text=resultSentiment, font=(FontStyle, 20), justify='center', fg=colorResultDirectInput)
            popupLabel.place(relx=0.31, rely=0.05, relwidth=0.4, relheight=0.1)

            # printing the result
            results.insert(END, "\n")
            results.insert(END, "\n")
            results.insert(END, " Your entry:")
            if(len(entryString) < 100):
                results.insert(END, "\"" + entryString + "\"")
            results.insert(END, "has")
            results.insert(END, resultSentiment)
            results.insert(END, "Sentiment and Confidence")
            results.insert(END, str(resultSentimentAndConfidence[1]))
    else:
        print("entryString"+entryString)
        results.insert(END, "Please enter the text you want to be analysed and then select Analyse-button.")
    # Button to close the popup window
    buttonPopup = Button(popupWindowDirectIput, text="OK", bd=5, command=popupWindowDirectIput.destroy)
    buttonPopup.place(relx=0.43, rely=0.87, relwidth=0.15, relheight=0.10)

# First page with main information about the application
class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       backgroundSet(self)
       # Lower frame with scrollbars for displaying of information about the program
       lower_frame = Frame(self, bg='#FFD164', bd=5)
       lower_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.7, anchor='n')
       lower_frame.grid_rowconfigure(0, weight=1)
       lower_frame.grid_columnconfigure(0, weight=1)
       infoMessagePage1 = Listbox(lower_frame, font=(FontStyle, 14), bg='white', fg='#3C1E5F', justify='center', bd=3)
       infoMessagePage1.grid(column=1, row=1, padx=10, ipady=10)
       infoMessagePage1.place(relwidth=1, relheight=1)
       scrollbar_vertical = Scrollbar(lower_frame, orient=VERTICAL)
       scrollbar_vertical.pack(side=RIGHT, fill=Y)
       scrollbar_vertical.configure(command=infoMessagePage1.yview)
       scrollbar_horizontal = Scrollbar(lower_frame, orient=HORIZONTAL)
       scrollbar_horizontal.pack(side=BOTTOM, fill=X)
       scrollbar_horizontal.configure(command=infoMessagePage1.xview)
       infoMessagePage1.configure(yscrollcommand=scrollbar_vertical.set)
       infoMessagePage1.configure(xscrollcommand=scrollbar_horizontal.set)
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "This program has the following abilities: \n")
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "- \"Email Analysis\" menu does Categorization and Sentiment analysis on text files in \n")
       infoMessagePage1.insert(END, "\t Swedish or English from a given input folder, \n")
       infoMessagePage1.insert(END, "\t presents the results and saves them in excel file \n\n")
       infoMessagePage1.insert(END, "- \"Direct Input\" does Sentiment analysis on direct input in Swedish or English")
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "\n")
       infoMessagePage1.insert(END, "\n Copyright © All rights reserved")

# Page with options for choosing input files, saving as new excel file or changing between Swedish and English
class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       backgroundSet(self)
       # Lower frame with scrollbars for displaying of categories and file names
       lower_frame = Frame(self, bg='#FFD164', bd=5)
       lower_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.7, anchor='n')
       lower_frame.grid_rowconfigure(0, weight=1)
       lower_frame.grid_columnconfigure(0, weight=1)
       optionCanvas = Canvas(lower_frame, bg='white', bd=3)
       optionCanvas.place(relwidth=1, relheight=0.85)

       # select language (English or Swedish)
       selectLanguageVar = StringVar()
       # Dictionary with options
       choices = {'English', 'Swedish'}
       selectLanguageVar.set('Swedish')  # set the default option
       # Popup menu with languages
       popupMenu = OptionMenu(optionCanvas, selectLanguageVar, *choices)
       popupLabel = Label(optionCanvas, text="Choose a language", font=(FontStyle, 12), bg='white')
       popupLabel.place(relx=0.1, rely=0.01, relwidth=0.3, relheight=0.2)
       popupMenu.configure(bd=3, bg='#EE7C7D')
       popupMenu.place(relx=0.5, rely=0.01, relwidth=0.3, relheight=0.18)

       # save result in excel file
       checkVar = IntVar(value=1)
       checkVarAppend = IntVar()
       excelFileCheckbutton = Checkbutton(optionCanvas, text="Save as excel", variable=checkVar, onvalue=1,
                                          offvalue=0, bg='white', font=(FontStyle, 12), height=5, width=20)
       excelFileCheckbutton.place(relx=0.05, rely=0.35, relwidth=0.3, relheight=0.15)
       excelFileAppendCheckbutton = Checkbutton(optionCanvas, text="Append to existing excel on Desktop", variable=checkVarAppend,
                                        onvalue=1, offvalue=0, bg='white', font=(FontStyle, 12), height=5, width=20)
       excelFileAppendCheckbutton.place(relx=0.077, rely=0.55, relwidth=0.45, relheight=0.15)
       entryLabel = Label(optionCanvas, text="Enter name of the excel", bg='white', font=(FontStyle, 12))
       entryLabel.place(relx=0.4, rely=0.38, relwidth=0.25, relheight=0.1)
       entryContentExcelFilename = Entry(lower_frame, font=(FontStyle, 12,), justify='left', bd=3)
       timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
       timestamp = str(timestamp)
       entryContentExcelFilename.insert(END, 'OutputFile ' + timestamp)
       entryContentExcelFilename.place(relx=0.7, rely=0.32, relwidth=0.25, relheight=0.1)

       # open folder with input files
       openFolder = Label(optionCanvas, text="Open a folder with input files", justify='left',
                          bg='white', font=(FontStyle, 12))
       openFolder.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.2)

       buttonOpenFolder = Button(optionCanvas, text="Browse", font=(FontStyle, 12), bg='#EE7C7D', highlightcolor='#d65859', activebackground='#f2d9e6',
                                 command=lambda: inputFolderDialog())
       buttonOpenFolder.place(relx=0.5, rely=0.7, relwidth=0.3, relheight=0.15)

       selectedFolderLabel = Label(optionCanvas, text="", justify='left', bg='white', font=(FontStyle, 12))
       selectedFolderLabel.place(relx=0.42, rely=0.85, relwidth=0.4, relheight=0.2)

       buttonAnalyzeInput = Button(lower_frame, text="Analyze", font=(FontStyle, 12), bg='#b3b3b3',
                                   activebackground='#f2d9e6',
                                   command=lambda: popupWindowInputFiles(selectLanguageVar.get(), checkVar.get(),
                                                                         entryContentExcelFilename.get(), selectedFolderInputFiles,
                                                                         errorTextFolderSelect, checkVarAppend.get()))
       buttonAnalyzeInput.place(relx=0.4, rely=0.89, relwidth=0.2, relheight=0.1)


        # when button Analyze is clicked display Loading Progress bar and present the selected input folder to the user
       def buttonAnalyzeInputClick(event):
           global selectedFolderInputFiles
           folder = selectedFolderInputFiles.split("/")
           selectedFolderLabel.configure(text="Folder selected: " + folder[-1])
           popupWindowLoading = Toplevel()
           popupWindowLoading.wm_title("Loading")
           popupWindowLoading.wm_geometry("300x40")
           progressbarLabel = Label(popupWindowLoading, text="Loading the result...", justify='left', font=(FontStyle, 14))
           progressbarLabel.pack(side="top")
           popupWindowLoading.after(3000, lambda: popupWindowLoading.destroy()) # Destroy the widget after 3 seconds

       buttonAnalyzeInput.bind("<Button-1>", buttonAnalyzeInputClick)

# Page with entry field for direct input and changing between Swedish and English
class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       backgroundSet(self)
       lower_frame = Frame(self, bg='#FFD164', bd=5)
       lower_frame.place(relx=0.5, rely=0.15, relwidth=0.9, relheight=0.7, anchor='n')
       lower_frame.grid_rowconfigure(0, weight=1)
       lower_frame.grid_columnconfigure(0, weight=1)

       # select language (English or Swedish)
       selectLanguageVar = StringVar()
       # Dictionary with options
       choices = {'English', 'Swedish'}
       selectLanguageVar.set('Swedish')  # set the default option
       # Popup menu with languages
       popupMenu = OptionMenu(lower_frame, selectLanguageVar, *choices)
       popupLabel = Label(lower_frame, text="Choose a language", font=(FontStyle, 12), bg='#FFD164')
       popupLabel.place(relx=0.1, rely=0.01, relwidth=0.3, relheight=0.2)
       popupMenu.configure(bd=3, bg='#EE7C7D')
       popupMenu.place(relx=0.5, rely=0.01, relwidth=0.3, relheight=0.15)

       # Entry text box
       entryTextLabel = Label(lower_frame, text="Enter text", bg='#FFD164', font=(FontStyle, 12))
       entryTextLabel.place(relx=0.37, rely=0.2, relwidth=0.25, relheight=0.1)
       entryTextContent = ScrolledText(lower_frame, font=(FontStyle, 12))
       entryTextContent.place(relx=0, rely=0.3, relwidth=1, relheight=0.55)

       buttonAnalyzeInput = Button(lower_frame, text="Analyze", font=(FontStyle, 12), bg='#b3b3b3',
                       activebackground='#f2d9e6', command=lambda: popupWindowDirectInput(selectLanguageVar.get(),
                                                                                          entryTextContent.get("1.0", "end-1c")))
       buttonAnalyzeInput.place(relx=0.4, rely=0.89, relwidth=0.2, relheight=0.1)

# Main view of the application with logo, info-box, button-bar and container for switching between the three pages
class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        menu_frame = Frame(self, bg='#FFD164', bd=5)
        menu_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        #logo
        self.logo = Canvas(menu_frame, bd=1)
        self.logo.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.img = PhotoImage(file="logo.png")
        self.img = self.img.subsample(6)
        self.logo.create_image(0, 0, anchor='nw', image=self.img)
        var = "Sentiment analysis and Categorization"
        infoMessage = Message(menu_frame, text=var, justify='center', width=350,
                                   font=(FontStyle, 16))
        infoMessage.place(relx=0.4, rely=0.1, relwidth=0.4, relheight=0.5)
        button_frame = Frame(self, bg='#FFD164', bd=5)
        button_frame.place(relx=0, rely=0.135, relwidth=1, relheight=0.2)
        button1 = Button(button_frame, text="Information", font=(FontStyle, 14), bg='#EE7C7D',
                         activebackground='#f2d9e6',
                         command=p1.lift)
        button1.place(relx=0.1, rely=0.25, relwidth=0.2, relheight=0.35)
        button2 = Button(button_frame, text="Text Analysis", font=(FontStyle, 14), bg='#EE7C7D',
                         activebackground='#f2d9e6',
                         command=p2.lift)
        button2.place(relx=0.4, rely=0.25, relwidth=0.2, relheight=0.35)
        button3 = Button(button_frame, text="Direct input", font=(FontStyle, 14), bg='#EE7C7D',
                         activebackground='#f2d9e6',
                         command=p3.lift)
        button3.place(relx=0.7, rely=0.25, relwidth=0.2, relheight=0.35)

        container = Frame(self)
        container.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # shows the first page
        p1.show()

# Start of the application
if __name__ == "__main__":
    root = Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.title("Sentiment Classification/Categorization Dialog Widget")
    root.minsize(850, 650)
    root.mainloop()