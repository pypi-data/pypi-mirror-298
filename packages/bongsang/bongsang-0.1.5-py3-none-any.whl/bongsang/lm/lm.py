from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy import stats


class LM:
    def __init__(self, X, y):
        self.lm = linear_model.LinearRegression()
        self.X = X
        self.y = y

    def fit(self):
        self.lm.fit(self.X, self.y)

    def predict(self, X):
        return self.lm.predict(X)

    def get_coef(self):
        return self.lm.coef_

    def get_intercept(self):
        return self.lm.intercept_

    def get_residuals(self):
        y_pred = self.lm.predict(self.X)
        residuals = self.y - y_pred
        return residuals

    def get_r_squared(self):
        return self.lm.score(self.X, self.y)

    def get_adjusted_r_squared(self):
        r_squared = self.get_r_squared()
        n = len(self.y)
        p = self.X.shape[1]
        adjusted_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
        return adjusted_r_squared

    def summary(self):
        # Print features and target
        print("=" * 50)
        print("Linear Regression Summary")
        print("X features: ", self.X.columns.tolist())
        print("y target: ", self.y.name)
        print("_" * 50)

        # Compute residuals
        y_pred = self.lm.predict(self.X)
        residuals = self.y - y_pred
        residuals_np = residuals.values  # Convert to NumPy array

        # Residuals summary statistics
        residuals_summary = {
            "Min": np.min(residuals_np),
            "1Q": np.percentile(residuals_np, 25),
            "Median": np.median(residuals_np),
            "3Q": np.percentile(residuals_np, 75),
            "Max": np.max(residuals_np),
        }

        print("Residuals:")
        print("    Min      1Q  Median      3Q     Max ")
        print(
            "{Min:>8.3f} {1Q:>8.3f} {Median:>8.3f} {3Q:>8.3f} {Max:>8.3f}".format(
                **residuals_summary
            )
        )
        print()

        # Degrees of freedom
        n = len(self.y)  # Number of observations
        p = self.X.shape[1]  # Number of predictors
        df_residuals = n - p - 1  # Degrees of freedom for residuals

        # Sum of Squares
        RSS = np.sum(residuals_np**2)  # Residual Sum of Squares
        TSS = np.sum((self.y - np.mean(self.y)) ** 2)  # Total Sum of Squares

        # Mean Squares
        MSE = RSS / df_residuals  # Mean Squared Error
        RSE = np.sqrt(MSE)  # Residual Standard Error
        MSR = (TSS - RSS) / p  # Mean Square Regression

        # Design matrix with intercept
        X_design = np.column_stack((np.ones(n), self.X.values))  # Add intercept term
        XTX_inv = np.linalg.inv(X_design.T @ X_design)  # Inverse of X'X

        # Standard errors of coefficients
        var_beta = MSE * XTX_inv
        se_beta = np.sqrt(np.diag(var_beta))

        # Coefficients, t-values, p-values
        coef = np.concatenate(([self.get_intercept()], self.get_coef()))
        t_values = coef / se_beta
        p_values = [2 * (1 - stats.t.cdf(np.abs(t), df_residuals)) for t in t_values]

        # Significance stars
        def significance(p):
            if p < 0.001:
                return "***"
            elif p < 0.01:
                return "**"
            elif p < 0.05:
                return "*"
            elif p < 0.1:
                return "."
            else:
                return ""

        sig_levels = [significance(p) for p in p_values]

        # Print Coefficients table
        print("Coefficients:")
        print("             Estimate  Std. Error  t value  Pr(>|t|) ")
        for i in range(len(coef)):
            name = "(Intercept)" if i == 0 else self.X.columns[i - 1]
            print(
                "{:<12} {:>9.5f} {:>10.5f} {:>8.3f}   {:>7.4f} {}".format(
                    name, coef[i], se_beta[i], t_values[i], p_values[i], sig_levels[i]
                )
            )
        print()

        # Print significance codes
        print("Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1")
        print()

        # Residual standard error
        print(
            "Residual standard error: {:.2f} on {} degrees of freedom".format(
                RSE, df_residuals
            )
        )

        # R-squared and Adjusted R-squared
        r_squared = self.get_r_squared()
        adjusted_r_squared = self.get_adjusted_r_squared()
        print(
            "Multiple R-squared:  {:.4f},\tAdjusted R-squared:  {:.4f}".format(
                r_squared, adjusted_r_squared
            )
        )

        # F-statistic and its p-value
        F_stat = MSR / MSE
        F_p_value = 1 - stats.f.cdf(F_stat, p, df_residuals)
        print(
            "F-statistic: {:.2f} on {} and {} DF,  p-value: {:.5f}".format(
                F_stat, p, df_residuals, F_p_value
            )
        )

    def plot(self, col_data="black", col_fit="red", lw=1):
        plt.scatter(self.X, self.y, color=col_data)
        plt.plot(self.X, self.predict(self.X), color=col_fit, linewidth=lw)
        plt.xlabel(self.X.columns[0])
        plt.ylabel(self.y.name)
        plt.title("Linear Regression Fit")
        plt.show()
