import tkinter
from tkinter import filedialog, colorchooser
import keyboard
import ObjectPython
import SceneHandler
import pygame, os
import pyperclip
import sys
import random
import basicFunctions
from SavingSystemUpgrade import SaveLoadSystem
from screeninfo import get_monitors
from PIL import ImageTk, Image

### Basic Variables
ObjectDraggedID = 0 

InspecID = 0
global saveloadmanager
saveloadmanager = SaveLoadSystem(".save", "save_data_folder")
global SceneObjects
SceneObjects = saveloadmanager.load_game_data(["Objects"], [[]])
global monitor

def GetMonitor():
        monitor = get_monitors()[0]
        for mon in get_monitors():
                if (mon.x==0):
                        monitor = mon
        return mon
monitor = GetMonitor()
Height = monitor.height
Width = monitor.width
### End Basic Variables
### Basic Functions
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

def checkRotation(rot):
        return rot%360

global m


def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
def GetEndOfAFile(fpath):
        change = False
        pathDot = ""
        fpath = fpath[::-1]
        for c in fpath:
                if c == "/":
                        change = True
                if change == True:
                        pathDot += c
        fpath = fpath.replace(pathDot, "")
        fpath = fpath[::-1]
        return fpath

def GetObjectByName(WantedName):
        for obj in SceneObjects:
                if (obj.name == WantedName):
                        return obj
        return SceneObjects[0]

def GetObjectByID(objId):
        for i in SceneObjects:
                if (int(i.thisId) == int(objId)):
                        return i
        return False

def SetLayers():
        for o in SceneObjects:
                o.layer = len(SceneObjects) - SceneObjects.index(o) + 1
        HeirarchyRefresh()

        

def allowedName(WantedName):
        global SceneObjects
        global InspecID
        for o in SceneObjects:
                if (o.name == WantedName and o.thisId != InspecID):
                        WantedNameEnd = WantedName[-3::1]
                        if "(" in WantedNameEnd and ")" in WantedNameEnd and WantedNameEnd[-2].isdigit():
                                WantedName = WantedName[:-3:1] + "("  + str(int(WantedNameEnd[-2]) + 1) + ")"
                                return allowedName(WantedName)
                        else :
                                return allowedName(WantedName+"(0)")
        return(WantedName)


def CreateObject():
        WantedObj = ObjectPython.Object()
        WantedObj.name = allowedName(WantedObj.name)
        SceneObjects.append(WantedObj)
        HeirarchyWin.title("Heirarchy*")
        SetLayers()
        HeirarchyRefresh()
        HierarchyList.select_set(0)
        OpenInspector(SceneObjects[len(SceneObjects)-1].name)


def SaveObject(name, active, pos, rotation, scale, image, color):
        obj = GetObjectByID(InspecID)
        
        SceneObjs = []
        ObjIndex = 0
        SceneObjs = saveloadmanager.load_game_data(["Objects"],[[]])
        for i in range(0, len(SceneObjs)):
                if SceneObjs[i].thisId == obj.thisId:
                        ObjIndex = i

        
        obj.SetName(name)
        obj.SetActive(active)
        obj.SetPos(pos)
        obj.SetRot(rotation)
        obj.SetScale(scale)
        
        if (image != "" and image != "Nothing"):
                obj.SetSprite(image)
        if (SceneObjs[ObjIndex].color != color):
                obj.SetColor (color)
        
        SceneObjs[ObjIndex] = obj
        saveloadmanager.save_game_data([SceneObjs], ["Objects"])

def PressingSave(e):
        c = e.keysym
        s = e.state

        # Manual way to get the modifiers
        ctrl  = (s & 0x4) != 0
        if ctrl:
                HeirarchyWin.title("Heirarchy")
                saveloadmanager.save_game_data([SceneObjects], ["Objects"])
### End Basic Functions
### Pygame scene window
pygame.font.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (350,230)

SceneWidth, SceneHeight = Width, Height
Scene = pygame.display.set_mode((SceneWidth-350-350,SceneHeight-200))
pygame.display.set_caption("Scene")

### End Pygame scene window
                
### Inspector
global InspectorWin
InspectorWin = tkinter.Tk()

InspectorWin.geometry("350x" + str(Height) + "-0+0")
InspectorWin.title("Inspector")

##### Basic Inspector Variables

