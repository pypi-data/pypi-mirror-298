"""
Measurement system analysis.

Construction and presentation of gauge repeatability and reproducibility study.
"""

from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from patsy import ModelDesc
import statsmodels
from statsmodels.formula.api import mixedlm

import mqr

@dataclass
class NameMapping:
    """
    A definition of terms that maps variables in an experiment to standard terms
    in a GRR study.

    Any values not specified take their default:
    - "measurement" for a measured observation/KPI value,
    - "part" for part ID,
    - "operator" for an operator ID, and
    - "replicate" for a replicate ID/label.

    Attributes
    ----------
    measurement (str) -- Column name referring to the observation/KPI.
    part (str) -- Column name referring to the categorical part ID.
    operator (str) -- Column name referring to the categorical operator ID.
    replicate (str) -- Column name referring to the categorical replicate ID.
    """
    measurement: str = field(default='measurement')
    part: str = field(default='part')
    operator: str = field(default='operator')
    replicate: str = field(default='replicate')
    _m: str = field(repr=False, default=None)
    _p: str = field(repr=False, default=None)
    _o: str = field(repr=False, default=None)
    _r: str = field(repr=False, default=None)

    def __init__(self, *, measurement=None, part=None, operator=None, replicate=None):
        """
        Construct NameMapping.

        Optional
        ---------
        measurement (str) -- see Attribute.
        part (str) -- see Attribute.
        operation (str) -- see Attribute.
        replicate (str) -- see Attribute.
        """
        if measurement:
            self.measurement = self._m = measurement
        if part:
            self.part = self._p = part
        if operator:
            self.operator = self._o = operator
        if replicate:
            self.replicate = self._r = replicate

@dataclass
class GRR:
    """
    A Gauge Repeatability and Reliability study.

    Constructs a model and calls `statsmodels.formula.api.ols`.

    Attributes
    ----------
    data (pd.DataFrame) -- Experiment runs and measurements, including columns
        for measurement, part, operator and replicate. See `NameMapping` for how
        to name these columns.
    tolerance (np.float64) -- Width of the tolerance of the process in the same
        units as the measurements.
    names (NameMapping) -- A name mapping that defines how custom names translate
        to the standard names used in this library. See `mqr.msa.NameMapping`.
    include_interaction (bool) -- When `True`, include terms in the ANOVA for
        the interaction between operator and part.
    nsigma (int) -- Target capability of the process.

    Attributes (automatically generated)
    ------------------------------------
    formula (str) -- Formula passed to statsmodels for regression.
    counts (tuple[int]) -- Number of measurements, and number of unique levels
        in categorical variables part, operator and replicate.
    residuals (np.ndarray) -- Error values from regression.
    anova_table (pd.DataFrame) -- Table of SS and MS values with p-values from
        the standard categorical contrasts in ANOVA.
    adequacy_table (pd.DataFrame) -- Statistics relating to quality of regression
        model. See `mqr.anova.adequacy`.
    grr_table (pd.DataFrame) -- Table showing contributions to variance from
        experimental repeatability, reproducibility, operator and part.
    discrimination (np.float64) -- Discrimination index. A measure of the
        resolution of the measurement system.
    model (statsmodels.regression.linear_model.OLS) -- Model used to calculate
        the ANOVA.
    regression_result (statsmodels.regression.linear_model.RegressionResultsWrapper) --
        Result of calling `fit()` on the `model`.
    """
    data: pd.DataFrame
    tolerance: np.float64
    names: NameMapping
    include_interaction: bool
    nsigma: int

    formula: str
    counts: tuple[int]

    model: statsmodels.regression.linear_model.OLS
    regression_result: statsmodels.regression.linear_model.RegressionResultsWrapper

    def __init__(
        self,
        data:pd.DataFrame,
        tolerance:float,
        names:NameMapping=None,
        include_interaction=True,
        include_intercept=True,
        nsigma=6):
        """
        Construct GRR.

        Arguments
        ---------
        data (pd.DataFrame) -- See attribute.
        tolerance (float) -- See attribute.

        Optional
        --------
        names (mqr.msa.NameMapping) -- See attribute.
        include_interaction (bool) -- See attribute.
        nsigma (float) -- See attribute.
        """
        self.data = data
        self.tolerance = tolerance
        self.include_interaction = include_interaction
        self.include_intercept = include_intercept
        self.names = names if names is not None else NameMapping()
        self.nsigma = nsigma

        self._configure_counts()
        self._configure_formula()

        self._fit_model(data)
        self._fit_varcomp()

    def _configure_counts(self):
        cols = [self.names._p, self.names._o, self.names._r]
        self.counts = self.data.loc[:, cols].nunique(axis=0)

    def _configure_formula(self):
        name_m = self.names._m
        name_p = self.names._p
        name_o = self.names._o
        combn = '*' if self.include_interaction else '+'
        intercept = '+ 1' if self.include_intercept else '- 1'
        formula = f'{name_m} ~ C({name_p}) {combn} C({name_o}) {intercept}'
        self.formula = ModelDesc.from_formula(formula).describe()

    def _fit_model(self, data):
        self.model = statsmodels.formula.api.ols(self.formula, self.data)
        self.regression_result = self.model.fit()

    def _fit_varcomp(self):
        name_m = self.names._m
        name_p = self.names._p
        name_o = self.names._o
        vc = {
            'Error': '1',
            'Operator': f'0 + C({name_o})',
            'Part': f'0 + C({name_p})',
        }
        if self.include_interaction:
            vc['Interaction'] = f'0 + C({name_p}):C({name_o})'
        groups = np.ones(self.data.shape[0])
        mod = mixedlm(f'{name_m} ~ 1', self.data, re_formula='0', vc_formula=vc, groups=groups)
        vcomp = mod.fit().vcomp
        if self.include_interaction:
            var, var_i, var_o, var_p = vcomp
            self.variance_components = var_p, var_o, var_i, var
        else:
            var, var_o, var_p = vcomp
            self.variance_components = var_p, var_o, 0.0, var

    def _repr_html_(self):
        return SummaryTable(self)._repr_html_()

