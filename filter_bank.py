from utils import *

def custom_passband(audio_file_name: str, pitch_shift: int = 4, lower_cut: float = 300, higher_cut: float = 2000) -> None:
        """
        This function builds a passband filter to resample the audio file in .wav format and, afterwards, removes the cut-off frequencies of ii.
    """
        if pitch_shift == 0:
            raise ValueError("No! If zero, there is no shift.")
        if audio_file_name[-4:-1].lower() not in '.wav':
            raise Exception("Only .wav files are allowed, surry.")
        
        sample_rate, audio = load_audio(audio_file_name)
        print(f"Length of input audio: {len(audio)}")

        plot_spectrum(audio, sample_rate, title=f"Original Spectrum - {audio_file_name}", name=audio_file_name)

        pitched = pitch_shift_resample(audio, semitones=pitch_shift)
        print(f"Length of pitched audio: {len(pitched)}")
        fir_filtered = apply_fir_bandpass(pitched, sample_rate, lower_cut, higher_cut)
        plot_spectrum(audio, sample_rate, title=f"", name=audio_file_name, stacked=False)
        plot_spectrum(fir_filtered, sample_rate, title=f"FIR Filtered PassBand {int(lower_cut)} Hz, {int(higher_cut)} Hz - {audio_file_name}", name=audio_file_name, stacked=True)
        print(f"Length of fir filtered audio: {len(fir_filtered)}")

        save_audio(f"./fir_filtered_output_wavs/output_robotic_{audio_file_name}.wav", sample_rate, fir_filtered)
        save_audio(f"./custom_passband_wavs/output_cpb_{int(pitch_shift)}_{int(lower_cut)}_{int(higher_cut)}_{audio_file_name}.wav", sample_rate, fir_filtered)
        save_audio(f"./current_output_wavs/output_fir_filtered.wav", sample_rate, fir_filtered)
        
        plot_audio_in_time(audio_ndarray=audio, name=audio_file_name, show=False, extra="original")
        plot_audio_in_time(audio_ndarray=fir_filtered, name=audio_file_name, show=False, extra=f"custom_{int(lower_cut)}_{int(higher_cut)}_{int(pitch_shift)}")

        plot_audio_in_time(audio_ndarray=audio, name=audio_file_name, show=False, extra="original")
        plot_audio_in_time(audio_ndarray=fir_filtered, name=audio_file_name, show=False, extra=f"STACKED_custom_{int(lower_cut)}_{int(higher_cut)}_{int(pitch_shift)}", stack=True)


def robot_rock(audio_file_name: str, pitch_shift: int = 4, lower_cut: float = 300, higher_cut: float = 2000, iir_cut_off: float = 800) -> None:
    """
        This function gets the pitch, passband parameters and IIR cut frequency to roboticize the voice.
    """
    if pitch_shift == 0:
        raise ValueError("No! If zero, there is no shift.")
    if audio_file_name[-4:-1].lower() not in '.wav':
        raise Exception("Only .wav files are allowed, surry.")
    
    sample_rate, audio = load_audio(audio_file_name)

    plot_spectrum(audio, sample_rate, title=f"Original Spectrum - {audio_file_name}", name=audio_file_name)

    pitched = pitch_shift_resample(audio, semitones=pitch_shift)

    fir_filtered = apply_fir_bandpass(pitched, sample_rate, lowcut=lower_cut, highcut=higher_cut)
    plot_spectrum(fir_filtered, sample_rate, title=f"FIR Filtered PassBand {int(lower_cut)} Hz, {int(higher_cut)} Hz - {audio_file_name}", name=audio_file_name)


    robotic = apply_iir_highpass(fir_filtered, sample_rate, iir_cut_off)

    plot_spectrum(robotic, sample_rate, title=f"Robotic IIR HighPass {int(higher_cut)} Hz - Inf - {audio_file_name}", name=audio_file_name)

    save_audio(f"./robotic_output_wavs/output_robotic_{audio_file_name}.wav", sample_rate, robotic)
    save_audio(f"./fir_filtered_output_wavs/output_robotic_{audio_file_name}.wav", sample_rate, fir_filtered)

    
    save_audio(f"./current_output_wavs/output_robotic.wav", sample_rate, robotic)
    save_audio(f"./current_output_wavs/output_fir_filtered.wav", sample_rate, fir_filtered)
