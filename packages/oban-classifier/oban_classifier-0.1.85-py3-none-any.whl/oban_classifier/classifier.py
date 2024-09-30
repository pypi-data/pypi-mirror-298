import numpy as np
import pandas as pd
from torch import nn
from skorch import NeuralNetClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score
import torch

class ObanModule(nn.Module):
    def __init__(self, input_dim, num_units=128, num_classes=2, nonlin=nn.ReLU(), dropout_rate=0.5):
        super(ObanModule, self).__init__()
        self.dense0 = nn.Linear(input_dim, num_units)
        self.nonlin = nonlin
        self.dropout = nn.Dropout(dropout_rate)
        self.dense1 = nn.Linear(num_units, num_units)
        self.output = nn.Linear(num_units, num_classes)
        # Softmax KALDIRILDI

    def forward(self, X, **kwargs):
        X = X.float()  # Girdiyi float32'ye zorlayın
        X = self.nonlin(self.dense0(X))
        X = self.dropout(X)
        X = self.nonlin(self.dense1(X))
        X = self.output(X)  # Sonuç direk logits (ham skorlar) olacak
        return X

def oban_classifier(X, y, num_units=128, num_classes=2, nonlin=nn.ReLU(), dropout_rate=0.5, 
                    max_epochs=10, lr=0.01, test_size=0.2, random_state=42):
    """
    Trains and evaluates a neural network classifier.
    """
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Normalize the dataset and convert to float32
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train).astype(np.float32)
    X_test = scaler.transform(X_test).astype(np.float32)

    # Convert labels (y_train, y_test) to LongTensor
    y_train = torch.tensor(y_train, dtype=torch.long)
    y_test = torch.tensor(y_test, dtype=torch.long)

    # Create a Skorch NeuralNetClassifier
    net = NeuralNetClassifier(
        ObanModule,
        module__input_dim=X_train.shape[1],
        module__num_units=num_units,
        module__num_classes=num_classes,
        module__nonlin=nonlin,
        module__dropout_rate=dropout_rate,
        max_epochs=max_epochs,
        lr=lr,
        iterator_train__shuffle=True,
        verbose=1,
        criterion=torch.nn.CrossEntropyLoss  # CrossEntropyLoss kullanılıyor
    )

    # Fit the model
    net.fit(X_train, y_train)

    # Make predictions
    y_pred = net.predict(X_test)

    # Embedded evaluate_performance function
    def evaluate_performance(y_true, y_pred):
        """
        Evaluates and prints performance metrics: accuracy, confusion matrix, precision, recall, and F1 score.
        """
        accuracy = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        precision_per_class = precision_score(y_true, y_pred, average=None)
        recall_per_class = recall_score(y_true, y_pred, average=None)
        f1_per_class = f1_score(y_true, y_pred, average=None)

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Confusion Matrix:\n{cm}")
        
        for i, (prec, rec, f1) in enumerate(zip(precision_per_class, recall_per_class, f1_per_class)):
            print(f"Class {i}:")
            print(f"  Precision: {prec:.4f}")
            print(f"  Recall: {rec:.4f}")
            print(f"  F1 Score: {f1:.4f}")

    # Evaluate performance
    evaluate_performance(y_test, y_pred)
