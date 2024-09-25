
# HintlyDataAnalysis – Mathematical, Financial, and Textual Analysis Library

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
  - [Math](#calculate-mean)
  - [Text](#count-interpunctions)
- [API](#api)
  - [Math](#math)
  - [Text](#text)
- [Authors](#authors)
- [License](#license)

## Description

HintlyDataAnalysis is a Python library designed for performing a variety of mathematical, financial, and textual analyses. The library offers functions to calculate means, percentage differences, data normalization, number repetition, financial angles, word counting, and text normalization.

## Installation

You can install the library using pip:

    pip install HintlyDataAnalysis

## Usage

After installation, import the library to access the functionalities.

Example Usage:

    from HintlyDataAnalysis import Math, Finance, Text, FilterType, NormalizeType

### Calculate mean
    mean_value = Math.Mean([1, 2, 3, 4])

### Calculate percentage difference
    percent_diff = Math.Difference(100, 120)

### Normalize data
    normalized_data = Math.Normalize([10, 15, 20], 100)

### Weighted average
    weighted_avg = Math.WeightedAverage([10, 20, 30], [1, 2, 3])

### Number repetition
    num_repeats = Math.NumberRepeat([1, 2, 2, 3, 3, 3])
### PercentNumberChance
    number_chance = Math.PercentNumberChance([5,10,15,20])
### Count interpunctions
    interpunctions = Text.CountInterpunctions("This is a test, with punctuation!")

### Count signs
    signs = Text.CountSigns("This is a test", lowerSigns=True)

### Count specific word
    word_count = Text.CountWord("This is a test", "test")

### Normalize text
    normalized_text = Text.NormalizeText("This is a TEST!", NormalizeType.LowText)
###
    print(mean_value, percent_diff, normalized_data, weighted_avg, num_repeats, number_chance)

## API

### Math

#### Math.Mean(analisysData: list)

Calculates the arithmetic mean of a list of numbers.

- **Parameters**:  
  `analisysData` (list): List of numbers to calculate the mean from.
- **Returns**:  
  The mean value of the data.

#### Math.Difference(a: float, b: float)

Calculates the percentage difference between two numbers.

- **Parameters**:  
  `a` (float): The base number.  
  `b` (float): The second number.
- **Returns**:  
  Percentage difference between `a` and `b`.

#### Math.Normalize(analisysData: list, normalizeNumber: int)

Normalizes a list of numbers relative to the largest value, scaling them to `normalizeNumber`.

- **Parameters**:  
  `analisysData` (list): List of numbers to normalize.  
  `normalizeNumber` (int): Value to normalize the data against.
- **Returns**:  
  A list of normalized data.

#### Math.WeightedAverage(analisysData: list, weights: list)

Calculates the weighted average of the data using the given weights.

- **Parameters**:  
  `analisysData` (list): List of numbers.  
  `weights` (list): List of weights corresponding to each number.
- **Returns**:  
  The weighted average of the data.

#### Math.NumberRepeat(numbers: list)

Counts the occurrences of each number in a list.

- **Parameters**:  
  `numbers` (list): List of numbers to analyze.
- **Returns**:  
  A dictionary where keys are numbers and values are the counts of their occurrences. 
#### Math.PercentNumberChance(numbers:list)
Calculates the incidence of each number as a percentage.
- **Parameters**
  `numbers` (list): List of numbers to calculate chance
- **Returns**:
  Dictionary with percentages assigned to numbers (keys)
### Text

#### Text.CountInterpunctions(text: str)

Counts the occurrences of specific punctuation marks in the provided text.

- **Parameters**:  
  `text` (str): The text to analyze.
- **Returns**:  
  A dictionary where the keys are punctuation marks and the values are their occurrences in the text.

#### Text.CountSigns(text: str, lowerSigns: bool)

Counts each unique character (case-sensitive or insensitive) in the text.

- **Parameters**:  
  `text` (str): The text to analyze.  
  `lowerSigns` (bool): If `True`, characters will be counted case-insensitively.
- **Returns**:  
  A dictionary of characters and their counts.

#### Text.CountWord(text: str, word: str)

Counts how many times a word appears in the text.

- **Parameters**:  
  `text` (str): The text to search within.  
  `word` (str): The word to count.
- **Returns**:  
  The number of occurrences of the word.
#### Text.NormalizeText(text: str, normalizeType: NormalizeType)

Normalizes text based on the chosen normalization type (e.g., delete punctuation, convert to lowercase).

- **Parameters**:  
  `text` (str): The text to normalize.  
  `normalizeType` (NormalizeType): The type of normalization to apply.
- **Returns**:  
  The normalized text.

## Authors

#### Franciszek Chmielewski (ferko2610@gmail.com)

## License

This project is licensed under the MIT License. More details can be found in the LICENSE file.

## Version History

- **0.1** – Initial release.
- **0.2** – Added Text class with normalization functions.
- **0.3** - Deleted Finance Tools.

### Future Plans

- Add more advanced financial and mathematical analysis tools.
- Expand text analysis capabilities.
