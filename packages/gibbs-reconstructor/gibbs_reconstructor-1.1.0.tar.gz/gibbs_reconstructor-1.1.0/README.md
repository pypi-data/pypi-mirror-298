# Gibbs Reconstructor

The `GibbsReconstructor` is a Python class designed to perform reconstruction of missing values in partially deleted signals, images, or sequences. It uses a regularized approach based on Gibbs sampling methods to estimate missing entries, making it ideal for scenarios where data might be incomplete or corrupted. This approach is particularly useful for tasks such as image inpainting, signal reconstruction, and sequence completion.

## Features

- **Reconstruction of Missing Data**: Fills in missing values (NaNs) in partially observed data matrices.
- **Gibbs Sampling**: Uses an exact Gibbs sampling approach to estimate missing values based on the observed data.
- **Ridge Regularization**: Supports ridge regularization to avoid overfitting during reconstruction.
- **Flexible Application**: Can be used for signals, sequences, images, or any dataset where partial data is available.

## Use Cases

- **Signal Completion**: Recover deleted or corrupted sections of time-series signals.
- **Image Inpainting**: Fill in missing pixels in images, making it useful for tasks like repairing damaged images or handling incomplete image data.
- **Sequence Reconstruction**: Complete sequences with missing or corrupted values, useful for various predictive modeling tasks in data science.

## How It Works

1. **Model Fitting**: The `fit()` method takes in a complete dataset and learns the underlying relationships between the features using a regularized least squares approach.
2. **Prediction**: The `predict()` method takes in data with missing values (represented as `NaN`s) and reconstructs those missing entries by leveraging the learned relationships. This method uses Gibbs sampling technique to estimate the missing values.

## Attributes

- **`alpha`**: A regularization parameter used for controlling the strength of ridge regression. It helps prevent overfitting during the reconstruction process.
  
## Methods

- **`fit(X)`**: Fits the GibbsReconstructor model on the given dataset `X`. The matrix `X` should be fully observed (i.e., no missing values) and is used to learn the underlying structure of the data.
  
- **`predict(z)`**: Predicts the missing values in the input array `z`. The missing values should be represented as `NaN`, and the method will return the input array with the missing values reconstructed.

## Installation

To use `GibbsReconstructor`, ensure you have the required dependencies installed:

```bash
pip install numpy tqdm