class SummaryTable:
    _grr: GRR

    def __init__(self, grr: GRR):
        self._grr = grr

    def _repr_html_(self):
        grr = self._grr
        html = f'''
            <table>
            <thead>
                <caption>Gauge Repeatability and Reliability Study</caption>
            </thead>
            <tbody>
                <thead>
                    <tr>
                        <th scope='col'></th>
                        <th scope='col'>Measurement</td>
                        <th scope='col'>Part</td>
                        <th scope='col'>Operator</td>
                        <th scope='col'>Replicate</td>
                    </tr>
                </thead>
                <tr>
                    <th scope='row'>Variable</th>
                    <td>{grr.names.measurement}</td>
                    <td>{grr.names.part}</td>
                    <td>{grr.names.operator}</td>
                    <td>{grr.names.replicate}</td>
                </tr>
                <tr>
                    <th scope='row'>Count</th>
                    <td>{grr.data.shape[0]}</td>
                    <td>{grr.counts[grr.names.part]}</td>
                    <td>{grr.counts[grr.names.operator]}</td>
                    <td>{grr.counts[grr.names.replicate]}</td>
                </tr>
                <thead><tr></tr></thead>
                <tr>
                    <th scope='row'>Tolerance</th>
                    <td>{grr.tolerance}</td>
                    <td colspan='3'></td>
                </tr>
                <tr>
                    <th scope='row'>N<sub>&#x03C3;</sub></th>
                    <td>{grr.nsigma}</td>
                    <td colspan='3'></td>
                </tr>
                <thead><tr></tr></thead>
                <tr>
                    <th scope='row'>Formula</th>
                    <td colspan='4'>{grr.formula}</td>
                </tr>
            </tbody>
            </table>
            '''
        return html

