from django.test import TestCase, override_settings
from unittest.mock import patch
from .services import generate_narration

class VoiceTests(TestCase):
    @patch.dict("os.environ", {"ENABLE_GEMINI": "False"}, clear=False)
    def test_voice_fails_safely_without_key(self):
        result = generate_narration("Quanto é dois mais dois?")
        self.assertIsNone(result.audio)
        self.assertIsNotNone(result.error)
