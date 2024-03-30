from scipy.io import loadmat


class PlotDataModel:
    def __init__(self):
        self.x_range = (0, 100)
        self.y_range = (0, 100)
        self.autoscale = True
        self.file_path = None
        self.wl = None  # Wavelengths
        self.TriggerTime = None  # Trigger time
        self.t = None  # Time variable
        self.spectra = None  # Spectra data
        self.Ref = None  # Reference spectra
        self.peak = None  # Peak values
        self.IntTime = None  # Integration time
        self.FWHM = None  # Full width at half maximum
        self.Ex = None  # Excitation values
        self.data = None  # Data array
        self.C = None  # Constant or calibration data
        self.Dark_Ref = None  # Dark reference

    def load_data(self, file_path):
        self.file_path = file_path
        data = loadmat(file_path)

        self.wl = data.get('wl', None)
        self.TriggerTime = data.get('TriggerTime', None)
        self.t = data.get('t', None)
        self.spectra = data.get('spectra', None)
        self.Ref = data.get('Ref', None)
        self.peak = data.get('peak', None)
        self.IntTime = data.get('IntTime', None)
        self.FWHM = data.get('FWHM', None)
        self.Ex = data.get('Ex', None)
        self.data = data.get('data', None)
        self.C = data.get('C', None)
        self.Dark_Ref = data.get('Dark_Ref', None)

        # Notify controller or view about data loading completion or update state as necessary
        # This might involve emitting a signal if using PyQt's signal-slot mechanism

    # Additional methods for data processing and manipulation can be added here
