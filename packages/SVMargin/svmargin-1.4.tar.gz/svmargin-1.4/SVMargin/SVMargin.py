import tensorflow as tf
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class ImbalancedSVM(BaseEstimator, ClassifierMixin):
    """ImbalancedSVM class using TensorFlow for GPU acceleration.
    An algorithm for imbalanced cost-sensitive classification problems
    using imbalanced margins.
    - class_weight: a map between classes and their weights,
    - kernel: 'linear', 'poly', or 'rbf',
    - degree: degree of the polynomial kernel,
    - gamma: gamma parameter for the RBF kernel,
    - C: regularization parameter.
    """

    def __init__(self, class_weight=None, kernel='linear', degree=3, gamma=1, C=1, verbose=False):
        if isinstance(class_weight, dict):
            self.class_weight = np.array(list(class_weight.values()), dtype=np.float32)
        else:
            self.class_weight = class_weight

        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.C = C
        self.verbose = verbose  # Verbosity flag

        # Set kernel function
        if kernel == 'linear':
            self.ker = self.linearKernel
        elif kernel == 'rbf':
            self.ker = self.RBFKernel
        elif kernel == 'poly':
            self.ker = self.polyKernel
        else:
            raise ValueError(f"Unsupported kernel type: {kernel}")

    def linearKernel(self, x1, x2):
        return tf.matmul(x1, x2, transpose_b=True)

    def RBFKernel(self, x1, x2):
        x1_sq = tf.reduce_sum(tf.square(x1), axis=1, keepdims=True)
        x2_sq = tf.reduce_sum(tf.square(x2), axis=1, keepdims=True)
        dist_sq = x1_sq - 2 * tf.matmul(x1, x2, transpose_b=True) + tf.transpose(x2_sq)
        return tf.exp(-self.gamma * dist_sq)

    def polyKernel(self, x1, x2):
        return tf.pow(1 + tf.matmul(x1, x2, transpose_b=True), self.degree)

    def fit(self, X, y, max_iter=5):
        """
        Solve the dual problem using SGD, optimized for GPU using TensorFlow.
        """
        # Ensure labels are integers
        if not np.issubdtype(y.dtype, np.integer):
            raise TypeError(f"Expected integer labels, but got {y.dtype}")

        # Convert data to TensorFlow tensors and move to GPU
        X = tf.convert_to_tensor(X, dtype=tf.float32)
        y = tf.convert_to_tensor(y, dtype=tf.int32)

        # Add intercept term
        temp = tf.ones((X.shape[0], 1), dtype=tf.float32)
        X = tf.concat([X, temp], axis=1)

        # Get unique classes and their count
        self.y_classes = tf.unique(y).y
        self.K = len(self.y_classes)

        # Initialize alpha
        N = X.shape[0]
        self.alpha = tf.Variable(tf.zeros([N, self.K], dtype=tf.float32))

        # Prepare class weights
        if isinstance(self.class_weight, dict):
            class_weight_list = [self.class_weight[c.numpy()] for c in self.y_classes]
            class_weight_tensor = tf.constant(class_weight_list, dtype=tf.float32)
        else:
            class_weight_tensor = tf.constant(self.class_weight, dtype=tf.float32)

        # Create a mapping from class labels to indices
        class_to_index = {c.numpy(): idx for idx, c in enumerate(self.y_classes)}

        # Training loop
        for epoch in range(max_iter):
            if self.verbose:
                print(f"\nEpoch {epoch + 1}/{max_iter}")
            for index in range(N):
                xi = tf.expand_dims(X[index], axis=0)  # Shape: (1, D)
                yi = y[index].numpy()
                yi_idx = class_to_index[yi]

                # Compute delta for all classes
                delta = -tf.ones(self.K, dtype=tf.float32)
                delta = tf.tensor_scatter_nd_update(delta, [[yi_idx]], [1.0])

                # Compute kernel between all samples and xi
                K_col = self.ker(X, xi)  # Shape: (N, 1)
                K_col = tf.squeeze(K_col, axis=1)  # Shape: (N,)

                # Compute sums for all classes using element-wise multiplication
                # and summing over the samples dimension (axis=0)
                sums = tf.reduce_sum(self.alpha * K_col[:, tf.newaxis], axis=0)  # Shape: (K,)

                # Compute condition
                cw_yt = class_weight_tensor[yi_idx]
                condition = cw_yt >= delta * sums

                # Update alpha
                delta_update = delta * tf.cast(condition, tf.float32)
                alpha_update = tf.tensor_scatter_nd_add(
                    self.alpha[index, :],
                    [[i] for i in range(self.K)],
                    delta_update
                )
                self.alpha = tf.tensor_scatter_nd_update(
                    self.alpha,
                    [[index]],
                    [alpha_update]
                )

                if self.verbose and index % 1000 == 0:
                    # Print progress every 1000 samples
                    print(f"  Sample {index + 1}/{N}")

            if self.verbose:
                # Optionally, compute and print metrics at the end of each epoch
                total_alpha = tf.reduce_sum(self.alpha).numpy()
                print(f"End of epoch {epoch + 1}")
                print(f"  Total alpha sum: {total_alpha}")

        # Store support vectors and alpha as numpy arrays
        self.sv = X.numpy()
        self.alpha = self.alpha.numpy()

        return self

    def predict(self, X):
        """
        Predict using the dual form (kernelized version) optimized with TensorFlow.
        """
        X = tf.convert_to_tensor(X, dtype=tf.float32)
        temp = tf.ones((X.shape[0], 1), dtype=tf.float32)
        X = tf.concat([X, temp], axis=1)

        # Convert support vectors and alpha to tensors
        sv = tf.convert_to_tensor(self.sv, dtype=tf.float32)
        alpha = tf.convert_to_tensor(self.alpha, dtype=tf.float32)

        # Compute kernel matrix between support vectors and X
        K_sx = self.ker(sv, X)  # Shape: (N_s, N_x)

        # Compute Sums = alpha.T @ K_sx
        sums = tf.matmul(tf.transpose(alpha), K_sx)  # Shape: (K, N_x)

        # Divide each row by the class weight
        class_weight_tensor = tf.constant(
            [self.class_weight[c] for c in self.y_classes],
            dtype=tf.float32
        )
        sums = sums / class_weight_tensor[:, tf.newaxis]

        # Get predicted classes
        max_indices = tf.argmax(sums, axis=0)
        y_pred = [self.y_classes[idx] for idx in max_indices.numpy()]

        return np.array(y_pred)
