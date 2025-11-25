import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import firwin, lfilter, iirfilter, sosfilt
from scipy.fft import fft, fftfreq, fftshift, ifft

# 1. Carregar arquivo de áudio

def load_audio(path):
    sr, audio = wavfile.read(path)

    # Normalize if integer PCM
    if audio.dtype != np.float32:
        audio = audio / np.max(np.abs(audio))

    # If stereo, convert to mono
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    return sr, audio

# 2. Espectro de Frequência
def plot_spectrum(audio, sample_rate, title: str ="Frequency Spectrum", show: bool = False, name: str = "input", stacked: bool = False) -> None:
    N = len(audio)
    freqs = fftshift(fftfreq(N, 1/sample_rate))
    spectrum = fftshift(np.abs(fft(audio)))
    alpha = 0.7
    if not stacked:
        plt.figure(figsize=(8, 6))
        alpha = 1
    plt.plot(freqs, spectrum, alpha=alpha)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.savefig(f"./current_output_plots/{title}_{name}{'_STACKED' if stacked else ''}.pdf", format="pdf")
    if show:
        plt.show()

# 3. Conversão de Amostragem de Pitch

def pitch_shift_resample(audio, semitones):
    """For pitch shifting, one must alter the semitones on the musical scale. """
    factor = 2 ** (semitones / 12)  # semitone ratio

    N = len(audio)
    new_length = int(N / factor)
    new_audio = np.interp(
        np.linspace(0, N, new_length),
        np.arange(N),
        audio
    )
    return new_audio

# Filtro FIR passa-bandas

def apply_fir_bandpass(audio, sample_rate, low_cut, high_cut, numtaps=1024):
    """
        Creates a FIR filter windowing, letting the audio to be filtered by the generated filter.
    """
    taps = firwin(numtaps, [low_cut, high_cut], pass_zero=False, fs=sample_rate)
    filtered = lfilter(taps, 1.0, audio)
    return filtered


# Filtro IIR passa-altas

def apply_iir_highpass(audio, sample_rate, cut_off_freq):
    sos = iirfilter(
        N=6,
        Wn=cut_off_freq,
        btype='highpass',
        ftype='butter',
        fs=sample_rate,
        output='sos'
    )
    filtered = sosfilt(sos, audio)
    return filtered


# Salvar arquivo de audio

def save_audio(path: str, sample_rate: float, audio):
    audio_norm = audio / np.max(np.abs(audio))  # Normalize audio, not to clip it.
    wavfile.write(path, sample_rate, (audio_norm * 32767).astype(np.int16))


def plot_audio_in_time(audio_ndarray, name: str, show: bool = False, extra: str = '', stack: bool = False) -> None:
    if not stack:
        plt.figure(figsize=(8, 6))
    plt.plot(audio_ndarray)
    plt.xlabel('Samples of Audio Array')
    plt.ylabel('Magnitude')
    plt.title(f'Audio: {name} {extra}')
    plt.grid(True)
    plt.savefig(f"./current_audio_in_time/{name}_{extra}.pdf", format='pdf')
    if show:
        plt.show()
    