global InspecName,InspecActive
global ObjName,Active
global PosX, PosY, RotZ, ScaleX, ScaleY
global InputPosX, InputPosY, InputRot, InputScaleX, InputScaleY
global InspecImage, InspecColor, objHex
InspecImage = "Nothing"
objHex = "#FFFFFF"

##### Basics window
InspecBasicsText = tkinter.Label(InspectorWin, text = "BASICS", font = ('Ariel', 25), width = 15)
InspecBasicsText.pack(side=tkinter.TOP)
ObjName = tkinter.StringVar()
Active = tkinter.IntVar()

def ChangeObjName(Event):
        global InspecID
        global objHex
        obj = GetObjectByID(InspecID)
        index_ = SceneObjects.index(obj)
        obj.SetName(ObjName.get())
        SceneObjects[index_] = obj
        global HeirarchyWin
        HeirarchyWin.title("Heirarchy*")
        HeirarchyRefresh()
        return True
def SetActive():
        global InspecID
        obj = GetObjectByID(InspecID)
        obj.SetActive(Active.get())
        HeirarchyWin.title("Heirarchy*")
        SetLayers()
NameText = tkinter.Label(InspectorWin,text = "Object name", font = ("Ariel", 20),width = 85)
NameText.pack(side=tkinter.TOP)
InspecName = tkinter.Entry(InspectorWin, text="", font = ('Ariel', 17), width = 25)
InspecName.pack(side=tkinter.TOP)
InspecName.bind('<KeyRelease>', ChangeObjName)
InspecName["textvariable"] = ObjName

InspecActive = tkinter.Checkbutton(InspectorWin, text = "Active", font = ('Ariel', 18), variable = Active, command = SetActive)
InspecActive.pack(side=tkinter.TOP)
##### End Basics

##### Transform
TransformText = tkinter.Label(InspectorWin,text = "TRANSFORM", font = ("Ariel", 25),width = 85)
TransformText.pack(side=tkinter.TOP)

PosX = tkinter.IntVar()
PosY = tkinter.IntVar()
RotZ = tkinter.IntVar()
ScaleX = tkinter.IntVar()
ScaleY = tkinter.IntVar()





def SetPosX(event):
        global InspecID
        obj = GetObjectByID(InspecID)
        obj.SetPos(pygame.Vector2(PosX.get(),obj.position.y))
        HeirarchyWin.title("Heirarchy*")
def SetPosY(event):
        global InspecID
        obj = GetObjectByID(InspecID)
        obj.SetPos(pygame.Vector2(obj.position.x,PosY.get()))
        HeirarchyWin.title("Heirarchy*")

def SetRot(event):
        global InspecID
        obj = GetObjectByID(InspecID)
        obj.SetRot(RotZ.get())
        HeirarchyWin.title("Heirarchy*")

def SetScaleX(event):
        global InspecID
        global ScaleX
        obj = GetObjectByID(InspecID)
        obj.SetScale(pygame.Vector2(ScaleX.get(),obj.scale.y))
        HeirarchyWin.title("Heirarchy*")

def SetScaleY(event):
        global InspecID
        global ScaleY
        obj = GetObjectByID(InspecID)
        obj.SetScale(pygame.Vector2(obj.scale.x,ScaleY.get()))
        HeirarchyWin.title("Heirarchy*")

PositionsText = tkinter.Label(InspectorWin,text = "Positions", font = ("Ariel", 20),width = 85)
PositionsText.pack(side=tkinter.TOP)


PositionsLabel = tkinter.Label(InspectorWin,width = 85, height = 125)
PositionsLabel.pack(side=tkinter.TOP)


InputPosX = tkinter.Entry(PositionsLabel, validate = 'key', textvariable = PosX,font = ("Ariel", 15), width = 14)
InputPosX.pack(side=tkinter.LEFT)
InputPosX.bind('<KeyRelease>', SetPosX)

InputPosY = tkinter.Entry(PositionsLabel, validate = 'key', textvariable = PosY,font = ("Ariel", 15), width = 14)
InputPosY.pack(side=tkinter.RIGHT)
InputPosY.bind('<KeyRelease>', SetPosY)

RotationText = tkinter.Label(InspectorWin,text = "Rotation", font = ("Ariel", 20),width = 85)
RotationText.pack(side=tkinter.TOP)

