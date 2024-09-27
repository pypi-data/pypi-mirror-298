import unittest
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from openSIMS.API import Cameca, Sample, Settings, SHRIMP, Simplex, Toolbox
import openSIMS as S

class Test(unittest.TestCase):

    def loadCamecaData(self):
        S.set('instrument','Cameca')
        S.set('path','data/Cameca_UPb')
        S.read()

    def loadCamecaUPbMethod(self):
        self.loadCamecaData()
        S.method('U-Pb',
                 U='238U',UOx='238U 16O2',
                 Pb204='204Pb',Pb206='206Pb',Pb207='207Pb')

    def setCamecaStandards(self):
        self.loadCamecaUPbMethod()
        S.standards(Plesovice=[0,1,3])

    def test_newCamecaSHRIMPinstance(self):
        cam = Cameca.Cameca_Sample()
        shr = SHRIMP.SHRIMP_Sample()
        self.assertIsInstance(cam,Sample.Sample)
        self.assertIsInstance(cam,Sample.Sample)

    def test_openCamecaASCfile(self):
        samp = Cameca.Cameca_Sample()
        samp.read("data/Cameca_UPb/Plesovice@01.asc")
        self.assertEqual(samp.signal.size,84)
        samp.view(show=False)

    def test_createButDontShowView(self):
        self.loadCamecaData()
        S.view(show=False)

    def test_methodPairing(self):
        self.loadCamecaUPbMethod()
        self.assertEqual(S.get('channels')['UOx'],'238U 16O2')

    def test_setStandards(self):
        self.setCamecaStandards()
        self.assertEqual(S.get('samples').iloc[0].group,'Plesovice')

    def test_settings(self):
        DP = S.settings('U-Pb').get_DP('Plesovice')
        a0 = S.settings('U-Pb').get_a0('Plesovice')
        self.assertEqual(DP,0.05368894845896288)
        self.assertEqual(a0,18.18037)

    def test_cps(self):
        self.loadCamecaUPbMethod()
        Pb206 = S.get('samples')['Plesovice@01'].cps('Pb206')
        self.assertEqual(Pb206.loc[0,'cps'],1981.191294204482)

    def test_process(self):
        self.setCamecaStandards()
        S.process()
        pars = S.get('pars')
        self.assertEqual(pars['b'],0.000375)
        
if __name__ == '__main__':
    unittest.main()