class VarianceTable:
    grr: NameMapping
    anova_table: pd.DataFrame
    table: pd.DataFrame
    num_distinct_cats: np.float64
    discrimination: np.float64

    @staticmethod
    def _table_index():
        return [
            'Gauge RR',
            'Repeatability',
            'Reproducibility',
            'Operator',
            'Operator*Part',
            'Part-to-Part',
            'Total']

    @staticmethod
    def _table_columns(nsigma):
        return [
            'VarComp',
            '% Contribution',
            'StdDev',
            f'StudyVar ({nsigma}*SD)',
            '% StudyVar',
            '% Tolerance']

    @staticmethod
    def _table_styles():
        return [
            {
                'selector': '.row_heading',
                'props': [
                    ('text-align', 'left'),
                ]
            },
            {
                'selector': 'th.row1,th.row2',
                'props': [
                    ('padding-left', '1.5em'),
                ]
            },
            {
                'selector': 'th.row3,th.row4',
                'props': [
                    ('padding-left', '3em'),
                ]
            }
        ]

    def __init__(self, grr: GRR):
        self.grr = grr
        self.anova_table = mqr.anova.summary(grr.regression_result)
        self._calculate_table(grr)
        self._set_discrimination()
        self._set_num_distinct_cats()

    def _calculate_table(self, grr):
        var_p, var_o, var_i, var = self.grr.variance_components

        table = pd.DataFrame(
            index=self._table_index(),
            columns=self._table_columns(grr.nsigma),
            dtype=np.float64)
        table.iloc[:, 0] = [
            var_o + var_i + var,         # GRR
                var,                     # Repeatability
                var_o + var_i,           # Reproducibility
                    var_o,               # Operator
                    var_i,               # Interaction
            var_p,                       # Part-to-Part
            var_p + var_o + var_i + var, # Total
        ]
        table.iloc[:, 1] = 100 * table.iloc[:, 0] / table.iloc[-1, 0]
        table.iloc[:, 2] = np.sqrt(table.iloc[:, 0])
        table.iloc[:, 3] = grr.nsigma * table.iloc[:, 2]
        table.iloc[:, 4] = 100 * table.iloc[:, 3] / table.iloc[-1, 3]
        table.iloc[:, 5] = 100 * table.iloc[:, 3] / grr.tolerance

        if not grr.include_interaction:
            table.drop(index=['Operator*Part'], inplace=True)

        self.table = table

    def _set_discrimination(self):
        var_meas = self.table.loc['Gauge RR', 'VarComp']
        var_total = self.table.loc['Total', 'VarComp']
        self.discrimination = np.sqrt(2 * var_total / var_meas - 1)

    def _set_num_distinct_cats(self):
        var_p, var_o, var_i, var = self.grr.variance_components
        self.num_distinct_cats = np.sqrt(2 * var_p / (var_o + var_i + var))

    def _repr_html_(self):
        n_cats = int(np.floor(self.num_distinct_cats))
        html = '<div style="display:flex; flex-direction:column; align-items:flex-start;">'
        html += self.table.style.set_table_styles(self._table_styles())._repr_html_()
        html += f'<div><b>Number of distinct categories:</b> {n_cats:d}</div>'
        html += '</div>'
        return html

# class ConfTable:
#     def _make_conf_int_table(self):
#         p, o, n = self.counts
#         [MS_p, MS_o, MS_i, MS_e] = self._mean_squares
#         var_grr = self.grr_table.loc['Gauge RR', 'VarComp']
#         var_p = self.grr_table.loc['Part-to-Part', 'VarComp']
#         var_tot = self.grr_table.loc['Total', 'VarComp']
#         intervals = _conf_int(p, o, n, MS_p, MS_o, MS_i, MS_e, self.alpha)
#         [
#             (var_p_lower, var_p_upper),
#             (var_grr_lower, var_grr_upper),
#             (var_tot_lower, var_tot_upper),
#             (rho_p_lower, rho_p_upper),
#             (rho_m_lower, rho_m_upper),
#         ] = intervals

#         values = np.array([
#             [var_grr, var_grr + var_grr_lower, var_grr + var_grr_upper],
#             [var_p, var_p + var_p_lower, var_p + var_p_upper],
#             [var_tot, var_tot + var_tot_lower, var_tot + var_tot_upper],
#             [np.nan, rho_m_lower*100, rho_m_upper*100],
#             [np.nan, rho_p_lower*100, rho_p_upper*100],
#         ])
#         table = pd.DataFrame(
#             values,
#             index=GRR._conf_index(),
#             columns=GRR._conf_columns(self.alpha))
#         self.conf_int_table = table

    # @staticmethod
    # def _conf_index():
    #     return [
    #         'Gauge RR',
    #         'Part-to-Part',
    #         'Total',
    #         'Gauge RR (%)',
    #         'Part-to-Part (%)',
    #     ]

    # @staticmethod
    # def _conf_columns(alpha):
    #     return [
    #         f'E(var)',
    #         f'[{100*alpha/2:.3g}%',
    #         f'{100*(1-alpha/2):.3g}%]'
    #     ]


# def _conf_int(p, o, n, MS_P, MS_O, MS_PO, MS_E, alpha=0.05):
#     # Burdick, Richard K., Connie M. Borror, and Douglas C. Montgomery. "A review of methods for measurement systems capability analysis." Journal of Quality Technology 35.4 (2003): 342-354.

#     V_LP, V_UP, V_LM, V_UM, V_LT, V_UT, L_star, U_star = _conf_int_intermediate_vals(p, o, n, MS_P, MS_O, MS_PO, MS_E, alpha)
    
#     var_p_lower = -np.sqrt(V_LP) / (o * n)
#     var_p_upper = np.sqrt(V_UP) / (o * n)

