from tkinter import*
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.lib.function_base import delete
import math

#Lưu ý: trục y trong máy tính nó bị quay xuống
'''Hằng số'''
dvDodai = 50 
colorVerticalLine = "blue" # đứng
colorHorizontalLine = "red" # ngang

#hằng số canvas
canvasWIDTH = 600
canvasHEIGHT = 600
#màu vector
colorVtX = "orange"
colorVtY = "green"
#bán kính vùng click đc của vetor
radiusCanChangeVtPos = 10
'''-------'''

def drawVector_Line( canvas, vt, color):
    x = vt[0]
    y = vt[1]
    #line
    #truc y no bi nguoc
    y = -y
    if (x == 0): 
        canvas.create_line(canvasWIDTH/2, 0, 
            canvasWIDTH/2, canvasHEIGHT, fill=color, width=2)
    elif (abs(y/x) >= 1):
        canvas.create_line(- x * canvasHEIGHT / (2 * y) + canvasWIDTH / 2, 0, 
            x * canvasHEIGHT / (2 * y) + canvasWIDTH / 2, canvasHEIGHT, fill=color, width=1)
    else:
        canvas.create_line( 0, - y * canvasWIDTH / (2 * x) + canvasHEIGHT / 2,
            canvasWIDTH, y * canvasWIDTH / (2 * x) + canvasHEIGHT / 2, fill=color, width=1)
    #vector
    canvas.create_line(canvasWIDTH/2, canvasHEIGHT/2, 
            canvasWIDTH/2 + x*dvDodai, canvasHEIGHT/2 + y*dvDodai, fill=color, width=3, arrow=LAST)
    #vẽ dấu chấm
    dentaX = vt[0]*dvDodai
    dentaY = -vt[1]*dvDodai
    while (dentaX >= -canvasWIDTH/2 and dentaX <= canvasWIDTH/2 
        and dentaY >= -canvasHEIGHT/2 and dentaY <= canvasHEIGHT/2
        and math.hypot(dentaX, dentaY) >= 2):
        canvas.create_oval( dentaX + canvasWIDTH/2 - 3, dentaY + canvasHEIGHT/2 - 3, dentaX + canvasWIDTH/2 + 3, dentaY + canvasHEIGHT/2 + 3, fill=color)
        canvas.create_oval( (canvasWIDTH/2 - dentaX) - 3, (canvasHEIGHT/2 - dentaY) - 3, (canvasWIDTH/2 - dentaX) + 3, (canvasHEIGHT/2 - dentaY) + 3, fill=color)
        dentaX += vt[0]*dvDodai
        dentaY += -vt[1]*dvDodai
        
        print(dentaX)

class CoSo:
    def __init__(self, matrix, colorX, colorY):
        self.matrix = matrix
        self.colorX = colorX
        self.colorY = colorY

#tk
tk = Tk()
tk.title("")
#tk.state("zoomed")
tk.columnconfigure(0, weight=1)
tk.columnconfigure(1, weight=1)

tk.rowconfigure(1, weight=1)


#buttons Frame
btnsFrame = Frame( tk)

btnDoiCoSo = Button( btnsFrame, text="Đổi cơ sở")
btnDoiCoSo.grid(row=0, column=0)
def setModeDoiCoSo(e):
    btnDoiCoSo.config(text="OK")
    btn2.config(state=DISABLED)
    myCanvasLeft.canvas.bind("<Button-1>", isClickInVectorLeft)
    btnDoiCoSo.bind("<Button-1>", completeDoiCoSo)

def isClickInVectorLeft(e):
        x = (e.x - canvasWIDTH/2)/dvDodai
        y = -(e.y - canvasHEIGHT/2)/dvDodai

        vtX = myCanvasLeft.coSoPhu.matrix[:,0]
        vtY = myCanvasLeft.coSoPhu.matrix[:,1]
        #x trc y sau
        if ((x - vtX[0])**2 + (y - vtX[1])**2 <= (radiusCanChangeVtPos/dvDodai)**2):
            myCanvasLeft.canvas.bind("<B1-Motion>", changeVectorXPos_Left)
        elif ((x - vtY[0])**2 + (y - vtY[1])**2 <= (radiusCanChangeVtPos/dvDodai)**2):
            myCanvasLeft.canvas.bind("<B1-Motion>", changeVectorYPos_Left)

