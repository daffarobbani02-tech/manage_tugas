from abc import ABC, abstractmethod


class LayananAIError(Exception):
    """Exception khusus jika komunikasi atau respons layanan AI gagal."""


class LayananAI(ABC):
    """Class induk (abstract) untuk penyedia layanan AI."""

    @abstractmethod
    def kirim_prompt(self, prompt: str) -> str:
        pass


class GeminiAI(LayananAI):
    """Implementasi layanan AI menggunakan Google Gemini API."""

    def __init__(self, api_key: str, model: str = "gemini-3.5-flash-lite"):
        if not api_key or not api_key.strip():
            raise ValueError("API key Gemini tidak boleh kosong.")
        self.__api_key = api_key.strip()  # Encapsulation (private)
        self._model = model

        try:
            from google import genai
        except ImportError as e:
            raise ImportError(
                "Package 'google-genai' belum terpasang. Jalankan: pip install google-genai"
            ) from e

        self._client = genai.Client(api_key=self.__api_key)

    def kirim_prompt(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt tidak boleh kosong.")
        try:
            respons = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
            )
            if not respons.text:
                raise LayananAIError("AI tidak mengembalikan jawaban.")
            return respons.text.strip()
        except LayananAIError:
            raise
        except Exception as e:
            raise LayananAIError(f"Gagal menghubungi Gemini API: {e}") from e


class LayananAIOffline(LayananAI):
    """Cadangan jika API key belum diatur atau sedang offline."""

    def kirim_prompt(self, prompt: str) -> str:
        return (
            "[Mode Offline] API key Gemini belum aktif. "
            "Atur GEMINI_API_KEY di file .env untuk mengaktifkan jawaban AI."
        )