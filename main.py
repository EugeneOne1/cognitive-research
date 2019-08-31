# Main Script (main.py)

import wx
import ui
import files
import structs

class ApplicationCore(wx.App):
    def OnInit(self):
        structs.ImportSettings(files.OpenJSON('settings.json',
                                              True,
                                              True,
                                              structs.CurLang('Files', 'ConfigurationFileName')))
        appIconPath = 'icon.png'
        if files.CheckExisting(appIconPath):
            structs.SetIcon(wx.Icon(appIconPath))
        else:
            ui.ErrMsg(structs.CurLang('Files', 'IconLoadingErrorTitle'),
                      structs.CurLang('Files', 'IconLoadingError'))
            return False
        ui.FramesStart()
        self.SetTopWindow(ui.mainFrame)
        
        return True

def main():
    core = ApplicationCore()
    core.MainLoop()
    files.SaveJSON(structs.ExportSettings(), 'settings.json')

if __name__ == '__main__':
    main()