RotationLabel = tkinter.Label(InspectorWin,width = 85, height = 125)
RotationLabel.pack(side=tkinter.TOP)

InputRot = tkinter.Entry(RotationLabel, validate = 'key', textvariable = RotZ,font = ("Ariel", 15))
InputRot.pack(side=tkinter.TOP)
InputRot.bind('<KeyRelease>', SetRot)

ScalesText = tkinter.Label(InspectorWin,text = "Scale", font = ("Ariel", 20),width = 85)
ScalesText.pack(side=tkinter.TOP)

ScalesLabel = tkinter.Label(InspectorWin,width = 85, height = 125)
ScalesLabel.pack(side=tkinter.TOP)

InputScaleX = tkinter.Entry(ScalesLabel, validate = 'key',  textvariable = ScaleX,font = ("Ariel", 15), width = 14)
InputScaleX.pack(side=tkinter.LEFT)
InputScaleX.bind('<KeyRelease>', SetScaleX)

InputScaleY = tkinter.Entry(ScalesLabel, validate = 'key', textvariable = ScaleY,font = ("Ariel", 15), width = 14)
InputScaleY.pack(side=tkinter.RIGHT)
InputScaleY.bind('<KeyRelease>', SetScaleY)
#### End Transform

##### Sprite Renderer

def ImageFileButton():
        global InspecID
        global InspecImage
        InspecImage = filedialog.askopenfilename(title = "Select sprite",filetypes = (("Image files:", ".png .jpg"),))
        obj = GetObjectByID(InspecID)
        obj.SetSprite(InspecImage)
        if (InspecImage != "" and InspecImage != "Nothing"):
                InspecImgButton.configure(text = GetEndOfAFile(InspecImage))
        HeirarchyWin.title("Heirarchy*")

def SetColorSprite():
        global objHex
        (rbg, objHex)= colorchooser.askcolor()
        InspecColor.configure(bg =objHex)
        obj = GetObjectByID(InspecID)
        obj.color = objHex
        HeirarchyWin.title("Heirarchy*")

InspecSpriteText = tkinter.Label(InspectorWin, text = "SPRITE RENDERER", font = ('Ariel', 25), width = 25)
InspecSpriteText.pack(side=tkinter.TOP)

InspecImgButton = tkinter.Button(InspectorWin, text = "Select image", font = ('Ariel', 15), width = 25, command = ImageFileButton)
InspecImgButton.pack(side=tkinter.TOP)

InspecBetweenLabel = tkinter.Label(InspectorWin, width = 25, height = 2)
InspecBetweenLabel.pack(side=tkinter.TOP)

InspecColor = tkinter.Button(InspectorWin, text = "Select Color", font = ('Ariel', 15), width = 25, command = SetColorSprite)
InspecColor.pack(side=tkinter.TOP)

##### End Sprite Renderer

InspectorWin.configure(bg = "#5b64e9")
ScalesLabel.configure(bg = "#5b64e9")
InspecActive.configure(bg = "#5b64e9")
PositionsText.configure(bg = "#5b64e9")
RotationText.configure(bg = "#5b64e9")
ScalesText.configure(bg = "#5b64e9")
InspecBasicsText.configure(bg = "#525cf1")
NameText.configure(bg = "#5b64e9")
TransformText.configure(bg = "#525cf1")
InspecSpriteText.configure(bg = "#525cf1")
InspecBetweenLabel.configure(bg = "#5b64e9")

def OpenInspector(Obj):
	import tkinter
	from tkinter import colorchooser
	from tkinter.messagebox import showinfo
	import basicFunctions
	
	global InspectorWin, InspecID, InspecName,InspecImgButton,InspecColor
	
	global PosX, PosY, RotZ, ScaleX, ScaleY

	global InspecColor,InspecImgButton
        
	InsObj = GetObjectByName(Obj)
	InspecID = InsObj.thisId
	InspecName.delete(0,tkinter.END)
	InspecName.insert(0,Obj)
	Active.set(InsObj.active)
	PosX.set(int(InsObj.position.x))
	PosY.set(int(InsObj.position.y))
	RotZ.set(int(InsObj.rotation))
	ScaleX.set(int(InsObj.scale.x))
	ScaleY.set(int(InsObj.scale.y))
	InspecColor.configure(bg = InsObj.color)
	if (InsObj.path != ""):InspecImgButton.configure(text = GetEndOfAFile(InsObj.path))
	else:InspecImgButton.configure(text = "Select Image")
	
	return

