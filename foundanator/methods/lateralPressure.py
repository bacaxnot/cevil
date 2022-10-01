#extermal libraries

#internal libraries
from classes.stressDistribution import *

#resultant methods
class RestMethod:
    '''
    ---
    Primary class of any method to find the lateral resultant of a given soil.

    Arguments:
    - soil: given soil.
    '''
    def __init__(self,  soil : Soil) -> None:
        self.soil = soil;
        pass
    
    @property
    def ko(self):
        for layer in self.soil.layers:
            layer.ko = 1 - np.sin(np.radians(layer.phi));
        pass

    def vStress(self):
        overload = self.soil.overload;
        stress = [[0, overload]];
        for i, layer in enumerate(self.soil.layers):
            #Saturation control
            if layer.saturated:
                value = (layer.gamma - 9.81) * layer.thick;
            else:
                value = layer.gamma * layer.thick;
            #Appending point up and down
            stress.extend(2 * [[stress[2*i][0] + layer.thick, stress[2*i][1] + value]])
        #Remove repeated last element
        stress.pop()
        #Return value
        return np.array(stress)

    def wStress(self):
        stress = [[0, 0]];
        for i, layer in enumerate(self.soil.layers):
            #Saturation control
            if layer.saturated:
                value = 9.81 * layer.thick;
            else:
                value = 0;
            #Appending point up and down
            stress.extend(2 * [[stress[2*i][0] + layer.thick, stress[2*i][1] + value]])         
        #Remove repeated last element
        stress.pop();
        #Return value
        return np.array(stress)

    def hStress(self,   kType = str):
        vStress = self.vStress();
        wStress = self.wStress();
        stress = [];
        #Computing the constant K
        getattr(self, kType)
        #Computing effective horizontal stress + water pressure per layer
        for i, layer in enumerate(self.soil.layers):
            k = getattr(layer, kType);
            topValue =  [vStress[2*i][0], k * vStress[2*i][1] + wStress[2*i][1]];
            botValue =  [vStress[2*i + 1][0], k * vStress[2*i + 1][1] + wStress[2*i + 1][1]];
            stress.extend([topValue, botValue]);
            pass
        #Return value
        return np.array(stress)

    def rest(self):
        stress = self.hStress('ko');
        def resultant():
            return areacoord()
        return stress

    pass

class RankineMethod(RestMethod):
    '''
    ---
    Rankine method to find the lateral resultant of a given soil.

    Arguments:
    - soil: given soil.
    '''
    def __init__(self, soil: Soil) -> None:
        super().__init__(soil)
        self.trial = self.active();
        pass

    @property
    def kp(self):
        for layer in self.soil.layers:
            layer.kp = (1 + np.sin(np.radians(layer.phi)))/(1 - np.sin(np.radians(layer.phi)));
        pass
    
    @property
    def ka(self):
        for layer in self.soil.layers:
            layer.ka = (1 - np.sin(np.radians(layer.phi)))/(1 + np.sin(np.radians(layer.phi)));
        pass

    def passive(self):
        hStress = super().hStress('kp');
        stress = [];
        #Adding cohesive effect
        for i, layer in enumerate(self.soil.layers):
            k = getattr(layer, 'kp');
            c = getattr(layer, 'c');
            topValue =  [hStress[2*i][0], hStress[2*i][1] + 2*np.sqrt(k)*c];
            botValue =  [hStress[2*i + 1][0], hStress[2*i + 1][1] + 2*np.sqrt(k)*c];
            stress.extend([topValue, botValue]);
            pass
        #Return value
        return np.array(stress)

    def active(self):
        hStress = super().hStress('ka');
        stress = [];
        #Adding cohesive effect
        for i, layer in enumerate(self.soil.layers):
            k = getattr(layer, 'ka');
            c = getattr(layer, 'c');
            topValue =  [hStress[2*i][0], hStress[2*i][1] - 2*np.sqrt(k)*c];
            botValue =  [hStress[2*i + 1][0], hStress[2*i + 1][1] - 2*np.sqrt(k)*c];
            stress.extend([topValue, botValue]);
            pass
        #Return value
        return np.array(stress)

class CoulombMethod(RestMethod):
    '''
    ---
    Coulomb method to find the lateral resultant of a given soil.

    Arguments:
    - soil: given soil.
    '''
    def __init__(self, soil: Soil) -> None:
        super().__init__(soil)   
        pass
        