# Application's GUI & Miscellanious Functions  (ui.py)

import wx
import wx.adv
import wx.lib.newevent
import enum
import textwrap

import structs
import log
import files

# Frames

mainFrame = None

def FramesStart       ():
    global mainFrame
    mainFrame = OpenFrame(mainMenuFrame)

def UpdateAll         (since = None):
    if since == None:
        since = mainFrame
    for child in since.GetChildren():
        UpdateAll(child)
    since.Refresh()
    since.Update()

def GoBack            (event):
    parent = event.GetEventObject().GetParent()
    if parent != None:
        if not parent.IsShown():
            parent.Show()
        elif not parent.IsEnabled():
                parent.Enable()
    event.GetEventObject().Destroy()

def OpenFrame         (frameType, source = None, hide_source = False, block_source = True):
    if source != None:
        if hide_source:
            source.Hide()
        elif block_source:
            source.Disable()
    frame = frameType(source)
    frame.Bind(wx.EVT_CLOSE, GoBack)
    frame.Center()
    frame.Show()
    return frame

class mainMenuFrame   (wx.Frame):

    def __init__          (self, parent):
        wx.Frame.__init__(self,
                          parent = parent,
                          style = wx.CLOSE_BOX | wx.CAPTION)
        self.SetIcon(structs.GetIcon())
        self.panel = wx.Panel(self)
        self.__SetLayout(self.panel)
        self.__SetBinding(self.panel)

    def __SetLayout       (self, panel):
        wx.Button(panel, name = 'StartButton')
        wx.Button(panel, name = 'SettingsButton')
        wx.Button(panel, name = 'AboutButton')
        wx.Button(panel, name = 'QuitButton')

        lowSizer1 = wx.BoxSizer(wx.VERTICAL)
        lowSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        topSizer  = wx.BoxSizer(wx.VERTICAL)
        baseSizer = wx.BoxSizer(wx.VERTICAL)

        style = {
            'lowSizer'  : { 'proportion' : 1, 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'topSizer'  : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'baseSizer' : { 'flag' : wx.ALL, 'border' : 3 }
        }

        lowSizer1.Add(panel.FindWindow('StartButton'),    **style['lowSizer'])
        lowSizer1.Add(panel.FindWindow('SettingsButton'), **style['lowSizer'])
        lowSizer2.Add(panel.FindWindow('AboutButton'), **style['lowSizer'])
        lowSizer2.Add(panel.FindWindow('QuitButton'),  **style['lowSizer'])
        topSizer.Add (lowSizer1,            **style['topSizer'])
        topSizer.Add (wx.StaticLine(panel), **style['topSizer'])
        topSizer.Add (lowSizer2,            **style['topSizer'])
        baseSizer.Add(topSizer, **style['baseSizer'])

        panel.SetSizer(baseSizer)

    def __SetText         (self, panel):
        self.SetTitle(structs.CurLang('MainMenu', 'Title'))
        text_source = structs.Language['MainMenu']
        for element in panel.GetChildren():
            name = element.GetName()
            if name in text_source:
                element.SetLabel(structs.CurLang('MainMenu', name, False))

    def __SetBinding      (self, panel):
        panel.FindWindow('StartButton').Bind(wx.EVT_BUTTON, self.__StartBtnClick)
        panel.FindWindow('SettingsButton').Bind(wx.EVT_BUTTON, self.__SettingsBtnClick)
        panel.FindWindow('AboutButton').Bind(wx.EVT_BUTTON, self.__AboutBtnClick)
        panel.FindWindow('QuitButton').Bind(wx.EVT_BUTTON, self.__QuitBtnClick)
        self.Bind(wx.EVT_PAINT, self.__OnRepaint)

    def __StartBtnClick   (self, event):
        if not structs.ImportQuestions(files.OpenJSON(structs.GetSetting('questions_pack'),
                                                  True,
                                                  True,
                                                  structs.CurLang('Files', 'QuestionsPackFileName'))):
            ErrMsg(structs.CurLang('Files', 'LoadingErrorTitle'),
                   structs.CurLang('Files', 'LoadingError') + ' ' + structs.CurLang('Files', 'QuestionsPackFileName', False),
                   self)
            return
        if not (structs.GetQuestionsNumber() % structs.GetSetting('groups_number') == 0):
            ErrMsg(structs.CurLang('Settings', 'WrongGroupsNumberTitle'),
                   structs.CurLang('Settings', 'WrongGroupsNumber'),
                   self)
            return
        if structs.GetSetting('image'):
            images = []
            for i in range(1, structs.GetSetting('groups_number') + 1):
                img = str(i) + '.png'
                if files.CheckExisting(img):
                    images.append(wx.Bitmap(img))
                else:
                    ErrMsg(structs.CurLang('Files', 'LoadingErrorTitle'),
                           structs.CurLang('Files', 'LoadingError') + ' ' + structs.CurLang('Files', 'ImageFileName', False),
                           self)
                    return
            structs.ImportImagePack(images)
        OpenFrame(newResearchFrame, self, True)

    def __SettingsBtnClick(self, event):
        OpenFrame(settingsFrame, self, False, True)

    def __AboutBtnClick   (self, event):
        InfMsg(structs.CurLang('About', 'Title'), structs.CurLang('About', 'Text'), self)

    def __QuitBtnClick    (self, event):
        self.Close()

    def __OnRepaint       (self, event):
        self.__SetText(self.panel)
        sizer = self.panel.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

class settingsFrame   (wx.Frame):

    def __init__        (self, parent):
        wx.Frame.__init__ (self,
                           parent = parent,
                           style = wx.CLOSE_BOX | wx.CAPTION)
        self.SetIcon(structs.GetIcon())
        self.panel = wx.Panel(self)
        self.__SetLayout(self.panel)
        self.__SetBinding(self.panel)
        self.__SetContents(self.panel)
    
    def __SetLayout     (self, panel):
        wx.CheckBox(panel,   name = 'AdditionalLabelSetting')
        wx.CheckBox(panel,   name = 'ImageSetting')
        wx.CheckBox(panel,   name = 'ScoreSetting')
        wx.StaticText(panel, name = 'QuestionsPackFileLabel',
                             style = wx.ALIGN_RIGHT)
        wx.StaticText(panel, name = 'QuestionsPackFile',
                             style = wx.ALIGN_LEFT)
        wx.StaticText(panel, name = 'QuestionsPackNone',
                             style = wx.ALIGN_LEFT)
        BrowseButton(panel,  name = 'QuestionsBrowseButton',
                             extension = files.ext.JSON,
                             defaultFilePath = structs.GetSetting('questions_pack'))
        wx.StaticText(panel, name = 'GroupsNumberLabel',
                             style = wx.ALIGN_RIGHT)
        wx.SpinCtrl(panel,   name = 'GroupsNumberSpiner')
        wx.Choice(panel,     name = 'LanguageChoice')
        wx.StaticText(panel, name = 'LanguageSettingLabel',
                             style = wx.ALIGN_RIGHT)
        wx.Button(panel,     name = 'OkButton')
        wx.Button(panel,     name = 'CancelButton')
        wx.Button(panel,     name = 'AcceptButton')
        wx.StaticBox(panel,  name = 'ResearchBox')
        wx.StaticBox(panel,  name = 'ApplicationBox')

        lowSizer1 = wx.StaticBoxSizer(panel.FindWindow('ResearchBox'),    wx.VERTICAL)
        lowSizer2 = wx.StaticBoxSizer(panel.FindWindow('ApplicationBox'), wx.VERTICAL)
        quesPackSizer = wx.BoxSizer(wx.HORIZONTAL)
        groupsNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
        langSizer = wx.BoxSizer(wx.HORIZONTAL)
        lowSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        baseSizer = wx.BoxSizer(wx.VERTICAL)

        style = {
            'lowSizer'     : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'topSizer'     : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'buttonsSizer' : { 'proportion' : 1, 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'grNumSizer'   : { 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'quesSizer'    : { 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'langSizer'    : { 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'baseSizer'    : { 'flag' : wx.ALL, 'border' : 3 }
        }

        quesPackSizer.Add(panel.FindWindow('QuestionsPackFileLabel'), **style['quesSizer'])
        quesPackSizer.Add(panel.FindWindow('QuestionsPackFile'),      **style['quesSizer'])
        quesPackSizer.Add(panel.FindWindow('QuestionsPackNone'),      **style['quesSizer'])
        quesPackSizer.Add(panel.FindWindow('QuestionsBrowseButton'),  **style['quesSizer'])
        groupsNumberSizer.Add(panel.FindWindow('GroupsNumberLabel'),  **style['grNumSizer'])
        groupsNumberSizer.Add(panel.FindWindow('GroupsNumberSpiner'), **style['grNumSizer'])
        lowSizer1.Add(quesPackSizer,                              **style['lowSizer'])
        lowSizer1.Add(groupsNumberSizer,                          **style['lowSizer'])
        lowSizer1.Add(panel.FindWindow('AdditionalLabelSetting'), **style['lowSizer'])
        lowSizer1.Add(panel.FindWindow('ImageSetting'),           **style['lowSizer'])
        lowSizer1.Add(panel.FindWindow('ScoreSetting'),           **style['lowSizer'])
        langSizer.Add(panel.FindWindow('LanguageSettingLabel'), **style['langSizer'])
        langSizer.Add(panel.FindWindow('LanguageChoice'),       **style['langSizer'])
        lowSizer2.Add(langSizer, **style['lowSizer'])
        lowSizer3.Add(panel.FindWindow('OkButton'),     **style['buttonsSizer'])
        lowSizer3.Add(panel.FindWindow('CancelButton'), **style['buttonsSizer'])
        lowSizer3.Add(panel.FindWindow('AcceptButton'), **style['buttonsSizer'])
        topSizer.Add(lowSizer1,            **style['topSizer'])
        topSizer.Add(lowSizer2,            **style['topSizer'])
        topSizer.Add(wx.StaticLine(panel), **style['topSizer'])
        topSizer.Add(lowSizer3,            **style['topSizer'])
        baseSizer.Add(topSizer, **style['baseSizer'])

        panel.SetSizer(baseSizer)

    def __SetText       (self, panel):
        self.SetTitle(structs.CurLang('Settings', 'Title'))
        text_source = structs.Language['Settings']
        for element in panel.GetChildren():
            name = element.GetName()
            if name in text_source:
                element.SetLabel(structs.CurLang('Settings', name, False))

    def __SetBinding    (self, panel):
        panel.FindWindow('OkButton').Bind(wx.EVT_BUTTON, self.__OkBtnClick)
        panel.FindWindow('CancelButton').Bind(wx.EVT_BUTTON, self.__CancelBtnClick)
        panel.FindWindow('AcceptButton').Bind(wx.EVT_BUTTON, self.__AcceptBtnClick)
        panel.FindWindow('AdditionalLabelSetting').Bind(wx.EVT_CHECKBOX, self.__ContentChanged)
        panel.FindWindow('ImageSetting').Bind(wx.EVT_CHECKBOX, self.__ContentChanged)
        panel.FindWindow('ScoreSetting').Bind(wx.EVT_CHECKBOX, self.__ContentChanged)
        panel.FindWindow('LanguageChoice').Bind(wx.EVT_CHOICE, self.__ContentChanged)
        panel.FindWindow('QuestionsBrowseButton').Bind(BrowseButton.EVT_FILE_CHOOSED, self.__ContentChanged)
        panel.FindWindow('GroupsNumberSpiner').Bind(wx.EVT_SPINCTRL, self.__ContentChanged)
        self.Bind(wx.EVT_PAINT, self.__OnRepaint)

    def __SetContents   (self, panel):
        self.__QuestionsFile(self.panel)
        panel.FindWindow('AdditionalLabelSetting').SetValue(structs.GetSetting('additional_label'))
        panel.FindWindow('ImageSetting').SetValue(structs.GetSetting('image'))
        panel.FindWindow('ScoreSetting').SetValue(structs.GetSetting('score'))

        panel.FindWindow('GroupsNumberSpiner').SetValue(structs.GetSetting('groups_number'))
        panel.FindWindow('GroupsNumberSpiner').SetRange(3, 12)

        langCtrl = panel.FindWindow('LanguageChoice')
        for lang in structs.GetAvailableLangs():
            langCtrl.Append(lang[1])
            if lang[0] == structs.GetSetting('lang'):
                sel = langCtrl.GetCount() - 1
        langCtrl.SetSelection(sel)

        panel.FindWindow('AcceptButton').Disable()

    def __ExportSettings(self, panel):
        structs.SetSetting('additional_label', panel.FindWindow('AdditionalLabelSetting').GetValue())
        structs.SetSetting('image', panel.FindWindow('ImageSetting').GetValue())
        structs.SetSetting('score', panel.FindWindow('ScoreSetting').GetValue())
        structs.SetSetting('lang', structs.Language['available'][panel.FindWindow('LanguageChoice').GetSelection()][0])
        structs.SetSetting('questions_pack', panel.FindWindow('QuestionsBrowseButton').GetFilePath())
        structs.SetSetting('groups_number', panel.FindWindow('GroupsNumberSpiner').GetValue())

    def __ContentChanged(self, event):
        self. __QuestionsFile(self.panel)
        self.panel.FindWindow('AcceptButton').Enable()

    def __QuestionsFile (self, panel):
        [ qpf, qpn, qbb ] = [ panel.FindWindow('QuestionsPackFile'),
                              panel.FindWindow('QuestionsPackNone'),
                              panel.FindWindow('QuestionsBrowseButton') ]
        if qbb.GetFilePath() != None:
            qpn.Hide()
            qpf.SetLabel(qbb.GetFileName('"', '"'))
            qpf.Show()
        else:
            qpf.Hide()
            qpn.Show()
        sizer = panel.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

    def __OkBtnClick    (self, event):
        self.__ExportSettings(self.panel)
        UpdateAll()
        self.Close()

    def __CancelBtnClick(self, event):
        self.Close()

    def __AcceptBtnClick(self, event):
        self.__ExportSettings(self.panel)
        self.panel.FindWindow('AcceptButton').Disable()
        UpdateAll()

    def __OnRepaint     (self, event):
        self.__SetText(self.panel)
        sizer = self.panel.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

class newResearchFrame(wx.Frame):
    
    def __init__        (self, parent):
        wx.Frame.__init__(self,
                          parent = parent,
                          style = wx.CLOSE_BOX | wx.CAPTION)
        self.SetIcon(structs.GetIcon())
        self.panel = wx.Panel(self)
        self.__SetLayout(self.panel)
        self.__SetBinding(self.panel)

    def __SetLayout     (self, panel):
        wx.StaticText(panel,         name = 'NameLabel',  style = wx.ALIGN_RIGHT)
        wx.TextCtrl(panel,           name = 'NameText')
        wx.StaticText(panel,         name = 'DateLabel',  style = wx.ALIGN_RIGHT)
        wx.adv.DatePickerCtrl(panel, name = 'DatePicker', style = wx.adv.DP_DEFAULT)
        wx.StaticText(panel,         name = 'SexLabel',   style = wx.ALIGN_RIGHT)
        wx.Choice(panel,             name = 'SexChoice',  choices = structs.CurLang('NewResearch', 'SexChoices'))
        wx.Button(panel,             name = 'StartButton')
        wx.Button(panel,             name = 'CancelButton')

        nameSizer    = wx.BoxSizer(wx.HORIZONTAL)
        dateSizer    = wx.BoxSizer(wx.HORIZONTAL)
        sexSizer     = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer     = wx.BoxSizer(wx.VERTICAL)
        baseSizer    = wx.BoxSizer(wx.VERTICAL)

        style = {
            'lowSizer1' : { 'proportion' : 1, 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'lowSizer2' : { 'proportion' : 2, 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'lowSizer3' : { 'proportion' : 1, 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'topSizer'  : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'baseSizer' : { 'flag' : wx.ALL, 'border' : 3 }
        }

        nameSizer.Add(panel.FindWindow('NameLabel'), **style['lowSizer1'])
        nameSizer.Add(panel.FindWindow('NameText'),  **style['lowSizer2'])
        dateSizer.Add(panel.FindWindow('DateLabel'),  **style['lowSizer1'])
        dateSizer.Add(panel.FindWindow('DatePicker'), **style['lowSizer2'])
        sexSizer.Add(panel.FindWindow('SexLabel'),  **style['lowSizer1'])
        sexSizer.Add(panel.FindWindow('SexChoice'), **style['lowSizer2'])
        buttonsSizer.Add(panel.FindWindow('StartButton'),  **style['lowSizer3'])
        buttonsSizer.Add(panel.FindWindow('CancelButton'), **style['lowSizer3'])
        topSizer.Add(nameSizer,            **style['topSizer'])
        topSizer.Add(dateSizer,            **style['topSizer'])
        topSizer.Add(sexSizer,             **style['topSizer'])
        topSizer.Add(wx.StaticLine(panel), **style['topSizer'])
        topSizer.Add(buttonsSizer,         **style['topSizer'])
        baseSizer.Add(topSizer, **style['baseSizer'])

        panel.SetSizer(baseSizer)

    def __SetText       (self, panel):
        self.SetTitle(structs.CurLang('NewResearch', 'Title'))
        text_source = structs.Language['NewResearch']
        for element in panel.GetChildren():
            name = element.GetName()
            if name in text_source:
                element.SetLabel(structs.CurLang('NewResearch', name, False))

    def __SetBinding    (self, panel):
        panel.FindWindow('StartButton').Bind(wx.EVT_BUTTON, self.__StartBtnClick)
        panel.FindWindow('CancelButton').Bind(wx.EVT_BUTTON, self.__CancelBtnClick)
        self.sexbind = ['m', 'f']
        self.Bind(wx.EVT_PAINT, self.__OnRepaint)

    def __Validate      (self, panel):
        name = len(panel.FindWindow('NameText').GetValue()) > 0
        sex  = panel.FindWindow('SexChoice').GetCurrentSelection() != -1
        result = name and sex
        wrnStr = structs.CurLang('NewResearch', 'ValidatorWrn') + ' :'
        if not name:
            wrnStr += '\n' + structs.CurLang('NewResearch', 'NameLabel')
        if not sex:
            wrnStr += '\n' + structs.CurLang('NewResearch', 'SexLabel')
        if not result:
            WrnMsg(structs.CurLang('NewResearch', 'ValidatorWrnTitle'), wrnStr, self)
        return result

    def __StartBtnClick (self, event):
        if self.__Validate(self.panel):
            person = structs.NewPerson(self.panel.FindWindow('NameText').GetValue(),
                                       self.panel.FindWindow('DatePicker').GetValue(),
                                       self.sexbind[self.panel.FindWindow('SexChoice').GetCurrentSelection()])
            log.NewResearch(person)
            self.Close()
            OpenFrame(researchFrame, mainFrame, True)
    
    def __CancelBtnClick(self, event):
        self.Close()

    def __OnRepaint(self, event):
        self.__SetText(self.panel)
        sizer = self.panel.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

class researchFrame   (wx.Frame):

    def __init__              (self, parent):
        wx.Frame.__init__(self,
                          parent = parent,
                          style = wx.CLOSE_BOX | wx.CAPTION)
        self.SetIcon(structs.GetIcon())
        
        self.stage = 1

        self.questionNumber = 0
        self.confidenceTime = structs.GetSetting('confidence_time')
        self.confidenceTimer = wx.Timer(self)
        self.roundNumber = 0
        self.roundsNubmer = structs.GetQuestionsNumber() // structs.GetSetting('groups_number')
        self.questionsAnswered = 0
        self.questions = []
        self.answers = []
        self.scores = [0] * structs.GetSetting('groups_number')
        self.stopwatch = log.Stopwatch()

        self.mainPanel    = wx.Panel(self)
        self.stagesPanels = [wx.Panel(self.mainPanel), wx.Panel(self.mainPanel)]
        self.groupPanels  = []
        self.panelsNumbers = {}
        self.sortRounds = [4, 7, 10]

        self.__SetLayout(self.mainPanel, self.stagesPanels)
        self.__SetBinding(self.mainPanel, self.stagesPanels)

        InfMsg(structs.CurLang('Research', 'Title')[self.stage - 1],
               structs.CurLang('Research', 'InformationText')[self.stage - 1],
               self)
        self.stagesPanels[1].Hide()
        self.__Stage_1_Restart(self.stagesPanels[0])

    def __SetLayout           (self, mainPanel, stagesPanels):
        wx.Button(mainPanel, name = 'QuitButton')

        topSizer = wx.BoxSizer(wx.VERTICAL)
        baseSizer = wx.BoxSizer(wx.VERTICAL)

        mainStyle = {
            'topSizerStaticLine'  : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'topSizer'  : { 'flag' : wx.ALL | wx.ALIGN_RIGHT, 'border' : 3 },
            'baseSizer' : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 }
        }

        self.__Stage_1_SetLayout(stagesPanels[0])
        self.__Stage_2_SetLayout(stagesPanels[1])

        topSizer.Add(wx.StaticLine(mainPanel),           **mainStyle['topSizerStaticLine'])
        topSizer.Add(mainPanel.FindWindow('QuitButton'), **mainStyle['topSizer'])
        baseSizer.Add(stagesPanels[0], **mainStyle['baseSizer'])
        baseSizer.Add(stagesPanels[1], **mainStyle['baseSizer'])
        baseSizer.Add(topSizer, **mainStyle['baseSizer'])

        mainPanel.SetSizer(baseSizer)

    def __SetBinding          (self, mainPanel, stagesPanels):
        self.__Stage_1_SetBinding(stagesPanels[0])
        self.__Stage_2_SetBinding(stagesPanels[1], self.groupPanels)
        mainPanel.FindWindow('QuitButton').Bind(wx.EVT_BUTTON, self.__QuitBtnClick)
        self.Bind(wx.EVT_PAINT, self.__OnRepaint)

    def __SetText             (self, mainPanel):
        self.SetTitle(structs.CurLang('Research', 'Title')[self.stage - 1])
        text_source = structs.Language['Research']
        for element in mainPanel.GetChildren():
            name = element.GetName()
            if name in text_source:
                element.SetLabel(structs.CurLang('Research', name, False))
        self.__Stage_2_SetText(self.stagesPanels[1], self.groupPanels)

    def __Stage_1_SetLayout   (self, panel):
        wx.StaticText(panel, name = 'QuestionNumber', style = wx.ALIGN_CENTRE_HORIZONTAL)
        wx.StaticText(panel, name = 'QuestionText', style = wx.ALIGN_CENTRE_HORIZONTAL)
        wx.Slider(panel,     name = 'ConfidenceSlider', value = 0, minValue = 0, maxValue = 20, style = wx.SL_AUTOTICKS)
        wx.StaticText(panel, name = 'ConfidencePercent', style = wx.ALIGN_LEFT)
        wx.StaticText(panel, name = 'ConfidenceTimerSec', style = wx.ALIGN_CENTRE_HORIZONTAL)
        wx.Button(panel,     name = 'NextButton')

        panel.FindWindow('ConfidenceSlider').SetTickFreq(1)

        topSizer = wx.BoxSizer(wx.VERTICAL)

        style = {
            'topSizer'    : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'buttonSizer' : { 'flag' : wx.ALL | wx.ALIGN_CENTER, 'border' : 3 }
        }

        topSizer.Add(panel.FindWindow('QuestionNumber'),     **style['topSizer'])
        topSizer.Add(panel.FindWindow('QuestionText'),       **style['topSizer'])
        topSizer.Add(wx.StaticLine(panel),                   **style['topSizer'])
        topSizer.Add(panel.FindWindow('ConfidenceTimerSec'), **style['topSizer'])
        topSizer.Add(panel.FindWindow('ConfidencePercent'),  **style['topSizer'])
        topSizer.Add(panel.FindWindow('ConfidenceSlider'),   **style['topSizer'])
        topSizer.Add(panel.FindWindow('NextButton'),         **style['buttonSizer'])

        panel.SetSizer(topSizer)

    def __Stage_1_SetBinding  (self, panel):
        panel.FindWindow('NextButton').Bind(wx.EVT_BUTTON, self.__Stage_1_NextBtnClick)
        panel.FindWindow('ConfidenceSlider').Bind(wx.EVT_SLIDER, self.__Stage_1_SliderEvt)
        self.Bind(wx.EVT_TIMER, self.__Stage_1_Timing, self.confidenceTimer)
        panel.Bind(wx.EVT_PAINT, self.__Stages_Repaint)

    def __Stage_1_Restart     (self, panel):
        self.questionNumber += 1
        if self.questionNumber <= structs.GetQuestionsNumber():
            self.confidenceTime = structs.GetSetting('confidence_time')
            self.__Stage_1_SetContents(panel)
            self.__Stage_1_SetText(panel, True)
            self.confidenceTimer.Start(1000)
        else:
            self.stage += 1
            self.Hide()
            InfMsg(structs.CurLang('Research', 'Title')[self.stage - 1],
               structs.CurLang('Research', 'InformationText')[self.stage - 1],
               self)
            self.questions = structs.GetQuestionsConfident(log.GetConfidences())
            self.__SetText(self.mainPanel)
            self.stagesPanels[0].Hide()
            self.stagesPanels[1].Show()
            self.Show()
            self.__Stage_2_Round(self.stagesPanels[1], self.groupPanels)

    def __Stage_1_SetText     (self, panel, timer):
        timerText = panel.FindWindow('ConfidenceTimerSec')
        nextBtn = panel.FindWindow('NextButton')
        slider = panel.FindWindow('ConfidenceSlider')
        percent = panel.FindWindow('ConfidencePercent')
        if timer:
            timerText.SetLabel(str(self.confidenceTime) +
                               structs.CurLang('Research', 'TimerSec', False))
            percent.Hide()
            slider.Hide()
            nextBtn.Hide()
            timerText.Show()
        else:
            nextBtn.SetLabel(structs.CurLang('Research', 'NextButton'))
            percent.SetLabel(structs.CurLang('Research', 'ConfidencePercent')
                             + ' ' + str(slider.GetValue()) + '%')
            percent.Show()
            slider.Show()
            nextBtn.Show()
            timerText.Hide()
        UpdateAll(panel)

    def __Stage_1_SetContents (self, panel):
        panel.FindWindow('ConfidenceSlider').SetValue(0)
        panel.FindWindow('QuestionNumber').SetLabel(structs.CurLang('Research', 'QuestionNumber')
                                                    + ' ' + str(self.questionNumber)
                                                    + '/60 :')
        panel.FindWindow('QuestionText').SetLabel(textwrap.fill(structs.GetQuestion(self.questionNumber), 40))

    def __Stage_1_Timing      (self, event):
        self.confidenceTime -= 1
        timer = self.confidenceTime > 0
        self.__Stage_1_SetText(self.stagesPanels[0], timer)
        if not timer:
            self.confidenceTimer.Stop()

    def __Stage_1_NextBtnClick(self, event):
        log.SetAnswerConfidence(self.questionNumber,
                                self.stagesPanels[0].FindWindow('ConfidenceSlider').GetValue() * 5)
        self.__Stage_1_Restart(self.stagesPanels[0])

    def __Stage_1_SliderEvt   (self, event):
        panel = self.stagesPanels[0]
        slider = panel.FindWindow('ConfidenceSlider')
        percent = panel.FindWindow('ConfidencePercent')
        percent.SetLabel(structs.CurLang('Research', 'ConfidencePercent')
                         + ' ' + str(slider.GetValue() * 5) + '%')

    def __Stage_2_SetLayout   (self, panel):
        wx.StaticText(panel, name = 'RoundNumber', style = wx.ALIGN_CENTER_HORIZONTAL)
        wx.Button(panel,     name = 'NextRoundButton')

        uppSizer = wx.BoxSizer(wx.HORIZONTAL)
        lowSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer = wx.BoxSizer(wx.VERTICAL)

        style = {
            'rndSizer' : { 'flag' : wx.ALL | wx.ALIGN_CENTER_VERTICAL, 'border' : 3 },
            'uppSizer' : { 'flag' : wx.ALL | wx.ALIGN_CENTER, 'border' : 3 },
            'lowSizer' : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 },
            'topSizer' : { 'flag' : wx.ALL | wx.EXPAND, 'border' : 3 }
        }

        gN = structs.GetSetting('groups_number')
        for groupNumber in range(gN):
            p = wx.Panel(panel)
            self.groupPanels.append(p)
            self.panelsNumbers[p] = groupNumber
            self.__Stage_2_SetLayoutG(p)
            lowSizer.Add(p, **style['lowSizer'])
            if groupNumber != gN - 1:
                lowSizer.Add(wx.StaticLine(panel, style = wx.LI_VERTICAL), **style['lowSizer'])

        uppSizer.Add(panel.FindWindow('RoundNumber'),     **style['rndSizer'])
        uppSizer.Add(panel.FindWindow('NextRoundButton'), **style['topSizer'])
        topSizer.Add(uppSizer,             **style['uppSizer'])
        topSizer.Add(wx.StaticLine(panel), **style['topSizer'])
        topSizer.Add(lowSizer,             **style['topSizer'])

        panel.SetSizer(topSizer)

    def __Stage_2_SetLayoutG  (self, panel):
        if structs.GetSetting('additional_label'):
            wx.StaticText(panel, name = 'AdditionalLabel', style = wx.ALIGN_CENTRE_HORIZONTAL)
        if structs.GetSetting('image'):
            wx.StaticBitmap(panel, name = 'Image')
        if structs.GetSetting('score'):
            wx.StaticText(panel, name = 'Score', style = wx.ALIGN_CENTRE_HORIZONTAL)
        wx.StaticText(panel, name = 'QuestionText', style = wx.ALIGN_CENTRE_HORIZONTAL)
        wx.TextCtrl(panel,   name = 'AnswerField')
        wx.Button(panel,     name = 'AnswerButton')
        wx.Button(panel,     name = 'ValidateButton')
        wx.Button(panel,     name = 'CancelButton')
        wx.StaticText(panel, name = 'AnswerText', style = wx.ALIGN_CENTRE_HORIZONTAL)

        topSizer = wx.BoxSizer(wx.VERTICAL)

        style = {
            'topSizer' : { 'flag' : wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER | wx.EXPAND, 'border' : 3 }
        }

        for elem in panel.GetChildren():
            topSizer.Add(elem, **style['topSizer'])
        
        panel.SetSizer(topSizer)

    def __Stage_2_SetBinding  (self, panel, gPanels):
        panel.FindWindow('NextRoundButton').Bind(wx.EVT_BUTTON, self.__Stage_2_NextRoundBtnClick)

        for gPanel in gPanels:
            gPanel.FindWindow('AnswerButton').Bind(wx.EVT_BUTTON, self.__Stage_2_AnswerBtnClick)
            gPanel.FindWindow('ValidateButton').Bind(wx.EVT_BUTTON, self.__Stage_2_ValidateBtnClick)
            gPanel.FindWindow('CancelButton').Bind(wx.EVT_BUTTON, self.__Stage_2_CancelBtnClick)
        
        panel.Bind(wx.EVT_PAINT, self.__Stages_Repaint)

    def __Stage_2_Round(self, panel, gPanels):
        self.roundNumber += 1
        self.questionsAnswered = 0
        self.answers = []
        if self.roundNumber <= self.roundsNubmer:
            if self.roundNumber in self.sortRounds and structs.GetSetting('score'):
                self.__Stage_2_SortPanels(gPanels)
            for gPanel in gPanels:
                self.__Stage_2_AnswerElementsHide(gPanel)
            self.__Stage_2_SetContents(panel)
            self.stopwatch.Reset()
            self.stopwatch.Start()
        else:
            self.stage += 1
            self.Hide()
            InfMsg(structs.CurLang('Research', 'Title')[self.stage - 1],
               structs.CurLang('Research', 'InformationText')[self.stage - 1],
               self)
            logs = log.ExportLog()
            if not files.SaveJSON(logs):
                files.SaveJSON(logs, log.GenLogName() + '.json')
            self.Close()

    def __Stage_2_SetText (self, panel, gPanels):
        for gPanel in gPanels:
            gPanel.FindWindow('AnswerButton').SetLabel(structs.CurLang('Research', 'AnswerButton'))
            gPanel.FindWindow('ValidateButton').SetLabel(structs.CurLang('Research', 'ValidateButton'))
            gPanel.FindWindow('CancelButton').SetLabel(structs.CurLang('Research', 'CancelButton'))
        UpdateAll(panel)

    def __Stage_2_SetContents (self, panel):
        panel.FindWindow('RoundNumber').SetLabel(structs.CurLang('Research', 'RoundNumber')
                                                 + ' ' + str(self.roundNumber) + '/' + str(self.roundsNubmer))
        self.__Stage_2_SetGroupsContents(self.groupPanels)
        btn = panel.FindWindow('NextRoundButton')
        if self.roundNumber == self.roundsNubmer:
            btn.SetLabel(structs.CurLang('Research', 'NextRoundButton')[1])
        else:
            btn.SetLabel(structs.CurLang('Research', 'NextRoundButton')[0])
        btn.Disable()
        UpdateAll(panel)

    def __Stage_2_SetGroupsContents(self, gPanels):
        content = {
            'AdditionalLabel' : self.__Stage_2_SetAdditonalLabel,
            'Score' : self.__Stage_2_SetScore,
            'QuestionText' : self.__Stage_2_SetQuestionText,
            'Image' : self._Stage_2_SetImage
        }
        for gPanel in gPanels:
            for element in gPanel.GetChildren():
                name = element.GetName()
                if name in content:
                    content[name](element, self.panelsNumbers[gPanel])

    def __Stage_2_SetScore(self, ScoreText, group):
        ScoreText.SetLabel(structs.CurLang('Research', 'ScoreText') + ' : ' + str(self.scores[group]))

    def __Stage_2_SetQuestionText(self, questionText, group):
        qnumber = self.__Stage_2_CalculateQuestionNumber(group)
        question = structs.GetQuestion(self.questions[qnumber])
        questionText.SetLabel(textwrap.fill(question, 40))

    def _Stage_2_SetImage(self, image, group):
        image.SetBitmap(structs.GetImage(group))

    def __Stage_2_SetAdditonalLabel(self, additionalLabel, group):
        additionalLabel.SetLabel(str(group + 1))

    def __Stage_2_CalculateQuestionNumber(self, group):
        return (self.roundNumber - 1) * structs.GetSetting('groups_number') + group

    def __Stage_2_NextRoundBtnClick(self, event):
        log.AddRound(structs.NewRound(self.roundNumber, self.answers))
        self.__Stage_2_Round(self.stagesPanels[1], self.groupPanels)

    def __Stage_2_AnswerBtnClick(self, event):
        panel = event.GetEventObject().GetParent()
        for gPanel in self.groupPanels:
            if not gPanel.FindWindow('AnswerButton').IsShown() and not gPanel.FindWindow('AnswerText').IsShown():
                self.__Stage_2_AnswerElementsHide(gPanel)
        self.__Stage_2_AnswerElementsShow(panel)
        panel.FindWindow('AnswerField').SetFocus()
        UpdateAll(panel.GetParent())

    def __Stage_2_ValidateBtnClick(self, event):
        self.stopwatch.Stop()
        panel = event.GetEventObject().GetParent()
        panelNumber = self.panelsNumbers[panel]
        answer = panel.FindWindow('AnswerField').GetValue()
        if self.__Stage_2_ValidateAnswer(answer):
            panel.FindWindow('AnswerField').Hide()
            panel.FindWindow('ValidateButton').Hide()
            panel.FindWindow('CancelButton').Hide()
            answerText = panel.FindWindow('AnswerText')
            answerText.SetLabel(textwrap.fill(structs.CurLang('Research', 'AnswerText') + ' : ' + answer, 40))
            answerText.Show()
            qn = self.__Stage_2_CalculateQuestionNumber(panelNumber)
            if structs.GetSetting('score'):
                self.__Stage_2_ScoreRecalc(panelNumber, qn, answer)
            if self.questionsAnswered == structs.GetSetting('groups_number'):
                panel.GetParent().FindWindow('NextRoundButton').Enable()
            UpdateAll(panel.GetParent())
            self.answers.append(structs.NewAnswer(self.questions[qn], answer, self.stopwatch.GetTime()))
        else:
            self.stopwatch.Start()

    def __Stage_2_ValidateAnswer(self, answer):
        if len(answer) == 0:
            WrnMsg(structs.CurLang('Research', 'EmptyAnswerWarningTitle'),
                   structs.CurLang('Research', 'EmptyAnswerWarning'),
                   self)
            return False
        self.questionsAnswered += 1
        return True

    def __Stage_2_ScoreRecalc(self, panelNumber, questionNumber, answer):
        self.scores[panelNumber] += log.GetConfidence(questionNumber) * int(structs.CheckAnswer(self.questions[questionNumber], answer))

    def __Stage_2_CancelBtnClick(self, event):
        panel = event.GetEventObject().GetParent()
        self.__Stage_2_AnswerElementsHide(panel)
        UpdateAll(panel.GetParent())

    def __Stage_2_AnswerElementsShow(self, panel):
        panel.FindWindow('AnswerButton').Hide()
        answerField = panel.FindWindow('AnswerField')
        answerField.SetValue('')
        answerField.Show()
        panel.FindWindow('ValidateButton').Show()
        panel.FindWindow('CancelButton').Show()
    
    def __Stage_2_AnswerElementsHide(self, panel):
        panel.FindWindow('AnswerButton').Show()
        panel.FindWindow('AnswerField').Hide()
        panel.FindWindow('ValidateButton').Hide()
        panel.FindWindow('CancelButton').Hide()
        panel.FindWindow('AnswerText').Hide()

    def __Stage_2_SortPanels(self, gPanels):
        temp = [self.panelsNumbers[gPanel] for gPanel in gPanels]
        temp = sorted(temp, reverse = True, key = lambda x : self.scores[x])
        for gPanel in gPanels:
            n = self.panelsNumbers[gPanel]
            self.panelsNumbers[gPanel] = temp[n]

    def __QuitBtnClick        (self, event):
        self.Close()

    def __Stages_Repaint(self, event):
        sizer = self.mainPanel.GetSizer()
        sizer.Layout()
        sizer.Fit(self)

    def __OnRepaint           (self, event):
        self.__SetText(self.mainPanel)
        self.__Stages_Repaint(event)

# Messages & Dialogs

def __Msg      (title, text, source, buttons, icon):
    props = buttons | icon

    if source == None:
        props |= wx.STAY_ON_TOP

    return wx.MessageDialog(source,
                            text,
                            title,
                            props)

def ErrMsg     (title, text, source = None):
    __Msg(title, text, source, wx.OK, wx.ICON_ERROR).ShowModal()

def ErrDia     (title, text, source = None):
    result = __Msg(title, text, source, wx.YES_NO, wx.ICON_ERROR).ShowModal()
    return True if result == wx.ID_YES else False

def InfMsg     (title, text, source = None):
    __Msg(title, text, source, wx.OK, wx.ICON_INFORMATION).ShowModal()

def InfDia     (title, text, source = None):
    result = __Msg(title, text, source, wx.YES_NO, wx.ICON_INFORMATION).ShowModal()
    return True if result == wx.ID_YES else False

def WrnMsg     (title, text, source = None):
    __Msg(title, text, source, wx.OK, wx.ICON_EXCLAMATION).ShowModal()

def WrnDia     (title, text, source = None):
    result = __Msg(title, text, source, wx.YES_NO, wx.ICON_EXCLAMATION).ShowModal()
    return True if result == wx.ID_YES else False

def QueDia     (title, text, source = None):
    result = __Msg(title, text, source, wx.YES_NO, wx.ICON_QUESTION).ShowModal()
    return True if result == wx.ID_YES else False

def __FileDia  (extension, source, mode):
    if source == None:
        source = wx.Window()
    mt = mode & (wx.FD_OPEN | wx.FD_SAVE)
    modeTitles = { wx.FD_OPEN : 'OpenFileDialogTitle', wx.FD_SAVE : 'SaveFileDialogTitle' }
    title = structs.CurLang('Files', modeTitles[mt])
    return wx.FileDialog(source,
                         message = title,
                         wildcard = files.Wildcard(extension),
                         style = mode)

def FileOpenDia(extension, source = None):
    dia = __FileDia(extension, source, wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if dia.ShowModal() == wx.ID_OK:
        return dia.GetPath()
    else:
        return None

def FileSaveDia(extension, source = None):
    dia = __FileDia(extension, source, wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if dia.ShowModal() == wx.ID_OK:
        return dia.GetPath()
    else:
        return None

class BrowseButton(wx.Button):

    fileChoosedEvent, EVT_FILE_CHOOSED = wx.lib.newevent.NewEvent()

    def __init__(self,
                 parent,
                 id = wx.ID_ANY,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = 0,
                 validator = wx.DefaultValidator,
                 name = wx.ButtonNameStr,
                 extension = files.ext.ANY,
                 defaultFilePath = None):
        wx.Button.__init__(self,
                           parent = parent,
                           id = id,
                           pos = pos,
                           size = size,
                           style = style,
                           validator = validator,
                           name = name)
        self.filePath = defaultFilePath
        self.extension = extension
        self.Bind(wx.EVT_BUTTON, self.__Browse)
        self.Bind(wx.EVT_PAINT, self.__OnRepaint)

    def __Browse(self, event):
        self.filePath = FileOpenDia(self.extension, self.GetParent())   
        if self.filePath != None:
            wx.PostEvent(self, self.fileChoosedEvent())

    def __OnRepaint(self, event):
        self.SetLabel(structs.CurLang('Files', 'BrowseButtonLabel'))

    def GetFilePath(self):
        return self.filePath
    
    def GetFileName(self, lquote, rquote):
        fp = self.GetFilePath()
        if fp == None:
            return fp
        else:
            return files.FileName(fp, lquote, rquote)