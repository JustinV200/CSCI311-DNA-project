# --- FILE PARSING ---
def read_fasta(filename):
    """Reads a FASTA file and returns a list of tuples: (header, sequence)."""
    sequences = []
    try:
        with open(filename, 'r') as f:
            header, seq = "", ""
            for line in f:
                line = line.strip()
                if not line: continue
                if line.startswith(">"):
                    if header: sequences.append((header, seq.upper()))
                    header = line[1:] 
                    seq = ""
                else:
                    seq += line 
            if header: sequences.append((header, seq.upper()))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file:\n{e}")
    return sequences
