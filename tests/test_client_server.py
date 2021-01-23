import time

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
    time.sleep(2)

    # Start a recording
    recorder_client.start_record()

    time.sleep(2)

    # Push some event markers
    recorder_client.push_event_marker("Hello")
    time.sleep(2)
    recorder_client.push_event_marker("World!")
    time.sleep(2)

    # Stop recording
    recorder_client.stop_record()

    time.sleep(2)

    # Shutdown
    recorder_client.shutdown()


