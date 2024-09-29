import numpy as np
from tqdm import tqdm


class GibbsReconstructor:
    """
    A class to perform Gibbs reconstruction of missing data in a dataset.

    This class uses a regularized approach to estimate the coefficients for reconstructing
    missing values in the input data matrix using Gibbs sampling methods.

    Attributes:
        alpha (float): Regularization parameter for the Ridge regression.

    Methods:
        fit(X, verbose=False): Fits the model to the input data matrix X, with an option to enable verbosity.
        predict(z): Predicts missing values in the input array z.
    """

    def __init__(self, alpha=1e-3):
        """
        Initializes the GibbsReconstructor with a given regularization parameter.

        Parameters:
            alpha (float): Regularization parameter. Default is 1e-3.
        """
        self.alpha = alpha

    def fit(self, X, verbose=False):
        """
        Fits the GibbsReconstructor model to the input data.

        This method computes the coefficients based on the provided dataset X,
        taking into account the regularization to handle overfitting.

        Parameters:
            X (ndarray): A 2D NumPy array of shape (n_samples, n_features) representing the input data.
            verbose (bool): If True, prints progress updates during the fitting process. Default is False.

        Returns:
            None: The coefficients are stored in the instance variable coef_.

        Notes:
            - If verbose is set to True, progress updates will be shown using tqdm.
        """
        n, p = X.shape

        X = np.hstack((X, np.ones((n, 1))))

        XtX = X.T @ X
        XtX.flat[:: p + 2] += n * self.alpha

        XtX_inv = np.linalg.inv(XtX)

        self.coef_ = np.zeros((p + 1, p + 1))

        mask = np.ones(p + 1, dtype=bool)
        for k in tqdm(range(p), desc="Fitting model", disable=not verbose):
            mask[k] = False

            b = XtX_inv[k, mask]
            c = XtX_inv[k, k]

            LHS = XtX_inv[np.ix_(mask, mask)]
            RHS = XtX[mask, k]

            self.coef_[k, mask] = LHS @ RHS - b * ((b @ RHS) / c)

            mask[k] = True

    def predict(self, z):
        """
        Predicts missing values in the input array z using the fitted model.

        This method reconstructs the data based on the learned coefficients.

        Parameters:
            z (ndarray): A 1D NumPy array containing the data with potential missing values (NaNs).

        Returns:
            ndarray: A reconstructed 1D NumPy array with estimated values for the missing entries.
        """
        p = z.shape[1]
        missing_idxs = np.where(np.isnan(z))

        z[missing_idxs] = 0

        A = np.eye(p + 1)
        for k in missing_idxs:
            A[k] = self.coef_[k] @ A
        A = A[:p, :p]
        A[missing_idxs, missing_idxs] -= 1

        return np.linalg.solve(A, z.T).T