#     var_grr_lower = -np.sqrt(V_LM) / (p * n)
#     var_grr_upper = np.sqrt(V_UM) / (p * n)

#     var_tot_lower = -np.sqrt(V_LT) / (p * o * n)
#     var_tot_upper = np.sqrt(V_UT) / (p * o * n)

#     rho_p_lower = L_p = p * L_star / (p * L_star + o)
#     rho_p_upper = U_p = p * U_star / (p * U_star + o)

#     rho_m_lower = 1 - U_p
#     rho_m_upper = 1 - L_p

#     return [
#         (var_p_lower, var_p_upper),
#         (var_grr_lower, var_grr_upper),
#         (var_tot_lower, var_tot_upper),
#         (rho_p_lower, rho_p_upper),
#         (rho_m_lower, rho_m_upper),
#     ]

# def _conf_int_intermediate_vals(p, o, n, MS_P, MS_O, MS_PO, MS_E, alpha=0.05):
#     # Burdick, Richard K., Connie M. Borror, and Douglas C. Montgomery. "A review of methods for measurement systems capability analysis." Journal of Quality Technology 35.4 (2003): 342-354.
#     # But doesn't match "Introduction to Statistical Quality Control", Montgomery... need to look a bit closer at this.

#     # Distributions
#     F_p = st.chi2(p-1)
#     F_o = st.chi2(o-1)
#     F_i = st.chi2((p-1)*(o-1))
#     F_e = st.chi2(p*o*(n-1))
#     F_po = st.f(p-1, o-1)
#     F_pi = st.f(p-1, (p-1)*(o-1))

#     # Intermediate quantities
#     G_1 = 1 - 1 / F_p.ppf(1-alpha/2)
#     G_2 = 1 - 1 / F_o.ppf(1-alpha/2)
#     G_3 = 1 - 1 / F_i.ppf(1-alpha/2)
#     G_4 = 1 - 1 / F_e.ppf(1-alpha/2)

#     H_1 = 1 / F_p.ppf(alpha/2) - 1
#     H_2 = 1 / F_o.ppf(alpha/2) - 1
#     H_3 = 1 / F_i.ppf(alpha/2) - 1
#     H_4 = 1 / F_e.ppf(alpha/2) - 1

#     G_13 = ((F_pi.ppf(1-alpha/2)-1)**2 - G_1**2 * F_pi.ppf(1-alpha/2)**2 - H_3**2) / F_pi.ppf(1-alpha/2)
#     H_13 = ((1-F_pi.ppf(alpha/2))**2 - H_1**2 * F_pi.ppf(alpha/2)**2 - G_3**2) / F_pi.ppf(alpha/2)

#     V_LP = G_1**2 * MS_P**2 + H_3**2 * MS_PO**2 + G_13 * MS_P
#     V_UP = H_1**2 * MS_P**2 + G_3**2 * MS_PO**2 + H_13 * MS_P**2 * MS_PO

#     V_LM = G_2**2 * MS_O**2 + G_3**2 * (p-1)**2 * MS_PO**2 + G_4**2 * p**2 * (n-1)**2 * MS_E**2
#     V_UM = H_2**2 * MS_O**2 + H_3**2 * (p-1)**2 * MS_PO**2 + H_4**2 * p**2 * (n-1)**2 * MS_E**2

#     V_LT = G_1**2 * p**2 * MS_P**2 + G_2**2 * o**2 * MS_O**2 + G_3**2 * (p*o - p - o)**2 * MS_PO**2 + G_4**2 * (p*o)**2 * (n-1)**2 * MS_E**2
#     V_UT = H_1**2 * p**2 * MS_P**2 + H_2**2 * o**2 * MS_O**2 + H_3**2 * (p*o - p - o)**2 * MS_PO**2 + H_4**2 * (p*o)**2 * (n-1)**2 * MS_E**2

#     L_star_num = MS_P - F_pi.ppf(1-alpha/2) * MS_PO
#     L_star_den = p * (n-1) * F_p.ppf(1-alpha/2) * MS_E + F_po.ppf(1-alpha/2) * MS_O + (p-1) * F_p.ppf(1-alpha/2) * MS_PO
#     L_star = L_star_num / L_star_den

#     U_star_num = MS_P - F_pi.ppf(alpha/2) * MS_PO
#     U_star_den = p * (n-1) * F_p.ppf(alpha/2) * MS_E + F_po.ppf(alpha/2) * MS_O + (p-1) * F_p.ppf(alpha/2) * MS_PO
#     U_star = U_star_num / U_star_den

#     return V_LP, V_UP, V_LM, V_UM, V_LT, V_UT, L_star, U_star
