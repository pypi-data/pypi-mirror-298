# SVMargin

**Version:** 1.4  
**License:** MIT License  
**Author:** Eran Kaufman
<br>**Email:** erankfmn@gmail.com 

## Overview

SVMmargin is a Python package designed to address the problem of imbalanced data and cost-sensitive multiclass classification using TensorFlow for GPU acceleration. The package enhances the sensitivity of critical classes by adjusting the decision boundary between them according to a class weight vector. This enables a tighter error bound for high-priority classes while minimizing the overall out-of-sample error across all classes.

The package supports multiple kernel methods, including linear, RBF, and polynomial kernels, implemented with TensorFlow for efficient computation. It is optimized for modern GPU architectures, making it suitable for large-scale datasets. Additionally, SVMmargin incorporates mechanisms for flexible regularization and robust handling of class imbalances, improving classification performance in real-world scenarios.
## Features

- **Imbalanced Classification:** Adjusts the imbalance of classes based on their inverse size.
- **Cost-Sensitive Classification:** Adjusts the sensitivity of classes based on their importance.
- **Apportioned Margin Framework:** Efficiently shifts decision boundaries according to a prioritization vector.
- **Support for Multiple Kernels:** Includes linear, RBF, and polynomial kernels.
- **TensorFlow Integration for Performance:** Optimized with TensorFlow, enabling large-scale training on GPUs for faster and more efficient processing of complex datasets.
- **Fisher Consistency:** Ensures the consistency of the classifier.
- **Generalization Bounds:** Provides theoretical guarantees on performance.
## Installation

You can install the package directly from PyPI using pip:

```bash
pip install SVMargin
```

## Usage
### For full examples and detailed use cases, refer to the SVMargin notebook on Kaggle:
### https://www.kaggle.com/code/amitronen1/svmargin
## Available Kernels

- Linear Kernel: `linear`
- RBF Kernel: `rbf`
- Polynomial Kernel: `poly`

You can select the kernel by specifying the `kernel` parameter when creating an instance of `ImbalancedSVM`.

## Class Weights

The `class_weight` parameter allows you to assign different importance to different classes. It accepts a dictionary where keys are class labels, and values are the corresponding weights.

## Examples

Here are a few usage examples:

### Linear Kernel Example

```python
cls = ImbalancedSVM(kernel='linear', class_weight={0: 10, 1: 1}, gamma=0.5, C=1, verbose= True)
cls.fit(X, y, max_iter=30)
predictions = cls.predict(X_test)
```

### RBF Kernel Example

```python
cls = ImbalancedSVM(kernel='rbf', gamma=0.5, class_weight={0: 1, 1: 10}, gamma=0.5, C=1, verbose= True)
cls.fit(X, y, max_iter=30)
predictions = cls.predict(X_test)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

If you would like to learn more about the theoretical background and the research behind this package, please refer to the following article:
Please cite this article when using this package!
- **Apportioned Margin Approach for Cost Sensitive Large Margin Classifiers**  
Gottlieb, LA., Kaufman, E. & Kontorovich, A. Apportioned margin approach for cost sensitive large margin classifiers. Ann Math Artif Intell 89, 1215–1235 (2021). https://doi.org/10.1007/s10472-021-09776-w



## Contact

If you have any questions or suggestions, feel free to reach out at erankfmn@gmail.com.