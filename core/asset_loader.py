import os
import pygame

class AssetLoader:
    def __init__(self):
        self._images = {}
        self._animations = {}

    def load_image(self, path, scale=None):
        key = (path, scale)
        if key in self._images:
            return self._images[key]
        try:
            img = pygame.image.load(path).convert_alpha()
            if scale:
                # if scale is a float (scale factor), compute new size based on image
                if isinstance(scale, float) or isinstance(scale, int):
                    w, h = img.get_size()
                    new_size = (int(w * float(scale)), int(h * float(scale)))
                elif isinstance(scale, tuple):
                    new_size = scale
                else:
                    new_size = img.get_size()
                img = pygame.transform.smoothscale(img, new_size)
            self._images[key] = img
            return img
        except Exception as e:
            print(f"[AssetLoader] Erro ao carregar imagem {path}: {e}")
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((255, 0, 255, 150))
            self._images[key] = surf
            return surf

    def load_animation(self, dir_path, frame_time, scale=None, loop=True):
        key = (dir_path, frame_time, scale, loop)
        if key in self._animations:
            return self._animations[key]
        try:
            from core.animation import Animation
            anim = Animation(dir_path, frame_time, scale, loop=loop)
            self._animations[key] = anim
            return anim
        except Exception as e:
            # Fallback: carrega todas as imagens do diretório como lista
            frames = []
            try:
                files = sorted(f for f in os.listdir(dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg')))
                for f in files:
                    img = self.load_image(os.path.join(dir_path, f), scale)
                    frames.append(img)
            except Exception as e2:
                print(f"[AssetLoader] Erro fallback animação {dir_path}: {e2}")
            meta = {"frames": frames, "frame_time": frame_time, "loop": loop}
            self._animations[key] = meta
            return meta

# singleton 
loader = AssetLoader()