# Research Logging (log.py)

import structs
import datetime
import json

# Stopwatch Class

class Stopwatch():

    def __init__(self):
        self.Reset()
    
    def Reset(self):
        self.start_time = None
        self.stop_time = None

    def Start(self):
        if self.start_time == None:
            self.start_time = datetime.datetime.now()
        elif self.stop_time != None:
            self.start_time += datetime.datetime.now() - self.stop_time
            self.stop_time = None
    
    def Stop(self):
        if self.start_time != None:
            self.stop_time = datetime.datetime.now()

    def GetTime(self):
        if self.start_time != None:
            if self.stop_time != None:
                td = (self.stop_time - self.start_time)
            else:
                td = (datetime.datetime.now() - self.start_time)
        else:
            return None
        return str(str(td.seconds) + '.' + str(td.microseconds))

# Logging Data & Functions

Research = {}

def NewResearch(person):
    global Research
    Research = {}
    Research['Person']     = person
    Research['Date']       = str(datetime.date.today())
    Research['Settings']   = {
        'AdditionalLabel' : structs.GetSetting('additional_label'),
        'Images'          : structs.GetSetting('image'),
        'Score'           : structs.GetSetting('score')
    }
    Research['QPack']      = structs.GetPackName()
    Research['Stage_1']    = {
        'Conform'    : structs.GetConform(),
        'Confidence' : [0] * structs.GetQuestionsNumber()
    }
    Research['Stage_2']    = {
        'Rounds' : []
    }

def ExportLog():
    return json.dumps(Research, indent = 4, ensure_ascii = False)

def GenLogName():
    if 'Person' in Research:
        return Research['Person']['full_name'].replace(" ", "_")
    else:
        return 'Log_' + str(datetime.date.today())

def GetConfidences():
    return Research['Stage_1']['Confidence']

def GetConfidence(number):
    return Research['Stage_1']['Confidence'][number - 1]

def SetAnswerConfidence(number, confidence):
    if number >= 1 and number <= structs.GetQuestionsNumber():
        Research['Stage_1']['Confidence'][number - 1] = confidence

def AddRound(data):
    Research['Stage_2']['Rounds'].append(data)