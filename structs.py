# Data Structures (structs.py)

import json

# Application Language Data & Functions

Language = {
    'available' : [
        ['ru', 'Русский'],
        ['en', 'English']
    ],
    'Returning' : {
        'NotAvailable' : {
            'ru' : 'Н/Д',
            'en' : 'N/A'
        }
    },
    'Files' : {
        'BrowseButtonLabel' : {
            'ru' : 'Обзор',
            'en' : 'Browse'
        },
        'Ext_TXT' : {
            'ru' : 'текстовый файл',
            'en' : 'text file'
        },
        'Ext_JSON' : {
            'ru' : 'JSON файл',
            'en' : 'JSON file'
        },
        'Ext_CONFIG' : {
            'ru' : 'файл конфигурации',
            'en' : 'configuration file'
        },
        'Ext_XML' : {
            'ru' : 'XML файл',
            'en' : 'XML file'
        },
        'Ext_LOG' : {
            'ru' : 'файл логов',
            'en' : 'log file'
        },
        'Ext_BMP' : {
            'ru' : 'растровое изображение',
            'en' : 'bitmap image'
        },
        'Ext_JPEG' : {
            'ru' : 'сжатое изображение',
            'en' : 'image'
        },
        'Ext_PNG' : {
            'ru' : 'изображение PNG',
            'en' : 'PNG image'
        },
        'Ext_ANY' : {
            'ru' : 'все файлы',
            'en' : 'all files'
        },
        'OpenFileDialogTitle' : {
            'ru' : 'открыть',
            'en' : 'open'
        },
        'SaveFileDialogTitle' : {
            'ru' : 'сохранить',
            'en' : 'save'
        },
        'OpenFileDefaultErrStr' : {
            'ru' : 'файл',
            'en' : 'file'
        },
        'OpenFileTitle' : {
            'ru' : 'файл не найден',
            'en' : 'file not found'
        },
        'OpenFileContent' : {
            'ru' : ' не найден, хотите открыть его самостоятельно?',
            'en' : ' not found, wish to open it on your own?'
        },
        'ConfigurationFileName' : {
            'ru' : 'файл кофигурации',
            'en' : 'configuration file'
        },
        'QuestionsPackFileName' : {
            'ru' : 'пакет вопросов',
            'en' : 'questions pack'
        },
        'ImageFileName' : {
            'ru' : 'изображение(я)',
            'en' : 'bitmap(s)'
        },
        'LoadingErrorTitle' : {
            'ru' : 'ошибка загрузки',
            'en' : 'loading error'
        },
        'LoadingError' : {
            'ru' : 'не удалось загрузить',
            'en' : 'couldn\'t load'
        },
        'IconLoadingErrorTitle' : {
            'ru' : 'Ошибка загрузки иконки',
            'en' : 'Icon loading error'
        },
        'IconLoadingError' : {
            'ru' : 'Не удалось загрузить icon.png',
            'en' : 'Couldn\'t load icon.png'
        }
    },
    'MainMenu' : {
        'Title' : {
            'ru' : 'Главное Меню',
            'en' : 'Main Menu'
        },
        'StartButton' : {
            'ru' : 'Начать',
            'en' : 'Start'
        },
        'SettingsButton' : {
            'ru' : 'Настройки',
            'en' : 'Settings'
        },
        'AboutButton' : {
            'ru' : 'О программе',
            'en' : 'About'
        },
        'QuitButton' : {
            'ru' : 'Выйти',
            'en' : 'Quit'
        }
    },
    'About' : {
        'Title' : {
            'ru' : 'Информация',
            'en' : 'Information'
        },
        'Text'  : {
            'ru' : 'Это приложение создано для проведения исследования влияния когнитивной нагрузки на выбор, совершаемый человеком.',
            'en' : 'This application created to research the influence of cognitive load on human\'s choice'
        }
    },
    'Settings' : {
        'Title' : {
            'ru' : 'Настройки',
            'en' : 'Settings'
        },
        'OkButton' : {
            'ru' : 'OK',
            'en' : 'OK'
        },
        'CancelButton' : {
            'ru' : 'Отмена',
            'en' : 'Cancel'
        },
        'AcceptButton' : {
            'ru' : 'Применить',
            'en' : 'Accept'
        },
        'ResearchBox' : {
            'ru' : 'Исследование',
            'en' : 'Research'
        },
        'ApplicationBox' : {
            'ru' : 'Приложение',
            'en' : 'Application'
        },
        'AdditionalLabelSetting' : {
            'ru' : 'Дополнительная надпись',
            'en' : 'Additional label'
        },
        'ImageSetting' : {
            'ru' : 'Изображение',
            'en' : 'Image'
        },
        'ScoreSetting' : {
            'ru' : 'Счет',
            'en' : 'Score'
        },
        'LanguageSettingLabel' : {
            'ru' : 'Язык',
            'en' : 'Language'
        },
        'QuestionsPackFileLabel' : {
            'ru' : 'Пакет вопросов',
            'en' : 'Questions pack'
        },
        'QuestionsPackNone' : {
            'ru' : 'не выбран',
            'en' : 'not loaded'
        },
        'GroupsNumberLabel' : {
            'ru' : 'Количество групп',
            'en' : 'Groups number'
        },
        'WrongGroupsNumberTitle' : {
            'ru' : 'Ошибка количества групп',
            'en' : 'Wrong groups number'
        },
        'WrongGroupsNumber' : {
            'ru' : 'Введенное количество групп не поддерживается данным пакетом вопросов.',
            'en' : 'The questions pack doesn\'t support the entered groups number'
        }
    },
    'NewResearch' : {
        'Title' : {
            'ru' : 'Новое Исследование',
            'en' : 'New Research'
        },
        'NameLabel' : {
            'ru' : 'ФИО',
            'en' : 'Full name'
        },
        'DateLabel' : {
            'ru' : 'Дата рождения',
            'en' : 'Birth date'
        },
        'SexLabel' : {
            'ru' : 'Пол',
            'en' : 'Sex'
        },
        'SexChoices' : {
            'ru' : [ 'Мужской', 'Женский' ],
            'en' : [ 'Male', 'Female' ]
        },
        'StartButton' : {
            'ru' : 'Начать',
            'en' : 'Start'
        },
        'CancelButton' : {
            'ru' : 'Отмена',
            'en' : 'Cancel'
        },
        'ValidatorWrnTitle' : {
            'ru' : 'Некорректные значения',
            'en' : 'Invalid values'
        },
        'ValidatorWrn' : {
            'ru' : 'Проверьте правильность заполнения полей',
            'en' : 'Check fields filling accuracy'
        }
    },
    'Research' : {
        'Title' : {
            'ru' : [ 'Первый этап', 'Второй этап', 'Благодарность' ],
            'en' : [ 'First stage', 'Second stage', 'Gratitude' ]
        },
        'InformationText' : {
            'ru' : [
                'Исследование разделено на 2 этапа. В первом этапе вам необходимо внимательно читать вопрос и попытаться оценить степень своей уверенности в ответе. Элементы меню для ввода результата оценки становятся доступны через определенное время.',
                'Во втором этапе вам необходимо отвечать на вопросы. Вы можете давать ответы в любом порядке. Если вы не знаете ответ на вопрос, то просто впишите в поле ответа любую непустую строку. После того, как вы ответите на все вопросы из группы, станет доступна кнопка следующего раунда.',
                'Спасибо за выделенное время и приложенные усилия.'
            ],
            'en' : [
                'The research is divided into 2 stages. In the first stage You should read the question carefully and try to rate the percent of confidence in the answer. Elements for entering the result of rating become available after a certain time.',
                'In the second stage You should answer the questions. You may answer in any order. If You don\'t know the answer, just enter any non-empty string into the answer field. After answering all the questions in group, the button of the next round becomes available.',
                'Thank you for your time and efforts.'
            ]
        },
        'SegsLabels' : {
            'ru' : ' 0  5  10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100',
            'en' : ' 0  5  10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100'
        },
        'QuestionNumber' : {
            'ru' : 'Вопрос',
            'en' : 'Question'
        },
        'NextButton' : {
            'ru' : 'Далее',
            'en' : 'Next'
        },
        'ConfidencePercent' : {
            'ru' : 'Уверенность в ответе',
            'en' : 'Answer confidence'
        },
        'TimerSec' : {
            'ru' : ' сек.',
            'en' : ' second(s)'
        },
        'RoundNumber' : {
            'ru' : 'Раунд',
            'en' : 'Round'
        },
        'NextRoundButton' : {
            'ru' : ['Следующий раунд', 'Завершить'],
            'en' : ['Next round', 'Finish']
        },
        'AnswerButton' : {
            'ru' : 'Ответить',
            'en' : 'Answer'
        },
        'ValidateButton' : {
            'ru' : 'OK',
            'en' : 'OK'
        },
        'CancelButton' : {
            'ru' : 'Отмена',
            'en' : 'Cancel'
        },
        'EmptyAnswerWarningTitle' : {
            'ru' : 'Внимание',
            'en' : 'Warning'
        },
        'EmptyAnswerWarning' : {
            'ru' : 'Поле ответа не заполнено.',
            'en' : 'Answer field is empty.'
        },
        'AnswerText' : {
            'ru' : 'Ответ',
            'en' : 'Answer'
        },
        'ScoreText' : {
            'ru' : 'Баллы',
            'en' : 'Score'
        }
    }
}

