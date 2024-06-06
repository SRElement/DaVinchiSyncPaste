#!/user/bin/env python
#\/ A very useful sorce for making GUI's for Resolve \/
#https://www.steakunderwater.com/wesuckless/viewtopic.php?t=1411

import json

ui =  fu.UIManager
disp = bmd.UIDispatcher(ui)

proj = resolve.GetProjectManager().GetCurrentProject()
timeline = proj.GetTimelineByIndex(1)
trackCount = timeline.GetTrackCount("audio")

#Can be found at the start but also have user select it on main screen?
cwd = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility"

def GetProgramDataDict():
    with open(cwd+"\\Data\\ProgramData.json", 'r') as f:
            programDataDict = json.loads(f.read())
            f.close()
    
    return programDataDict

def SaveProgramData(programDataDict):
    with open(cwd+"\\Data\\ProgramData.json", 'w') as f:
            f.write(json.dumps(programDataDict))
            f.close()

def GetCharacterDict(charName):
    # Retive Character json
    programDataDict = GetProgramDataDict()

    return programDataDict["Characters"][charName]

#---------------------------------------NewPage---------------------------------------

def CharCreatorWindow(charName):

    width,height = 600,200
    win = disp.AddWindow({
        "ID":"CharCreatorWin",
        "WindowTitle":"Character Creator",
        "Geometry":[100,100,width,height],
        "Spacing":10,
        "Margin":20,
    },
    [
        ui.VGroup({
           "ID":"root" 
        },
        [
            ui.VGap(0, 0.5),

            ui.HGroup({
                "Weight":0
            },
            [
                ui.Label({
                    "ID":"varLabel",
                    "Text":"Name:"
                }),
                ui.LineEdit({
                    "ID":"NameEdit",
                    "PlaceholderText":"Enter Character Name"
                })
            ]),
            
            ui.HGroup({
                "Weight":0
            },
            [
                ui.Label({
                    "ID":"varLabel",
                    "Text":"Image File:"
                }),
                ui.Button({
                    "ID":"FileButton",
                    "Text":"Select a File"
                })
            ]),

            ui.HGroup({
                "Weight":0
            },
            [
                ui.Label({
                    "ID":"varLabel",
                    "Text":"Audio Track:"
                }),
                ui.ComboBox({
                    "ID":"TrackCombo",
                    "Text":"Select Track"
                })
            ]),

            ui.HGroup({
                "Weight":0
            },
            [
                ui.Label({
                    "ID":"varLabel",
                    "Text":"Audio Folder:"
                }),
                ui.Button({
                    "ID":"FolderButton",
                    "Text":"Select a Folder"
                })
            ]),

            ui.VGap(5),

            ui.HGroup({
                "Weight":0
            },
            [
                ui.Button({
                    "ID":"ReturnButton",
                    "Text":"Return"
                }),
                ui.Button({
                    "ID":"SaveButton",
                    "Text":"Save Character"
                })
            ]),

            ui.VGap(0,0.5)
        ])
    ])

    itm = win.GetItems()


    # Get Track Names for ComboBox
    for i in range(1,trackCount+1):
        itm["TrackCombo"].AddItem(timeline.GetTrackName("audio",i))

    #If character passed in, load character info
    if charName != None:
        #Load char json
        charDict = GetCharacterDict(charName)

        #Fill in data for character
        itm["NameEdit"].Text = charName
        itm["FileButton"].Text = charDict["imgPath"]
        itm["TrackCombo"].CurrentIndex = int(charDict["track"])+1
        itm["FolderButton"].Text = charDict["audioPath"]


    # On Close, quit TODO make return to main page (prompt unfinished work?)
    def OnWindowClose(ev):
        win.Hide()
        MainWindow()
    win.On.CharCreatorWin.Close = OnWindowClose
    win.On.ReturnButton.Clicked = OnWindowClose

    # Find Image File TODO what should the defult path be? recently selected path but also before that
    def OnFileButtonClicked(ev):
        selectedPath = str(fu.RequestFile('C:/'))
        itm["FileButton"].Text = selectedPath
    win.On.FileButton.Clicked = OnFileButtonClicked

    # Find Audio Folder
    def OnFolderButtonClicked(ev):
        selectedPath = str(fu.RequestDir('C:/'))
        itm["FolderButton"].Text = selectedPath
    win.On.FolderButton.Clicked = OnFolderButtonClicked

    # Save Char As JSON TODO Check to see if values are valid e.g. name != '' (error handling)
    def OnSaveButtonClicked(ev):

        #Retrive data
        name = itm["NameEdit"].Text
        imgPath = itm["FileButton"].Text
        track = itm["TrackCombo"].CurrentIndex
        audioPath = itm["FolderButton"].Text

        #Open ProgramData to add the character to it
        programDataDict = GetProgramDataDict()
        
        #Add the character data to the JSON
        programDataDict["Characters"][name] = {
            "imgPath":imgPath,
            "track":track,
            "audioPath":audioPath
        }

        #Write back to file
        SaveProgramData(programDataDict)

        win.Hide()
        MainWindow()
    win.On.SaveButton.Clicked = OnSaveButtonClicked

    win.Show()
    disp.RunLoop()
    win.Hide()

    return win,win.GetItems()

