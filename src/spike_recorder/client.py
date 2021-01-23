import zmq
import multiprocessing

import logging
logger = logging.getLogger(__name__)

import spike_recorder.server


class SpikeRecorder:
    """
    The main API for launching and controlling the Backyard Brains SpikeRecorder GUI
    applications.
    """

    def __init__(self):
        self.context = zmq.Context()
        self.socket = None

    @staticmethod
    def launch() -> multiprocessing.Process:
        """
        Launch the BackyardBrains SpikeRecorder app. This launches the application
        asynchronously.

        Note: the only way to safely shutdown the process from Python is to subsequently
            connect and shutdown
            >>> spike_client = SpikeRecorder()
            >>> spike_client.launch()
            >>> spike_client.connect()
            >>> spike_client.shutdown()

        Returns:
            The multiprocessing.Process running that the application is running inside.
        """
        return spike_recorder.server.launch(is_async=True)

    def connect(self):
        """
        Connect to an already running BackyardBrains SpikeRecorder GUI application.

        Returns:
            None
        """

        # Launch the SpikeRecorder process

        # Connect to the command server, wait until
        logger.info("Connecting to SpikeRecorder server ...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def shutdown(self):
        """
        Close the SpikeRecorder GUI application completely.

        Returns:
            None
        """
        self._check_server()

        logger.info("Shutting down SpikeRecorder ...")

        # Send the shutdown command
        self._send("shutdown")

    def start_record(self):
        """
        Begin a recording session.

        Returns:
            None
        """
        self._check_server()
        self._send("start")
        logger.info("Recording Started")

    def stop_record(self):
        """
        Stop a recording session. This results in the saving of two files, a WAV file with the
        recorded spike data and a txt file annotating event markers that were generated while
        recording. See Backyard Brains documention for more information:

        https://backyardbrains.com/products/files/SpikeRecorderDocumentation.2018.02.pdf

        Returns:
            None
        """
        self._check_server()
        self._send("stop")
        logger.info("Recording Stopped")

    def push_event_marker(self, marker: str):
        """
        Immediately push an event marker into the recordring. The SpikeRecorder GUI application
        only supports adding markers name 0-9 by pressing the numeric keys on the keyboard. This
        function allows adding markes with arbitrary string literals.

        Args:
            marker: An arbitrary string label to identify this marker.

        Returns:
            None
        """

        self._check_server()

        if marker not in ['stop', 'start', 'shutdown']:
            self._send(marker)
        else:
            raise ValueError(f"Can't send event marker called {marker}, this a reserved value!")

    def _check_server(self):
        """
        Check if the socket has been setup with a connection to the server.

        Returns:

        """
        if not self.socket:
            raise ValueError("SpikeRecorder server connection not setup!")

    def _send(self, command):
        """
        Send a command message to SpikeRecorder GUI application server. This is just a string message
        send to a ZeroMQ socket.

        Args:
            command: The string command to send.

        Returns:
            None
        """

        # FIXME: This should probably be a JSON message or something

        logger.info(f"Sending: {command}")
        self.socket.send(command.encode())

        # Get the reply.
        message = self.socket.recv()
        logger.info(f"Received: {message}")