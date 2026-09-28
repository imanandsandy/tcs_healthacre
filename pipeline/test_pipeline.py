from pipeline.consultation_pipeline import ConsultationPipeline


pipeline = ConsultationPipeline()

result = pipeline.process_audio(
    "data/test_audio.mp3"
)

print("\n========== RAW TRANSCRIPT ==========")
print(result["transcript"])

print("\n========== REDACTED TRANSCRIPT ==========")
print(result["redacted_transcript"])

print("\n========== SOAP NOTE ==========")

for section, content in result["soap_note"].items():
    print(f"\n{section.upper()}:")
    print(content)