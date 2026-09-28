from llm.soap_generator import SOAPGenerator


generator = SOAPGenerator()

conversation = """
The patient reports fever and cough for the last three days.
The fever is intermittent. The patient also reports a mild headache.
No difficulty in breathing was mentioned.
The doctor advised the patient to drink plenty of fluids
and prescribed paracetamol.
The patient was asked to follow up after three days.
"""

soap_note = generator.generate(conversation)

print("\n========== SOAP NOTE ==========\n")
print(soap_note.model_dump_json(indent=2))