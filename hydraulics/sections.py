#LIBRERIAS EXTERNAS
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from abc import ABC, abstractmethod
#LIBRERIAS PROPIAS

#BASE CLASS
class Section(ABC):
    """
    Abstract class for any kind of Section.
    
    - Primitive Attributes:
        - Depend on class instance.
    - Derivated Attributes:
        - area: Area of the section (A)
        - topWidth: Width of the top of the water in the section (T)
        - wetPerimeter: Wet Perimeter of the section (Pm)
        - hRadius: Hydraulic Radius of the section (Rh)
        - hDepth: Hydraulic Depth of the section (Dh)
    """
    @abstractmethod
    def area(self):
        pass
    @abstractmethod
    def topWidth(self):
        pass
    @abstractmethod
    def wetPerimeter(self):
        pass
    @abstractmethod
    def hRadius(self):
        pass
    @abstractmethod
    def hDepth(self):
        pass

#CLASS INSTANCES
class TrapezoidSection(Section):
    """
    Section class instance for Trapezoidal Section.
    
    - Primitive Attributes:
        - baseWidth: Width of the base of the section (b)
        - wHeigth: Heigth of the water in the section (y)
        - slopeStep: Step of the slope of the section (m)
        - units: System of units used.
    - Derivated Methods:
        - area: Area of the section (A)
        - topWidth: Width of the top of the water in the section (T)
        - wetPerimeter: Wet Perimeter of the section (Pm)
        - hRadius: Hydraulic Radius of the section (Rh)
        - hDepth: Hydraulic Depth of the section (Dh)
    """
    #CONSTRUCTOR
    def __init__(self, b : float,
                       y : float,
                       m : float,
                       units: str = "m") -> "TrapezoidSection":
        self.baseWidth = b;
        self.wHeigth = y;
        self.slopeStep = m;
        self.units = units;
    #PRINCIPAL ATTRIBUTE METHODS
    def area(self, wHeigth : float = False):
        """
        Returns the area of the section.
        """
        b = self.baseWidth;
        y = (self.wHeigth, wHeigth) [bool(wHeigth) == True];
        m = self.slopeStep;
        return y*(m*y + b)
    def topWidth(self, wHeigth : float = False):
        """
        Returns the top width (water surface) of the section.
        """
        b = self.baseWidth;
        y = (self.wHeigth, wHeigth) [bool(wHeigth) == True];
        m = self.slopeStep;
        return 2*m*y + b
    def wetPerimeter(self, wHeigth : float = False):
        """
        Returns the wet perimeter of the section.
        """
        b = self.baseWidth;
        y = (self.wHeigth, wHeigth) [bool(wHeigth) == True];
        m = self.slopeStep;
        return b + 2*y*np.sqrt(1 + m**2)
    def hRadius(self, wHeigth : float = False):
        """
        Returns the hydraulic ratio of the section.
        """
        A = self.area(wHeigth);
        Pm = self.wetPerimeter(wHeigth);
        return A/Pm
    def hDepth(self, wHeigth : float = False):
        """
        Returns the hydraulic depth of the section.
        """
        A = self.area(wHeigth);
        T = self.topWidth(wHeigth);
        return A/T
    #SECONDARY ATTRIBUTE METHODS
    def cDepth(self, Q : float,
                      g : float = 9.81):
        """
        Finds the critical depth of the section with a given flow rate (Q).
        """
        #Variables
        b = self.baseWidth;
        m = self.slopeStep;
        #Function to solve
        f = lambda yc : yc*(b + m*yc) - ( (Q**2/g)*(b + m*yc) )**(1/3)
        #Solve function and return answer
        return fsolve(f, 0.1)[0]
    def alternDepths(self, Q : float,
                           E : float,
                           Inclination : float = 0,
                           Coriolis : float = 1,
                           g : float = 9.81):
        """
        Finds the altern depths of the section with a given flow rate (Q) and specific energy (E)
        """
        #Variables
        m = self.slopeStep;
        b = self.baseWidth;
        cos_omega = np.cos(np.radians(Inclination));
        alpha = Coriolis;
        #Polynomial to solve
        coeff = [2*g**cos_omega*m**2, 2*g*((2*b*m)*cos_omega-(E*m**2)), 2*g*((b**2)*cos_omega-(E*2*b*m)), -2*g*(E*b**2), 0, alpha*Q**2];
        #Solving polynomial and returning answer
        ya = np.roots(coeff)
        return ya[ya>0]
    def specificEnergy(self, Q : float,
                             y : float = False,
                             Inclination : float = 0,
                             Coriolis : float = 1,
                             g : float = 9.81):
        """
        Finds the Specific Energy of the section with a given flow rate (Q) and Water Heigth (y).
        """
        #Variables
        cos_omega = np.cos(np.radians(Inclination));
        alpha = Coriolis;
        y = (self.wHeigth, y) [bool(y) == True];
        #Specific energy in terms of y
        E = lambda y : y*cos_omega + alpha*(Q**2)/(2*g*self.area(y)**2)
        return E(y)
    def flowRate(self, E : float,
                       y : float = False,
                       Inclination : float = 0,
                       Coriolis : float = 1,
                       g : float = 9.81):
        """
        Finds the flow rate (Q) of the section with a given Specific Energy (E).
        """
        #Variables
        cos_omega = np.cos(np.radians(Inclination));
        alpha = Coriolis;
        y = (self.wHeigth, y) [bool(y) == True];
        A = self.area(y);
        #Return value
        return A*np.sqrt((2*g/alpha)*(E - y*cos_omega))
    #NON ATTRIBUTE METHODS
    def setCritical(self, Q : float):
        """
        Sets the Section to the Critical State (Fr = 1) with a given flow rate (Q).
        """
        self.wHeigth = self.cDepth(Q)
    def drawSpecificEnergyCurve(self, Q : float,
                                      Yo : float,
                                      Yf : float,
                                      Step : float = 0.1,
                                      Inclination : float = 0,
                                      Coriolis : float = 1):
        """
        Draws the Specific Energy curve of the Section in the interval [Yo, Yf] with a given flow rate (Q).
        """
        #Discretizing section
        Yplot = np.arange(Yo, Yf, Step);
        Eplot = np.array([self.specificEnergy(Q, yi, Inclination, Coriolis) for yi in Yplot]);
        #Plotting
        plt.plot(Eplot,Yplot)
        plt.title(f"E[{self.units}] vs y[{self.units}]")
        plt.xlabel(f"E [{self.units}]")
        plt.ylabel(f"y [{self.units}]")
        plt.show()
    def drawFlowRateCurve(self, E : float,
                                Yo: float = False,
                                Yf: float = False,
                                Step : float = 0.1,
                                Inclination : float = 0,
                                Coriolis : float = 1):
        """
        Draws the Flow Rate curve of the Section in the interval [Yo, Yf] with a given Specific Energy (E).
        """
        #Discretizing section
        Yplot = np.arange(Yo, Yf, Step);
        Qplot = np.array([self.flowRate(E, yi, Inclination, Coriolis) for yi in Yplot]);
        #Plotting
        plt.plot(Qplot,Yplot)
        plt.title(f"Q[{self.units}^3/s] vs y[{self.units}]")
        plt.xlabel(f"Q [{self.units}^3/s]")
        plt.ylabel(f"y [{self.units}]")
        plt.show()

        

