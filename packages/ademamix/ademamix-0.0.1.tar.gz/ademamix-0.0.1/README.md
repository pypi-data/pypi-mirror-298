# AdEMAMix Optimizer

![PyPI](https://img.shields.io/pypi/v/adememix) ![License](https://img.shields.io/github/license/ovuruska/torch_ademamix/adememix)
## Overview

AdEMAMix is a optimizer that builds upon the widely-used AdamW algorithm, introducing two Exponential Moving Averages (EMAs) of past gradients for enhanced historical data utilization. This approach enables faster convergence and lower training minima, particularly beneficial for large-scale models like LLMs and image classification tasks. For a comprehensive understanding of AdEMAMix, including its methodology and performance benchmarks, refer to the original paper: "The AdEMAMix Optimizer: Better, Faster, Older" by Matteo Pagliardini, Pierre Ablin, and David Grangier, available at [https://arxiv.org/abs/2409.03137](https://arxiv.org/abs/2409.03137).
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Installation
You can install the package via PyPI:

```bash
pip install adememix
```

Alternatively, you can clone the repository and install it manually:

```bash
pip install git+https://github.com/ovuruska/torch_ademamix.git
```

I apologize for the confusion. You're right, I should have kept it in English. Here's the expanded Usage section in English:

## Usage

AdEMAMix optimizer can be easily used in PyTorch, similar to other optimizers. Here's a more detailed usage example:

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from ademamix import AdEMAMix

# Model definition (example)
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)

# Create model and data loader
model = SimpleModel()
train_loader = DataLoader(your_dataset, batch_size=32, shuffle=True)

# Training parameters
num_epochs = 10
num_iterations = len(train_loader) * num_epochs

# Optimizer setup
optimizer = AdEMAMix(
    model.parameters(),
    lr=1e-3,
    betas=(0.9, 0.999, 0.9999),
    alpha=5.0,
    weight_decay=1e-2,
    T_alpha=num_iterations,
    T_beta3=num_iterations
)

# Loss function
criterion = nn.MSELoss()

# Training loop
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        if batch_idx % 100 == 0:
            print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item()}')
```

### Setting T_alpha and T_beta3 Parameters

The `T_alpha` and `T_beta3` parameters control the time-dependent behavior of AdEMAMix. These parameters are typically set equal to the total number of iterations (`num_iterations`).

- `T_alpha`: Controls how the alpha parameter changes over time.
- `T_beta3`: Controls how the beta3 parameter changes over time.

Things to consider when setting these parameters:

1. Calculate the total number of iterations for your training:
   ```python
   num_iterations = len(train_loader) * num_epochs
   ```

2. Set `T_alpha` and `T_beta3` equal to this number:
   ```python
   optimizer = AdEMAMix(
       model.parameters(),
       lr=1e-3,
       T_alpha=num_iterations,
       T_beta3=num_iterations,
       # ... other parameters ...
   )
   ```

3. If your training duration is very long or short, you can adjust these values. For example:
   - For faster adaptation: `T_alpha = num_iterations // 2`
   - For slower adaptation: `T_alpha = num_iterations * 2`

4. You can fine-tune the optimizer's behavior by setting `T_alpha` and `T_beta3` to different values.

Note: If you leave these parameters as `None`, AdEMAMix will use constant alpha and beta3 values.

### Advanced Usage

AdEMAMix allows for fine-tuning in different scenarios:

```python
optimizer = AdEMAMix(
    model.parameters(),
    lr=1e-3,
    betas=(0.9, 0.999, 0.9999),  # (beta1, beta2, beta3)
    alpha=5.0,
    weight_decay=1e-2,
    T_alpha=num_iterations,
    T_beta3=num_iterations,
    amsgrad=True,  # Use AMSGrad variant
    foreach=True,  # For faster updates (if supported)
    maximize=False,  # If True, maximizes the loss (e.g., for GAN training)
    capturable=True,  # For use with CUDA graphs
    differentiable=False  # To make the optimizer differentiable
)
```



You can easily replace your existing Adam or AdamW optimizer with AdEMAMix by modifying just a few lines in your existing code.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you encounter any bugs or have suggestions for improvements. Please ensure that your contributions adhere to our code of conduct and follow the repository guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References
If you use AdEMAMix in your research, please cite the following papers:

1. Matteo Pagliardini, Pierre Ablin, David Grangier (2024). *The AdEMAMix Optimizer: Better, Faster, Older*. [arXiv:2409.03137](https://arxiv.org/abs/2409.03137)

---

