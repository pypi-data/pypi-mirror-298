# word_family_counter

A Python script for counting word families in a text file using advanced morphological analysis with spaCy.

## Features

- Processes text files to count word families
- Uses spaCy for advanced linguistic analysis and lemmatization
- Handles contractions, compound words, and various text preprocessing tasks
- Supports multiple languages (depending on available spaCy models)
- Provides detailed output with word family frequencies

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/BlueBirdBack/word_family_counter.git
   cd word_family_counter
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the command with a text file as an argument:

```
word_family_counter path/to/your/text_file.txt
```

Optional arguments:
- `--verbose`: Increase output verbosity for debugging purposes
- `--language`: Specify the spaCy model to use (default: en_core_web_sm)

Example:
```
word_family_counter sample.txt --verbose --language en_core_web_md
```

Note: Ensure that you have installed the required spaCy model before running the command. If you encounter an error about missing models, run the installation command in step 4 again.

## Output

The script will display:
1. Total number of words in the text
2. Total number of unique word families
3. A list of word families sorted by frequency (descending) and then alphabetically

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

BlueBirdBack - avery@bluebirdback.com

Project Link: [https://github.com/BlueBirdBack/word_family_counter](https://github.com/BlueBirdBack/word_family_counter)
