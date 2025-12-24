# core/animation.py
import pygame
import os

class Animation:
    def __init__(self, frames_folder, duration=0.1, scale=1.0, loop=True):
        """
        frames_folder: pasta com os frames PNG
        duration: tempo entre frames
        scale: fator de escala
        loop: se True, animação fica em loop; se False, para no último frame
        """
        self.frames = []
        self.duration = duration
        self.scale = scale
        self.loop = loop
        self.current_frame = 0
        self.timer = 0
        self.finished = False  # ← NOVO
        
        self.load_frames(frames_folder)

    def load_frames(self, folder):
        if not os.path.exists(folder):
            print(f"AVISO: Pasta {folder} não encontrada")
            fallback = pygame.Surface((32, 32))
            fallback.fill((255, 0, 255))
            self.frames.append(fallback)
            return
        
        files = sorted([f for f in os.listdir(folder) if f.endswith('.png')])
        
        if not files:
            print(f"AVISO: Nenhum PNG em {folder}")
            fallback = pygame.Surface((32, 32))
            fallback.fill((255, 0, 255))
            self.frames.append(fallback)
            return
        
        for filename in files:
            filepath = os.path.join(folder, filename)
            try:
                frame = pygame.image.load(filepath).convert_alpha()
                
                if self.scale != 1.0:
                    w, h = frame.get_size()
                    new_w = int(w * self.scale)
                    new_h = int(h * self.scale)
                    frame = pygame.transform.scale(frame, (new_w, new_h))
                
                self.frames.append(frame)
            except Exception as e:
                print(f"AVISO: Erro ao carregar {filepath}: {e}")
        
        if not self.frames:
            fallback = pygame.Surface((32, 32))
            fallback.fill((255, 0, 255))
            self.frames.append(fallback)

    def update(self, dt):
        if len(self.frames) <= 1 or self.finished:
            return
            
        self.timer += dt
        if self.timer >= self.duration:
            self.timer = 0
            self.current_frame += 1
            
            # Se chegou no último frame
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0  # volta ao início
                else:
                    self.current_frame = len(self.frames) - 1  # trava no último
                    self.finished = True  # ← marca como finalizada

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False  # ← NOVO