def ExportLocales():
    return json.dumps(Language, indent = 4)

def Lang(section, element, locale, capitalize = False):
    if section not in Language:
        s = CurLang('Returning', 'NotAvailable', False)
    elif element not in Language[section]:
        s = CurLang('Returning', 'NotAvailable', False)
    elif locale not in Language[section][element]:
        s = CurLang('Returning', 'NotAvailable', False)
    else:
        s = Language[section][element][locale]
    if capitalize:
        if type(s) is str:
            s = s.capitalize()
    return s

def CurLang(section, element, capitalize = True):
    return Lang(section, element, Settings['lang'], capitalize)

def GetAvailableLangs():
    return Language['available']

# Settings Data & Functions

Settings = {
    'additional_label' : False,
    'image'            : False,
    'score'            : False,
    'groups_number'    : 5,
    'lang'             : 'ru',
    'questions_pack'   : None,
    'confidence_time'  : 3
}

ApplicationIcon = None

def SetIcon(icon):
    global ApplicationIcon
    ApplicationIcon = icon

def GetIcon():
    return ApplicationIcon

def SetSetting(setting, value):
    if setting in Settings:
        Settings[setting] = value

def GetSetting(setting):
    if setting in Settings:
        return Settings[setting]
    else:
        return False

def ImportSettings(data):
    if data != None:
        loaded = json.loads(data)
        for setting in loaded:
            SetSetting(setting, loaded[setting])
    else:
        return False
    return True

