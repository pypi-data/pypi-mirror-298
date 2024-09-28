from dataclasses import dataclass, field
from typing import Any, List, Dict, Callable
import uuid
import logging
import numpy as np
from numpy import ndarray
import pandas as pd
from .data_samplers import get_sampler

@dataclass
class ThompsonSamplingWrapper:
    
    # dataclass fields
    base_model_class: Any
    num_models: int
    sampler: str = "with_replacement"
    init_kwargs: dict = field(default_factory=dict)
    fit_kwargs: dict = field(default_factory=dict)
    predict_kwargs: dict = field(default_factory=dict)
    models: Dict[int, tuple] = field(init=False)
    sampler_func: Callable = field(init=False)
    
    # set later
    predicted_probabilities: Dict[str, ndarray] = field(default_factory=dict)
    output_df: pd.DataFrame = field(init=False, default=pd.DataFrame())

    # checkpoints
    is_trained: bool = field(init=False, default=False)
    has_output_sampled: bool = field(init=False, default=False)
    
    def __post_init__(self):
        """
        Initialize an ensemble of models after the dataclass initialization.
        Check if the base_model_class has a predict_proba method.
        """
        if not hasattr(self.base_model_class, 'predict_proba'):
            raise AttributeError("The base_model_class must have a 'predict_proba' method in order to use Thompson Sampling.")
        
        # initialize models
        self.models = {i: (self.base_model_class(*self.init_args, **self.init_kwargs), uuid.uuid4()) for i in range(self.num_models)}

        # get sampler function
        self.sampler_func = get_sampler(self.sampler)

        # setup logger
        self.logger = logging.getLogger(__name__)

        # log the initialization of the wrapper
        self.logger.info(f"Initialized {self.num_models} models of type {self.base_model_class}")

        # test the model class
        self._test()

    def _test(self):
        """
        Test the model class by making a copy, fitting it and then predicting on a small dataset.
        """
        # make a copy of the model
        model = self.base_model_class(*self.init_args, **self.init_kwargs)

        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([0, 1, 0])

        # fit the model
        model.fit(X, y, **self.fit_kwargs)

        # predict on the same data
        y_pred = model.predict_proba(X, **self.predict_kwargs)

        # make sure predictions are of shape (n_samples,2)
        assert y_pred.shape == (3, 2), "Predictions are not of shape (n_samples,2)"

        return True
    
    def get_model_ids(self):
        """
        Get the model IDs.
        """
        return [model_id for model_id in self.models]
    
    def get_models(self):
        """
        Get the models.
        """
        return self.models
    
    def is_trained(self):
        """
        Get the is_trained flag.
        """
        return self.is_trained
    
    def get_num_models(self):
        """
        Get the number of models.
        """
        return self.num_models
    
    def get_sampler(self):
        """
        Get the sampler.
        """
        return self.sampler
    
    def get_output_df(self):
        """
        Get the output dataframe.
        """
        if not self.has_output_sampled:
            _, _ = self.predict_proba(X)

        return self.output_df

    def fit(self, X, y, *args, **kwargs):
        """
        Fit all models in the ensemble.

        Args:
            X: The input features.
            y: The target values.
            *args: Additional positional arguments to pass to the fit method.
            **kwargs: Additional keyword arguments to pass to the fit method.
        """

        # fit models
        for i, (model, model_id) in enumerate(self.models.values()):

            # sample data - can be with or without replacement
            X_sampled, y_sampled = self.sampler_func(X, y, *args, **kwargs)
            
            # log the training of the model
            self.logger.info(f"Training model {i+1}/{self.num_models} (ID: {model_id})")
            
            # fit the model
            model.fit(X_sampled, y_sampled.values.ravel(), **self.fit_kwargs)
            
            # save the model once it is trained
            self.models[i] = (model, model_id)

        self.logger.info(f"Trained {self.num_models} models")
        self.is_trained = True

    def set_predicted_probabilities(self, X, *args, **kwargs):
        """
        Predict the probabilities of the positive class for all models in the ensemble.

        Args:
            X: The input features.
            *args: Additional positional arguments to pass to the predict_proba method.
            **kwargs: Additional keyword arguments to pass to the predict_proba method.
        """

        # predict the probabilities for each model
        for i, (model, model_id) in enumerate(self.models.values()):

            # log the prediction of the model
            self.logger.info(f"Predicting with model {i+1}/{self.num_models} (ID: {model_id})")
            
            # predict the probabilities
            y_pred_proba = model.predict_proba(X, **self.predict_kwargs)
            
            # save the predicted probabilities
            self.predicted_probabilities[model_id] = y_pred_proba

        return self.predicted_probabilities
    
    def get_predicted_probabilities(self):
        """
        Get the predicted probabilities for all models in the ensemble.
        """
        # extract the P=1 and hstack them
        probabilities = np.column_stack([self.predicted_probabilities[model_id][:, 1].ravel() for model_id in self.predicted_probabilities])
        return probabilities
        
    def predict_proba(self, X, *args, **kwargs):
        """for each row in X, randomly sample a model and return the predicted probability"""

        # check if predicted probabilities have been set
        if not self.predicted_probabilities:
            raise ValueError("Predicted probabilities have not been set. Call set_predicted_probabilities first.")
        
        # horizontally stack the P=1 columns of each model's predicted probabilities 
        probabilities = np.column_stack([self.predicted_probabilities[model_id][:, 1].ravel() for model_id in self.predicted_probabilities])

        # generate a matrix of random 0/1 values - at most one 1 per row    
        # Get the number of rows and columns
        num_rows, num_cols = probabilities.shape

        # Randomly select column indices for each row
        selected_columns = np.random.randint(0, num_cols, size=num_rows)

        # Select the elements based on the randomly chosen column indices
        random_elements = probabilities[np.arange(num_rows), selected_columns]

        # create a dataframe with the selected columns and random elements
        self.output_df = pd.DataFrame({'thompson_sampled_model_index': selected_columns, 'thompson_sampled_probability': random_elements})
        self.has_output_sampled = True

        # log the sampling
        self.logger.info(f"Sampled probabilities for {num_rows} rows")

        # select the predicted probabilities for each row in X
        return selected_columns, random_elements


# main function to test the wrapper
def main():

    # create a wrapper from LogisticRegression
    from sklearn.linear_model import LogisticRegression
    wrapper = ThompsonSamplingWrapper(base_model_class=LogisticRegression, num_models=10)
    print("tested LogisticRegression wrapper")

    # create a wrapper from LightGBM
    from lightgbm import LGBMClassifier
    wrapper = ThompsonSamplingWrapper(base_model_class=LGBMClassifier, num_models=10)
    print("tested LGBMClassifier wrapper")

    # create a wrapper from XGBoost with args and kwargs
    from xgboost import XGBClassifier
    wrapper = ThompsonSamplingWrapper(
        base_model_class=XGBClassifier,
        num_models=5,
        init_kwargs={'max_depth': 3, 'learning_rate': 0.1, 'n_estimators': 100, 'objective': 'binary:logistic'}
    )
    print("tested XGBClassifier wrapper with args and kwargs")

    # Another example with RandomForestClassifier
    from sklearn.ensemble import RandomForestClassifier
    wrapper = ThompsonSamplingWrapper(
        base_model_class=RandomForestClassifier,
        num_models=8,
        init_kwargs={'n_estimators': 50, 'max_depth': 5, 'min_samples_split': 5, 'random_state': 42}
    )
    print("tested RandomForestClassifier wrapper with args and kwargs")
    
if __name__ == "__main__":
    main()