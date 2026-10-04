import hashlib
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from ai_voice.services import generate_narration, gemini_enabled
from curriculum.models import Exercise

class Command(BaseCommand):
    help = "Gera áudios opcionais de exercícios com cache por hash."
    def handle(self, *args, **options):
        if not gemini_enabled():
            self.stdout.write(self.style.WARNING("Gemini desativado: nenhum áudio foi gerado.")); return
        directory = Path(settings.BASE_DIR) / "static" / "audio"
        directory.mkdir(parents=True, exist_ok=True)
        generated = skipped = 0
        for exercise in Exercise.objects.filter(is_active=True):
            digest = hashlib.sha256(exercise.prompt.encode()).hexdigest()[:16]
            target = directory / f"exercise-{exercise.pk}-{digest}.wav"
            if target.exists(): skipped += 1; continue
            result = generate_narration(exercise.prompt)
            if result.audio:
                target.write_bytes(result.audio); exercise.audio_path = f"audio/{target.name}"; exercise.save(update_fields=["audio_path"]); generated += 1
        self.stdout.write(self.style.SUCCESS(f"Áudios gerados: {generated}; ignorados: {skipped}."))
