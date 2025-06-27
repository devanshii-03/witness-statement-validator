# 🕵️‍♀️ Witness Statement Validator

An **AI-powered NLP application** that analyzes a **single witness statement** for linguistic markers of **credibility, uncertainty, and complexity**. It uses advanced Natural Language Processing techniques and a heuristic-based scoring engine to generate a "suspicion verdict," all through a clean GUI built in Python.

---

## 📋 Table of Contents
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [How It Works: The NLP Pipeline](#-how-it-works-the-nlp-pipeline)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [How to Run](#-how-to-run)
- [Project Structure](#-project-structure)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Key Features

-   ⚖️ **Credibility Scoring Engine**: Generates a "suspicion score" based on a set of linguistic heuristics.
-   🏷️ **Linguistic Marker Analysis**: Detects patterns like hedging, passive voice, negations, sentence complexity, and vague language.
-   🏛️ **Core NLP Breakdown**: Performs and displays detailed analysis for:
    -   Part-of-Speech (POS) Tagging
    -   Syntactic Dependency Parsing
    -   Morphological Analysis (lemmas, tags)
    -   Named Entity Recognition (NER)
-   🖼️ **Interactive GUI**: A user-friendly interface built with Tkinter featuring separate tabs for detailed analysis and the final verdict.
-   💾 **Exportable Reports**: Allows saving the full analysis and verdict to a text file for documentation.

---

## 🖼️ Screenshots

*(Add screenshots of your application here. Showcasing the "Analysis" and "Verdict" tabs would be highly effective.)*

![GUI Screenshot](https://i.imgur.com/your-screenshot-1.png)

---

## 🧠 How It Works: The NLP Pipeline

The application processes a single statement through a multi-stage pipeline:

1.  **Core NLP Processing**: The statement is parsed by **spaCy** to extract fundamental linguistic data, including tokens, sentences, POS tags, dependency trees, and named entities.
2.  **Detailed Analysis Display**: The application visualizes the core NLP data (POS, Parsing, Morphology, etc.) in the "Analysis" tab for expert review.
3.  **Heuristic Scoring (`generate_verdict`)**: The code then calculates a "suspicion score" by scanning for specific linguistic patterns often associated with deception or uncertainty, such as:
    -   **Hedging & Uncertainty**: Use of modal verbs (`might`, `could`) and adverbs of doubt.
    -   **Sentence Complexity**: Presence of multiple dependent clauses.
    -   **Passive Voice & Vague References**: High ratio of pronouns vs. named entities.
    -   **Negations & Tense Shifts**: Frequent use of "not" and inconsistent verb tenses.
4.  **Verdict Generation**: Based on the cumulative score, the application presents a final verdict (e.g., "NO SUSPICION DETECTED," "MODERATELY SUSPICIOUS") with a list of the specific indicators that were flagged.

---

## 🛠️ Tech Stack

-   **Language**: Python 3.9+
-   **GUI Framework**: Tkinter
-   **Core NLP Libraries**:
    -   **spaCy**: For high-performance parsing, dependency extraction, NER, and lemmatization.
    -   **NLTK**: Used primarily for its WordNet lexical database access.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites
-   Python 3.9 or higher
-   `pip` package installer

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/devanshii-03/witness-statement-validator.git](https://github.com/devanshii-03/witness-statement-validator.git)
    cd witness-statement-validator
    ```

2.  **Create and Activate a Virtual Environment** (Recommended)
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLP Models**
    ```bash
    python -m spacy download en_core_web_sm
    python -m nltk.downloader wordnet omw-1.4
    ```

---

## ▶️ How to Run

Once the installation is complete, run the application with the following command:

```bash
python app.py
```

This will launch the Tkinter GUI. Enter a witness statement and click "Validate Statement" to see the results.

## 📁 Project Structure
```
witness-statement-validator/
│
├── main.py             # Main application with GUI logic and NLP processing
├── README.md          # Project description (this file)
└── testcases.txt         # Sample test cases
```

## ✨ Future Roadmap
[ ] Two-Statement Comparison: Implement semantic similarity and contradiction detection between two statements.

[ ] PDF Report Generation: Export the analysis results into a formatted PDF document.

[ ] Refine Scoring Engine: Tune the heuristics in the generate_verdict function for higher accuracy.

[ ] Multilingual Support: Extend functionality to analyze statements in other languages.

## 🤝 Contributing
Pull requests and suggestions are welcome! If you want to contribute, please fork the repository and submit a pull request with your changes.

## ✍️ Author
This project was developed by Devanshi Nikam.
