import time
import zfused_maya.widgets.progresswidget as progresswidget



ui = progresswidget.ProgressWidget()
ui.show()



#ui.close()

for i in range(101):
    time.sleep(0.1)
    a += i
    
    progresswidget.ProgressWidget.PROGRESS_LOGGER["model file"].set_value(i)
    #ui.setValue(i)
    ui.repaint()