#---------------------------------------NewPage---------------------------------------

def MainWindow():
    width,height = 400,200

    win = disp.AddWindow({
        "ID":"MainWindow",
        "WindowTitle":"Character Editor",
        "Geometry":[100,100,width,height],
        "Spacing":10,
        "Margin":20
    },
    [
        ui.VGroup({
            "ID":"root"
        },
        [
            ui.VGap(0, 0.1),

            ui.HGroup({
                "Weight":3
            },
            [
                ui.Tree({
                    "ID":"CharTree",
                    "ColumnCount":1,
                    "SortingEnabled":True,
                    "Events":{
                        "ItemDoubleClicked":True,
                        "ItemClicked":True
                    }
                }),
            ]),

            ui.HGroup({
                "Weight":0
            },
            [
                ui.Button({
                    "ID":"DeleteCharButton",
                    "Text":"- Delete Character",
                    "Enabled":False
                }),
                ui.Button({
                    "ID":"NewCharButton",
                    "Text":"+ New Character"
                })
            ]),

            ui.VGap(0, 0.1)
        ])  
    ])

    itm = win.GetItems()

    def populateCharTree():
        # Retive Character Dict
        programDataDict = GetProgramDataDict()

        #Populate CharTree with characters from the json
        for character in programDataDict["Characters"]:
            itmRow = itm["CharTree"].NewItem()
            itmRow.Text[0] = character
            itm["CharTree"].AddTopLevelItem(itmRow)

    # Add a header row
    hdr = itm["CharTree"].NewItem()
    hdr.Text[0] = "Characters"
    itm["CharTree"].SetHeaderItem(hdr)
    populateCharTree()

    def OnCharTreeRowClick(ev):
        itm["DeleteCharButton"].Enabled = True
    win.On.CharTree.ItemClicked = OnCharTreeRowClick

    #A tree row was double clicked on
    def OnCharTreeRowDoubleClick(ev):
        win.Hide()
        CharCreatorWindow(ev["item"].Text[0])
    win.On.CharTree.ItemDoubleClicked = OnCharTreeRowDoubleClick

    # When window closed
    def OnWindowClose(ev):
        disp.ExitLoop()
    win.On.MainWindow.Close = OnWindowClose

    # Delte a character
    def OnDeleteCharButtonClicked(ev):
        # Retive Character json, delete entry and then save
        programDataDict = GetProgramDataDict()
        del programDataDict["Characters"][itm["CharTree"].CurrentItem().Text[0]]
        SaveProgramData(programDataDict)
        #Refresh Tree to reflect change
        itm["CharTree"].Clear()
        populateCharTree()
    win.On.DeleteCharButton.Clicked = OnDeleteCharButtonClicked

    # Open Character Creation Page when new NewCharButton clicked
    def OnNewCharButtonClicked(ev):
        win.Hide()
        CharCreatorWindow(None)
    win.On.NewCharButton.Clicked = OnNewCharButtonClicked

    win.Show()
    disp.RunLoop()
    win.Hide()

    return win,win.GetItems()

MainWindow()


