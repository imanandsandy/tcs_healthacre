from privacy.phi_redactor import PHIRedactor


redactor = PHIRedactor()

text = """
Patient John Doe is 45 years old.
His phone number is 9876543210.
He lives in Pune.
His email is john.doe@example.com.
"""


redacted = redactor.redact(text)

print("\nORIGINAL:")
print(text)

print("\nREDACTED:")
print(redacted)