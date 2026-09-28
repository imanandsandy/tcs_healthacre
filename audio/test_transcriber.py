from audio.transcriber import AudioTranscriber


transcriber = AudioTranscriber("base")

result = transcriber.transcribe("data/test_audio.mp3")

print("\nTRANSCRIPT:")
print(result)