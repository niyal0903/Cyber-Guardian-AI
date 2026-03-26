import os
import time
import logging
import numpy as np
import sounddevice as sd
import soundfile as sf
import librosa
from scipy.spatial.distance import cosine

# ── Logging ──
log = logging.getLogger("VoiceAuth")

# ── Config ──
MASTER_FEAT_FILE = "master_voice_feat.npy"
MASTER_WAV_FILE  = "master_voice.wav"
SAMPLE_RATE      = 22050
DURATION         = 4        # seconds
N_MFCC           = 40       # 13 (Gemini) → 40 (better)
THRESHOLD        = 0.28     # 0.20=strict, 0.28=balanced, 0.35=loose
MAX_ATTEMPTS     = 3        # Failed attempts allowed
LOCKOUT_SEC      = 30       # Lockout duration after max fails


class VoiceAuthenticator:
    """
    Production-grade voice authenticator.
    Gemini ke 13-MFCC se upgrade: 40 MFCC + Delta features.
    """

    def __init__(self):
        self.master_feat  = None
        self.fail_count   = 0
        self.locked_until = 0
        self._load_master()

    # ── Master Feature Load ──
    def _load_master(self):
        if os.path.exists(MASTER_FEAT_FILE):
            self.master_feat = np.load(MASTER_FEAT_FILE)
            log.info("Master voice fingerprint loaded.")
        else:
            log.warning("master_voice_feat.npy not found. Run enroll_voice.py first.")

    # ── Feature Extraction (40 MFCC + Delta) ──
    def _extract_features(self, audio_array=None, file_path=None):
        """
        40 MFCC + Delta = 80-dim feature vector.
        Gemini se 6x more information — better accuracy.
        """
        if audio_array is not None:
            y = audio_array.flatten().astype(np.float32)
        elif file_path:
            y, _ = librosa.load(file_path, sr=SAMPLE_RATE, duration=DURATION)
        else:
            raise ValueError("audio_array ya file_path dena hoga")

        # 40 MFCC
        mfcc  = librosa.feature.mfcc(y=y, sr=SAMPLE_RATE, n_mfcc=N_MFCC)

        # Delta MFCC (rate of change — adds temporal info)
        delta = librosa.feature.delta(mfcc)

        # Combine: mean of each
        feat = np.concatenate([
            np.mean(mfcc.T,  axis=0),
            np.mean(delta.T, axis=0),
        ])
        return feat

    # ── Record Live Audio ──
    def _record(self):
        print("\n  Jarvis: Apni awaaz se verify karein sir...")
        print("  Clearly bolo: 'Jarvis activate secure mode'")
        print("  Recording", end="", flush=True)

        for _ in range(DURATION):
            time.sleep(1)
            print(".", end="", flush=True)

        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        print(" Done.")
        return audio

    # ── Main Authorize ──
    def authorize(self, speaker=None):
        """
        Returns: (bool, str) — (success, message)
        """
        def speak_msg(msg):
            print(f"  Jarvis: {msg}")
            if speaker:
                try:
                    speaker.Speak(msg)
                except Exception:
                    pass

        # ── Lockout check ──
        now = time.time()
        if now < self.locked_until:
            remaining = int(self.locked_until - now)
            msg = f"System locked for {remaining} seconds due to failed attempts."
            speak_msg(msg)
            return False, msg

        # ── Master loaded? ──
        if self.master_feat is None:
            msg = "Master voice not enrolled. Run enroll_voice.py first sir."
            speak_msg(msg)
            return False, msg

        # ── Record + Extract ──
        try:
            audio = self._record()
            live_feat = self._extract_features(audio_array=audio)
        except Exception as e:
            log.error(f"Recording error: {e}")
            return False, f"Recording failed: {e}"

        # ── Compare ──
        score = cosine(self.master_feat, live_feat)
        log.info(f"Voice cosine distance: {score:.4f} (threshold: {THRESHOLD})")

        if score < THRESHOLD:
            # ── SUCCESS ──
            self.fail_count = 0
            msg = "Voice verified. Access granted sir."
            speak_msg(msg)
            return True, msg

        else:
            # ── FAILED ──
            self.fail_count += 1
            remaining_attempts = MAX_ATTEMPTS - self.fail_count

            if self.fail_count >= MAX_ATTEMPTS:
                self.locked_until = time.time() + LOCKOUT_SEC
                self.fail_count   = 0
                msg = (
                    f"Maximum attempts exceeded. "
                    f"System locked for {LOCKOUT_SEC} seconds. "
                    f"Security breach attempt logged."
                )
                speak_msg(msg)
                log.warning("SECURITY: Max voice auth attempts exceeded — lockout triggered")
                return False, msg

            msg = (
                f"Voice mismatch. Score {score:.2f}. "
                f"{remaining_attempts} attempts remaining sir."
            )
            speak_msg(msg)
            return False, msg

    # ── Enroll New Master (runtime) ──
    def re_enroll(self, speaker=None):
        """Runtime mein dobara enroll karo."""
        def speak_msg(msg):
            print(f"  Jarvis: {msg}")
            if speaker:
                try: speaker.Speak(msg)
                except: pass

        speak_msg("Starting voice enrollment. Please say the passphrase 3 times.")

        features = []
        for i in range(3):
            speak_msg(f"Recording {i+1} of 3. Say: Jarvis activate secure mode")
            audio = self._record()
            feat  = self._extract_features(audio_array=audio)
            features.append(feat)
            speak_msg(f"Sample {i+1} captured.")

        # Average
        self.master_feat = np.mean(features, axis=0)
        np.save(MASTER_FEAT_FILE, self.master_feat)
        sf.write(MASTER_WAV_FILE, audio, SAMPLE_RATE)

        speak_msg("Voice enrollment complete. Your voice is now the key sir.")
        log.info("Voice re-enrolled successfully.")
        return True


# ─────────────────────────────────────────────
#  GLOBAL INSTANCE (Jarvis ke liye)
# ─────────────────────────────────────────────

_voice_auth = VoiceAuthenticator()


def verify_voice(speaker=None):
    """Jarvis ke liye simple function."""
    return _voice_auth.authorize(speaker=speaker)


def enroll_voice(speaker=None):
    """Jarvis se voice enroll karo."""
    return _voice_auth.re_enroll(speaker=speaker)


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Voice Auth — Standalone Test")
    print("Pehle enroll karo: python enroll_voice.py")
    success, msg = verify_voice()
    print(f"Result: {success} — {msg}")