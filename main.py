import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import nltk
import spacy
import threading
import traceback
import re

class WitnessValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Witness Statement Validator")
        self.root.geometry("800x700")
        
        # Header
        self.header = tk.Label(root, text="Witness Statement Validator", font=('Arial', 16, 'bold'))
        self.header.pack(pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(root, text="Statement Input")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.label = tk.Label(input_frame, text="Enter Witness Statement:", font=('Arial', 12))
        self.label.pack(pady=5, anchor="w", padx=10)
        
        self.text_input = tk.Text(input_frame, height=8, font=("Arial", 12))
        self.text_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.validate_btn = ttk.Button(btn_frame, text="Validate Statement", command=self.validate)
        self.validate_btn.pack(side="left", padx=5)
        self.validate_btn.config(state="disabled")  # Disable until resources are loaded
        
        self.clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left", padx=5)
        
        self.save_btn = ttk.Button(btn_frame, text="Save Results", command=self.save_results)
        self.save_btn.pack(side="left", padx=5)
        
        # Status indicator
        self.status_var = tk.StringVar()
        self.status_var.set("Initializing NLP resources...")
        self.status = ttk.Label(btn_frame, textvariable=self.status_var, font=('Arial', 10, 'italic'))
        self.status.pack(side="right", padx=10)
        
        # Output section with tabs
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Analysis tab
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Analysis")
        
        analysis_scroll = ttk.Scrollbar(analysis_frame, orient="vertical")
        self.output = tk.Text(analysis_frame, height=20, font=("Courier", 10), wrap="word",
                              yscrollcommand=analysis_scroll.set)
        
        analysis_scroll.config(command=self.output.yview)
        analysis_scroll.pack(side="right", fill="y")
        self.output.pack(side="left", fill="both", expand=True)
        
        # Verdict tab
        verdict_frame = ttk.Frame(notebook)
        notebook.add(verdict_frame, text="Verdict")
        
        verdict_scroll = ttk.Scrollbar(verdict_frame, orient="vertical")
        self.verdict_output = tk.Text(verdict_frame, height=20, font=("Arial", 12), wrap="word",
                                     yscrollcommand=verdict_scroll.set)
        
        verdict_scroll.config(command=self.verdict_output.yview)
        verdict_scroll.pack(side="right", fill="y")
        self.verdict_output.pack(side="left", fill="both", expand=True)
        
        # Setup complete flag
        self.setup_complete = False
        
        # Load spaCy in a background thread
        self.load_thread = threading.Thread(target=self.load_resources)
        self.load_thread.daemon = True
        self.load_thread.start()
        
        # Check loading status periodically
        self.root.after(100, self.check_loading)

    def load_resources(self):
        """Load spaCy model"""
        try:
            global nlp
            nlp = spacy.load("en_core_web_sm")
            
            # Download wordnet if needed for WSD
            try:
                nltk.download('wordnet')
                nltk.download('omw-1.4')
            except:
                pass  # Continue even if wordnet download fails
                
            self.setup_complete = True
        except Exception as e:
            print(f"Error loading resources: {e}")
            self.status_var.set("Error loading spaCy model")
            messagebox.showerror("Resource Error", 
                               f"Failed to load NLP resources.\n"
                               f"Error: {str(e)}\n\n"
                               f"Please install spaCy model manually:\n"
                               f"python -m spacy download en_core_web_sm")

    def check_loading(self):
        """Check if loading is complete"""
        if self.setup_complete:
            self.status_var.set("Ready")
            self.validate_btn.config(state="normal")
        else:
            self.root.after(100, self.check_loading)

    def clear(self):
        """Clear input and output fields"""
        self.text_input.delete("1.0", "end")
        self.output.delete("1.0", "end")
        self.verdict_output.delete("1.0", "end")

    def save_results(self):
        """Save analysis results to file"""
        if not self.output.get("1.0", "end-1c").strip():
            messagebox.showinfo("Nothing to Save", "Please analyze a statement first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=== ANALYSIS ===\n\n")
                f.write(self.output.get("1.0", "end-1c"))
                f.write("\n\n=== VERDICT ===\n\n")
                f.write(self.verdict_output.get("1.0", "end-1c"))
            messagebox.showinfo("Success", f"Results saved to {file_path}")

    def validate(self):
        """Validate and analyze the witness statement"""
        if not self.setup_complete:
            messagebox.showwarning("Not Ready", "Still loading NLP resources. Please wait.")
            return
            
        statement = self.text_input.get("1.0", "end-1c").strip()
        if not statement:
            messagebox.showwarning("Empty Input", "Please enter a witness statement.")
            return

        try:
            self.status_var.set("Analyzing...")
            self.output.delete("1.0", "end")
            self.verdict_output.delete("1.0", "end")
            self.root.update()
            
            # Process with spaCy
            doc = nlp(statement)
            
            # POS Tagging using spaCy
            self.output.insert("end", "====== POS TAGGING ======\n")
            self.output.insert("end", "Shows the part of speech for each word\n\n")
            for token in doc:
                self.output.insert("end", f"{token.text}: {token.pos_}\n")
            
            # Bigrams using spaCy
            self.output.insert("end", "\n====== BIGRAMS ======\n")
            self.output.insert("end", "Shows pairs of adjacent words\n\n")
            tokens = [token.text for token in doc]
            for i in range(len(tokens)-1):
                self.output.insert("end", f"({tokens[i]}, {tokens[i+1]})\n")
            
            # Word Sense Analysis (simplified)
            self.output.insert("end", "\n====== WORD SENSE ANALYSIS ======\n")
            self.output.insert("end", "Shows key words with their context\n\n")
            for token in doc:
                if token.pos_ in ['NOUN', 'VERB', 'ADJ'] and len(token.text) > 3:
                    context = ' '.join([t.text for t in token.lefts]) + ' ' + token.text + ' ' + ' '.join([t.text for t in token.rights])
                    context = context.strip()
                    self.output.insert("end", f"{token.text} ({token.pos_}): {context}\n")
            
            # Syntactic Parsing
            self.output.insert("end", "\n====== SYNTACTIC PARSING ======\n")
            self.output.insert("end", "Shows the grammatical structure of the sentence\n\n")
            for token in doc:
                self.output.insert("end", f"{token.text} → {token.dep_} → {token.head.text}\n")
            
            # Morphological Analysis
            self.output.insert("end", "\n====== MORPHOLOGICAL ANALYSIS ======\n")
            self.output.insert("end", "Shows detailed grammatical properties of each word\n\n")
            for token in doc:
                self.output.insert("end", f"{token.text}: Lemma={token.lemma_}, POS={token.pos_}, Tag={token.tag_}, Dependency={token.dep_}\n")
                
            # Named Entity Recognition
            self.output.insert("end", "\n====== NAMED ENTITIES ======\n")
            self.output.insert("end", "Identifies people, places, organizations, etc.\n\n")
            for ent in doc.ents:
                self.output.insert("end", f"{ent.text}: {ent.label_}\n")
            
            # Generate suspicion verdict
            self.generate_verdict(doc, statement)
            
            self.status_var.set("Analysis complete")

        except Exception as e:
            self.status_var.set("Error occurred")
            error_msg = f"An error occurred:\n{str(e)}\n\n{traceback.format_exc()}"
            self.output.delete("1.0", "end")
            self.output.insert("end", error_msg)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def generate_verdict(self, doc, statement):
        """Generate a suspicion verdict based on linguistic analysis without hardcoded word lists"""
        # Initialize suspicion indicators
        suspicion_indicators = []
        raw_score = 0
        
        # Set the maximum possible raw score to normalize against
        MAX_RAW_SCORE = 100
        NORMALIZED_MAX = 50  # We want to normalize to a scale of 0-50
        
        # 1. Check for hedging language and uncertainty markers using POS and dependency patterns
        modal_verbs = sum(1 for token in doc if token.tag_ == "MD")  # Modal verbs like might, could
        adverbs_of_doubt = sum(1 for token in doc if token.pos_ == "ADV" and 
                            token.lemma_ in nlp.vocab and 
                            any(t in token.text.lower() for t in ["ly", "ably", "ibly"]))
        hedging_count = modal_verbs + adverbs_of_doubt
        
        if hedging_count >= 2:
            suspicion_indicators.append(f"High uncertainty detected ({hedging_count} hedging phrases/modal verbs)")
            raw_score += min(hedging_count * 5, 15)  # Cap at 15 points
        
        # 2. Check for contradictions using dependency parsing
        # Look for coordinating conjunctions (but, however) and clausal relationships
        conjunctions = sum(1 for token in doc if token.dep_ in ["cc", "conj"] and 
                        token.head.pos_ in ["VERB", "ADJ"])
        if conjunctions >= 2:
            suspicion_indicators.append(f"Potential contradictory structures detected ({conjunctions} contrasting conjunctions)")
            raw_score += min(conjunctions * 5, 15)  # Cap at 15 points
        
        # 3. Check for passive voice using dependency parsing
        passive_constructions = sum(1 for token in doc if "pass" in token.dep_)
        if passive_constructions >= 1:
            suspicion_indicators.append(f"Use of passive voice detected ({passive_constructions} instances)")
            raw_score += min(passive_constructions * 5, 10)  # Cap at 10 points
        
        # 4. Check for vague language using entity recognition and word vectors
        concrete_entities = len(doc.ents)  # Named entities are concrete references
        pronouns = sum(1 for token in doc if token.pos_ == "PRON")  # Pronouns can be vague references
        
        vagueness_ratio = pronouns / max(1, len(doc) - pronouns)
        if vagueness_ratio > 0.3 and pronouns > 3:  # More than 30% pronouns
            suspicion_indicators.append(f"High use of vague references ({pronouns} pronouns, low named entities)")
            raw_score += min(int(vagueness_ratio * 20), 15)  # Cap at 15 points
        
        # 5. Check sentence complexity using syntactic parsing
        clause_markers = sum(1 for token in doc if token.dep_ in ["ccomp", "xcomp", "advcl", "acl"])
        avg_words_per_sentence = len([token for token in doc if not token.is_punct]) / max(1, len(list(doc.sents)))
        
        complexity_score = clause_markers + (1 if avg_words_per_sentence > 25 else 0)
        if complexity_score >= 3:
            suspicion_indicators.append(f"Overly complex sentence structure ({clause_markers} dependent clauses)")
            raw_score += min(complexity_score * 3, 10)  # Cap at 10 points
        
        # 6. Check for negations using dependency parsing
        negation_count = sum(1 for token in doc if token.dep_ == "neg" or "Neg" in token.dep_)
        if negation_count >= 2:
            suspicion_indicators.append(f"High use of negations ({negation_count} instances)")
            raw_score += min(negation_count * 3, 10)  # Cap at 10 points
        
        # 7. Check for temporal discontinuities using POS tagging and dependencies
        temporal_markers = sum(1 for token in doc if 
                        (token.pos_ == "ADV" and token.dep_ == "advmod" and token.head.pos_ == "VERB") or
                        token.ent_type_ == "DATE" or token.ent_type_ == "TIME")
        
        temporal_shifts = 0
        prev_tense = None
        for token in doc:
            if token.pos_ == "VERB":
                current_tense = token.tag_[:2]  # Extract tense info from tag
                if prev_tense and current_tense != prev_tense:
                    temporal_shifts += 1
                prev_tense = current_tense
        
        if temporal_shifts >= 2 or temporal_markers >= 4:
            suspicion_indicators.append(f"Temporal discontinuities detected ({temporal_shifts} tense shifts, {temporal_markers} time markers)")
            raw_score += min((temporal_shifts + temporal_markers) * 2, 10)  # Cap at 10 points
        
        # 8. Check level of detail (ratio of descriptive words)
        descriptors = sum(1 for token in doc if token.pos_ in ["ADJ", "ADV"])
        descriptor_ratio = descriptors / max(1, len([t for t in doc if not t.is_punct]))
        
        if descriptor_ratio > 0.25:  # More than 25% of words are descriptive
            suspicion_indicators.append(f"Unusually high level of descriptive detail ({descriptors} descriptors, {descriptor_ratio:.1%} of text)")
            raw_score += min(int(descriptor_ratio * 40), 15)  # Cap at 15 points
        
        # Normalize the score to 0-50 scale
        normalized_score = min(int((raw_score / MAX_RAW_SCORE) * NORMALIZED_MAX), NORMALIZED_MAX)
        
        # Calculate final verdict based on normalized score
        if normalized_score >= 30:
            verdict = "HIGHLY SUSPICIOUS"
            color = "red"
        elif normalized_score >= 20:
            verdict = "MODERATELY SUSPICIOUS"
            color = "orange"
        elif normalized_score >= 11:
            verdict = "SLIGHTLY SUSPICIOUS" 
            color = "blue"
        else:
            verdict = "NO SUSPICION DETECTED"
            color = "green"
        
        # Display verdict
        self.verdict_output.tag_config("verdict", foreground="white", background=color, font=("Arial", 14, "bold"))
        self.verdict_output.tag_config("heading", font=("Arial", 22, "bold"))
        self.verdict_output.tag_config("normal", font=("Arial", 18))
        
        self.verdict_output.insert("end", f"\n   {verdict}   \n\n", "verdict")
        self.verdict_output.insert("end", f"Suspicion Score: {normalized_score}/50\n\n", "heading")
        
        if suspicion_indicators:
            self.verdict_output.insert("end", "Key Indicators:\n", "heading")
            for i, indicator in enumerate(suspicion_indicators, 1):
                self.verdict_output.insert("end", f"{i}. {indicator}\n", "normal")
        else:
            self.verdict_output.insert("end", "No significant linguistic markers of deception detected.\n", "normal")
        
        # Add analysis explanation
        self.verdict_output.insert("end", "\nAnalysis Explanation:\n", "heading")
        self.verdict_output.insert("end", 
            "This verdict is based on linguistic analysis of deception markers including: " +
            "uncertainty markers, contradictions, passive voice, vague references, " +
            "sentence complexity, negations, temporal discontinuities, and level of detail.\n\n" +
            "Higher scores indicate more linguistic patterns typically associated with deceptive statements. " +
            "This is an automated analysis and should be considered as one factor in a complete evaluation.\n", "normal")

        # For short statements
        if len(doc) < 20:
            self.verdict_output.insert("end", "\nNote: Statement is quite short. Analysis may be limited.\n", "normal")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = WitnessValidatorApp(root)
    root.mainloop()