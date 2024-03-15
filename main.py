import sys
from PyQt6.QtWidgets import QApplication
from tauq_plot_analysis_app import TauqPlotAnalysisApp

def main():
    app = QApplication(sys.argv)
    window = TauqPlotAnalysisApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
