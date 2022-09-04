class MockExplore:
    def __init__(self) -> None:
        pass

    def connect(self, device_name):
        return

    def record_data(self, file_name, file_type, do_overwrite, block):
        return

    def set_marker(self, code):
        return

    def stop_recording(self):
        print("Fake Explore stop recording")