def changeVectorXPos_Left(e):
    x = (e.x - canvasWIDTH/2)/dvDodai
    y = -(e.y - canvasHEIGHT/2)/dvDodai
    (myCanvasLeft.coSoPhu).matrix[0,0] = x
    (myCanvasLeft.coSoPhu).matrix[1,0] = y
    myCanvasLeft.render()

    myCanvasRight.coSoPhu.matrix = np.linalg.pinv(myCanvasLeft.coSoPhu.matrix) @ np.array([[1,0], [0,1]], dtype=float)
    myCanvasRight.polygon = np.linalg.pinv(myCanvasLeft.coSoPhu.matrix) @ myCanvasLeft.polygon
    myCanvasRight.render()
def changeVectorYPos_Left(e):
    x = (e.x - canvasWIDTH/2)/dvDodai
    y = -(e.y - canvasHEIGHT/2)/dvDodai
    (myCanvasLeft.coSoPhu).matrix[0,1] = x
    (myCanvasLeft.coSoPhu).matrix[1,1] = y
    myCanvasLeft.render()

    myCanvasRight.coSoPhu.matrix = np.linalg.pinv(myCanvasLeft.coSoPhu.matrix) @ np.array([[1,0], [0,1]], dtype=float)
    myCanvasRight.polygon = np.linalg.pinv(myCanvasLeft.coSoPhu.matrix) @ myCanvasLeft.polygon
    myCanvasRight.render()
    

def completeDoiCoSo(e):
    # xoá tất cả event cũ
    myCanvasLeft.canvas.unbind("<Button-1>")
    myCanvasLeft.canvas.unbind("<B1-Motion>")

    myCanvasRight.canvas.unbind("<Button-1>")
    myCanvasRight.canvas.unbind("<B1-Motion>")

    btnDoiCoSo.config(text="Đổi cơ sở")
    btn2.config(state=NORMAL)
    btnDoiCoSo.bind("<Button-1>", setModeDoiCoSo)

btnDoiCoSo.bind("<Button-1>", setModeDoiCoSo)


btn2 = Button( btnsFrame, text="Vẽ đa giác")
btn2.grid(row=0, column=1)
btnsFrame.grid(row=0, column=0, columnspan=2)


def drawPointCanvasLeft(e):
    x = (e.x - canvasWIDTH/2)/dvDodai
    y = -(e.y - canvasHEIGHT/2)/dvDodai
    vt = np.array([[x], [y]], dtype=float)
    myCanvasLeft.polygon = np.hstack( [myCanvasLeft.polygon, vt])
    
    myCanvasLeft.renderPoints()

    vt = np.linalg.pinv(myCanvasLeft.coSoPhu.matrix) @ vt

    myCanvasRight.polygon = np.hstack( [myCanvasRight.polygon, vt])
    myCanvasRight.renderPoints()

    
    
def startDrawPoints(e):
    #vẽ các điểm trước
    btn2.config(text="OK")
    btnDoiCoSo.config(state=DISABLED)

    myCanvasLeft.canvas.bind("<Button-1>", drawPointCanvasLeft)
    myCanvasLeft.polygon = np.array([[],[]], dtype=float)
    myCanvasLeft.render()

    myCanvasRight.polygon = np.array([[],[]], dtype=float)
    myCanvasRight.render()

    btn2.bind("<Button-1>", completeDrawPoints)

def completeDrawPoints(e):
    btn2.config(text="Vẽ đa giác")
    btnDoiCoSo.config(state=NORMAL)

    myCanvasLeft.render()

    #canvasRight
    myCanvasRight.render()


    myCanvasLeft.canvas.unbind("<Button-1>")
    btn2.bind("<Button-1>", startDrawPoints)

btn2.bind("<Button-1>", startDrawPoints)
    
#gia tri vector co the thay doi: True --> x; False --> Y
vectorNeedChangeVal = True

