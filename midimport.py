from cyclopts import App

from pathlib import Path

import json

import mido

app = App()


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


instrument_map = {
    0: ("Acoustic Grand Piano", "Piano Timbres"),
    1: ("Bright Acoustic Piano", "Piano Timbres"),
    2: ("Electric Grand Piano", "Piano Timbres"),
    3: ("Honky-tonk Piano", "Piano Timbres"),
    4: ("Rhodes Piano", "Piano Timbres"),
    5: ("Chorused Piano", "Piano Timbres"),
    6: ("Harpsichord", "Piano Timbres"),
    7: ("Clavinet", "Piano Timbres"),
    8: ("Celesta", "Chromatic Percussion"),
    9: ("Glockenspiel", "Chromatic Percussion"),
    10: ("Music Box", "Chromatic Percussion"),
    11: ("Vibraphone", "Chromatic Percussion"),
    12: ("Marimba", "Chromatic Percussion"),
    13: ("Xylophone", "Chromatic Percussion"),
    14: ("Tubular Bells", "Chromatic Percussion"),
    15: ("Dulcimer", "Chromatic Percussion"),
    16: ("Hammond Organ", "Organ Timbres"),
    17: ("Percussive Organ", "Organ Timbres"),
    18: ("Rock Organ", "Organ Timbres"),
    19: ("Church Organ", "Organ Timbres"),
    20: ("Reed Organ", "Organ Timbres"),
    21: ("Accordion", "Organ Timbres"),
    22: ("Harmonica", "Organ Timbres"),
    23: ("Tango Accordion", "Organ Timbres"),
    24: ("Acoustic Nylon Guitar", "Guitar Timbres"),
    25: ("Acoustic Steel Guitar", "Guitar Timbres"),
    26: ("Electric Jazz Guitar", "Guitar Timbres"),
    27: ("Electric Clean Guitar", "Guitar Timbres"),
    28: ("Electric Muted Guitar", "Guitar Timbres"),
    29: ("Overdriven Guitar", "Guitar Timbres"),
    30: ("Distortion Guitar", "Guitar Timbres"),
    31: ("Guitar Harmonics", "Guitar Timbres"),
    32: ("Acoustic Bass", "Bass Timbres"),
    33: ("Fingered Electric Bass", "Bass Timbres"),
    34: ("Plucked Electric Bass", "Bass Timbres"),
    35: ("Fretless Bass", "Bass Timbres"),
    36: ("Slap Bass 1", "Bass Timbres"),
    37: ("Slap Bass 2", "Bass Timbres"),
    38: ("Synth Bass 1", "Bass Timbres"),
    39: ("Synth Bass 2", "Bass Timbres"),
    40: ("Violin", "String Timbres"),
    41: ("Viola", "String Timbres"),
    42: ("Cello", "String Timbres"),
    43: ("Contrabass", "String Timbres"),
    44: ("Tremolo Strings", "String Timbres"),
    45: ("Pizzicato Strings", "String Timbres"),
    46: ("Orchestral Harp", "String Timbres"),
    47: ("Timpani", "String Timbres"),
    48: ("String Ensemble 1", "Ensemble Timbres"),
    49: ("String Ensemble 2", "Ensemble Timbres"),
    50: ("Synth Strings 1", "Ensemble Timbres"),
    51: ("Synth Strings 2", "Ensemble Timbres"),
    52: ("Ensemble Timbres", 'Choir "Aah"'),
    53: ("Ensemble Timbres", 'Choir "Ooh"'),
    54: ("Synth Voice", "Ensemble Timbres"),
    55: ("Orchestral Hit", "Ensemble Timbres"),
    56: ("Trumpet", "Brass Timbres"),
    57: ("Trombone", "Brass Timbres"),
    58: ("Tuba", "Brass Timbres"),
    59: ("Muted Trumpet", "Brass Timbres"),
    60: ("French Horn", "Brass Timbres"),
    61: ("Brass Section", "Brass Timbres"),
    62: ("Synth Brass 1", "Brass Timbres"),
    63: ("Synth Brass 2", "Brass Timbres"),
    64: ("Soprano Sax", "Reed Timbres"),
    65: ("Alto Sax", "Reed Timbres"),
    66: ("Tenor Sax", "Reed Timbres"),
    67: ("Baritone Sax", "Reed Timbres"),
    68: ("Oboe", "Reed Timbres"),
    69: ("English Horn", "Reed Timbres"),
    70: ("Bassoon", "Reed Timbres"),
    71: ("Clarinet", "Reed Timbres"),
    72: ("Piccolo", "Pipe Timbres"),
    73: ("Flute", "Pipe Timbres"),
    74: ("Recorder", "Pipe Timbres"),
    75: ("Pan Flute", "Pipe Timbres"),
    76: ("Bottle Blow", "Pipe Timbres"),
    77: ("Shakuhachi", "Pipe Timbres"),
    78: ("Whistle", "Pipe Timbres"),
    79: ("Ocarina", "Pipe Timbres"),
    80: ("Square Wave Lead", "Synth Lead"),
    81: ("Sawtooth Wave Lead", "Synth Lead"),
    82: ("Calliope Lead", "Synth Lead"),
    83: ("Chiff Lead", "Synth Lead"),
    84: ("Charang Lead", "Synth Lead"),
    85: ("Voice Lead", "Synth Lead"),
    86: ("Fifths Lead", "Synth Lead"),
    87: ("Bass Lead", "Synth Lead"),
    88: ("New Age Pad", "Synth Pad"),
    89: ("Warm Pad", "Synth Pad"),
    90: ("Polysynth Pad", "Synth Pad"),
    91: ("Choir Pad", "Synth Pad"),
    92: ("Bowed Pad", "Synth Pad"),
    93: ("Metallic Pad", "Synth Pad"),
    94: ("Halo Pad", "Synth Pad"),
    95: ("Sweep Pad", "Synth Pad"),
    96: ("Rain Effect", "Synth Effects"),
    97: ("Soundtrack Effect", "Synth Effects"),
    98: ("Crystal Effect", "Synth Effects"),
    99: ("Atmosphere Effect", "Synth Effects"),
    100: ("Brightness Effect", "Synth Effects"),
    101: ("Goblins Effect", "Synth Effects"),
    102: ("Echoes Effect", "Synth Effects"),
    103: ("Sci-Fi Effect", "Synth Effects"),
    104: ("Sitar", "Ethnic Timbres"),
    105: ("Banjo", "Ethnic Timbres"),
    106: ("Shamisen", "Ethnic Timbres"),
    107: ("Koto", "Ethnic Timbres"),
    108: ("Kalimba", "Ethnic Timbres"),
    109: ("Bagpipe", "Ethnic Timbres"),
    110: ("Fiddle", "Ethnic Timbres"),
    111: ("Shanai", "Ethnic Timbres"),
    112: ("Tinkle Bell", "Sound Effects"),
    113: ("Agogo", "Sound Effects"),
    114: ("Steel Drums", "Sound Effects"),
    115: ("Woodblock", "Sound Effects"),
    116: ("Taiko Drum", "Sound Effects"),
    117: ("Melodic Tom", "Sound Effects"),
    118: ("Synth Drum", "Sound Effects"),
    119: ("Reverse Cymbal", "Sound Effects"),
    120: ("Guitar Fret Noise", "Sound Effects"),
    121: ("Breath Noise", "Sound Effects"),
    122: ("Seashore", "Sound Effects"),
    123: ("Bird Tweet", "Sound Effects"),
    124: ("Telephone Ring", "Sound Effects"),
    125: ("Helicopter", "Sound Effects"),
    126: ("Applause", "Sound Effects"),
    127: ("Gun Shot", "Sound Effects"),
}


