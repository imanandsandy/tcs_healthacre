from fastapi import APIRouter, UploadFile, File, HTTPException
# from privacy.phi_redactor import PHIRedactor
import os
import shutil
from llm.soap_generator import SOAPGenerator
# from audio.transcriber import AudioTranscriber
from audio.transcriber import AudioTranscriber
from privacy.phi_redactor import PHIRedactor


router = APIRouter()
soap_generator = SOAPGenerator()
transcriber = AudioTranscriber("base")
redactor = PHIRedactor()

# router = APIRouter()

# transcriber = AudioTranscriber("base")


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TCS Healthcare AI"
    }


@router.post("/consultation/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...)
):
    try:
        os.makedirs("data/uploads", exist_ok=True)

        file_path = os.path.join(
            "data/uploads",
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = transcriber.transcribe(file_path)

        return {
            "filename": file.filename,
            "transcript": transcript
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.post("/consultation/redact")
async def redact_consultation(
    file: UploadFile = File(...)
):
    try:
        os.makedirs("data/uploads", exist_ok=True)

        file_path = os.path.join(
            "data/uploads",
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Audio → Text
        transcript = transcriber.transcribe(file_path)

        # Text → PHI Redaction
        redacted_transcript = redactor.redact(transcript)

        return {
            "filename": file.filename,
            "transcript": transcript,
            "redacted_transcript": redacted_transcript
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.post("/consultation/process")
async def process_consultation(
    file: UploadFile = File(...)
):
    try:
        os.makedirs("data/uploads", exist_ok=True)

        file_path = os.path.join(
            "data/uploads",
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Audio → Transcript
        transcript = transcriber.transcribe(file_path)

        # 2. Transcript → PHI Redaction
        redacted_transcript = redactor.redact(
            transcript
        )

        # 3. Redacted Transcript → SOAP
        soap_note = soap_generator.generate(
            redacted_transcript
        )

        return {
            "filename": file.filename,
            "redacted_transcript": redacted_transcript,
            "soap_note": soap_note.model_dump()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )