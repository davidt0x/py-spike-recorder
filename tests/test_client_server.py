import time
import os

from spike_recorder.client import SpikeRecorder


def test_client():
    """
    Integrated test of SpikeRecorder client server

        - Lauchs server application.
        - Connects
        - Starts a recording
        - Sends some event markers
        - Stops the recording
        - Shuts things down

    """
    recorder_client = SpikeRecorder()

    recorder_client.launch()
    recorder_client.connect()

    # Give things time to show up
    time.sleep(3)

    # Start a recording
    recorder_client.start_record("test.wav")

    time.sleep(3)

    # Push some event markers
    recorder_client.push_event_marker("Hello")
    time.sleep(1)
    recorder_client.push_event_marker("World!")
    time.sleep(3)

    # Stop recording
    recorder_client.stop_record()

    time.sleep(3)

    # Make sure the recording session WAV and events txt is there.
    assert os.path.isfile("test.wav")
    assert os.path.isfile("test-events.txt")

    # Shutdown
    recorder_client.shutdown()