patch_presets = [
    ("Lo-Fi Piano", "FEATURED"),
    ("House Piano", "FEATURED"),
    ("Summer Breeze", "FEATURED"),
    ("Synthwave Chords", "FEATURED"),
    ("Marimba", "FEATURED"),
    ("Reflection Guitar", "FEATURED"),
    ("Log Bass", "FEATURED"),
    ("Wire Bass", "FEATURED"),
    ("Electric Bass", "FEATURED"),
    ("Dancing Strings", "FEATURED"),
    ("Drum Kit", "FEATURED"),
    ("Tokyo Lights", "FUTURE BASS PACK"),
    ("Fresh!", "FUTURE BASS PACK"),
    ("DECORATE", "FUTURE BASS PACK"),
    ("Spring emotion", "FUTURE BASS PACK"),
    ("Tempura", "FUTURE BASS PACK"),
    ("Sequence Saw", "FUTURE BASS PACK"),
    ("Square Synth", "FUTURE BASS PACK"),
    ("Mirai!", "FUTURE BASS PACK"),
    ("Summer Sweat", "FUTURE BASS PACK"),
    ("SK-Pizzicato", "FUTURE BASS PACK"),
    ("Kokoponkon", "FUTURE BASS PACK"),
    ("YM-2800 DAC Piano", "LO-FI PACK"),
    ("Tadpole Piano", "LO-FI PACK"),
    ("MK-939 Piano", "LO-FI PACK"),
    ("Night Market Piano", "LO-FI PACK"),
    ("Crossed Key Matrix", "LO-FI PACK"),
    ("Out-Of-Tune Doorbell", "LO-FI PACK"),
    ("Corroded Melody IC", "LO-FI PACK"),
    ("Low Battery", "LO-FI PACK"),
    ("Hivehole", "LO-FI PACK"),
    ("Enchanted Circuit", "LO-FI PACK"),
    ("Enchanted Wire", "LO-FI PACK"),
    ("Enchanted Lead", "LO-FI PACK"),
    ("PATCH34", "LO-FI PACK"),
    ("Unsettling Bass", "LO-FI PACK"),
]


