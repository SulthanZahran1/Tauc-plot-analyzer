from PyQt6.QtWidgets import QApplication
import sys
from PlotAnalysisController import PlotAnalysisController
from PlotAnalysisView import PlotAnalysisView
from PlotDataModel import PlotDataModel


def main():
    app = QApplication(sys.argv)
    model = PlotDataModel()
    view = PlotAnalysisView()
    controller = PlotAnalysisController(model, view)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
