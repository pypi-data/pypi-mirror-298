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

```bash
==============================================================
Linear Regression Summary
X features:  ['size']
y target:  price
______________________________________________________________
Residuals:
    Min      1Q  Median      3Q     Max
 -49.388  -27.388   -6.388   29.577   64.333

Coefficients:
             Estimate  Std. Error  t value  Pr(>|t|)
(Intercept)   98.24833   58.03348    1.693    0.1289
size           0.10977    0.03297    3.329    0.0104 *

Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 41.33 on 8 degrees of freedom
Multiple R-squared:  0.5808,    Adjusted R-squared:  0.5284
F-statistic: 11.08 on 1 and 8 DF,  p-value: 0.01039
==============================================================
```

![Sample](docs/sample.png)