@app.command
def list_channels(mid_file: Path):
    mid = mido.MidiFile(mid_file, clip=True)
    channels = []
    for msg in mid:
        if msg.type == "program_change":
            channels.append((msg.channel, instrument_map[msg.program]))

    channels.sort()

    print(f"{color.BOLD}{"Channel":<12}{"Instrument":<25}Category{color.END}")
    for channel, (instrument, category) in channels:
        print(f"{channel:<12}{instrument:<25}{category}")


@app.command
def view_patch_presets():
    print(f"{color.BOLD}{"Index":<10}{"Instrument":<25}Category{color.END}")
    for i, (instrument, category) in enumerate(patch_presets):
        print(f"{i:<10}{instrument:<25}{category}")

@app.command
def convert_to_patch(mid_file: Path):
    mid = mido.MidiFile(mid_file, clip=True)
    def roundPartial(value, resolution):
        return round(value / resolution) * resolution


    patterns = []
    prev_tempo = None
    time = 0
    for msg in mid:
        time += msg.time
        if msg.type == "program_change":
            print(msg)
        if msg.type == "set_tempo":
            print(msg)
            print("Tempo set to", msg.tempo)
            bpm = 6e7 / msg.tempo
            if prev_tempo != msg.tempo:
                if prev_tempo is not None:
                    print("TIME", msg.time)
                    length = time * patterns[-1]["bpm"] / 60 / 4
                    print("LENGTH", length)
                    patterns[-1]["time"] = time
                    patterns[-1]["cumulative_time"] = time if len(patterns) <= 1 else time + patterns[-2]["cumulative_time"]
                    patterns[-1]["length"] = roundPartial(length, 0.25)
                    time = 0 # time resets every time tempo changes
                patterns.append({"bpm": bpm})
            print("bpm:", round(bpm, 1))
            prev_tempo = msg.tempo
    else:
        length = time * patterns[-1]["bpm"] / 60 / 4
        print("LENGTH", length)
        patterns[-1]["time"] = time
        patterns[-1]["cumulative_time"] = time if len(patterns) <= 1 else time + patterns[-2]["cumulative_time"]
        patterns[-1]["length"] = roundPartial(length, 0.25)
        print("TIME", time)
        print("length", length)
    print(patterns)
    mid.save(mid_file.with_name(f"{mid_file.stem}_converted.mid"))

    # Initialize lists to store MIDI data and output
    midi_events = []
    outputs = [[]]
    i = 0

    # Extract relevant MIDI events and convert them to dictionaries
    for event in mid:
        midi_events.append(event.dict())

    # Convert delta times to absolute times
    current_time = 0
    for event in midi_events:
        event["time"] += current_time
        current_time = event["time"]

        # Convert note_on events with 0 velocity to note_off events
        if event["type"] == "note_on" and event["velocity"] == 0:
            event["type"] = "note_off"

        # Prepare the event data for output
        event_data = []
        if event["type"] in ["note_on", "note_off"]:
            event_data = [event["type"], event["note"], event["time"], event["channel"]]
            if event["time"] < patterns[i]["cumulative_time"]:
                if i >= 1:
                    event_data[2] -= patterns[i - 1]["cumulative_time"]
                outputs[i].append(event_data)
            else:
                i += 1
                event_data[2] -= patterns[i - 1]["cumulative_time"]
                outputs.append([event_data])
            print("event_data", event_data)

    # Display the processed MIDI events
    for i, output in enumerate(outputs):
        print("Pattern", i)
        for event in output:
            print(event)

    def generate_tracks(output):
        # create a 31-element list of empty lists called "tracks"
        tracks = [[] for _ in range(31)]

        # put all notes in the right track
        for event in output:
            tracks[event[3]].append(event)

        # put all notes in the right order
        for track in tracks:
            track.sort(key=lambda event: event[2])

        # print all tracks
        for track in tracks:
            print(track)
        print()

        return tracks


    tracks_list = []
    for output in outputs:
        tracks_list.append(generate_tracks(output))

    import uuid


    def format_tracks(tracks):
        tracks_with_duration = [[] for _ in range(31)]

        # calculate the duration of each note
        for event in range(len(tracks)):
            for j in range(len(tracks[event])):
                if tracks[event][j][0] == "note_on":
                    for k in range(j, len(tracks[event])):
                        if (
                            tracks[event][k][0] == "note_off"
                            and tracks[event][k][1] == tracks[event][j][1]
                        ):
                            tracks_with_duration[event].append(
                                {
                                    "id": str(uuid.uuid4()),
                                    "pitch": float(tracks[event][j][1]),
                                    "time": tracks[event][j][2],
                                    "duration": round(
                                        (tracks[event][k][2] - tracks[event][j][2])
                                        * bpm
                                        / 60,
                                        4,
                                    ),
                                }
                            )
                            break

        # print all tracks with duration
        for event in tracks_with_duration:
            print(event)
        print()

        return tracks_with_duration


    tracks_with_duration_list = []
    for tracks in tracks_list:
        tracks_with_duration_list.append(format_tracks(tracks))

    total_time = 0
    for msg in mid:
        total_time += msg.time

    print("Total time:", total_time)

    size = round(
        total_time * bpm / 60 / 4
    )  # because 60 seconds in a minute (we use bpm <- minute) and 4 beats in a bar

    print("Size:", size)

    # program_change channel=0 program=36 time=0
    # program_change channel=1 program=0 time=0
    # program_change channel=2 program=32 time=0
    # program_change channel=3 program=0 time=0
    # program_change channel=4 program=81 time=0
    # program_change channel=5 program=80 time=0
    # program_change channel=6 program=81 time=0
    # program_change channel=7 program=42 time=0
    # program_change channel=8 program=64 time=0
    # program_change channel=9 program=0 time=0
    # program_change channel=10 program=64 time=0
    # program_change channel=11 program=64 time=0
    # program_change channel=12 program=64 time=0
    # program_change channel=13 program=64 time=0
    # program_change channel=14 program=64 time=0
    # program_change channel=15 program=64 time=0
    channel_patches = [
        35,
        31,
        30,
        31,
        9,
        80,
        5,
        16,
        11,
        33,
        11,
        11,
        11,
        11,
        11,
        11,
    ]

    res = {
        "value0": {
            "patterns": [
                {
                    "bpm": round(patterns[i]["bpm"], 1),
                    "length": patterns[i]["length"],
                    "name": "",
                    "id": str(uuid.uuid4()),
                    "tracks": tracks_with_duration_list[i],
                }
                for i in range(len(patterns))
            ],
            "channels": [
                {
                    "patch": patch,
                    "atk": 0.0010000000474974514,
                    "rel": 0.12999999523162843,
                    "volume": 1.0,
                    "pan": 0.0,
                    "lp": 20000.0,
                    "tune": 0.0,
                    "soft": True
                }
                for patch in channel_patches
            ]
        }
    }

    # output to song.json
    with open("song.json", "w") as f:
        json.dump(res, f, indent=4)
        


@app.default
def default_action():
    print("Hello world! This runs when no command is specified.")


app()
