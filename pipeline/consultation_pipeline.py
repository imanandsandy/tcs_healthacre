from audio.transcriber import AudioTranscriber
from privacy.phi_redactor import PHIRedactor
from llm.soap_generator import SOAPGenerator


class ConsultationPipeline:

    def __init__(self):
        self.transcriber = AudioTranscriber("base")
        self.redactor = PHIRedactor()
        self.soap_generator = SOAPGenerator()

    def process_audio(self, audio_path: str) -> dict:

        # 1. Audio → Transcript
        transcript = self.transcriber.transcribe(audio_path)

        # 2. Transcript → PHI Redaction
        redacted_transcript = self.redactor.redact(transcript)

        # 3. Sanitized Transcript → SOAP
        soap_note = self.soap_generator.generate(
            redacted_transcript
        )

        return {
            "transcript": transcript,
            "redacted_transcript": redacted_transcript,
            "soap_note": soap_note.model_dump()
        }