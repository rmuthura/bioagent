from agents.blast_agent import blast_agent

# Test protein sequence - this is human insulin
test_sequence = "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"

print("Starting BioAgent analysis...")
print("=" * 50)

results = blast_agent(test_sequence, sequence_type="protein")

print("\nTop BLAST Hits:")
print("-" * 30)
for i, hit in enumerate(results["hits"], 1):
    print(f"{i}. {hit['title'][:80]}")
    print(f"   Identity: {hit['identity_percent']}% | E-value: {hit['evalue']}")

print("\nAI Interpretation:")
print("-" * 30)
print(results["interpretation"])