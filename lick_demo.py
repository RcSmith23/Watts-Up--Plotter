"""
a line + legend Picker 
Enable picking on the legend to toggle the legended line on and off
"""

import matplotlib.pyplot as plt
from numpy import *

# xy data
t = arange(0.0, 0.5, 0.1)
y1 = 2*sin(2*pi*t)
y2 = 4*sin(2*pi*2*t)
y3 = 0.8+0.2*t

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Click on legend line to toggle line on/off')

# lines 
ax.plot(arange(3),      'g')
ax.plot(t, y1,          'xr', lw=2, picker=5, label='lab1')
ax.plot(arange(3)-3,    'g')
ax.plot(t, y2,          'ob', lw=2, picker=5, label='lab2')
ax.plot(t, y3,          'm', lw=2, picker=5, label='lab3')
ax.plot(arange(3)+3,    'g')
selected, =ax.plot([], [], 'o', ms=12, alpha=0.2, color='red')

# legend
leg = ax.legend(loc='best', numpoints=2, fancybox=True, shadow=True)
lines, labels = ax.get_legend_handles_labels()

# Enable picking on the legend line
leglines=leg.get_lines()
for legline in leglines: legline.set_picker(5)

# legend displays the number of points for each label
texts=leg.get_texts()
for text in texts : 
    lab  = text.get_text()
    line = lines[labels.index(lab)]
    n    = len(line.get_xdata())
    text.set_text(lab + ", " + str(n))

def onpick(event):    
    if event.artist in leg.get_lines(): # Legend Pick
        legline=event.artist
        ax.set_title('legend pick: ' + legline.get_label())
        line = lines[leg.get_lines().index(legline)]
        # toggle line visibility:
        vis = not line.get_visible()
        line.set_visible(vis)
        # by default a line would remain pickable even if not visible : 
        if vis : line.set_picker(5)
        else : line.set_picker(None)
        # Change the alpha on the legend line
        if vis: 
            legline.set_alpha(1.0)
            try: legline._legmarker.set_alpha(1)
            except AttributeError: pass
        else:
            legline.set_alpha(0.2)
            try: legline._legmarker.set_alpha(0.2)
            except AttributeError: pass
    else: # Line Pick 
        selected.set_visible(False)
        thisline = event.artist
        ind      = event.ind
        if len(ind)>1 :
            print "More than 1 point selected, use zoom !", ind
        ind=array([ind[0]])
        xdata = thisline.get_xdata()[ind]
        ydata = thisline.get_ydata()[ind]
        selected.set_data(xdata, ydata)
        selected.set_visible(True)
        ax.set_title('line pick: ' + thisline.get_label())
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', onpick)
plt.show()
