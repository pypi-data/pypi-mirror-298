# Flexible Scorer Library

Flexible Scorer is a Python library that allows you to evaluate and score text content based on custom criteria using OpenAI's GPT models. It provides a systematic way to assess texts, taking advantage of AI's capabilities to interpret and analyze content according to user-defined parameters.

## Features 
- **Customizable Criteria**:Score texts based on any criteria you define (e.g., humor, clarity, relevance)
- **Scalable Scoring System**: Utilizes a 1 to 10 scale for nuanced evaluations
- **OpenAI GPT Integration**: Leverages powerful language models for deep text analysis
- **Probability Analysis**: Computes weighted scores using token log probabilities
- **Visualization Tools**: Includes functions to plot and visualize scoring results using Plotly

## Installation

Installation through PIP manager
```bash
pip install flexiblescorer
```
### Dependencies
- numpy
- openai
- plotly
- scipy

# Getting Started

## Set OpenAI API key as environment
Enter OpenAI API key to use model

### a. For Windows Users
```commandline
    set OPENAI_API_KEY=your-api-key-here
```


### b. For macOS and Linux Users
```
    export OPENAI_API_KEY=your-api-key-here
```

Replace 'your-api-key-here' with your actual OpenAI API key, which you can obtain from your OpenAI account

## Basic Usage Example
```
from flexible_scorer import FlexibleScorer

# Define your evaluation criteria
criteria = "humor"

# Initialize the scorer with the criteria
scorer = FlexibleScorer(criteria)

# Texts to evaluate
texts = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "This is a serious statement without any humor.",
    "Why did the math book look sad? Because it had too many problems."
]

# Additional instructions (optional)
additional_instructions = "Consider clever wordplay and puns in your evaluation."

# Score the texts
scores = []
for text in texts:
    score = scorer.score(text, additional_instructions)
    scores.append(score)
    print(f"Text: {text}\nScore: {score}\n")

# Plot the results
scorer.plot_results(texts, scores)
```
- __FlexibleScorer__: The main class used to score texts based on your criteria
- __criteria__: A String defining what aspect you want to evaluate (e.g., "humor", "clarity")
- __score()__: Method to evaluate a single text. Optionally, you can provide additional instructions to guide the evaluation
- __plot_results()__: Method to visualize the scores of multiple texts
## API Reference
### FlexibleScorer
Initialization
```
    scorer = FlexibleScorer(criteria, model='gpt-4')
```
- __criteria (str)__: The criteria upon which to evaluate the text
- __model (str, optional)__: The OpenAI GPT model to use (default is 'gpt-4')

### Methods
- __score(text, additional_instructions='')__
  - __text(str)__: The text content to evaluate
  - __additional_instructions (str, optional)__: Extra guidelines for the evaluations
  - __Returns (float)__: A normalized score between 0 and 1
- __plot_results(texts, scores)__
  - __texts (list of str)__: A list of text contents evaluated
  - __scores (list of float)__: Corresponding scores for the texts
  - __Displays__: An interactive bar chart of the results
  
## OpenAI API  Usage
This library uses the OpenAI API under the hood. Ensure you comply with OpenAI's Usage Policies when using this package

## License
This project is licensed under the MIT License

## Contributing 
Contributions are welcome! Please open an issue or submit a pull request on Github

## Acknowledgments 
- Thanks to OpenAI for providing access to their powerful language models
- Inspired by the need for flexible and customizable text evaluation tools