def ExportSettings():
    return json.dumps(Settings, indent = 4, ensure_ascii = False)

# Research Data & Functions

ImagePack = []

def ImportImagePack(images):
    global ImagePack
    if len(images) != GetSetting('groups_number'):
        return False
    ImagePack = images
    return True

def GetImage(group):
    return ImagePack[group]
    
QuestionsPack = {}

def ImportQuestions(data):
    global QuestionsPack
    if data == None:
        return False
    loaded = json.loads(data)

    requiredFields = ['PackName', 'Author', 'Contents', 'Conform']
    for field in requiredFields:
        if field not in loaded:
            return False
    if len(loaded['Contents']) < 60:
        return False
    else:
        loaded['Contents'] = loaded['Contents'][:60]
    for field in requiredFields:
        QuestionsPack[field] = loaded[field]
    return True

def GetPackName():
    if 'PackName' in QuestionsPack:
        return QuestionsPack['PackName']
    else:
        return None

def GetQuestionsNumber():
    if 'Contents' in QuestionsPack:
        return len(QuestionsPack['Contents'])
    return 0

def __QuestionsNumberCheck(number):
    global QuestionsPack
    if number < 1:
        return False
    elif number > GetQuestionsNumber():
        return False
    return True

def GetQuestion(number):
    global QuestionsPack
    if not __QuestionsNumberCheck(number):
        return CurLang('Returning', 'NotAvailable')
    return QuestionsPack['Contents'][number - 1]['Question']

def GetAnswers(number):
    global QuestionsPack
    if not __QuestionsNumberCheck(number):
        return CurLang('Returning', 'NotAvailable')
    return QuestionsPack['Contents'][number - 1]['Answers']

def GetConform():
    global QuestionsPack
    return QuestionsPack['Conform']

def GetConformed(round, card):
    global QuestionsPack
    return QuestionsPack['Conform'][round - 1][card]

def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0
    for sym in s1:
        if sym in s2:
            c += 1
    return c / (a + b - c)

def ansCompare(s1, s2):
    s1, s2 = s1.lower(), s2.lower()
    

def CheckAnswer(number, answer):
    if not __QuestionsNumberCheck(number):
        return False
    answer = answer.lower()
    for ans in GetAnswers(number):
        if answer == ans.lower():
            return True
    return False

def NewPerson(fullName, birthDate, sex):
    newPerson = {
        'full_name'  : fullName,
        'birth_date' : str(birthDate),
        'sex'        : sex
    }
    return newPerson

def NewAnswer(questionNumber, answer, answerMoment):
    return {
        'Question_Number' : questionNumber,
        'Question'        : GetQuestion(questionNumber),
        'Answers'         : GetAnswers(questionNumber),
        'User_Answer'     : answer,
        'Answer_Moment'   : answerMoment,
        'Correctness'     : CheckAnswer(questionNumber, answer)
    }

def NewRound(number, answers):
    return {
        'Round Number'  : number,
        'Round Answers' : answers
    }

def GetQuestionsConfident(confidences):
    questionsList = list(i for i in range(1, GetQuestionsNumber() + 1))
    return sorted(questionsList, reverse = True, key = lambda x : confidences[x - 1])