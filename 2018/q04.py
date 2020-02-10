import collections
import dataclasses
import datetime
import enum
import heapq
import re
import util
import math

def parse_record(record_string):
    # First parse all records and sort by date
    events = []
    for line in record_string.split('\n'):
        line = line.rstrip('\n')
        m = re.fullmatch(r"\[(\d+)-(\d\d)-(\d\d)\ (\d\d):(\d\d)] (.*?)", line)
        assert m

        date = datetime.datetime(
            year=int(m[1]),
            month=int(m[2]),
            day=int(m[3]),
            hour=int(m[4]),
            minute=int(m[5]),
        )
        event_string = m[6]
        heapq.heappush(events, (date, event_string))

    # Strategy 1: Find the guard that has the most minutes asleep; what
    # minute does that guard spend asleep the most?
    guard_no = None
    last_slept = None
    slept = collections.defaultdict(lambda: 0)
    slept_minutes = collections.defaultdict(lambda: [0] * 60)

    for (date, event) in events:
        if event == "falls asleep":
            last_slept = date
        elif event == "wakes up":
            assert last_slept
            slept[guard_no] += (date - last_slept).total_seconds() / 60.0

            # Fill in minutes slept?
            # First add date's minutes (not including woken up minute)
            for minute in range(date.minute):
                slept_minutes[guard_no][minute] += 1
            # Add last_slept's minutes
            for minute in range(last_slept.minute, 60):
                slept_minutes[guard_no][minute] += 1
            # Add all the whole hours in between - don't include partial hours
            hours = math.floor((date - last_slept).total_seconds() / 3600.0)
            for minute in range(60):
                slept_minutes[guard_no][minute] += (hours * 60)

        else:
            m = re.fullmatch(r"Guard #(\d+) begins shift", event)
            assert m
            guard_no = m[1]

    slept_the_most = max(slept.keys(), key=lambda guard_no: slept[guard_no])
    most_slept_minute = max(range(60), key=lambda m: slept_minutes[slept_the_most[m]])
    print(f"guard={guard_the_most} min={most_slept_minute}")
    return slept_the_most *  most_slept_minute

parse_record("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""")
