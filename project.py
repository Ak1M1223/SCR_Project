import pygame
import sys
import random
import math
pygame.init()

class TimeGraph:
    ys = []
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, screen, color, Rect):
        self.rm = ResourceManager
        self.color = color
        self.Rect = Rect
        self.screen = screen
    def Draw(self, y):
        pygame.draw.rect(self.screen, (0,0,0), self.Rect, 0)
        pygame.draw.rect(self.screen, (100,100,100), self.Rect, 2)
        self.ys.append(y)
        if len(self.ys) > self.Rect[2]:
            self.ys.pop(0)
        #print(len(self.ys))
        counter = 0

        for y in self.ys:
            self.screen.set_at((int(self.Rect[0] +  counter), int(self.Rect[1] + self.Rect[3] - y[0])), self.color)
            counter += 1
        pygame.draw.line(self.screen, (255,0,0),(self.Rect[0],self.Rect[1] + self.Rect[3] - int(y[1])), (self.Rect[0] + self.Rect[2], self.Rect[1] + self.Rect[3] - int(y[1])))


class Button:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self,text,screen,color,Rect):
        self.color = color
        self.normalcolor = color
        self.pressedcolor = (color[0]/2, color[1]/2, color[2]/2,)
        self.Rect = Rect
        self.text = text
        self.screen = screen
        self.state = False
        self.listeners = []
        self.oldstate = False

    def DrawButton(self):
        pygame.draw.rect(self.screen, self.color, self.Rect, 0)
        font = pygame.font.SysFont(None, 20)
        textbuffer = font.render(self.text, True, (0, 0, 0))
        place = (int(self.Rect[0] + self.Rect[2]/2 - textbuffer.get_width()/2), int(self.Rect[1] + self.Rect[3]/2 - textbuffer.get_height()/2))
        self.screen.blit(textbuffer,place)
    def IsClicked(self):
        mousePos = pygame.mouse.get_pos()
        if(mousePos[0] > self.Rect[0] and mousePos[0] < self.Rect[0] + self.Rect[2] and mousePos[1] > self.Rect[1] and mousePos[1] < self.Rect[1] + self.Rect[3] and pygame.mouse.get_pressed() == (1, 0, 0)):
            self.color = self.pressedcolor
            self.state = True
        else:
            self.color = self.normalcolor
            self.state = False
        self.IsChanged()
    def AddListener(self, listener):
        self.listeners.append(listener)

    def NotifyAllListeners(self):
        for listener in self.listeners:
            listener.Update()
    def IsChanged(self):
        if self.oldstate != self.state:
            self.oldstate = self.state
            self.NotifyAllListeners()
    def GetState(self):
        return self.state

class InfoPanel:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self,screen,color,Rect):
        self.screen = screen
        self.color = color
        self.Rect = Rect

    def Draw(self,text):
        pygame.draw.rect(self.screen, (0,0,0), self.Rect, 0)
        font = pygame.font.SysFont(None, 20)
        textbuffer = font.render(text, True, self.color)
        place = (int(self.Rect[0]), int(self.Rect[1] + self.Rect[3]/2 - textbuffer.get_height()/2))
        self.screen.blit(textbuffer,place)


#ObserverPattern
class Listener: #Abstrakcyjna klasa
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, subject):
        self.subject = subject

    def Update(self):
        pass

#Specjalne Listenery/Funkcje przycisków
class ButtonListenerResCon(Listener):
    def AddResourcesInfo(self,rm):
        self.rm = rm
    def Update(self):
        if not self.subject.GetState():
            self.rm.ListConsumer[0].SetValue(0)

class ButtonListenerResMax(Listener):
    def AddResourcesInfo(self,rm):
        self.rm = rm
    def Update(self):
        if not self.subject.GetState():
            self.rm.ListProducer[0].SetValue(0)

class ButtonListenerCoPl(Listener):
    def AddResourcesInfo(self, rm):
        self.rm = rm

    def Update(self):
        if not self.subject.GetState():
            self.rm.ListConsumer[0].SetValue(self.rm.ListConsumer[0].GetValue() + 0.1)
            #print(self.rm.ListConsumer[0].GetValue())


class ButtonListenerCoMi(Listener):
    def AddResourcesInfo(self,rm):
        self.rm = rm
    def Update(self):
        if not self.subject.GetState():
            self.rm.ListConsumer[0].SetValue(self.rm.ListConsumer[0].GetValue() - 0.1)
            print(self.rm.ListConsumer[0].GetValue())


class ButtonListenerPrMi(Listener):
    def AddResourcesInfo(self,rm):
        self.rm = rm
    def Update(self):
        if not self.subject.GetState():
            self.rm.ListProducer[0].SetValue(self.rm.ListProducer[0].GetValue() - 5)

class ButtonListenerPrPl(Listener):
    def AddResourcesInfo(self,rm):
        self.rm = rm
    def Update(self):
        if not self.subject.GetState():
            self.rm.ListProducer[0].SetValue(self.rm.ListProducer[0].GetValue() + 5)

#Endof ObserverPattern
#MVC pattern
class Controller:
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self):
        pass
    def run(self):
        pass