class SquareSection(TrapezoidSection):
    #CONSTRUCTOR
    def __init__(self, b: float,
                       y: float) -> "SquareSection":
        super().__init__(b=b, y=y, m=0)

class TriangleSection(TrapezoidSection):
    #CONSTRUCTOR
    def __init__(self, y: float,
                       m: float) -> "TrapezoidSection":
        super().__init__(b=0, y=y, m=m)

class CircleSection(Section):
    #CONSTRUCTOR
    def __init__(self, d: float,
                       thetha: float = 0,
                       y: float = 0) -> "CircleSection":
        self.diameter = d
        self.wThetha = thetha
        self.wHeigth = y
    #ATTRIBUTES
    @property
    def wThetha(self):
        d = self.diameter;
        y = self.__wHeigth;
        if y:
            self.__wThetha = 2*np.arccos((d - 2*y)/d);
        return self.__wThetha
    @wThetha.setter
    def wThetha(self, thetha):
        self.__wThetha = thetha;    
    @property
    def wHeigth(self):
        d = self.diameter;
        thetha = self.__wThetha;
        if thetha:
            self.__wHeigth = (d/2)*(1 - np.cos(thetha/2));
        return self.__wHeigth
    @wHeigth.setter
    def wHeigth(self, y):
        self.__wHeigth = y;
    @property
    def area(self):
        d = self.diameter;
        thetha = self.wThetha;
        return (d**2)*(thetha - np.sin(thetha))/8
    @property
    def topWidth(self):
        d = self.diameter;
        thetha = self.wThetha;
        return d*np.sin(thetha/2)
    @property
    def wetPerimeter(self):
        d = self.diameter;
        thetha = self.wThetha;
        return thetha*d/2
    @property
    def hRadius(self):
        A = self.area;
        Pm = self.wetPerimeter;
        return A/Pm
    @property
    def hDepth(self):
        A = self.area;
        T = self.topWidth;
        return A/T