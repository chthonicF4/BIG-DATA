import math

class ThreeVector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def SetXYZ(self, x ,y ,z):
        self.x = x
        self.y = y
        self.z = z

    def print(self):
        print(self.x, self.y, self.z)

    def Mag2(self):
        return ((self.x * self.x) + (self.y * self.y) +  (self.z * self.z))

    def Dot(self, other):
        return (self.x*other.x + self.y*other.y + self.z*other.z)

    def Perp2(self):
        return self.x*self.x + self.y*self.y

    def Perp(self):
        return math.sqrt(self.Perp2())

    def Pt(self):
        return self.Perp()

    def Phi(self):
        if (self.x == 0.0 and self.y == 0.0):
            return 0
        else:
            return math.atan2(self.y, self.x)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return ThreeVector(x,y,z)

class TLorentzVector:
    def __init__(self):
        self.fP = ThreeVector()
        self.fE = 0
        self.pt = 0

    def Px(self):
        return self.fP.x
    def Py(self):
        return self.fP.y
    def Pz(self):
        return self.fP.z
    def E(self):
        return self.fE
    def Vect(self):
        return self.fP

    def SetT(self, t):
        self.fE = t

    def Perp(self):
        return self.fP.Perp()

    def Pt(self):
        return self.Perp()
    
    def Killer(self):
        pass

    def SetXYZT(self,x,y,z,t):
        self.fP.SetXYZ(x, y, z)
        self.SetT(t)

    def SetPxPyPzE(self, px, py, pz, E):
        self.SetXYZT(px, py, pz, E)

    def SetPtEtaPhiE(self, pt, eta, phi, E):
        self.pt = abs(pt)
        self.SetXYZT(self.pt*math.cos(phi), self.pt *math.sin(phi), self.pt*math.sinh(eta), E)

    def Mag2(self):
        return (self.fE * self.fE) - self.fP.Mag2()

    def Mag(self):
        mm = self.Mag2()
        if (mm < 0.0):
            return  -1 * math.sqrt(-1 * mm)
        else:
            return math.sqrt(mm)

    def Phi(self):
        return self.fP.Phi()

    def M(self):
        return self.Mag()

    def Mt(self):
        mm = self.Mt2();
        if (mm < 0.0): 
            return -1 * math.sqrt(-mm)
        else :
            return math.sqrt(mm)

    def Mt2(self):
        return self.E()*self.E() - self.fP.z*self.fP.z

    def __add__(self, other):
        fP = self.fP + other.fP
        E = self.E() + other.E()
        sum = TLorentzVector()
        sum.SetXYZT(fP.x, fP.y, fP.z, E)
        return sum






if __name__ == '__main__':
    myLV = TLorentzVector()
    myT = ThreeVector(1,2,3)
    print(myT.Mag2())
    myT.SetXYZ(3,4,5)
    myT.print()
    print(myLV.SetPtEtaPhiE(4,5,6,7))
    #print('Works')
    print(myLV.M())
    myT2 = ThreeVector(2,4,6)

    myT3 = myT+myT2
    myT3.print()
    print(myLV.Px(), myLV.Py(), myLV.Pz(), myLV.E())

    myLV2 = TLorentzVector()
    myLV3 = TLorentzVector()

    myLV2.SetXYZT(2,3,4,5)
    myLV3.SetXYZT(4,6,8,10)

    myLV4 = myLV2 + myLV3
    print(myLV4.Px(), myLV4.Py(), myLV4.Pz(), myLV4.E())

    myLV5 =  TLorentzVector()
    myLV5.SetPxPyPzE(5,6,7,8)
    print('Pt is {}'.format(myT.Pt()))

    newT = ThreeVector(1,2,3)
    print('Pt is {}'.format(newT.Pt()))
    print('Pt is {}'.format(myLV5.Pt()))
    print(myLV5.Mt())
