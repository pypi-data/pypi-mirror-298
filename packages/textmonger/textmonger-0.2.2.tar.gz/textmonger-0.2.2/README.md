# The Text Monger

The Text Monger is a Python package that provides various text analysis tools, including readability scoring, power words distribution, named entity recognition (NER), and sentiment analysis.

## Features

- **Readability Analysis:** Analyze the readability of text using various metrics such as Flesch Reading Ease, Gunning Fog Index, and more.
- **Power Words Distribution:** Visualize the distribution of power words in your text, highlighting impactful language.
- **Named Entity Recognition (NER):** Extract and highlight named entities (like names, organizations, locations) from the text.
- **Sentiment Analysis:** Determine the sentiment polarity (positive, negative, or neutral) and subjectivity of the text using `TextBlob`.

## Installation

You can install The Text Monger package using `pip`:

```bash
pip install textmonger
```

## Usage

After installation, you can run The Text Monger from the command line. Here's how you can use it:

### Command-Line Interface (CLI)

To analyze a piece of text, simply run the following command in your terminal:

```bash
textmonger
```

You will be prompted to enter the text you want to analyze. Type or paste your text, and when you're done, type `END` on a new line to finish input. The tool will then output the readability analysis, power words distribution, named entity recognition, and sentiment analysis.

### Example

```bash
$ textmonger
Enter Text to analyze (type 'END' on a new line to finish):
The quick brown fox jumps over the lazy dog.
END

================================================================================
                              Readability Analysis
================================================================================
| Metric                       | Score               |
| ---------------------------- | ------------------ |
| Reading ease                 | Difficult           |
| Reading level                | Grade 14.4          |
| Smog index                   | Grade 15.8          |
| Gunning Fog index            | Grade 15.46         |
| Coleman-Liau index           | Grade 13.06         |
| Automated Readability index  | Grade 16.4          |
| Dale-Chall Readability score | 9.88                |
| Text standard                | 15th and 16th grade |
================================================================================
                              Power Words Distribution
================================================================================
<Your Output Here>

================================================================================
                              Named Entity Recognition (NER)
================================================================================
<Your Output Here>

================================================================================
                              Sentiment Analysis
================================================================================
| Polarity       | 0.0 (Neutral)                   |
| Subjectivity   | 0.5 (Subjective)                |
================================================================================
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue to discuss what you would like to change.

## Contact

If you have any questions, feel free to reach out to the project maintainer:

- **Author:** Sahil Garje
- **Email:** sahilgarje@gmail.com