### End Inspector Window

### Heirarchy Window

def CheckNames(e):
        global InspecID
        global SceneObjects
        obj = GetObjectByID(InspecID)
        index_ = SceneObjects.index(obj)
        SceneObjects[index_].name = allowedName(SceneObjects[index_].name)
        HeirarchyRefresh()

global HierarchyList
global FirstTimeOpenHeir
FirstTimeOpenHeir = True

def HeirarchyRefresh():
        global saveloadmanager
        global HeirarchyWin
        global HierarchyList
                
        L = tkinter.Label(HeirarchyWin, text ="Hierarchy",width = 35, height = 69)
        L.pack()
	
        HierarchyList.delete(0,tkinter.END)
        for obj in SceneObjects:
                HierarchyList.insert(0, obj.name)
                
        HierarchyList.pack(fill="both")

def HeirarchyOpen():
        import tkinter
        from tkinter import colorchooser
        from tkinter.messagebox import showinfo
        from SavingSystemUpgrade import SaveLoadSystem
        global saveloadmanager
        global HeirarchyWin
        global HierarchyList, FirstTimeOpenHeir

        HeirarchyWin = tkinter.Tk()
        HeirarchyWin.geometry("350x"+str(Height-200)+"+0+200")
        HeirarchyWin.title("Heirarchy")
        HeirarchyWin.bind('s', PressingSave)
        def item_selected(event):
                selected_indice = HierarchyList.curselection()
                selected_lang= ",".join([HierarchyList.get(i) for i in selected_indice])
                msg = f'You selected: {selected_lang}'

                if (selected_lang != ""):
                        OpenInspector(selected_lang)
        SceneObjects = saveloadmanager.load_game_data(["Objects"], [[ObjectPython.Object()]])


        def GetItemRight(event):
                global InsObj
                global InspecID
                HierarchyList.selection_clear(0,tkinter.END)
                HierarchyList.selection_set(HierarchyList.nearest(event.y))
                HierarchyList.activate(HierarchyList.nearest(event.y))
                selected_indice = HierarchyList.curselection()
                selected_lang= ",".join([HierarchyList.get(i) for i in selected_indice])
                InsObj = GetObjectByName(selected_lang)
                InspecID = InsObj.thisId
                do_popup(event)
        
        L = tkinter.Label(HeirarchyWin, text ="Hierarchy",width = 35, height = 69)
        L.pack()

        HierarchyList = tkinter.Listbox(L, height = HeirarchyWin.winfo_screenheight(),  width = int(HeirarchyWin.winfo_reqwidth()))

	
        for obj in SceneObjects:
                HierarchyList.insert(0, obj.name)
        if (len(SceneObjects) > 0 and FirstTimeOpenHeir):
                FirstTimeOpenHeir = False
                HierarchyList.select_set(0)
                OpenInspector(SceneObjects[len(SceneObjects)-1].name)
	
        HierarchyList.bind('<<ListboxSelect>>', item_selected)
        HierarchyList.bind('<Button-3>', GetItemRight)
        HierarchyList.bind('<Button-1>', CheckNames) 
        HierarchyList.pack(fill="both")
	
HeirarchyOpen()
##### Basic Menu

def CopyObject():
        global InspecID
        pyperclip.copy('Object10' + str(InspecID))

def PasteObject():
        global InspecID, SceneObjects
        if "Object10" not in pyperclip.paste():
                return;
        DesiObjId = pyperclip.paste().replace('Object10', "") 
        DesiObj = GetObjectByID(DesiObjId)
        objIndex = SceneObjects.index(DesiObj)

        PastedObj = ObjectPython.Object()
        PastedObj.SetName(allowedName(DesiObj.name))
        PastedObj.SetActive(DesiObj.active)
        PastedObj.SetPos(DesiObj.position)
        PastedObj.SetRot(DesiObj.rotation)
        PastedObj.SetScale(DesiObj.scale)
        
        if (DesiObj.path != "" and DesiObj.path != "Nothing"):
                PastedObj.SetSprite(DesiObj.path)
        PastedObj.SetColor (DesiObj.color)
        
        SceneObjects.append(PastedObj)
        saveloadmanager.save_game_data([SceneObjects], ["Objects"])
        HeirarchyRefresh()

