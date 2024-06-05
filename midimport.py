from cyclopts import App

from pathlib import Path

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


@app.default
def default_action():
    print("Hello world! This runs when no command is specified.")


app()
