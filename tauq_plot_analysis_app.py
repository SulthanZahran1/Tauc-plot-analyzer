from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMenuBar, QToolBar, QStatusBar, QFileDialog, QGroupBox, QRadioButton, QSlider, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction
from pyqtgraph import PlotWidget, LinearRegionItem
from scipy.io import loadmat
from process_data import runAnalysis


class TauqPlotAnalysisApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tauq Plot Analysis App")
        self.setGeometry(100, 100, 800, 600)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QVBoxLayout()
        self.createMenuBar()
        self.createToolBar()
        self.createStatusBar()
        self.setupUI()
        self.mainWidget.setLayout(self.mainLayout)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePlot)
        self.currentTimeIndex = 0  # To keep track of the current time step in your data
        self.showMaximized()


    def createMenuBar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

    def createToolBar(self):
        toolBar = QToolBar("Main Toolbar")
        self.addToolBar(toolBar)

    def createStatusBar(self):
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.showMessage("Ready")

    def uploadData(self):
        # Open file dialog to select the .mat file
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "MAT Files (*.mat);;All Files (*)")
        if filePath:
            print(f"Selected file: {filePath}")
            # Load data from the selected .mat file
            data = loadmat(filePath)

            # Assign each variable from the .mat file to an attribute of the class
            self.wl = data.get('wl', None)  # Wavelengths
            self.TriggerTime = data.get('TriggerTime', None)  # Trigger time
            self.t = data.get('t', None)  # Time variable
            self.spectra = data.get('spectra', None)  # Spectra data
            self.Ref = data.get('Ref', None)  # Reference spectra
            self.peak = data.get('peak', None)  # Peak values
            self.IntTime = data.get('IntTime', None)  # Integration time
            self.FWHM = data.get('FWHM', None)  # Full width at half maximum
            self.Ex = data.get('Ex', None)  # Excitation values
            self.data = data.get('data', None)  # Data array
            self.C = data.get('C', None)  # Constant or calibration data
            self.Dark_Ref = data.get('Dark_Ref', None)  # Dark reference

            print(f"wl = {self.wl}")
            # Data is now loaded and stored in attributes of your class, ready for use

    def onPlay(self):
        self.timer.start(100)  # Update interval in milliseconds

    def onPause(self):
        self.timer.stop()

    def onStop(self):
        self.timer.stop()
        self.currentTimeIndex = 0
        self.updatePlot()  # To reset the plot

    def onSliderChanged(self, value):
        self.currentTimeIndex = value
        self.updatePlot()

    def updatePlot(self):
        # Update your plot based on self.currentTimeIndex
        # This could involve changing the data source for the plot or updating plot attributes
        # Example: self.plotWidget.plot(new_x_data, new_y_data, clear=True)

        # Optionally, update the slider position
        self.timeSlider.setValue(self.currentTimeIndex)

        # Increment the currentTimeIndex for the next update, ensure it loops or stops at the end
        self.currentTimeIndex += 1
        if self.currentTimeIndex >= self.maxTimeIndex:  # Assuming you have a maximum time index
            self.timer.stop()  # Stop at the last frame
            # Or loop: self.currentTimeIndex = 0

    def onBackward(self):
        self.currentTimeIndex = max(0, self.currentTimeIndex - 1)  # Ensure index doesn't go below 0
        self.updateControls()

    def onForward(self):
        self.currentTimeIndex = min(self.maxTimeIndex, self.currentTimeIndex + 1)  # Ensure index doesn't exceed max
        self.updateControls()

    def regionChangedHandler(self):
        # This function is called when the region is changed.
        region = self.linearRegion.getRegion()
        print(f"Fitting range selected: {region}")

    def setupUI(self):
        # Data Input Section
        dataInputLayout = QHBoxLayout()
        uploadButton = QPushButton("Upload Data")
        uploadButton.clicked.connect(self.uploadData)  # Connect to the placeholder function
        dataInputLayout.addWidget(uploadButton)

        # Plot Configuration Options
        plotConfigLayout = QVBoxLayout()
        scaleGroupBox = QGroupBox("Plot Scale")
        scaleLayout = QHBoxLayout()
        linearScaleRadioButton = QRadioButton("Linear")
        logScaleRadioButton = QRadioButton("Logarithmic")
        scaleLayout.addWidget(linearScaleRadioButton)
        scaleLayout.addWidget(logScaleRadioButton)
        scaleGroupBox.setLayout(scaleLayout)
        plotConfigLayout.addWidget(scaleGroupBox)

        # Analysis Tools
        analysisToolsLayout = QVBoxLayout()
        runAnalysisButton = QPushButton("Run Analysis")
        runAnalysisButton.clicked.connect(runAnalysis)  # Connect to the placeholder function
        analysisToolsLayout.addWidget(runAnalysisButton)

        # Visualization / Output
        visualizationLayout = QVBoxLayout()
        self.plotWidget = PlotWidget()  # Make plotWidget an attribute of the class
        self.plotWidget.setBackground('white')
        self.plotWidget.setXRange(400, 1100)
        self.plotWidget.setYRange(0, 100)
        visualizationLayout.addWidget(self.plotWidget)

        visualizationLayout1 = QVBoxLayout()
        self.plotWidget1 = PlotWidget()  # Make plotWidget an attribute of the class
        self.plotWidget1.setBackground('white')
        self.plotWidget1.setXRange(400, 1100)
        self.plotWidget1.setYRange(0, 100)
        visualizationLayout1.addWidget(self.plotWidget1)

        # Media Player Controls
        controlsLayout = QHBoxLayout()
        self.playButton = QPushButton("Play")
        self.pauseButton = QPushButton("Pause")
        self.stopButton = QPushButton("Stop")
        self.backwardButton = QPushButton("<<")
        self.forwardButton = QPushButton(">>")
        self.timeDisplayLabel = QLabel("0:00 / 0:00")  # Initial time display

        self.playButton.clicked.connect(self.onPlay)
        self.pauseButton.clicked.connect(self.onPause)
        self.stopButton.clicked.connect(self.onStop)

        self.backwardButton.clicked.connect(self.onBackward)
        self.forwardButton.clicked.connect(self.onForward)

        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.pauseButton)
        controlsLayout.addWidget(self.stopButton)

        controlsLayout.addWidget(self.backwardButton)
        # Keep your existing media player controls here
        controlsLayout.addWidget(self.forwardButton)
        controlsLayout.addWidget(self.timeDisplayLabel)

        timemsLayout = QVBoxLayout()
        self.timeSlider = QSlider(Qt.Orientation.Horizontal)
        # self.timeSlider.setMinimumSize(200, 30)
        self.timeSlider.valueChanged.connect(self.onSliderChanged)
        timemsLayout.addWidget(self.timeSlider)

        # Combining Layouts
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(dataInputLayout)
        leftLayout.addLayout(plotConfigLayout)
        leftLayout.addLayout(analysisToolsLayout)
        leftLayout.addLayout(controlsLayout)
        leftLayout.addLayout(timemsLayout)  # Add media player controls to the left layout

        rightLayout = QVBoxLayout()
        rightLayout.addLayout(visualizationLayout)

        righterLayout = QVBoxLayout()
        righterLayout.addLayout(visualizationLayout1)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout, 0.1)
        mainLayout.addLayout(rightLayout, 2)
        mainLayout.addLayout(righterLayout, 2)

        # Create a container widget and set the main layout on it
        containerWidget = QWidget()
        containerWidget.setLayout(mainLayout)

        # Now add the container widget to the existing mainLayout
        self.mainLayout.addWidget(containerWidget)

        # Linear Region Item for range selection on the plot
        self.linearRegion = LinearRegionItem(values=[0.5, 1.5], orientation=LinearRegionItem.Vertical)
        self.plotWidget.addItem(self.linearRegion)
        self.linearRegion.sigRegionChanged.connect(self.regionChangedHandler)