m = tkinter.Menu(HierarchyList, tearoff = 0)
m.add_command(label ="Create an object", command=CreateObject)
m.add_command(label ="Copy", command=CopyObject)
m.add_command(label ="Paste", command=PasteObject)
m.add_command(label ="Reload",command=HeirarchyRefresh)
#m.add_separator()
#m.add_command(label ="Rename")


##### stop Basic Menu

### stop Heirarchy Window

### Scene Management
<<<<<<< Updated upstream
=======
run = True

##### Save popup

global PopupSave

def QuitWithoutSave():
        global run
        run = False
def SavePopup():
        global HeirarchyWin, run

        if "*" not in HeirarchyWin.title():
                run = False
                return
        from tkinter.messagebox import showinfo
        PopupSave = tkinter.Tk()
        PopupSave.geometry(f"350x150+"+str(int(Width/2 - 175))+"+"+str(int(Height/2 - 75)))
        PopupSave.wm_title("Save Check")

        l = tkinter.Label(PopupSave, text="Are you sure you wanna quit?\n You have unsaved changes", font=("Ariel", 18))
        l.pack(side=tkinter.TOP)

        b = tkinter.Button(PopupSave,bg="#bd0909",highlightbackground="Red", text="Yes", command=QuitWithoutSave,font=("Ariel", 15), height=3, width=12)
        b.pack(side=tkinter.LEFT)
        b = tkinter.Button(PopupSave,bg="#13a842",highlightbackground="Green", text="No", command=PopupSave.destroy,font=("Ariel", 15), height=3, width=12)
        b.pack(side=tkinter.RIGHT)


##### End Save popup

def GetVectorNorDir(Pos1, Pos2):
        return [(Pos1[0] - Pos2[0]),(Pos1[1] - Pos2[1])]

##### Collision outline

def CheckOutline(outline):
        _outline = outline
        myoutline = []
        myoutline.append(_outline[0])
        for index in range(0, len(_outline)):
                #If index should be checked
                if index > 0 and index < len(_outline)-1:
                        if GetVectorNorDir(_outline[index-1], _outline[index]) != GetVectorNorDir(_outline[index], _outline[index+1]):
                                myoutline.append(_outline[index])
        myoutline.append(_outline[len(_outline)-1])
        print("Outline: " + str(myoutline))
        return outline

def ShowOutline(Force):
        for obj in SceneObjects:
                if obj.path != "" and obj.path != "Nothing" and (len(obj.polcolliderpoints) == 0 or Force):
                        ObjSprite = pygame.image.load(obj.path)
                        Size = int(ObjSprite.get_size()[0] + ObjSprite.get_size()[1])
                        ObjSprite = pygame.transform.scale(ObjSprite, ((int((Size/ObjSprite.get_size()[1]) * obj.scale.x)),int((Size/ObjSprite.get_size()[0]) * obj.scale.y)))
                        ObjSprite = pygame.transform.rotate(ObjSprite, obj.rotation)
                        ObjRect = ObjSprite.get_rect(center = ObjSprite.get_rect(center = (obj.position.x,obj.position.y)).center)
                        objMask = pygame.mask.from_surface(ObjSprite)
                        obj.collisiondepth = 3
                        outline = [(p[0] + ObjRect[0], p[1] + ObjRect[1]) for p in objMask.outline(obj.collsiondepth)]
                        outline = CheckOutline(outline)
                        obj.polcolliderpoints = outline
                if len(obj.polcolliderpoints) >= 2:
                        pygame.draw.lines(Scene, (126, 255,126), False, obj.polcolliderpoints, 1)


##### End Collision outline

global DragOffset

>>>>>>> Stashed changes
def DrawEveryChar():
        for SceneO in SceneObjects:
                if (SceneO.path != ""):
                        ObjSprite = pygame.image.load(SceneO.path)
                        Size = int(ObjSprite.get_size()[0] + ObjSprite.get_size()[1])
                        ObjSprite = pygame.transform.scale(ObjSprite, ((int((Size/ObjSprite.get_size()[1]) * SceneO.scale.x)),int((Size/ObjSprite.get_size()[0]) * SceneO.scale.y)))
                        ObjSprite = pygame.transform.rotate(ObjSprite, SceneO.rotation)
                        ObjRect = ObjSprite.get_rect(center = ObjSprite.get_rect(center = (SceneO.position.x,SceneO.position.y)).center)
                        Scene.blit(ObjSprite, ObjRect)

