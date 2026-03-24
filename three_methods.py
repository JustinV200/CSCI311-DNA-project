import tkinter as tk
from tkinter import filedialog, messagebox

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

# --- ALGORITHMS ---
def longest_common_substring(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    longest = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > longest: longest = dp[i][j]
            else:
                dp[i][j] = 0
    return longest

def longest_common_subsequence(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def edit_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0: dp[i][j] = j
            elif j == 0: dp[i][j] = i
            elif s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]


# --- GUI APPLICATION CLASS ---
class DNAMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Sequence Matcher")
        self.root.geometry("600x500")
        self.root.configure(padx=20, pady=20)

        # Variables to store file paths
        self.query_path = tk.StringVar()
        self.db_path = tk.StringVar()
        # Variable to store the selected algorithm (default is 1)
        self.algo_choice = tk.IntVar(value=1)

        self.build_ui()

    def build_ui(self):
        # 1. File Selection Section
        tk.Label(self.root, text="Step 1: Select Files", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Query File
        frame_query = tk.Frame(self.root)
        frame_query.pack(fill="x", pady=5)
        tk.Label(frame_query, text="Query File:", width=12, anchor="w").pack(side="left")
        tk.Entry(frame_query, textvariable=self.query_path, width=40).pack(side="left", padx=5)
        tk.Button(frame_query, text="Browse", command=self.browse_query).pack(side="left")

        # Database File
        frame_db = tk.Frame(self.root)
        frame_db.pack(fill="x", pady=5)
        tk.Label(frame_db, text="Database File:", width=12, anchor="w").pack(side="left")
        tk.Entry(frame_db, textvariable=self.db_path, width=40).pack(side="left", padx=5)
        tk.Button(frame_db, text="Browse", command=self.browse_db).pack(side="left")

        # 2. Algorithm Selection Section
        tk.Label(self.root, text="Step 2: Select Algorithm", font=("Arial", 14, "bold")).pack(anchor="w", pady=(20, 10))
        
        tk.Radiobutton(self.root, text="1. Longest Common Substring", variable=self.algo_choice, value=1).pack(anchor="w")
        tk.Radiobutton(self.root, text="2. Longest Common Subsequence (LCS)", variable=self.algo_choice, value=2).pack(anchor="w")
        tk.Radiobutton(self.root, text="3. Edit Distance", variable=self.algo_choice, value=3).pack(anchor="w")

        # 3. Run Button
        tk.Button(self.root, text="Run Matching Algorithm", bg="green", fg="white", font=("Arial", 12, "bold"), 
                  command=self.run_matching).pack(pady=20, fill="x")

        # 4. Results Section
        tk.Label(self.root, text="Results:", font=("Arial", 14, "bold")).pack(anchor="w")
        self.result_text = tk.Text(self.root, height=6, width=60, state="disabled", bg="#f0f0f0")
        self.result_text.pack(fill="both", expand=True)

    def browse_query(self):
        filepath = filedialog.askopenfilename(title="Select Query FASTA/TXT File")
        if filepath:
            self.query_path.set(filepath)

    def browse_db(self):
        filepath = filedialog.askopenfilename(title="Select Database FASTA/TXT File")
        if filepath:
            self.db_path.set(filepath)

    def log_result(self, message):
        """Helper to print text to the GUI text box."""
        self.result_text.configure(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.configure(state="disabled")

    def run_matching(self):
        q_file = self.query_path.get()
        db_file = self.db_path.get()

        if not q_file or not db_file:
            messagebox.showwarning("Missing Files", "Please select both a Query and Database file.")
            return

        self.log_result("Loading files and calculating... Please wait.")
        self.root.update() # Force UI to update before heavy math starts

        query_data = read_fasta(q_file)
        db_data = read_fasta(db_file)

        if not query_data or not db_data:
            self.log_result("Error: One or both files are empty or invalid.")
            return

        query_header, query_seq = query_data[0]
        choice = self.algo_choice.get()

        best_header = ""
        best_score = -1 if choice in [1, 2] else float('inf')

        # Run the comparison against the whole database
        for db_header, db_seq in db_data:
            if choice == 1:
                score = longest_common_substring(db_seq, query_seq)
                if score > best_score:
                    best_score = score
                    best_header = db_header
            elif choice == 2:
                score = longest_common_subsequence(db_seq, query_seq)
                if score > best_score:
                    best_score = score
                    best_header = db_header
            elif choice == 3:
                score = edit_distance(db_seq, query_seq)
                if score < best_score:
                    best_score = score
                    best_header = db_header

        # Format the final output
        result_msg = "--- ANALYSIS COMPLETE ---\n"
        result_msg += f"Algorithm: {['Longest Common Substring', 'Longest Common Subsequence', 'Edit Distance'][choice-1]}\n"
        result_msg += f"Best Match: {best_header}\n"
        
        if choice in [1, 2]:
            result_msg += f"Score: {best_score} matching characters\n"
        else:
            result_msg += f"Edit Distance: {best_score} operations (lower is better)\n"

        self.log_result(result_msg)

# --- START THE APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DNAMatcherApp(root)
    root.mainloop()