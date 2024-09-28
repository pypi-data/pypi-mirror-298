from pathlib import Path
import json


class Event:

    def __init__(self, event_type: str, start_time: float):
        self.event_type = event_type
        self.start_time = start_time
        self.thread_id: int = 0
        self.end_time: float = 0.0
        self.children: list[Event] = []

    def serialize(self):
        return {
            "event_type": self.event_type,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "thread_id": self.thread_id,
            "children": [c.serialize() for c in self.children],
        }

    def __str__(self):
        return json.dumps(self.serialize(), indent=4)


class LogLine:

    def __init__(self, timestamp: float, thread_id: int, message: str):
        self.timestamp = timestamp
        self.message = message
        self.thread_id = thread_id

    def __str__(self):
        return f"{self.timestamp} | {self.thread_id} | {self.message}"


class TraceProcessor:

    def on_log_line(self, line: str) -> LogLine | None:
        if "|" in line and not line.startswith("|"):
            entries = line.split("|")
            if len(entries) != 3:
                return None
            timestamp, thread_id, message = entries
            return LogLine(
                float(timestamp.strip()), int(thread_id.strip()), message.strip()
            )
        return None

    def get_last_event_of_type(self, event_type: str, events):
        for event in reversed(events):
            if event.event_type == event_type:
                return event
        return None

    def process_trace(self, trace_file: Path, trace_config_path: Path):

        log_lines = []
        with open(trace_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                maybe_log_line = self.on_log_line(line)
                if maybe_log_line:
                    log_lines.append(maybe_log_line)

        with open(trace_config_path, "r", encoding="utf-8") as f:
            trace_config = json.load(f)

        events = []
        for log_line in log_lines:
            for event_config in trace_config["event_types"]:
                if log_line.message.startswith(event_config["start_flag"]):
                    events.append(Event(event_config["type"], log_line.timestamp))
                elif log_line.message.startswith(event_config["end_flag"]):
                    last_event = self.get_last_event_of_type(
                        event_config["type"], events
                    )
                    if last_event:
                        last_event.end_time = log_line.timestamp

        return events
