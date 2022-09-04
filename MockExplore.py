class MockExplore:
    def __init__(self, log=False) -> None:
        self.log = log

    def connect(self, device_name):
        if (self.log):
            print("Mock Explore connect:", device_name)
        return

    def record_data(self, file_name, file_type, do_overwrite, block):
        if (self.log):
            print("Mock Explore connect:", file_name,
                  file_type, do_overwrite, block)
        return

    def set_marker(self, code):
        return

    def stop_recording(self):
        if (self.log):
            print("Mock Explore stop recording")
