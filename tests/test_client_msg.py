import json
from spike_recorder.client import CommandMsg, CommandType


def test_json_serialize():

    def check_round_trip(msg):
        assert msg == CommandMsg.from_json(msg.to_json())

    check_round_trip(CommandMsg(type=CommandType.SHUTDOWN))
    check_round_trip(CommandMsg(type=CommandType.START_RECORD, args={"filename": "test"}))
    check_round_trip(CommandMsg(type=CommandType.STOP_RECORD))
    check_round_trip(CommandMsg(type=CommandType.PUSH_EVENT_MARKER, args={"name": "test2"}))
    check_round_trip(CommandMsg(type=CommandType.REPLY_OK))
    check_round_trip(CommandMsg(type=CommandType.REPLY_ERROR, args={"what": "blah blah"}))
