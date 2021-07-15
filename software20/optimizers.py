"""Optimizer decorators."""

import importlib
import os
from functools import partial
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import SCORERS
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import Pipeline


class Optimizer:

    def __init__(self, opt_fn, data=None, batch_size=3, test_size=0.2):
        self._opt_fn = opt_fn
        self._data = data
        self._batch_size = batch_size
        self._test_size = test_size
        self.model_ = None
        self.model_dir = Path(os.path.dirname(self.module.__file__)) / "models"
        self.model_dir.mkdir(exist_ok=True)
    
    def parser(self, parser_fn):
        self._parser_fn = parser_fn

    @property
    def data(self) -> Path:
        if self._data is None:
            return (
                Path(os.path.dirname(self.module.__file__))
                / "data" / f"{self._opt_fn.__name__}.data"
            )
        return Path(self._data)
    
    @property
    def model_path(self) -> Path:
        return (
            Path(os.path.dirname(self.module.__file__))
            / "models" / f"{self._opt_fn.__name__}.model"
        )

    @property
    def module(self):
        return importlib.import_module(self._opt_fn.__module__)

    def batch_to_vectors(self, batch):
        features, targets = [], []
        for f, t in batch:
            features.append(f)
            targets.append(t)
        return pd.DataFrame(features), np.array(targets)

    def optimize(self):
        # TODO: don't hard code this!
        self.model_ = Pipeline(
            steps=[
                (
                    "featurizer", ColumnTransformer([
                        ("count_vectorizer", CountVectorizer(), [0]),
                    ])
                ),
                ("estimator", SGDClassifier(warm_start=True, loss="log"))
            ]
        )
        # TODO: also don't hard code this!
        scorer = SCORERS.get("roc_auc")

        print(
            f"optimizing model {self.model_} with evaluation metric {scorer}"
        )

        with open(self.data) as f:
            dataset = [self._parser_fn(line) for line in f.readlines()]

        X, y = self.batch_to_vectors(dataset)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self._test_size
        )
        self.model_.fit(X_train, y_train)
        train_score = scorer(self.model_, X_train, y_train)
        test_score = scorer(self.model_, X_test, y_test)
        print(f"train score: {train_score}")
        print(f"test score: {test_score}")
        joblib.dump(self.model_, self.model_path)
        return self.model_

    def __call__(self, *args, as_proba=False) -> Any:
        X = [args]
        # TODO: reserved for when model is trained 
        if self.model_path.exists():
            self.model_ = joblib.load(self.model_path)
        else:
            self.model_ = self.optimize()

        predicted_probas = self.model_.predict_proba(X)
        if as_proba:
            return predicted_probas[0, 1]
        return predicted_probas.argmax()


def optimize(fn=None, *, data=None):
    if fn is None:
        return partial(optimize, data=data)
    return Optimizer(fn, data)
