from enum import Enum
CaptureMode = Enum('CaptureMode', 'Win32UI mss')
FULL_CAPTURE_MODE = CaptureMode.Win32UI
#CAPTURE_MODE = CaptureMode.mss
FAST_CAPTURE_MODE = CaptureMode.Win32UI
#CAPTURE_MODE = CaptureMode.mss
if FULL_CAPTURE_MODE == CaptureMode.Win32UI:
    from Model.ImageCaptureWin32UI import ImageCapture as FullImageCapture
else:
    from Model.ImageCaptureMSS import ImageCapture as FullImageCapture

if FAST_CAPTURE_MODE == CaptureMode.Win32UI:
    from Model.ImageCaptureWin32UI import ImageCapture as FastImageCapture
else:
    from Model.ImageCaptureMSS import ImageCapture as FastImageCapture