#canvas
class myCanvas:
    def __init__ (self, canvas, coSoPhu, colorHorizontalLine, colorVerticalLine):
        self.canvas = canvas
        self.coSoPhu = coSoPhu #la 1 class nha
        self.colorHorizontalLine = colorHorizontalLine
        self.colorVerticalLine = colorVerticalLine
        self.polygon = np.array([[],[]], dtype=float)
    def render(self):
        self.canvas.delete("all")
        #vẽ đa giác
        self.renderPolygon_Line()

        #đường ngang trung tâm
        self.canvas.create_line(0, canvasHEIGHT/2, canvasWIDTH, canvasHEIGHT/2, fill=self.colorHorizontalLine, width=2)
        x = dvDodai
        while (x <= canvasWIDTH/2):
            self.canvas.create_oval(canvasWIDTH/2 + x - 3, canvasHEIGHT/2 - 3, canvasWIDTH/2 + x + 3, canvasHEIGHT/2 + 3, fill=self.colorHorizontalLine)
            self.canvas.create_oval( canvasWIDTH/2 - x - 3, canvasHEIGHT/2 - 3, canvasWIDTH/2 - x + 3, canvasHEIGHT/2 + 3, fill=self.colorHorizontalLine)
            x += dvDodai
        


        self.canvas.create_line(canvasWIDTH/2, canvasHEIGHT/2, canvasWIDTH/2 + dvDodai, canvasHEIGHT/2, fill=self.colorHorizontalLine, width=4, arrow=LAST)
       
        #đường dọc trung tâm  
        x = dvDodai
        while (x <= canvasHEIGHT/2):
            self.canvas.create_oval(canvasWIDTH/2 - 3, canvasHEIGHT/2 + x - 3, canvasWIDTH/2 + 3, canvasHEIGHT/2 + x + 3, fill=self.colorVerticalLine)
            self.canvas.create_oval( canvasWIDTH/2 - 3, canvasHEIGHT/2 - x - 3, canvasWIDTH/2 + 3, canvasHEIGHT/2 - x + 3, fill=self.colorVerticalLine)
            x += dvDodai
        self.canvas.create_line(canvasWIDTH/2, 0, canvasWIDTH/2, canvasHEIGHT, fill=self.colorVerticalLine, width=2)
        self.canvas.create_line(canvasWIDTH/2, canvasHEIGHT/2, canvasWIDTH/2, canvasHEIGHT/2 - dvDodai, fill=self.colorVerticalLine, width=4, arrow=LAST)
        print(self.coSoPhu.matrix)
        #render coSo

        vtX = (self.coSoPhu).matrix[:,0]
        drawVector_Line(self.canvas, vtX, self.coSoPhu.colorX)

        vtY = (self.coSoPhu).matrix[:,1]
        drawVector_Line(self.canvas, vtY, self.coSoPhu.colorY)
    def renderPoints(self):
        size = np.size( self.polygon, 1)
        if (size != 0):
            cvPolygon = (self.polygon)*dvDodai
            cvPolygon[0, :] = cvPolygon[0, :] + canvasWIDTH/2
            cvPolygon[1, :] = canvasHEIGHT/2 - cvPolygon[1, :]
            for i in range(size):
                x = cvPolygon[0,i]
                y = cvPolygon[1,i]
                self.canvas.create_oval( x - 3, y - 3, x + 3, y + 3, fill="white")
    def renderPolygon_Line(self):
        if (np.size( self.polygon, 1) != 0):
            print("ve da giac")
            
            cvPolygon = (self.polygon)*dvDodai
            cvPolygon[0, :] = cvPolygon[0, :] + canvasWIDTH/2
            cvPolygon[1, :] = canvasHEIGHT/2 - cvPolygon[1, :]
            size = np.size(cvPolygon, 1)
            for index in range(size):
                vt = cvPolygon[:,index]
                self.canvas.create_line(*(vt), vt[0], canvasHEIGHT/2, fill=self.colorVerticalLine, width=1, dash=(3,2))
                self.canvas.create_line(*(vt), canvasWIDTH/2, vt[1], fill=self.colorHorizontalLine, width=1, dash=(3,2))
                #co so phu
                vtPhu = (np.linalg.pinv(self.coSoPhu.matrix) @ self.polygon[:,index])*dvDodai
                A = np.array([vtPhu[0], 0], dtype=float)
                A = transpose(self.coSoPhu.matrix @ (A.transpose()))

                self.canvas.create_line( *(vt), A[0] + canvasWIDTH/2, canvasHEIGHT/2 - A[1], fill=self.coSoPhu.colorX, width=1, dash=(3,2))

                A = np.array([ 0, vtPhu[1]], dtype=float)
                A = transpose(self.coSoPhu.matrix @ (A.transpose()))

                self.canvas.create_line( *(vt), A[0] + canvasWIDTH/2, canvasHEIGHT/2 - A[1], fill=self.coSoPhu.colorY, width=1, dash=(3,2))


            print(cvPolygon)
            self.canvas.create_polygon( *(cvPolygon.transpose().flatten()), fill="white")
    
    #event

 
