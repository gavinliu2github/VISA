#-------------------------------------------------------------------------------
#  Get a screen catpure from TDS2000 series scope and save it to a file

# python        2.7         (http://www.python.org/)
# pyvisa        1.4         (http://pyvisa.sourceforge.net/)
# numpy         1.6.2       (http://numpy.scipy.org/)
# MatPlotLib    1.0.1       (http://matplotlib.sourceforge.net/)
#-------------------------------------------------------------------------------

import visa
import numpy as np
from struct import unpack
import pylab

scope = visa.instrument('USB0::0x0699::0x0369::C101084')

Volts = []
Time = [] # FIXME how to add to empty list?

for chn in [1,2]:
    scope.write('DATA:SOU CH'+str(chn))
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')
    
    
    ymult = float(scope.ask('WFMPRE:YMULT?'))
    yzero = float(scope.ask('WFMPRE:YZERO?'))
    yoff = float(scope.ask('WFMPRE:YOFF?'))
    xincr = float(scope.ask('WFMPRE:XINCR?'))
    
    
    scope.write('CURVE?')
    data = scope.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]
    
    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    
    Volts.append((ADC_wave - yoff) * ymult  + yzero)
    
    Time.append(np.arange(0, xincr * len(ADC_wave), xincr))
    
    
pylab.subplot(2,1,1)
pylab.plot(Time[1], Volts[1])
pylab.subplot(2,1,2)
pylab.plot(Time[0], Volts[0])
pylab.show()