class ConcreteController(Controller):
    y = 0
    def __init__(self,ButtonList,GraphList,Info,RM):
        self.ButtonList = ButtonList
        self.GraphList = GraphList
        self.Info = Info
        self.RM = RM

    def run(self):
        while True:
            for button in self.ButtonList:
                button.DrawButton()
                button.IsClicked()
            info = self.RM[0].GetResource()
            self.GraphList[0].Draw(info)
            text1 = "Dostępne zasoby: {}".format(info[1])
            text2 = "Używane zasoby:  {}".format(int(info[0]))
            if self.RM[0].MaxWarning():
                text3 = "Brak nowych zasobów!"
            else:
                text3 = "Zasoby dostępne!"

            if self.RM[0].MinWarning():
                text4 = "Brak używanych zasobów!"
            else:
                text4 = "Zasoby w użyciu!"


            self.Info[0].Draw(text1)
            self.Info[1].Draw(text2)
            self.Info[2].Draw(text3)
            self.Info[3].Draw(text4)

            #print(self.RM[0].MaxWarning() , " max")
            #print(self.RM[0].MinWarning() , " min")
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: sys.exit()
            pygame.display.flip()



#EndofMVCPattern

#Klasy Producenta i Konsumenta
class Producer:
    def __init__(self, perSec):
        self.perSec = perSec

    def SetValue(self, perSec):
        self.perSec = perSec

    def GetValue(self):
        return self.perSec

class Consumer:
    def __init__(self, perSec):
        self.perSec = perSec

    def SetValue(self, perSec):
        self.perSec = perSec

    def GetValue(self):
        return self.perSec

#Kontroler Zasobów
class ResourceManager:
    resource = 0
    maxresources = 0
    maxWarning = False
    minWarning = False
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, ListProducer, ListConsumer):
        self.ListProducer = ListProducer
        self.ListConsumer = ListConsumer

    def SetResource(self,value):
        self.resource = value

    def GetResource(self):
        self.maxresources = 0
        for producer in self.ListProducer:
            self.maxresources += producer.GetValue()

        for consumer in self.ListConsumer:
            self.resource += consumer.GetValue()
            if self.resource <= 0:
                self.minWarning = True
                self.resource = 0
            else:
                self.minWarning = False

            if self.resource >= self.maxresources:
                self.maxWarning = True
                self.resource = self.maxresources
            else:
                self.maxWarning = False
        return self.resource,self.maxresources

    def MaxWarning(self):
        return self.maxWarning

    def MinWarning(self):
        return self.minWarning


#Kod Główny
if __name__ == "__main__":
    print("Joachim Tomik, Marzena Watarzyszyn")
    screen = pygame.display.set_mode([600,600])
    pygame.display.set_caption('Konsument Producent')
    cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    #Przyciski
    buttonprpl = Button("Zasoby +",screen, (200,200,200),(405,5,195,95))
    buttonprmi = Button("Zasoby -", screen, (200, 200, 200), (405, 105, 195, 95))
    buttonkopl = Button("Konsumpcja +", screen, (200, 200, 200), (405, 205, 195, 95))
    buttonkomi = Button("Konsumpcja -", screen, (200, 200, 200), (405, 305, 195, 95))
    buttonresk = Button("Reset Konsumpcji", screen, (200, 200, 200), (405, 505, 195, 95))
    buttonresz = Button("Reset Zasobów", screen, (200, 200, 200), (405, 405, 195, 95))
    buttonList = [buttonkomi, buttonkopl, buttonprmi, buttonprpl, buttonresz, buttonresk]

    graph1 = TimeGraph(screen, (200, 100, 100), (0, 0, 400, 400))
    graphList = [graph1]

    pr1 = Producer(0)
    co1 = Consumer(0)

    rm = ResourceManager([pr1], [co1])

    inf1 = InfoPanel(screen, (255, 0, 0), (0, 405, 200, 25))
    inf2 = InfoPanel(screen, (255, 0, 0), (0, 430, 200, 25))
    inf3 = InfoPanel(screen, (255, 0, 0), (0, 455, 200, 25))
    inf4 = InfoPanel(screen, (255, 0, 0), (0, 480, 200, 25))
    infoList = [inf1,inf2,inf3,inf4]

    controller = ConcreteController(buttonList, graphList, infoList, [rm])
    #Przypisanie funkcjonalności przyciskow
    listenerres = ButtonListenerResMax(buttonresz)
    listenerres.AddResourcesInfo(rm)
    buttonresz.AddListener(listenerres)

    listenerres = ButtonListenerResCon(buttonresk)
    listenerres.AddResourcesInfo(rm)
    buttonresk.AddListener(listenerres)

    listenerprpl = ButtonListenerPrPl(buttonprpl)
    listenerprpl.AddResourcesInfo(rm)
    buttonprpl.AddListener(listenerprpl)

    listenerprmi = ButtonListenerPrMi(buttonprmi)
    listenerprmi.AddResourcesInfo(rm)
    buttonprmi.AddListener(listenerprmi)

    listenercopl = ButtonListenerCoPl(buttonkopl)
    listenercopl.AddResourcesInfo(rm)
    buttonkopl.AddListener(listenercopl)

    listenercomi = ButtonListenerCoMi(buttonkomi)
    listenercomi.AddResourcesInfo(rm)
    buttonkomi.AddListener(listenercomi)



    keys = pygame.key.get_pressed()
    controller.run() #włączenie kontrolera UI