def HandleSceneObjects(event, mx, my):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if  event.button == 1:
                        for SceneO in SceneObjects:
                                ObjSprite = pygame.image.load(SceneO.path)
                                Size = int(ObjSprite.get_size()[0] + ObjSprite.get_size()[1])
                                ObjSprite = pygame.transform.scale(ObjSprite, ((int((Size/ObjSprite.get_size()[1]) * SceneO.scale.x)),int((Size/ObjSprite.get_size()[0]) * SceneO.scale.y)))
                                ObjSprite = pygame.transform.rotate(ObjSprite, SceneO.rotation)
                                Collider = ObjSprite.get_rect(center = ObjSprite.get_rect(center = (SceneO.position.x,SceneO.position.y)).center)
                                
                                if Collider.collidepoint((mx, my)):                        
                                        SceneO.drag = True
                                        return
                                else:
                                        SceneO.drag = False
                if event.button == 4:
                        for SceneO in SceneObjects:
                                ObjSprite = pygame.image.load(SceneO.path)
                                Size = int(ObjSprite.get_size()[0] + ObjSprite.get_size()[1])
                                ObjSprite = pygame.transform.scale(ObjSprite, ((int((Size/ObjSprite.get_size()[1]) * SceneO.scale.x)),int((Size/ObjSprite.get_size()[0]) * SceneO.scale.y)))
                                ObjSprite = pygame.transform.rotate(ObjSprite, SceneO.rotation)
                                Collider = ObjSprite.get_rect(center = ObjSprite.get_rect(center = (SceneO.position.x,SceneO.position.y)).center)
                                
                                if Collider.collidepoint((mx, my)):
                                        SceneO.rotation += (5)
                                        SceneO.rotation = int(SceneO.rotation%360)
                                        RotZ.set(int(SceneO.rotation))
                                        return
                if event.button == 5:
                        for SceneO in SceneObjects:
                                ObjSprite = pygame.image.load(SceneO.path)
                                Size = int(ObjSprite.get_size()[0] + ObjSprite.get_size()[1])
                                ObjSprite = pygame.transform.scale(ObjSprite, ((int((Size/ObjSprite.get_size()[1]) * SceneO.scale.x)),int((Size/ObjSprite.get_size()[0]) * SceneO.scale.y)))
                                ObjSprite = pygame.transform.rotate(ObjSprite, SceneO.rotation)
                                Collider = ObjSprite.get_rect(center = ObjSprite.get_rect(center = (SceneO.position.x,SceneO.position.y)).center)
                                
                                if Collider.collidepoint((mx, my)):
                                        SceneO.rotation += (355)
                                        SceneO.rotation = int(SceneO.rotation%360)
                                        RotZ.set(int(SceneO.rotation))
                                        return
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for SceneO in SceneObjects:
<<<<<<< Updated upstream
                        SceneO.drag = False
=======
                        if SceneO.drag:
                                #ShowOutline(True)
                                SceneO.drag = False
>>>>>>> Stashed changes
mouseX, mouseY = 0, 0

FPS = 150
def main():
        clock = pygame.time.Clock()
        global ObjectDraggedID
        run = True
        while run:
                clock.tick(FPS)
                pygame.display.set_caption(("Scene " + str(clock.get_fps())))

                mouseX, mouseY = pygame.mouse.get_pos()
                bgColor = basicFunctions.HexToRGB(SceneObjects[0].color)

                for event in pygame.event.get():
                        HandleSceneObjects(event, mouseX, mouseY)
                        if event.type == pygame.QUIT:
                                global exitNum
                                run = False
                for obj in SceneObjects:
                        if (obj.drag):
                                obj.SetPos(pygame.Vector2(mouseX, mouseY))
                                PosX.set(mouseX)
                                PosY.set(mouseY)
                
                Scene.fill(bgColor)
                DrawEveryChar()
                pygame.display.flip()
                HeirarchyWin.update()
        global PopupSave
        pygame.quit()
        InspectorWin.destroy()
        HeirarchyWin.destroy()
        PopupSave.destroy()
        

if __name__ == "__main__":
     main()
### End Scene Management