# core/audio_manager.py
import pygame
import os
import struct
import wave
import math
import random


class AudioManager:
    """Gerenciador de áudio do jogo - música de fundo e efeitos sonoros."""

    def __init__(self, music_volume=0.4, sfx_volume=0.6):
        self.music_volume = music_volume
        self.sfx_volume = sfx_volume
        self.sfx = {}
        self.current_music = None

        self.music_dir = os.path.join("assets", "audio", "music")
        self.sfx_dir = os.path.join("assets", "audio", "sfx")

        os.makedirs(self.music_dir, exist_ok=True)
        os.makedirs(self.sfx_dir, exist_ok=True)

        self._ensure_audio_files()
        self._load_sfx()

    # ===================== API PÚBLICA =====================

    def play_music(self, track_name, loops=-1, fade_ms=1000):
        """Toca música de fundo. loops=-1 para loop infinito."""
        if track_name == self.current_music:
            return

        filepath = self._find_file(self.music_dir, track_name)
        if filepath:
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops, fade_ms=fade_ms)
                self.current_music = track_name
            except Exception as e:
                print(f"AVISO: Não foi possível tocar música '{track_name}': {e}")

    def stop_music(self, fade_ms=500):
        """Para a música com fade out."""
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def play_sfx(self, name):
        """Toca um efeito sonoro."""
        if name in self.sfx:
            self.sfx[name].play()

    def set_music_volume(self, volume):
        """Define volume da música (0.0 a 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Define volume dos efeitos sonoros (0.0 a 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sfx.values():
            sound.set_volume(self.sfx_volume)

    # ===================== CARREGAMENTO =====================

    def _find_file(self, directory, name):
        """Busca arquivo de áudio com extensões suportadas."""
        for ext in [".wav", ".ogg", ".mp3"]:
            filepath = os.path.join(directory, f"{name}{ext}")
            if os.path.exists(filepath):
                return filepath
        return None

    def _load_sfx(self):
        """Carrega todos os efeitos sonoros na memória."""
        sfx_names = [
            "attack", "jump", "damage", "enemy_death",
            "key_pickup", "player_death", "level_complete",
        ]
        for name in sfx_names:
            filepath = self._find_file(self.sfx_dir, name)
            if filepath:
                try:
                    self.sfx[name] = pygame.mixer.Sound(filepath)
                    self.sfx[name].set_volume(self.sfx_volume)
                except Exception as e:
                    print(f"AVISO: Não foi possível carregar SFX '{name}': {e}")

    # ===================== GERAÇÃO DE PLACEHOLDERS =====================

    def _ensure_audio_files(self):
        """Gera arquivos de áudio placeholder se não existirem."""
        sfx_generators = {
            "attack": self._gen_attack,
            "jump": self._gen_jump,
            "damage": self._gen_damage,
            "enemy_death": self._gen_enemy_death,
            "key_pickup": self._gen_key_pickup,
            "player_death": self._gen_player_death,
            "level_complete": self._gen_level_complete,
        }

        music_generators = {
            "menu": self._gen_music_menu,
            "gameplay": self._gen_music_gameplay,
            "gameover": self._gen_music_gameover,
            "victory": self._gen_music_victory,
        }

        generated = False

        for name, generator in sfx_generators.items():
            if not self._find_file(self.sfx_dir, name):
                print(f"  Gerando SFX: {name}")
                data = generator()
                self._save_wav(os.path.join(self.sfx_dir, f"{name}.wav"), data)
                generated = True

        for name, generator in music_generators.items():
            if not self._find_file(self.music_dir, name):
                print(f"  Gerando música: {name}")
                data = generator()
                self._save_wav(os.path.join(self.music_dir, f"{name}.wav"), data)
                generated = True

        if generated:
            print("  Áudio placeholder gerado com sucesso!")
            print("  Dica: substitua por arquivos reais em assets/audio/")

    def _save_wav(self, filepath, audio_data, sample_rate=44100):
        """Salva dados de áudio bruto como arquivo WAV mono 16-bit."""
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data)

    @staticmethod
    def _pack_samples(samples_float):
        """Converte lista de floats [-1,1] para bytes PCM 16-bit."""
        return b''.join(
            struct.pack('<h', max(-32768, min(32767, int(s * 32767))))
            for s in samples_float
        )

    def _tone(self, freq, duration, volume=0.3, sr=44100, fade_out=True):
        """Gera tom senoidal simples como lista de floats."""
        n = int(sr * duration)
        samples = []
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - i / n) if fade_out else 1.0
            samples.append(volume * env * math.sin(2 * math.pi * freq * t))
        return samples

    # ---------- Geradores de SFX ----------

    def _gen_attack(self):
        """Swoosh rápido de ataque."""
        sr = 44100
        dur = 0.2
        n = int(sr * dur)
        samples = []
        prev = 0
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - (i / n) ** 0.5)
            raw = random.uniform(-1, 1)
            filtered = 0.6 * prev + 0.4 * raw
            prev = filtered
            freq = 800 - 600 * (i / n)
            tone_val = 0.15 * math.sin(2 * math.pi * freq * t)
            samples.append(env * (0.2 * filtered + tone_val))
        return self._pack_samples(samples)

    def _gen_jump(self):
        """Tom ascendente de pulo."""
        sr = 44100
        dur = 0.2
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - (i / n) ** 0.7)
            freq = 300 + 500 * (i / n)
            samples.append(0.25 * env * math.sin(2 * math.pi * freq * t))
        return self._pack_samples(samples)

    def _gen_damage(self):
        """Som de dano recebido — tom descendente com harmônico."""
        sr = 44100
        dur = 0.3
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - (i / n) ** 0.5)
            freq = 500 - 300 * (i / n)
            val = 0.3 * math.sin(2 * math.pi * freq * t)
            val += 0.1 * math.sin(2 * math.pi * freq * 3 * t)
            samples.append(env * val)
        return self._pack_samples(samples)

    def _gen_enemy_death(self):
        """Burst grave de morte do inimigo."""
        sr = 44100
        dur = 0.35
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            env = max(0.0, 1.0 - (i / n))
            freq = 200 - 120 * (i / n)
            val = 0.3 * math.sin(2 * math.pi * freq * t)
            val += 0.15 * math.sin(2 * math.pi * freq * 2.5 * t)
            samples.append(env * val)
        return self._pack_samples(samples)

    def _gen_key_pickup(self):
        """Três notas ascendentes ao coletar chave (C5-E5-G5)."""
        samples = []
        for freq in [523.25, 659.25, 783.99]:
            samples.extend(self._tone(freq, 0.12, 0.25))
        return self._pack_samples(samples)

    def _gen_player_death(self):
        """Tom longo e descendente de morte do jogador."""
        sr = 44100
        dur = 0.8
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            progress = i / n
            env = max(0.0, 1.0 - progress ** 0.4)
            freq = 450 - 300 * progress
            val = 0.35 * math.sin(2 * math.pi * freq * t)
            val += 0.1 * math.sin(2 * math.pi * (freq * 1.5) * t)
            samples.append(env * val)
        return self._pack_samples(samples)

    def _gen_level_complete(self):
        """Arpejo ascendente de fase completa (C-E-G-C8va)."""
        samples = []
        for freq in [523.25, 659.25, 783.99, 1046.50]:
            dur = 0.15 if freq < 1000 else 0.3
            samples.extend(self._tone(freq, dur, 0.25))
        return self._pack_samples(samples)

    # ---------- Geradores de Música ----------

    def _gen_music_menu(self):
        """Música ambiente calma para o menu (Cm, 10s loop)."""
        sr = 44100
        dur = 10.0
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            val = 0.0
            val += 0.07 * math.sin(2 * math.pi * 130.81 * t)   # C3
            val += 0.05 * math.sin(2 * math.pi * 155.56 * t)   # Eb3
            val += 0.04 * math.sin(2 * math.pi * 196.00 * t)   # G3
            val += 0.03 * math.sin(2 * math.pi * 261.63 * t)   # C4
            # LFO suave — período 5s → 2 ciclos completos em 10s (loop perfeito)
            lfo = 0.4 + 0.6 * math.sin(2 * math.pi * 0.2 * t)
            val *= lfo
            if i < 882:          # micro fade-in (~20 ms)
                val *= i / 882
            samples.append(val)
        return self._pack_samples(samples)

    def _gen_music_gameplay(self):
        """Música rítmica para gameplay (Cm, 110 BPM, 8s loop)."""
        sr = 44100
        dur = 8.0
        n = int(sr * dur)
        bpm = 110
        beat_dur = 60.0 / bpm

        melody = [
            261.63, 293.66, 311.13, 349.23, 392.00, 349.23, 311.13, 293.66,
            261.63, 246.94, 220.00, 246.94, 261.63, 293.66, 311.13, 261.63,
        ]

        samples = []
        for i in range(n):
            t = i / sr
            beat = t / beat_dur
            val = 0.0

            # Baixo (muda a cada 2 beats)
            bass_notes = [130.81, 130.81, 110.00, 116.54]
            bass_idx = int(beat / 2) % len(bass_notes)
            val += 0.08 * math.sin(2 * math.pi * bass_notes[bass_idx] * t)

            # Kick leve a cada beat
            beat_pos = beat % 1.0
            if beat_pos < 0.05:
                kick_env = 1.0 - beat_pos / 0.05
                val += 0.06 * kick_env * math.sin(2 * math.pi * 60 * t)

            # Melodia (muda a cada meio beat)
            mel_idx = int(beat * 2) % len(melody)
            mel_pos = (beat * 2) % 1.0
            if mel_pos < 0.4:
                mel_env = max(0, 1.0 - mel_pos / 0.4)
                val += 0.04 * mel_env * math.sin(2 * math.pi * melody[mel_idx] * t)

            if i < 882:
                val *= i / 882
            samples.append(val)
        return self._pack_samples(samples)

    def _gen_music_gameover(self):
        """Música sombria para game over (Gdim, 8s loop)."""
        sr = 44100
        dur = 8.0
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            val = 0.0
            val += 0.06 * math.sin(2 * math.pi * 98.00 * t)    # G2
            val += 0.05 * math.sin(2 * math.pi * 116.54 * t)   # Bb2
            val += 0.04 * math.sin(2 * math.pi * 138.59 * t)   # Db3
            # LFO — período 8s (1 ciclo completo → loop perfeito)
            lfo = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.125 * t))
            val *= lfo
            if i < 882:
                val *= i / 882
            samples.append(val)
        return self._pack_samples(samples)

    def _gen_music_victory(self):
        """Música triunfante para vitória (Cmaj, 8s loop)."""
        sr = 44100
        dur = 8.0
        n = int(sr * dur)
        samples = []
        for i in range(n):
            t = i / sr
            val = 0.0
            val += 0.07 * math.sin(2 * math.pi * 261.63 * t)   # C4
            val += 0.06 * math.sin(2 * math.pi * 329.63 * t)   # E4
            val += 0.05 * math.sin(2 * math.pi * 392.00 * t)   # G4
            val += 0.04 * math.sin(2 * math.pi * 523.25 * t)   # C5
            # LFO — período 4s (2 ciclos em 8s → loop perfeito)
            lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.25 * t)
            val *= lfo
            if i < 882:
                val *= i / 882
            samples.append(val)
        return self._pack_samples(samples)
