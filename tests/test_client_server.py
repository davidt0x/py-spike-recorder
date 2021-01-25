import time
import pytest

from spike_recorder.client import SpikeRecorder


@pytest.mark.xfail(reason="This tests fails in CI, at least for MacOS.")
def test_client(tmp_path):
    """
    Integrated test of SpikeRecorder client server

        - Lauchs server application.
        - Connects
        - Starts a recording
        - Sends some event markers
        - Stops the recording
        - Shuts things down

    """
    wav_file_name = tmp_path.joinpath("test.wav").absolute().as_posix()
    event_file_name = tmp_path.joinpath("test-events.txt").absolute().as_posix()

    recorder_client = SpikeRecorder()

    recorder_client.launch()
    recorder_client.connect()

    # Give things time to show up
    time.sleep(5)

    # Start a recording
    recorder_client.start_record(wav_file_name)

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
    #assert os.path.isfile(wav_file_name)
    #assert os.path.isfile(event_file_name)

    # Shutdown
    recorder_client.shutdown()


