# bongsang

A collection of statistics and machine learning libraries developed by Bongsang Kim, including a linear regression class similar to R's `lm` function.

## Installation

````bash
pip install bongsang


## Accessing Sample Datasets

The `bongsang.datasets` subpackage provides sample datasets for easy experimentation.

### Example:

```python
from bongsang.datasets import load_house

# Load the house dataset
df = load_house()

# Now you can use df with the LM class
from bongsang import lm

X = df[['size']]
y = df['price']

model = lm.LM(X, y)
model.fit()
model.summary()
model.plot()
````