#canvas 1
canvasLeft = Canvas( tk, background="black", width=canvasWIDTH, height=canvasHEIGHT)
canvasLeft.grid(row=1,column=0, sticky="NEWS")
coSoLeft = CoSo( np.array([[1,0],[0,1]], dtype=float), "orange", "green")
myCanvasLeft = myCanvas( canvasLeft, coSoLeft, "red", "blue")
myCanvasLeft.render()
#ban đầu thì nó sẽ trùng rồi kéo đi đâu đó thì để sau


#canvas 2
canvasRight = Canvas( tk, background="black", width=canvasWIDTH, height=canvasHEIGHT)
canvasRight.grid(row=1,column=1, sticky="NEWS")

#chổ này nhớ sửa
heVectorRight = np.linalg.pinv( coSoLeft.matrix) @ np.array([[1,0], [0,1]], dtype=float)

coSoRight = CoSo( heVectorRight, "red", "blue")

myCanvasRight = myCanvas( canvasRight, coSoRight, "orange", "green")
myCanvasRight.render()


    
tk.mainloop()
#vẽ hệ tọa độ
def mainCoordinate_Grid( canvas):

    #grid tr nha
        #đường ngang ngoài
    ''''i = 1
    while (dvDodai*i <= canvasHEIGHT/2):
        canvas.create_line(0, canvasHEIGHT/2 + dvDodai*i, canvasWIDTH, canvasHEIGHT/2 + dvDodai*i, fill="white", width=1)
        canvas.create_line(0, canvasHEIGHT/2 - dvDodai*i, canvasWIDTH, canvasHEIGHT/2 - dvDodai*i, fill="white", width=1)
        i = i + 1
        #đường dọc
    i = 1
    while (dvDodai*i <= canvasWIDTH/2):
        canvas.create_line(canvasWIDTH/2 + dvDodai*i, 0, canvasWIDTH/2 + dvDodai*i, canvasHEIGHT, fill="white", width=1)
        canvas.create_line(canvasWIDTH/2 - dvDodai*i, 0, canvasWIDTH/2 - dvDodai*i, canvasHEIGHT, fill="white", width=1)
        i = i + 1
    #đường ngang trung tâm
    canvas.create_line(0, canvasHEIGHT/2, canvasWIDTH, canvasHEIGHT/2, fill=colorHorizontalLine, width=2)
    #đường dọc trung tâm  
    canvas.create_line(canvasWIDTH/2, 0, canvasWIDTH/2, canvasHEIGHT, fill=colorVerticalLine, width=2)'''
    #mũi tên tọa độ
    canvas.create_line(canvasWIDTH/2, canvasHEIGHT/2, canvasWIDTH/2 + dvDodai, canvasHEIGHT/2, fill=colorHorizontalLine, width=4, arrow=LAST)
    canvas.create_line(canvasWIDTH/2, canvasHEIGHT/2, canvasWIDTH/2, canvasHEIGHT/2 - dvDodai, fill=colorVerticalLine, width=4, arrow=LAST)