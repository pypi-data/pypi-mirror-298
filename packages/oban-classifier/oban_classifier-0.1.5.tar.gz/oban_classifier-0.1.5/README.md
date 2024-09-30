# Oban Classifier

**Oban Classifier** is a flexible neural network-based classifier built on top of PyTorch and Skorch. It supports both binary and multiclass classification, and allows users to define parameters such as the number of units, activation function, dropout rate, and more.

## Features

- Supports **binary and multiclass classification**.
- Allows **user-defined parameters** for hidden units, activation functions, dropout, and more.
- Built using **Skorch** and **PyTorch** for easy integration with scikit-learn pipelines.
- Provides detailed **performance metrics** including accuracy, precision, recall, F1-score, and confusion matrix.

## Installation

You can install the library via pip after publishing it on PyPI:

```bash
pip install oban_classifier


### Usage Example

from oban_classifier import oban_classifier
from sklearn.datasets import load_breast_cancer
import pandas as pd

# Load the Breast Cancer dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Train and evaluate the model
oban_classifier(X, y, num_units=64, num_classes=2, max_epochs=20, lr=0.01)


