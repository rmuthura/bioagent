from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez

Entrez.email = "your_email@example.com"  # Replace with your real email

def run_blast(sequence, program="blastp", database="nr", hitlist_size=5):
    """
    Run a BLAST search against NCBI.
    program: blastp for protein, blastn for DNA
    """
    print(f"Running BLAST search... this takes 1-3 minutes")
    
    result_handle = NCBIWWW.qblast(
        program=program,
        database=database,
        sequence=sequence,
        hitlist_size=hitlist_size
    )
    
    blast_records = NCBIXML.parse(result_handle)
    blast_record = next(blast_records)
    
    return blast_record

def parse_blast_results(blast_record):
    """
    Extract the useful information from raw BLAST results
    """
    hits = []
    
    for alignment in blast_record.alignments:
        hsp = alignment.hsps[0]
        
        hit = {
            "title": alignment.title[:200],
            "length": alignment.length,
            "score": hsp.score,
            "evalue": hsp.expect,
            "identities": hsp.identities,
            "positives": hsp.positives,
            "gaps": hsp.gaps,
            "identity_percent": round((hsp.identities / hsp.align_length) * 100, 2),
            "query_sequence": hsp.query[:100],
            "subject_sequence": hsp.sbjct[:100]
        }
        hits.append(hit)
    
    return hits