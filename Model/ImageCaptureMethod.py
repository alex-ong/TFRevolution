from enum import Enum
CaptureMode = Enum('CaptureMode', 'Win32UI mss')
CAPTURE_MODE = CaptureMode.Win32UI
#CAPTURE_MODE = CaptureMode.mss
if CAPTURE_MODE == CaptureMode.Win32UI:
    from Model.ImageCaptureWin32UI import ImageCapture
else:
    from Model.ImageCaptureMSS import ImageCapture
