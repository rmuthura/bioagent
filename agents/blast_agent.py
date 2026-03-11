from utils.blast_utils import run_blast, parse_blast_results
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def blast_agent(sequence, sequence_type="protein"):
    """
    Agent that runs BLAST and interprets results using LLM
    """
    # Step 1 - Run BLAST
    program = "blastp" if sequence_type == "protein" else "blastn"
    database = "nr" if sequence_type == "protein" else "nt"
    
    blast_record = run_blast(sequence, program=program, database=database)
    hits = parse_blast_results(blast_record)
    
    if not hits:
        return {"hits": [], "interpretation": "No significant BLAST hits found."}
    
    # Step 2 - Format hits for LLM
    hits_text = ""
    for i, hit in enumerate(hits, 1):
        hits_text += f"""
Hit {i}:
- Match: {hit['title']}
- Identity: {hit['identity_percent']}%
- E-value: {hit['evalue']}
- Score: {hit['score']}
"""

    # Step 3 - LLM interpretation
    prompt = f"""
You are an expert bioinformatician analyzing BLAST search results.

Sequence type: {sequence_type}
Query sequence: {sequence[:100]}...

BLAST Results:
{hits_text}

Please provide:
1. What this sequence most likely is
2. Its probable biological function
3. How confident we should be based on the E-values and identity percentages
4. Any notable observations about the hits
5. Recommended next steps for further analysis

Write clearly for a scientist who understands biology but wants a concise summary.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system", 
                "content": "You are an expert bioinformatician providing clear, accurate analysis of biological sequence data."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        temperature=0.3
    )
    
    interpretation = response.choices[0].message.content
    
    return {
        "hits": hits,
        "interpretation": interpretation
    }