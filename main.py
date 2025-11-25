from filter_bank import robot_rock, custom_passband

AUDIO_NAME: str = 'input.wav'   # Input file to be meddled with. Must be .wav format.
CHOSEN_FILTER: str = 'noisy'

# For custom filtering
PITCH_SHIFT: int = 0.00000001           # If to increase pitch, put positive.
LOWER_CUT: float = 0.000001          # Passband lower_cut
HIGHER_CUT: float = 20000       # Passband higher_cut
IIR_CUT_OFF: float = 0.01       # Highpass lower_cut

filters = ['custom', 'robot', 'high-pitch', 'low-pitch', 'chipmunk', 'muffled', 'noisy']
chosen_filter = CHOSEN_FILTER.lower().strip()

if chosen_filter not in filters:
    raise Exception('No filter identified')

if chosen_filter == 'custom':
    print("------")
    print("Chosen filter: CUSTOM PASSBAND")
    print(f"PITCH SHIFT: {PITCH_SHIFT}, FREQ: [{LOWER_CUT} Hz, {HIGHER_CUT} Hz]")
    custom_passband(audio_file_name=AUDIO_NAME, 
            pitch_shift=PITCH_SHIFT, 
            lower_cut=LOWER_CUT, 
            higher_cut=HIGHER_CUT)
    print("------")

if chosen_filter == 'robot':
    robot_rock(audio_file_name=AUDIO_NAME,
            pitch_shift=4,
            lower_cut=300,
            higher_cut= 3000,
            iir_cut_off=1000)

if chosen_filter == 'muffled':
    print("------")
    print("Chosen filter: MUFFLED (LOW PASS FILTER)")
    print(f"PITCH SHIFT: ~0 Hz, FREQ: [ 0 Hz, 1000 Hz]")
    custom_passband(audio_file_name=AUDIO_NAME,
                    pitch_shift=0.0001,
                    lower_cut=0.00001,
                    higher_cut=1000)
    print("------")

if chosen_filter == 'noisy':
    print("------")
    print("Chosen filter: NOISY (HIGH PASS FILTER)")
    print(f"PITCH SHIFT: ~0 Hz, FREQ: [1500 Hz, INF Hz]")
    custom_passband(audio_file_name=AUDIO_NAME,
                    pitch_shift=0.1,
                    lower_cut=1500,
                    higher_cut=20000)
    print("------")

if chosen_filter == 'low-pitch':
    print("------")
    print("Chosen filter: LOW-PITCH (Interpolation) ")
    print(f"PITCH SHIFT: -7 semitones, FREQ: [~0 Hz, ~5000 Hz]")
    custom_passband(audio_file_name=AUDIO_NAME,
                    pitch_shift=-7,
                    lower_cut=0.1,
                    higher_cut=20000)
    print("------")

if chosen_filter == 'high-pitch':
    print("------")
    print("Chosen filter: HIGH-PITCH (Decimation) ")
    print(f"PITCH SHIFT: +7 semitones, FREQ: [~0 Hz, ~20000 Hz]")
    custom_passband(audio_file_name=AUDIO_NAME,
                    pitch_shift=7,
                    lower_cut=0.1,
                    higher_cut=20000)
    print("------")

if chosen_filter == 'chipmunk':
    print("------")
    print("Chosen filter: CHIPMUNK (Decimation) ")
    print(f"PITCH SHIFT: +12 semitones, FREQ: [~0 Hz, ~20000 Hz]")
    custom_passband(audio_file_name=AUDIO_NAME,
                    pitch_shift=14,
                    lower_cut=0.1,
                    higher_cut=20000)
    print("------")
