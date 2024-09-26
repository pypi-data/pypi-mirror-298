import os
from PIL import Image as PILImage
from IPython.display import display, Image

# Получение пути к директории с изображениями
package_dir = os.path.dirname(__file__)
image_dir = os.path.join(package_dir, "images")

def p(option=None):
    task_map = {
        1: """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import sympy as sp
import math
import warnings
import statsmodels.api as sm
warnings.filterwarnings('ignore')

data = pd.read_excel('C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx', sheet_name='Вариант 1', skiprows=[1], usecols='A:B')
data.head()

plt.figure(figsize=(15, 10))

plt.plot(data['T'], data['EMPLDEC_Y'])

plt.title('График исходного ряда')
plt.xlabel('T')
plt.ylabel('EMPLDEC_Y')
plt.grid()

plt.show()

----------------------------------------------

По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте
заявленной потребности в рабочих. Сезоннность в ряде не наблюдается,
но присутствуют реские всплески в 2008, 2014, 2021 годах.
Можно сделать предположение о том, что это связанно
с кризисным мировым положением. Экономический кризис
в начале второго десятка 21 века, кризисная ситуация
в 14 и 21 году в западной Европе.
А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией


По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте заявленной потребности в рабочих. Сезоннность в ряде не наблюдается, но присутствуют реские всплески в 2008, 2014, 2021 годах. Можно сделать предположение о том, что это связанно с кризисным мировым положением. Экономический кризис в начале второго десятка 21 века, кризисная ситуация в 14 и 21 году 
в западной Европе. А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией

----------------------------------------------

y1, y2 = np.array_split(data['EMPLDEC_Y'], 2)
n1, n2 = y1.shape[0], y2.shape[0]

y1_mean, y2_mean = y1.mean(), y2.mean()
sigma_1, sigma_2 = y1.var(), y2.var()

F = sigma_1/sigma_2
F_crit = sts.f(n1-1, n2-1).isf(0.05)

print('Гипотеза принимается') if F < F_crit else print('Гипотеза отвергается')


sigma = np.sqrt(((n1 - 1) * sigma_1 + (n2 - 1) * sigma_2)/(n1 + n2 - 2))
t = abs(y1_mean - y2_mean)/(sigma * np.sqrt(1/n1 + 1/n2))
t_crit = sts.t(n1 + n2 - 2).isf(0.05/2)

print('Тренд отсутствует') if t < t_crit else print('Тренд присутствует')

----------------------------------------------

3. Провести проверку наличия тренда с помощью метода Фостера-Стьюарта. Сравнить выводы двух тестов. (9 баллов)

----------------------------------------------

kt = []
lt = []

for i in range(1, len(data['EMPLDEC_Y'])):
    kt.append(int(data['EMPLDEC_Y'][i] > data['EMPLDEC_Y'][:i].max()))
    lt.append(int(data['EMPLDEC_Y'][i] < data['EMPLDEC_Y'][:i].min()))
    
s = sum(kt) + sum(lt)
d = sum(kt) - sum(lt)

sigma_1 = np.sqrt(2*np.log(data.shape[0]) - 3.4253)
sigma_2 = np.sqrt(2*np.log(data.shape[0]) - 0.8456)

mu = (1.693872*np.log(data.shape[0]) - 0.299015)/(1 - 0.035092*np.log(data.shape[0]) + 0.002705 * data.shape[0])

ts = abs(s - mu)/sigma_1
td = abs(s - 0)/sigma_2


t_crit = sts.t(data.shape[0]-1).isf(0.05/2)

print('Тренд ряда присутствует') if ts > t_crit else print('Тренд ряда отсутствует')

print('Тренд дисперсии присутствует') if td > t_crit else print('Тренд дисперсии отсутствует')

----------------------------------------------

Оба теста показывают наличие тренда.

----------------------------------------------

4. Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 4 периода вперед. (7 баллов)

Y = data['EMPLDEC_Y'].rolling(window=3).mean().dropna().reset_index(drop=True)

delta_y = ((Y.shift(1) - Y.shift(-1))/2).dropna()
delta_2y = ((delta_y.shift(1) - delta_y.shift(-1))/2).dropna()
exp = delta_y/Y.dropna()
ln = np.log(delta_y)
gp = np.log(exp)
lg = np.log(delta_y/Y**2).dropna()

plt.scatter(np.arange(1, len(exp)+1), exp)
plt.scatter(np.arange(1, len(ln)+1), ln)
plt.scatter(np.arange(1, len(gp)+1), gp)
plt.scatter(np.arange(1, len(lg)+1), lg)

data_train, data_test = data.iloc[:-4, :], data.iloc[-4:, :]

X = sm.add_constant(data['T'])
y = np.log(data['EMPLDEC_Y'])

model = sm.OLS(y, X).fit()

print(model.summary())

----------------------------------

X_forecast = np.arange(2022, 2026+1)
forecast = np.exp(model.predict(sm.add_constant(pd.Series(X_forecast))))

Se = np.sqrt(sum((data['EMPLDEC_Y'] - np.exp(model.predict(X)))**2)/(data.shape[0] - 1 - 1))
t = sts.t(data.shape[0] - 2).isf(0.05/2)

upper = []
lower = []

for i in range(len(forecast)):
  Sy = Se * np.sqrt(1 + 1/data.shape[0] + (X_forecast[i] - data['T'].mean())**2/
   (sum((data['T'] - data['T'].mean())**2)))
  U = Sy * t
  upper.append(forecast[i] + U)
  lower.append(forecast[i] - U)
upper = np.array(upper, dtype='float')
lower = np.array(lower, dtype='float')

----------------------------

plt.figure(figsize=(15, 10))
plt.plot(data['T'], data['EMPLDEC_Y'], label = 'Исходный ряд', color='blue')
plt.plot(data['T'], np.exp(model.predict(X)), label = 'Смоделированный ряд', color='green', linestyle='--')
plt.plot(data['T'][2:], Y, label='Сглаженный ряд', color='orange')
plt.plot(X_forecast, forecast, label = 'Предсказание', color='red', linestyle='--')
plt.fill_between(X_forecast, lower, upper, color='grey', alpha=0.6, label='Доверительный интервал')

plt.title('Прогнозирование с помощью кривой роста')
plt.legend(loc='upper left')
plt.grid()
plt.show()""",
        2: """Построить  модель, используя панельные данные, для прогнозирования коэффициента рождаемости с учетом специфики регионов РФ. 

––––––––––––––––––––––––––––––––––

1.  составить спецификацию моделей Pool, RE, FE (5 баллов)

––––––––––––––––––––––––––––––––––

import pandas as pd
import numpy as np
import scipy.stats as sts
from sklearn.preprocessing import normalize, StandardScaler, MinMaxScaler

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
import linearmodels.iv.model as lm

---------------------------------

data = pd.read_excel("C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx", sheet_name='Вариант 2', usecols='A:G', index_col=[0, 1])
data.head()

---------------------------------

sns.heatmap(data.corr(), annot=True, fmt='.2f')

plt.title('Матрица коррелированности признаков')
plt.show()

------------------------------------

data = data.drop('СООТНОШЕНИЕ Б/Р', axis=1)
data.head()

--------------------------------------

data[['БЕЗРАБОТИЦА', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']] = MinMaxScaler().fit_transform(data[['БЕЗРАБОТИЦА', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']])
data.head()

-------------------------------------

2. построить три типа моделей панельных данных, провести аналитическое исследование качества модолей. (10 баллов)

––––––––––––––––––––––––––––––––––

test = sm.add_constant(data.loc[(slice(None), 2019), :])
train = sm.add_constant(data[data.index.get_level_values('Год') != 2019])

X_train, y_train, X_test, y_test = train.drop('КОЭФ РОЖД НА 1000 ЧЕЛ', axis=1), train['КОЭФ РОЖД НА 1000 ЧЕЛ'], test.drop('КОЭФ РОЖД НА 1000 ЧЕЛ', axis=1), test['КОЭФ РОЖД НА 1000 ЧЕЛ']

---------------------------------------

Pool = PanelOLS(y_train, X_train, entity_effects=False, time_effects=False).fit()
print(Pool)

----------------------------------------

FE = PanelOLS(y_train, X_train.drop('const', axis=1), entity_effects=True, time_effects=False).fit()
print(FE)

---------------------------------------

RE = RandomEffects(y_train, X_train).fit()
print(RE)

---------------------------------------

3. провести сравнительный анализ моделей, используя тесты Фишера, Хаусмана,Бреуша-Пагана. Сделать выводы.(5 баллов)

––––––––––––––––––––––––––––––––––

# Тест Фишера(Pool VS Fixed Effects)
F = (Pool.resid_ss - FE.resid_ss)/(Pool.nobs - 1) * (FE.df_resid)/(FE.resid_ss)
F_crit = sts.f(Pool.nobs - 1, FE.df_resid).isf(0.05)

print('Модель Pool') if F < F_crit else print('Модель Fixed Effects')

----------------------------------------------------------

# Тест Хаусмана(Fixed effects VS Random Effects)
H = np.dot((FE.params - RE.params.drop('const')).T, np.linalg.inv(FE.cov - RE.cov.drop('const').drop('const', axis=1)).dot(FE.params - RE.params.drop('const')))
chi_crit = sts.chi((FE.params - RE.params).size).isf(0.05)

print('Модель Random Effects') if H > chi_crit else print('Модель Fixed Effects')
-------------------------------------------------------

# Тест Бреуша-Пагана(Pool VS Random Effects)
BP = (Pool.nobs * Pool.time_info.total)/(2*(Pool.time_info.total-1)) * ((Pool.time_info.total**2 *sum(Pool.resids.groupby(level=0).sum()**2))/(Pool.resid_ss) - 1)**2
chi_crit = sts.chi(1).isf(1)

print('Модель Random Effects') if BP > chi_crit else print('Модель Pool')
-------------------------------

Так как межгрупповая дисперсия не равна нулю, что говорит нам о том, что данные имеют различные статистики в зависимости от территории. Следовательно модель Poll не подходит. Так же исходя из результатов теста Хаусмана можно сделать вывод о том, что оценки в модели RE смещённый и несостоятельные, что говорит о неправдоподобности результаов моделирования. На основании этого берём модь FE.

––––––––––––––––––––––––––––––––––

4. Построить прогноз по лучшей модели (выбор обосновать). Результаты моделирования и прогнозирования изобразить на графике. (10 баллов)

––––––––––––––––––––––––––––––––––

modeled = np.sum(RE.predict(effects=True), axis=1)
forecast = RE.predict(X_test[X_train.columns]) + RE.predict(effects=True)[RE.predict(effects=True).index.get_level_values('Год') == 2018].estimated_effects.values.reshape(-1, 1)
modeled_renamed = modeled.rename('predictions')
forecast = pd.concat([pd.DataFrame(modeled_renamed[modeled_renamed.index.get_level_values('Год') == 2018]), forecast], axis=0)

––––––––––––––––––––––––––––––––––

for region in data.index.get_level_values('Название региона').unique():
  plt.figure(figsize=(15, 7))
  years = np.array([2017, 2018, 2019])
  plt.plot(years,
           data[data.index.get_level_values('Название региона') == region]['КОЭФ РОЖД НА 1000 ЧЕЛ'],
           label='Фактические значения',
           marker='o')
  plt.plot(years[:-1],
           modeled[modeled.index.get_level_values('Название региона') == region],
           label='Смоделированные значения',
           linestyle = '--',
           marker='x')
  print(forecast[forecast.index.get_level_values('Название региона') == region])
  plt.plot(years[-2:],
           forecast[forecast.index.get_level_values('Название региона') == region],
           label='Предсказанные значения',
           linestyle = '--',
           marker='x')

  plt.grid()
  plt.title(region)
  plt.xticks(years)
  plt.xlabel('Год')
  plt.ylabel('КОЭФ РОЖД НА 1000 ЧЕЛ')
  plt.legend(loc='lower right')
  plt.show()


""",
        3: """1. Запишите структурную форму модели в матричном виде и проведите проверку идентифицируемости системы правилами ранга и порядка (8 баллов)

–––––––––––––––

sp.init_printing()
a_11, b_11, a_21, b_21, a_31, b_31 = sp.symbols("alpha_11, beta_11, alpha_21, beta_21, alpha_31, beta_31")
a_11, b_11, a_21, b_21, a_31, b_31

----––––––––––––

M = sp.Matrix([[1, -a_11, 0, 0, -b_11],
               [0, 1, -a_21, -b_21, 0],
               [-a_31, 0, 1, -b_31, 0]])
M
----––––––––––––

R1 = sp.Matrix([[0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0]])
(M * R1.T).rank()

----––––––––––––

R2 = sp.Matrix([[1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1]])
(M * R2.T).rank()

----––––––––––––

R3 = sp.Matrix([[0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1]])
(M * R3.T).rank()

----––––––––––––

2. Какая оптимальная процедура оценивания системы, обоснуйте? Если система неидентифицируема, предложите способ для идентификации системы (5 баллов)

----––––––––––––

Методы оценивания параметров систем регрессионых уравнений

КМНК(Косвенный метод наименьших квадратов) - применяется для оценки параметров идентифицируемой системы. ДМНК(Двухшаговый метод наименьших квадратов) - применяется для оценки сверхидентифицируемых систем. ТМНК(Трёхшаговый метод наименьших квадратов) - подходит для всех видов систем, но работает хуже чем ДМНК и на параметры накладывааются ограничения

----––––––––––––

3. Оцените систему с помощью выбранной оптимальная процедуры, запишите оцененный вид спецификации. (10 баллов)

----––––––––––––

y1, y2, y3, x1, x2, x3, u1, u2, u3, b11, b12, a21, b21, a31, b31 = symbols('y_1 y_2 y_3 x_1 x_2 x_3 u_1 u_2 u_3 b_11 b_12 a_21 b_21 a_31 b_31')
eq1 = Eq(y1, b11*x1 + b12*x2)
eq2 = Eq(y2, a21*y1 + b21*x3)
eq3 = Eq(y3, a31*y2 + b31*x1)

Y = solve([eq1, eq2, eq3], [y1, y2, y3], dict=True)[0]
Y

----––––––––––––

df = pd.read_excel("C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx", sheet_name='Вариант 5', usecols='A:E')
df.head()

----––––––––––––

model1 = sm.OLS(df['y1'], df[['y2', 'x2']]).fit()
df['y1_pred'] = model1.predict()
print(model1.summary())

----––––––––––––

model2 = sm.OLS(df['y2'], df[['y3', 'x1']]).fit()
df['y2_pred'] = model2.predict()
print(model2.summary())

----––––––––––––

model3 = sm.OLS(df['y3'], df[['y1', 'x1']]).fit()
df['y3_pred'] = model3.predict()
print(model3.summary())

----––––––––––––

model11 = sm.OLS(df['y1'], df[['y2_pred', 'x2']]).fit()
df['y11_pred'] = model11.predict()
print(model11.summary())

----––––––––––––

model21 = sm.OLS(df['y2'], df[['y3_pred', 'x1']]).fit()
df['y21_pred'] = model21.predict()
print(model21.summary())

----––––––––––––

model31 = sm.OLS(df['y3'], df[['y1_pred', 'x1']]).fit()
df['y31_pred'] = model31.predict()
print(model31.summary())

----––––––––––––

4. Проиллюстрируйте графически результаты моделирования, сделайте выводы о качестве модели и о ее применимости. (7 баллов)

–––––––––––––––––

plt.plot(df['y1'])
plt.plot(df['y11_pred'])
plt.show()

----––––––––––––

plt.plot(df['y2'])
plt.plot(df['y21_pred'])
plt.show()

----––––––––––––

plt.plot(df['y3'])
plt.plot(df['y31_pred'])
plt.show()""",
        4: """data = '''2007 I	87,1
II	132,9
III	156,5
IV	226,7
2008 I	107,5
II	156,2
III	175,6
IV	223,7
2009 I	88,2
II	123,7
III	144,6
IV	203,1
2010 I	83,9
II	130,5
III	152,2
IV	225,7
2011 I	87,4
II	140,6
III	169,6
IV	259,5
2012 I	99,4
II	155,3
III	178,8
IV	267,7
2013 I	102
II	155,8
III	178,3
IV	270,8
2014 I	98,8
II	156,2
III	177,9
IV	263,4
2015 I	91,7
II	138,2
III	153,4
IV	238,9
2016 I	86
II	130,7
III	149,6
IV	246,2
2017 I	91,4
II	137,8
III	156,4
IV	255,6
2018 I	97,1
II	145,6
III	172,9
IV	260,7
2019 I	98,3
II	145,9
III	176
IV	267,5
2020 I	101,7
II	138,1
III	167,2
IV	270,8
2021 I	105,8
II	154,6
III	180,4
IV	296,6'''
data = [i.split('\t') for i in data.replace(',', '.').split('\n')]
for i in range(0, len(data), 4):
    temp = data[i][0].split()[0]
    data[i + 1][0] = temp + ' ' + data[i + 1][0]
    data[i + 2][0] = temp + ' ' + data[i + 2][0]
    data[i + 3][0] = temp + ' ' + data[i + 3][0]
    data[i][1], data[i + 1][1], data[i + 2][1], data[i + 3][1] =\
    float(data[i][1]), float(data[i + 1][1]), float(data[i + 2][1]), float(data[i + 3][1])
df = pd.DataFrame(data, columns=['T', 'INVFC_Q_DIRI'])
y = np.array(df['INVFC_Q_DIRI'])
t = np.array(df['T'])
df.head()

---------------

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y)
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
ax.set_yticks(np.arange(250, 500, 50), minor=True)
plt.title('Индекс реальных инвестиций в основной капитал (INVFC_Q_DIRI) по кварталам')
plt.grid(which = "major", linewidth = 1)
plt.grid(which = "minor", linestyle = "dashed", linewidth = 0.5);

---------------

# предварительное сглаживание, коэффициенты свои
rho = np.array([1.5, 4, 6, 7, 6, 4, 1.5])
k = rho.size
n = y.size
t1, t2 = k // 2, k - k // 2
y_new = np.array([np.dot(rho, y[i - t1:i + t2]) / rho.sum() for i in range(t1, n - t2)])
t_new = t[t1:n - t2]

--------------

1. Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна. (10 баллов

––––––––––––––

def Brown(y, a0, a1):
    mini = np.inf
    for b in np.arange(0, 1, 0.01):
        A0 = a0
        A1 = a1
        modeled = []
        for i in range(0, len(y)):
            y_hat = A0 + A1 * (i + 1)
            modeled.append(y_hat)
            ei = y[i] - y_hat
            A0 = A0 + A1 + (1 - b) ** 2 * ei
            A1 = A1 + (1 - b) ** 2 * ei
        modeled = pd.Series(modeled)
        if sum((pd.Series(np.array(y)) - modeled) ** 2) < mini:
            mini = sum((y - modeled) ** 2)
            itog_b = b
            itog_modeled = modeled
    return itog_modeled, A0, A1

# Задаем начальные параметры для адаптивной модели Брауна
a0 = y[0]
a1 = (y[1] - y[0])

# Прогнозируем с использованием модели Брауна
brown_modeled, A0, A1 = Brown(y, a0, a1)

# Визуализация
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y, label='Фактические данные')
plt.plot(t, brown_modeled, label='Модель Брауна', linestyle='--')
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
plt.title('Прогнозирование по методу Брауна')
plt.legend()
plt.grid(which="major", linewidth=1)
plt.grid(which="minor", linestyle="dashed", linewidth=0.5)
plt.show()

----------

2. Осуществить прогнозирование с применением адаптивной модели прогнозирования Хольта-Уинтерса. (10 баллов)

––––––––––

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Прогнозирование с использованием Хольта-Уинтерса
model = ExponentialSmoothing(y, seasonal='add', seasonal_periods=4)
hw_fit = model.fit()
hw_forecast = hw_fit.fittedvalues

# Визуализация
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y, label='Фактические данные')
plt.plot(t, hw_forecast, label='Модель Хольта-Уинтерса', linestyle='--')
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
plt.title('Прогнозирование по методу Хольта-Уинтерса')
plt.legend()
plt.grid(which="major", linewidth=1)
plt.grid(which="minor", linestyle="dashed", linewidth=0.5)
plt.show()

-------

"3. Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t выделить компоненты временного ряда: тренд f_t, сезонную компоненту S_t и остаточную последовательность ε_t. (10 баллов)

from ecmodels.decompose import chetverikov_decompose
chetverikov_decompose(df['INVFC_Q_DIRI'], 4)

-------""",
        5: """import numpy as np
import pandas as pd
import scipy.stats as sts
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics import tsaplots
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

import warnings
warnings.filterwarnings('ignore')

––––––––––––––––––

1. Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1)
Берём эти наборы:  1. Платина  2. Золото  3. Серебро  4. LUKOIL

–––––––––––––––––––

data = pd.read_excel('Серебро.xlsx')

––––––––––––––––––

# Доходность = (x(i+1) - x(i)) / x(i))
prof = pd.DataFrame(((data['<CLOSE>'].shift(-1) - data['<CLOSE>'])/data['<CLOSE>']).dropna())
prof.head()

––––––––––––––––––

3. Ряды 1 и 2 проверить, соответствуют ли они определению стационарных рядов. (8 баллов)

–––––––––––––––––––

Проверка ряда стоимости закрытия акций на стационарность.

–––––––––––––––––––

data['E(x_i)'] = data['<CLOSE>'].expanding().mean()

plt.plot(data['E(x_i)'][1:])
plt.title('E(x_i)')
plt.show()

––––––––––––––––––

data['VAR(x_i)'] = data['<CLOSE>'].expanding().var(ddof=1)

plt.plot(data['VAR(x_i)'][1:])
plt.title('VAR(x_i)')
plt.show()

––––––––––––––––––

COV_CLOSE = []

for i in range(1, data.shape[0]-1):
    array_1 = data['<CLOSE>'][:i+1]
    array_2 = data['<CLOSE>'][1:i+2]
    cov = np.cov(array_1, array_2, ddof=1)[0, 1]
    COV_CLOSE.append(cov)

data['COV(x_i, x_i+1)'] = [np.nan] + COV_CLOSE + [np.nan]

plt.plot(data['COV(x_i, x_i+1)'])
plt.title('COV(x_i, x_i+1)')
plt.show()

––––––––––––––––––

Исходя из графиков мат.ожидаяния, дисперсии и ковариации ряд цен не является стационарным рядом

–––––––––––––––––––

Проверка доходностей на стационарность

–––––––––––––––––––

plt.plot(prof['<CLOSE>'])

plt.title('График Доходностей')
plt.show()

––––––––––––––––––

prof['E(x_i)'] = prof['<CLOSE>'].expanding().mean()

plt.plot(prof['E(x_i)'][1:])
plt.title('E(x_i)')
plt.show()

––––––––––––––––––

prof['VAR(x_i)'] = prof['<CLOSE>'].expanding().var(ddof=1)

plt.plot(prof['VAR(x_i)'][1:])
plt.title('VAR(x_i)')
plt.show()

––––––––––––––––––

COV_CLOSE = []

for i in range(1, prof.shape[0]-1):
    array_1 = prof['<CLOSE>'][:i+1]
    array_2 = prof['<CLOSE>'][1:i+2]
    cov = np.cov(array_1, array_2, ddof=1)[0, 1]
    COV_CLOSE.append(cov)

prof['COV(x_i, x_i+1)'] = [np.nan] + COV_CLOSE + [np.nan]

plt.plot(prof['COV(x_i, x_i+1)'])
plt.title('COV(x_i, x_i+1)')
plt.show()

––––––––––––––––––

По графикам мат. ожидания, дисперсии и ковариации для доходностей ряд является стационарным. Мат. ожидание колеблется вокруг некоторого постоянного значения. График дисперсии сохраняет постоянное значение на протяжении времени и график ковариации также сохраняет постоянное значение на протяжении времени.

–––––––––––––––––––

4. Для ряда 1 построить ARIMA, для ряда 2 ARMA, выбор параметров модели обосновать. Построить прогнозы по моделям на 5 периодов вперед и сравнить с фактическими значениями. Сделать выводы о прогнозных способностях моделей. Провести их сравнение. Сделать аналитические выводы (20 баллов)

–––––––––––––––––––

ARIMA для стоимости закрытия акций

–––––––––––––––––––

# Сначала строим графики с дифференцированием. По ним определяем p и q. В ARIMA подставляем недифференцированные данные, а в параметр d указываем тот порядок по которому проводили дифференцирование. q смотрим по графику ACF выбираем лаг сильно вылетающий за синюю область, с графиком PACF делаем тоже самое только для параметра p.

fig, ax = plt.subplots(2, 1, figsize=(8, 5))
tsaplots.plot_acf(data['<CLOSE>'].diff(1).dropna(), ax=ax[0])
tsaplots.plot_pacf(data['<CLOSE>'].diff(1).dropna(), ax=ax[1])

plt.tight_layout()
plt.show()

––––––––––––––––––

X_train, X_test = data['<CLOSE>'][:-5], data['<CLOSE>'][-5: ]
ARIMA1 = ARIMA(X_train, order=(12, 1, 12)).fit()
print(ARIMA1.summary())

––––––––––––––––––

forecast = pd.concat([ARIMA1.predict().iloc[[-1]], ARIMA1.forecast(steps=5)]).reset_index(drop=True)

––––––––––––––––––

plt.figure(figsize=(15, 5))

plt.plot(data['<DATE>'][220:], data['<CLOSE>'][220:], label='Close')
plt.plot(data['<DATE>'][220:-5], ARIMA1.predict()[220:], label='Model')
plt.plot(data['<DATE>'][-6:], forecast, label='Forecast')


plt.xticks(rotation=45)
plt.title('Prediction')
plt.legend()
plt.grid()
plt.show()

––––––––––––––––––

ARMA для доходности акций

–––––––––––––––––––

# ACF По первому выходящиму за синие окно выбираем q = 12
# PCAP По первому выходящиму за синие окно выбираем p = 12

fig, ax = plt.subplots(2, 1, figsize=(8, 5))
tsaplots.plot_acf(prof['<CLOSE>'], ax=ax[0])
tsaplots.plot_pacf(prof['<CLOSE>'], ax=ax[1])

plt.tight_layout()
plt.show()

––––––––––––––––––

X_train, X_test = prof['<CLOSE>'][:-5], prof['<CLOSE>'][-5: ]
ARIMA2 = ARIMA(X_train, order=(12, 0, 12)).fit()
print(ARIMA2.summary())

––––––––––––––––––

def from_doh_to_price(forecast, X):
    prices = [X.iloc[-1] * forecast.iloc[0] + X.iloc[-1]]
    for i in range(1, len(forecast)):
        prices.append(prices[-1] * forecast.iloc[i] + prices[-1])
    return prices

––––––––––––––––––

forecast = ARIMA2.forecast(steps=5)

––––––––––––––––––

forecast_price = from_doh_to_price(forecast, data['<CLOSE>'][-6:])
forecast = [data['<CLOSE>'].iloc[-6]] + forecast_price

––––––––––––––––––

plt.figure(figsize=(15, 5))

plt.plot(data['<DATE>'][250:], data['<CLOSE>'][250:], label='Close')
plt.plot(data['<DATE>'][-6:], forecast, label='Forecast')


plt.xticks(rotation=45)
plt.title('Forecast')
plt.legend()
plt.grid()
plt.show()

–––––––––––––––––––

Сравнение моделей

––––––––––––––––––––

p, q, d, T = 12, 12, 1, len(ARIMA1.resid)
sigma_2 = sum(ARIMA1.resid**2)/T

AIC = np.log(sigma_2) + (2*(p + q + 1))/T
BIC = np.log(sigma_2) + ((p + q + 1)/T) * np.log(T)
HQC = np.log(sigma_2) + ((2*(p + q + 1))/T) * np.log(np.log(T))

print(f'ARIMA1(12, 1, 12):\nAIC = {AIC}\nBIC = {BIC}\nHQC = {HQC}')

–––––––––––––––––––

p, q, d, T = 12, 12, 0, len(ARIMA2.resid)
sigma_2 = sum(ARIMA2.resid**2)/T

AIC = np.log(sigma_2) + (2*(p + q + 1))/T
BIC = np.log(sigma_2) + ((p + q + 1)/T) * np.log(T)
HQC = np.log(sigma_2) + ((2*(p + q + 1))/T) * np.log(np.log(T))

print(f'ARMA2(12, 0, 12):\nAIC = {AIC}\nBIC = {BIC}\nHQC = {HQC}')

–––––––––––––––––––

print(f'MAE = {mean_absolute_error(X_test, ARIMA1.forecast(steps=5))}')
print(f'MAE = {mean_absolute_error(X_test, forecast_price)}')
print(f'MSE = {mean_squared_error(X_test, ARIMA1.forecast(steps=5))}')
print(f'MSE = {mean_squared_error(X_test, forecast_price)}')

–––––––––––––––––––

По информационным критериям Акаике, Шварца и Ханнана-Куина вторая модель получается лучше т.к. значение критериев меньше чем у первой модели. Модель ARIMA показала лучший результат по ошибке предсказанных значений. На основе этого выберем модель ARMA(12, 12) т.к. по информационным модель сильно выигрывает у модели ARIMA(12, 1, 12) и несильно проигрывает по ошибке MAE.  Выпишем спецификацию лючшей модели ARMA(12, 12):
выпиши сюда формулу лучшей модели """,
        6: """import numpy as np
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as sts
from fitter import Fitter
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.tsa.arima.model as smt
from statsmodels. tsa.stattools import adfuller

from sklearn.metrics import mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose

––––––––––

1. Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1) - ПЛАТИНА, САХАР, ЗОЛОТО

––––––––
gold = pd.read_excel('Золото.xlsx')

gold_close = gold['<CLOSE>']

–––––––––––––

gold_new = np.diff(gold_close, n=1)
n = gold_new.size
plt.plot(gold_new)
plt.grid();

–––––––––––––

2. Рассчитать доходность акции за выбранный период. (ряд 2) (3 балла)

––––––––––––––

shifted = gold_close.shift(1) # сдвигаем данные на шаг вперед
profitability = ((shifted-gold_close)/gold_close).iloc[1:] # рассчитываем доходность

# строим график, чтобы посмотреть на доходность
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(profitability)+1), profitability)
plt.title('')
plt.xticks(range(1, len(alum['<DATE>'])+1, 24), alum['<DATE>'][::24], rotation=45)
plt.tight_layout()
plt.title('Ряд доходности', size=15)
plt.show()

–––––––––––––––

profitability_new = np.diff(profitability, n=1)
n = profitability_new.size
plt.plot(profitability_new)
plt.grid();

–––––––––––––––

3. Ряды 1 и 2 проверить, соответствуют ли они определению стационарных рядов. (8 баллов)

–––––––––––

# Для основного ряда
means = np.array([gold_close[:i].mean() for i in range(1, n)])

plt.title('Зависимость мат.ожидания от времени')
plt.plot(np.arange(1, n), means)
plt.grid();

––––––––––––––––

s2s = np.array([gold_close[:i].var(ddof=1) for i in range(2, n)])

plt.title('Зависимость дисперсии от времени')
plt.plot(np.arange(2, n), s2s)
plt.grid();

––––––––––––––––

COV_CLOSE = []
data = pd.DataFrame()

for i in range(1, gold_close.shape[0]-1):
    array_1 = gold_close[:i+1]
    array_2 = gold_close[1:i+2]
    cov = np.cov(array_1, array_2, ddof=1)[0, 1]
    COV_CLOSE.append(cov)

data['COV(x_i, x_i+1)'] = [np.nan] + COV_CLOSE + [np.nan]

plt.plot(data['COV(x_i, x_i+1)'])
plt.title('COV(x_i, x_i+1)')
plt.show()

–––––––––––––––

# Ряд цен на золото не является не является стационарным по определению
(np.diff(gold_close)**2).sum()/((gold_close-gold_close.mean())**2).sum()

–––––––––––––––––

# Доходность
means = np.array([profitability[:i].mean() for i in range(1, n)])

plt.title('Зависимость мат.ожидания от времени')
plt.plot(np.arange(1, n), means)
plt.grid();

–––––––––––––––––

s2s = np.array([profitability[:i].var(ddof=1) for i in range(2, n)])

plt.title('Зависимость дисперсии от времени')
plt.plot(np.arange(2, n), s2s)
plt.grid();

–––––––––––––––––

COV_CLOSE = []
data = pd.DataFrame()

for i in range(1, profitability.shape[0]-1):
    array_1 = profitability[:i+1]
    array_2 = profitability[1:i+2]
    cov = np.cov(array_1, array_2, ddof=1)[0, 1]
    COV_CLOSE.append(cov)

data['COV(x_i, x_i+1)'] = [np.nan] + COV_CLOSE + [np.nan]

plt.plot(data['COV(x_i, x_i+1)'])
plt.title('COV(x_i, x_i+1)')
plt.show()

–––––––––––––––––

# Ряд доходности золота является стационарным по определению
(np.diff(profitability)**2).sum()/((profitability-profitability.mean())**2).sum()

––––––––––––––––––

5. Построить автокорреляционные функции. Построить их графики. Сделать аналитические выводы. Оценить порядок p и q в ARMA, где это возможно. (7 баллов)

–––––––––––––

# Для обычного ряда не строим, если он не стационарен. Вместо обычного ряда используем стационаризируемый - дифференцированный. В блокноте он записан
# как gold_new.

––––––––––––––––––

# Доходность

–––––––––––––––––––

# ACF - q, смотрим какой первый выходит за предел синего полотна, и выбираем соответствующий порядок для q
fig, ax = plt.subplots(figsize=(12,5))
plot_acf(profitability, lags=20, ax=ax)
plt.xlabel('Лаг')
plt.ylabel('ACF')
ax.set_xticks(list(range(21)))
plt.show()

––––––––––––––––––––

# PACF - p, смотрим какой первый выходит за предел синего полотна, и выбираем соответствующий порядок для p

fig, ax = plt.subplots(figsize=(12,5))
plot_pacf(profitability, lags=20, method='ywm', ax=ax)
plt.xlabel('Лаг')
plt.ylabel('PACF')
ax.set_xticks(list(range(21)))
plt.show()

–––––––––––––––––

6. Для ряда 2 построить: Модель AR(1), MA(2), ARMA(2,3) и провести их сравнение. Сделать аналитические выводы. Также в случае определения параметров p и q с помощью коррелограммы, построить эти модели и сравнить с AR(1), MA(2), ARMA(2,3) (12 баллов)

–––––––––––

def criterions(model):
    k = model.df_model - 1
    T = model.nobs
    dispersion = (model.resid**2).sum()/T
    print('AIC = ',  np.log(dispersion) + 2*k/T)
    print('SBIC = ', np.log(dispersion) + k*np.log(T)/T)
    print('HQIC = ', np.log(dispersion)+2*k*np.log(np.log(T))/T)
    return


–––––––––––––––––

# AR(1)
AR = smt.ARIMA(profitability, order=(1, 0, 0))
AR_fit = AR.fit()
print(AR_fit.summary())

––––––––––––––––––

criterions(AR_fit)


––––––––––––––––––

# MA(2)
MA = smt.ARIMA(profitability, order=(0, 0, 2))
MA_fit = MA.fit()
print(MA_fit.summary())

–––––––––––––––––

criterions(MA_fit)


––––––––––––––––––

#ARMA(2, 3)
ARMA = smt.ARIMA(profitability, order=(2, 0, 3))
ARMA_fit = ARMA.fit()
print(ARMA_fit.summary())

––––––––––––––––––––

criterions(ARMA_fit)

––––––––––––––––––––

# Наилучшим образом (согласно критериям Акаике, Шварца, Ханнана-Куина) себя показала модель ARMA(2, 3).
# Сравним их с моделями AR(12), MA(12), ARMA(12, 12)

––––––––––––––––––––

# AR(12)
AR_12 = smt.ARIMA(profitability, order=(12, 0, 0))
AR_12_fit = AR_12.fit()
print(AR_12_fit.summary())

––––––––––––––––––––

criterions(AR_12_fit)

––––––––––––––––––––

# MA(12)
MA_12 = smt.ARIMA(profitability_new, order=(0, 0, 12))
MA_12_fit = MA_12.fit()
print(MA_12_fit.summary())

–––––––––––––––––––

criterions(MA_12_fit)

–––––––––––––––––––

# ARMA(12, 12)
ARMA_12 = smt.ARIMA(profitability_new, order=(12, 0, 12))
ARMA_12_fit = ARMA_12.fit()
print(ARMA_12_fit.summary())

–––––––––––––––––––

criterions(ARMA_12_fit)

–––––––––––––––––––

# Сравниваем модели по принципу у кого меньше критерии. ВСЁ

–––––––––––––––––––

Лучшей по критериям Акаике, Шварца и Ханнана-Куина стала модель ARMA(12, 12) Выпишем её спецификацию:

––––––––––––––––––––

То есть коэффициенты
const   -8.722e-06  
ar.L1     -0.7792   
ar.L2     -0.6448   
ar.L3     -0.8857   
ar.L4     -0.7658   
ar.L5     -0.6869   
ar.L6     -0.7966   
ar.L7     -1.0763   
ar.L8     -0.7902   
ar.L9     -0.5320   
ar.L10    -0.2689   
ar.L11    -0.1566   
ar.L12    -0.1523   
Выписываем с
𝑌𝑡−𝑖, где 𝑖- число перед 𝐿
А эти:
ma.L1     -0.0691   
ma.L2     -0.1947   
ma.L3     0.1091   
ma.L4     0.1035   
ma.L5     -0.1330   
ma.L6     0.0645   
ma.L7     0.2160   
ma.L8     -0.2041   
ma.L9     -0.2536   
ma.L10    -0.1381   
ma.L11     0.1477   
ma.L12    -0.2268   
sigma2   6.954e-05  
Выписываем с
𝜀𝑡−𝑖, где 𝑖- число перед 𝐿
""",
7: """import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects, compare
from statsmodels.stats.diagnostic import het_breuschpagan

# Загрузка данных
data = pd.read_excel(r"C:\\Даня\\Desktop\\Книга1.xlsx")

# Предобработка данных
data = data.dropna()  # Удаление пропусков
data['year'] = data['Год']
data['region'] = data['Название региона']




# Установка индекса для панельных данных
data.set_index(['region', 'year'], inplace=True)

# Зависимая переменная
Y = data['БЕЗРАБОТИЦА']

# Независимые переменные
X = data[['СООТНОШЕНИЕ Б/Р', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ', 'КОЭФ РОЖД НА 1000 ЧЕЛ']]
X = sm.add_constant(X)

# 1. Объединенная модель
pooled_model = sm.OLS(Y, X).fit()

# 2. Модель случайных эффектов
random_model = RandomEffects(Y, X).fit()

# 3. Модель фиксированных эффектов
fixed_model = PanelOLS(Y, X).fit()

# Оценка моделей
print("Pooled OLS Results:")
print(pooled_model.summary())

print("\nRandom Effects Results:")
print(random_model)  # Если summary() вызывает ошибку

print("\nFixed Effects Results:")
print(fixed_model)  # Если summary() вызывает ошибку

from linearmodels.panel import compare
comparison = compare({'Fixed Effects': fixed_model, 'Random Effects': random_model})

# Вывод результатов теста Хаусмана
print(comparison)


# Модели случайных и фиксированных эффектов
random_model = RandomEffects(Y, X).fit()
fixed_model = PanelOLS(Y, X, entity_effects=True).fit()

# 1. Тест Фишера (результат уже включен в вывод модели фиксированных эффектов)
print("Fixed Effects Model Results (including F-test):")
print(fixed_model)



# 3. Тест Бреуша-Пагана для проверки гетероскедастичности
bp_test = het_breuschpagan(random_model.resids, random_model.model.exog)
print("\nBreusch-Pagan Test Results:")
print(f"Lagrange multiplier statistic: {bp_test[0]}")
print(f"p-value: {bp_test[1]}")
print(f"f-value: {bp_test[2]}")
print(f"f p-value: {bp_test[3]}")""",
            8: """9 вариант 

import numpy as np
import pandas as pd

data = '''2012 1 782
2 862,5
3 908,5
4 876,3
5 892,4
6 782
7 788,9
8 784,3
9 825,7
10 901,6
11 878,6
12 924,6
2013 1 752,1
2 825,7
3 874
4 874
5 811,9
6 828
7 851
8 816,5
9 869,4
10 828
11 917,7
12 959,1
2014 1 784,3
2 703,8
3 933,8
4 938,4
5 853,3
6 795,8
7 943
8 837,2
9 759
10 830,3
11 724,5
12 742,9
2015 1 558,9
2 572,7
3 653,2
4 604,9
5 611,8
6 593,4
7 538,2
8 489,9
9 517,5
10 522,1
11 494,5
12 561,2
2016 1 342,7
2 400,2
3 457,7
4 427,8
5 432,4
6 473,8
7 446,2
8 453,1
9 501,4
10 480,7
11 522,1
12 621
2017 1 512,9
2 515,2
3 627,9
4 510,6
5 556,6
6 577,3
7 480,7
8 575
9 604,9
10 616,4
11 657,8
12 729,1
2018 1 683,1
2 618,7
3 731,4
4 717,6
5 733,7
6 726,8
7 685,4
8 752,1
9 782
10 825,7
11 816,5
12 832,6
2019 1 625,6
2 699,2
3 740,6
4 724,5
5 646,3
6 644
7 662,4
8 678,5
9 706,1
10 740,6
11 706,1
12 779,7
2020 1 618,7
2 565,8
3 595,7
4 494,5
5 400,2
6 466,9
7 466,9
8 441,6
9 609,5
10 547,4
11 586,5
12 706,1
2021 1 531,3
2 595,7
3 713
4 722,2
5 690
6 874
7 894,7
8 855,6
9 901,6
10 924,6
11 966
12 1145,4
2022 1 938,4
'''

# Преобразуем данные
data = [i.split() for i in data.replace(',', '.').split('\n')]

# Для простоты добавим к каждому году его значение для всех месяцев
full_data = []
current_year = None
for row in data:
    if len(row) == 3:  # Это строка с новым годом
        current_year = row[0]
        full_data.append([f"{current_year}-{row[1]}", float(row[2])])
    elif len(row) == 2:  # Это строка с месяцем текущего года
        full_data.append([f"{current_year}-{row[0]}", float(row[1])])


df = pd.DataFrame(full_data, columns=['T', 'EX_NON-CIS_M'])

# Преобразуем данные в массивы numpy
y = np.array(df['EX_NON-CIS_M'])
t = np.array(df['T'])

# Вывод первых строк
print(df.head())

import matplotlib.pyplot as plt

# Построим график временных рядов
plt.figure(figsize=(10,6))
plt.plot(df['T'], df['EX_NON-CIS_M'], marker='o')
plt.title('Временной ряд значений EX_NON-CIS_M')
plt.xlabel('Дата')
plt.ylabel('Значение EX_NON-CIS_M')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()


#Выявление аномальных наблюдений с помощью распределения Стьюдента.
import numpy as np
import pandas as pd
from scipy import stats

# Расчёт среднего и стандартного отклонения для всего ряда
mean = df['EX_NON-CIS_M'].mean()
std = df['EX_NON-CIS_M'].std(ddof=1)  # стандартное отклонение с ddof=1 для корректного расчета

# t-статистика для каждой точки временного ряда
t_values = (df['EX_NON-CIS_M'] - mean) / std

# Критическое значение для t-распределения (двусторонний тест с alpha = 0.05)
alpha = 0.05
critical_value = stats.t.ppf(1 - alpha / 2, df.shape[0] - 1)

# Фильтрация аномалий - значения, где t-статистика превышает критическое значение
anomalies_student = df[np.abs(t_values) > critical_value]

# Выводим только аномальные наблюдения
if anomalies_student.empty:
    print("Аномальные наблюдения не найдены.")
else:
    print(f"Аномальные наблюдения по распределению Стьюдента:\n{anomalies_student}")



#4. Проверка наличия тренда с помощью метода Фостера-Стьюарта.


def foster_stuart_test(series):
    n = len(series)
    S = 0
    for i in range(n-1):
        for j in range(i+1, n):
            S += np.sign(series[j] - series[i])
    return S

# Рассчитаем тест Фостера-Стьюарта
S_value = foster_stuart_test(df['EX_NON-CIS_M'])

# Нормируем значение
Z = S_value / np.sqrt(len(df) * (len(df) - 1) * (2*len(df) + 5) / 18)

# Определим критическое значение для уровня значимости 0.05
Z_critical = stats.norm.ppf(1 - alpha / 2)

# Проверка наличия тренда
if np.abs(Z) > Z_critical:
    print("Тренд присутствует.")
else:
    print("Тренд отсутствует.")""",

9: """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Данные
data = {
    'Year': [
        '2006-1', '2006-2', '2006-3', '2006-4',
        '2007-1', '2007-2', '2007-3', '2007-4',
        '2008-1', '2008-2', '2008-3', '2008-4',
        '2009-1', '2009-2', '2009-3', '2009-4',
        '2010-1', '2010-2', '2010-3', '2010-4',
        '2011-1', '2011-2', '2011-3', '2011-4',
        '2012-1', '2012-2', '2012-3', '2012-4',
        '2013-1', '2013-2', '2013-3', '2013-4',
        '2014-1', '2014-2', '2014-3', '2014-4',
        '2015-1', '2015-2', '2015-3', '2015-4',
        '2016-1', '2016-2', '2016-3', '2016-4',
        '2017-1', '2017-2', '2017-3', '2017-4',
        '2018-1', '2018-2', '2018-3', '2018-4',
        '2019-1', '2019-2', '2019-3', '2019-4',
        '2020-1', '2020-2', '2020-3', '2020-4',
        '2021-1', '2021-2', '2021-3', '2021-4'
    ],
    'Value': [
        251.8652174, 276.873913, 316.3391304, 325.2304348,
        294.7913043, 337.7173913, 387.073913, 425.9565217,
        385.9869565, 445.1434783, 501.826087, 461.6913043,
        362.373913, 401.9478261, 452.6652174, 470.2782609,
        434.6, 477.2608696, 525.5, 576.0565217,
        566.2956522, 627.6, 684.5913043, 735.1652174,
        660.1217391, 714.6086957, 770.2521739, 816.0391304,
        711.7391304, 761.2130435, 826.2391304, 874.1,
        752.6695652, 828.0086957, 893.2173913, 962.1956522,
        802.9521739, 858.7391304, 947.3304348, 1003.469565,
        821.0913043, 889.226087, 966.7434783, 1045.373913,
        895.0478261, 952.9391304, 1031.226087, 1113.965217,
        977.1521739, 1085.643478, 1182.469565, 1270.46087,
        1067.482609, 1155.108696, 1228.065217, 1298.973913,
        1076.378261, 1028.778261, 1199.165217, 1346.434783,
        1163.956522, 1341.43913, 1474.4, 1706.956522
    ]
}

# Создание DataFrame
df = pd.DataFrame(data)
df['Year'] = pd.to_datetime(df['Year'].str.replace('-', '-01-', regex=False), format='%Y-%m-%d')
df.set_index('Year', inplace=True)

# Линейная регрессия для прогнозирования
X = np.arange(len(df)).reshape(-1, 1)
y = df['Value'].values
model = LinearRegression()
model.fit(X, y)

# Прогноз на следующие 8 кварталов
future_X = np.arange(len(df), len(df) + 8).reshape(-1, 1)
predictions = model.predict(future_X)

# Адаптивная модель Брауна
alpha = 0.2
df['Brown'] = df['Value'].ewm(alpha=alpha).mean()

# Прогноз на следующие 8 кварталов с использованием модели Брауна
brown_forecast = [df['Brown'].iloc[-1]]
for _ in range(8):
    next_value = brown_forecast[-1]
    brown_forecast.append(next_value)

# Визуализация результатов
plt.figure(figsize=(14, 12))

# Исходные данные и линейный тренд
plt.subplot(3, 1, 1)
plt.plot(df.index, df['Value'], label='Исходные данные', color='blue')
plt.plot(pd.date_range(start=df.index[-1] + pd.DateOffset(months=3), periods=8, freq='Q'), predictions, label='Линейный тренд (Прогноз)', color='red')
plt.title('Исходные данные и линейный тренд')
plt.legend()

# Адаптивная модель Брауна
plt.subplot(3, 1, 2)
plt.plot(df.index, df['Value'], label='Исходные данные', color='blue')
plt.plot(df.index, df['Brown'], label='Модель Брауна', color='green')
plt.plot(pd.date_range(start=df.index[-1] + pd.DateOffset(months=3), periods=8, freq='Q'), brown_forecast[1:], label='Прогноз Брауна', color='red')
plt.title('Адаптивная модель Брауна')
plt.legend()

# Параметры
n_seasons = 4 # Период сезонности (для кварталов)

# Выделение тренда с помощью скользящего среднего
df['Trend'] = df['Value'].rolling(window=n_seasons).mean()

# Выделение сезонной компоненты
seasonal = []
for i in range(n_seasons):
    seasonal.append(df['Value'][i::n_seasons].mean())
seasonal_full = np.tile(seasonal, len(df) // n_seasons + 1)[:len(df)]
df['Seasonal'] = seasonal_full

# Остаточная компонента
df['Residual'] = df['Value'] - df['Trend'] - df['Seasonal']

# Визуализация результатов
plt.figure(figsize=(14, 12))

# Исходный ряд и тренды
plt.subplot(3, 1, 1)
plt.plot(df.index, df['Value'], label='Исходные данные', color='blue')
plt.plot(df.index, df['Trend'], label='Тренд (Скользящее среднее)', color='orange')
plt.title('Исходный ряд и тренды')
plt.legend()

# Сезонная волна
plt.subplot(3, 1, 2)
plt.plot(df.index[:n_seasons], df['Seasonal'][:n_seasons], label='Первая сезонная волна', color='green')
plt.plot(df.index[n_seasons:2*n_seasons], df['Seasonal'][n_seasons:2*n_seasons], label='Вторая сезонная волна', color='red')
plt.title('Сезонная волна')
plt.legend()

# Остаточная компонента
plt.subplot(3, 1, 3)
plt.plot(df.index, df['Residual'], label='Остаточная компонента', color='purple')
plt.axhline(0, color='black', lw=0.5)
plt.title('Остаточная компонента')
plt.legend()

# Остатки
df['Residual'] = df['Value'] - df['Brown']
plt.subplot(3, 1, 3)
plt.plot(df.index, df['Residual'], label='Остаточная компонента', color='purple')
plt.title('Остаточная компонента')
plt.axhline(0, color='black', lw=0.5)
plt.legend()

plt.tight_layout()
plt.show()

""",

10: """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sts
import sympy as sp
import math
import warnings
import statsmodels.api as sm
warnings.filterwarnings('ignore')

data = pd.read_excel('C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx', sheet_name='Вариант 1', skiprows=[1], usecols='A:B')
data.head()

plt.figure(figsize=(15, 10))

plt.plot(data['T'], data['EMPLDEC_Y'])

plt.title('График исходного ряда')
plt.xlabel('T')
plt.ylabel('EMPLDEC_Y')
plt.grid()

plt.show()

По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте
заявленной потребности в рабочих. Сезоннность в ряде не наблюдается,
но присутствуют реские всплески в 2008, 2014, 2021 годах.
Можно сделать предположение о том, что это связанно
с кризисным мировым положением. Экономический кризис
в начале второго десятка 21 века, кризисная ситуация
в 14 и 21 году в западной Европе.
А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией


По исходному ряду можно сказать о наличии тренда и сделать вывод о будущем росте заявленной потребности в рабочих. Сезоннность в ряде не наблюдается, но присутствуют реские всплески в 2008, 2014, 2021 годах. Можно сделать предположение о том, что это связанно с кризисным мировым положением. Экономический кризис в начале второго десятка 21 века, кризисная ситуация в 14 и 21 году 
в западной Европе. А также можно сказать о росте в 2018 - 2020 годах свзанных с пандемией

y1, y2 = np.array_split(data['EMPLDEC_Y'], 2)
n1, n2 = y1.shape[0], y2.shape[0]

y1_mean, y2_mean = y1.mean(), y2.mean()
sigma_1, sigma_2 = y1.var(), y2.var()

F = sigma_1/sigma_2
F_crit = sts.f(n1-1, n2-1).isf(0.05)

print('Гипотеза принимается') if F < F_crit else print('Гипотеза отвергается')


sigma = np.sqrt(((n1 - 1) * sigma_1 + (n2 - 1) * sigma_2)/(n1 + n2 - 2))
t = abs(y1_mean - y2_mean)/(sigma * np.sqrt(1/n1 + 1/n2))
t_crit = sts.t(n1 + n2 - 2).isf(0.05/2)

print('Тренд отсутствует') if t < t_crit else print('Тренд присутствует')


3. Провести проверку наличия тренда с помощью метода Фостера-Стьюарта. Сравнить выводы двух тестов. (9 баллов)

kt = []
lt = []

for i in range(1, len(data['EMPLDEC_Y'])):
    kt.append(int(data['EMPLDEC_Y'][i] > data['EMPLDEC_Y'][:i].max()))
    lt.append(int(data['EMPLDEC_Y'][i] < data['EMPLDEC_Y'][:i].min()))
    
s = sum(kt) + sum(lt)
d = sum(kt) - sum(lt)

sigma_1 = np.sqrt(2*np.log(data.shape[0]) - 3.4253)
sigma_2 = np.sqrt(2*np.log(data.shape[0]) - 0.8456)

mu = (1.693872*np.log(data.shape[0]) - 0.299015)/(1 - 0.035092*np.log(data.shape[0]) + 0.002705 * data.shape[0])

ts = abs(s - mu)/sigma_1
td = abs(s - 0)/sigma_2


t_crit = sts.t(data.shape[0]-1).isf(0.05/2)

print('Тренд ряда присутствует') if ts > t_crit else print('Тренд ряда отсутствует')

print('Тренд дисперсии присутствует') if td > t_crit else print('Тренд дисперсии отсутствует')

Оба теста показывают наличие тренда.

----------------------------------------------

4. Провести прогнозирование с помощью кривой роста. Рассчитать точечный и интервальный прогноз на 4 периода вперед. (7 баллов)

Y = data['EMPLDEC_Y'].rolling(window=3).mean().dropna().reset_index(drop=True)

delta_y = ((Y.shift(1) - Y.shift(-1))/2).dropna()
delta_2y = ((delta_y.shift(1) - delta_y.shift(-1))/2).dropna()
exp = delta_y/Y.dropna()
ln = np.log(delta_y)
gp = np.log(exp)
lg = np.log(delta_y/Y**2).dropna()

plt.scatter(np.arange(1, len(exp)+1), exp)
plt.scatter(np.arange(1, len(ln)+1), ln)
plt.scatter(np.arange(1, len(gp)+1), gp)
plt.scatter(np.arange(1, len(lg)+1), lg)

data_train, data_test = data.iloc[:-4, :], data.iloc[-4:, :]

X = sm.add_constant(data['T'])
y = np.log(data['EMPLDEC_Y'])

model = sm.OLS(y, X).fit()

print(model.summary())

----------------------------------

X_forecast = np.arange(2022, 2026+1)
forecast = np.exp(model.predict(sm.add_constant(pd.Series(X_forecast))))

Se = np.sqrt(sum((data['EMPLDEC_Y'] - np.exp(model.predict(X)))**2)/(data.shape[0] - 1 - 1))
t = sts.t(data.shape[0] - 2).isf(0.05/2)

upper = []
lower = []

for i in range(len(forecast)):
  Sy = Se * np.sqrt(1 + 1/data.shape[0] + (X_forecast[i] - data['T'].mean())**2/
   (sum((data['T'] - data['T'].mean())**2)))
  U = Sy * t
  upper.append(forecast[i] + U)
  lower.append(forecast[i] - U)
upper = np.array(upper, dtype='float')
lower = np.array(lower, dtype='float')

----------------------------

plt.figure(figsize=(15, 10))
plt.plot(data['T'], data['EMPLDEC_Y'], label = 'Исходный ряд', color='blue')
plt.plot(data['T'], np.exp(model.predict(X)), label = 'Смоделированный ряд', color='green', linestyle='--')
plt.plot(data['T'][2:], Y, label='Сглаженный ряд', color='orange')
plt.plot(X_forecast, forecast, label = 'Предсказание', color='red', linestyle='--')
plt.fill_between(X_forecast, lower, upper, color='grey', alpha=0.6, label='Доверительный интервал')

plt.title('Прогнозирование с помощью кривой роста')
plt.legend(loc='upper left')
plt.grid()
plt.show()""",
11: """data = '''2007 I	87,1
II	132,9
III	156,5
IV	226,7
2008 I	107,5
II	156,2
III	175,6
IV	223,7
2009 I	88,2
II	123,7
III	144,6
IV	203,1
2010 I	83,9
II	130,5
III	152,2
IV	225,7
2011 I	87,4
II	140,6
III	169,6
IV	259,5
2012 I	99,4
II	155,3
III	178,8
IV	267,7
2013 I	102
II	155,8
III	178,3
IV	270,8
2014 I	98,8
II	156,2
III	177,9
IV	263,4
2015 I	91,7
II	138,2
III	153,4
IV	238,9
2016 I	86
II	130,7
III	149,6
IV	246,2
2017 I	91,4
II	137,8
III	156,4
IV	255,6
2018 I	97,1
II	145,6
III	172,9
IV	260,7
2019 I	98,3
II	145,9
III	176
IV	267,5
2020 I	101,7
II	138,1
III	167,2
IV	270,8
2021 I	105,8
II	154,6
III	180,4
IV	296,6'''
data = [i.split('\t') for i in data.replace(',', '.').split('\n')]
for i in range(0, len(data), 4):
    temp = data[i][0].split()[0]
    data[i + 1][0] = temp + ' ' + data[i + 1][0]
    data[i + 2][0] = temp + ' ' + data[i + 2][0]
    data[i + 3][0] = temp + ' ' + data[i + 3][0]
    data[i][1], data[i + 1][1], data[i + 2][1], data[i + 3][1] =\
    float(data[i][1]), float(data[i + 1][1]), float(data[i + 2][1]), float(data[i + 3][1])
df = pd.DataFrame(data, columns=['T', 'INVFC_Q_DIRI'])
y = np.array(df['INVFC_Q_DIRI'])
t = np.array(df['T'])
df.head()

---------------

fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y)
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
ax.set_yticks(np.arange(250, 500, 50), minor=True)
plt.title('Индекс реальных инвестиций в основной капитал (INVFC_Q_DIRI) по кварталам')
plt.grid(which = "major", linewidth = 1)
plt.grid(which = "minor", linestyle = "dashed", linewidth = 0.5);

---------------

# предварительное сглаживание, коэффициенты свои
rho = np.array([1.5, 4, 6, 7, 6, 4, 1.5])
k = rho.size
n = y.size
t1, t2 = k // 2, k - k // 2
y_new = np.array([np.dot(rho, y[i - t1:i + t2]) / rho.sum() for i in range(t1, n - t2)])
t_new = t[t1:n - t2]

--------------

1. Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна. (10 баллов

def Brown(y, a0, a1):
    mini = np.inf
    for b in np.arange(0, 1, 0.01):
        A0 = a0
        A1 = a1
        modeled = []
        for i in range(0, len(y)):
            y_hat = A0 + A1 * (i + 1)
            modeled.append(y_hat)
            ei = y[i] - y_hat
            A0 = A0 + A1 + (1 - b) ** 2 * ei
            A1 = A1 + (1 - b) ** 2 * ei
        modeled = pd.Series(modeled)
        if sum((pd.Series(np.array(y)) - modeled) ** 2) < mini:
            mini = sum((y - modeled) ** 2)
            itog_b = b
            itog_modeled = modeled
    return itog_modeled, A0, A1

# Задаем начальные параметры для адаптивной модели Брауна
a0 = y[0]
a1 = (y[1] - y[0])

# Прогнозируем с использованием модели Брауна
brown_modeled, A0, A1 = Brown(y, a0, a1)

# Визуализация
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y, label='Фактические данные')
plt.plot(t, brown_modeled, label='Модель Брауна', linestyle='--')
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
plt.title('Прогнозирование по методу Брауна')
plt.legend()
plt.grid(which="major", linewidth=1)
plt.grid(which="minor", linestyle="dashed", linewidth=0.5)
plt.show()

----------

2. Осуществить прогнозирование с применением адаптивной модели прогнозирования Хольта-Уинтерса. (10 баллов)

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Прогнозирование с использованием Хольта-Уинтерса
model = ExponentialSmoothing(y, seasonal='add', seasonal_periods=4)
hw_fit = model.fit()
hw_forecast = hw_fit.fittedvalues

# Визуализация
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
plt.plot(t, y, label='Фактические данные')
plt.plot(t, hw_forecast, label='Модель Хольта-Уинтерса', linestyle='--')
plt.xticks(t[::8], labels=t[::8])
ax.set_xticks(t[::2], minor=True)
plt.title('Прогнозирование по методу Хольта-Уинтерса')
plt.legend()
plt.grid(which="major", linewidth=1)
plt.grid(which="minor", linestyle="dashed", linewidth=0.5)
plt.show()

-------

"3. Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t выделить компоненты временного ряда: тренд f_t, сезонную компоненту S_t и остаточную последовательность ε_t. (10 баллов)

from ecmodels.decompose import chetverikov_decompose
chetverikov_decompose(df['INVFC_Q_DIRI'], 4)

-------""",
12: """Построить  модель, используя панельные данные, для прогнозирования коэффициента рождаемости с учетом специфики регионов РФ. 
1.  составить спецификацию моделей (Pool, RE, FE (5 баллов)

import pandas as pd
import numpy as np
import scipy.stats as sts
from sklearn.preprocessing import normalize, StandardScaler, MinMaxScaler

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from linearmodels.panel import PanelOLS, RandomEffects
import linearmodels.iv.model as lm

---------------------------------

data = pd.read_excel("C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx", sheet_name='Вариант 2', usecols='A:G', index_col=[0, 1])
data.head()

---------------------------------

sns.heatmap(data.corr(), annot=True, fmt='.2f')

plt.title('Матрица коррелированности признаков')
plt.show()

------------------------------------

data = data.drop('СООТНОШЕНИЕ Б/Р', axis=1)
data.head()

--------------------------------------

data[['БЕЗРАБОТИЦА', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']] = MinMaxScaler().fit_transform(data[['БЕЗРАБОТИЦА', 'ИПЦ НА ЖИЛЬЕ', 'ИПЦ НА ПРОД ТОВАРЫ']])
data.head()

-------------------------------------

2. построить три типа моделей панельных данных, провести аналитическое исследование качества модолей. (10 баллов)

test = sm.add_constant(data.loc[(slice(None), 2019), :])
train = sm.add_constant(data[data.index.get_level_values('Год') != 2019])

X_train, y_train, X_test, y_test = train.drop('КОЭФ РОЖД НА 1000 ЧЕЛ', axis=1), train['КОЭФ РОЖД НА 1000 ЧЕЛ'], test.drop('КОЭФ РОЖД НА 1000 ЧЕЛ', axis=1), test['КОЭФ РОЖД НА 1000 ЧЕЛ']

---------------------------------------

Pool = PanelOLS(y_train, X_train, entity_effects=False, time_effects=False).fit()
print(Pool)

----------------------------------------

FE = PanelOLS(y_train, X_train.drop('const', axis=1), entity_effects=True, time_effects=False).fit()
print(FE)

---------------------------------------

RE = RandomEffects(y_train, X_train).fit()
print(RE)

---------------------------------------

3. провести сравнительный анализ моделей, используя тесты Фишера, Хаусмана,Бреуша-Пагана. Сделать выводы.(5 баллов)

# Тест Фишера(Pool VS Fixed Effects)
F = (Pool.resid_ss - FE.resid_ss)/(Pool.nobs - 1) * (FE.df_resid)/(FE.resid_ss)
F_crit = sts.f(Pool.nobs - 1, FE.df_resid).isf(0.05)

print('Модель Pool') if F < F_crit else print('Модель Fixed Effects')
----------------------------------------------------------

# Тест Хаусмана(Fixed effects VS Random Effects)
H = np.dot((FE.params - RE.params.drop('const')).T, np.linalg.inv(FE.cov - RE.cov.drop('const').drop('const', axis=1)).dot(FE.params - RE.params.drop('const')))
chi_crit = sts.chi((FE.params - RE.params).size).isf(0.05)

print('Модель Random Effects') if H > chi_crit else print('Модель Fixed Effects')
-------------------------------------------------------

# Тест Бреуша-Пагана(Pool VS Random Effects)
BP = (Pool.nobs * Pool.time_info.total)/(2*(Pool.time_info.total-1)) * ((Pool.time_info.total**2 *sum(Pool.resids.groupby(level=0).sum()**2))/(Pool.resid_ss) - 1)**2
chi_crit = sts.chi(1).isf(1)

print('Модель Random Effects') if BP > chi_crit else print('Модель Pool')
-------------------------------

Так как межгрупповая дисперсия не равна нулю, что говорит нам о том, что данные имеют различные статистики в зависимости от территории. Следовательно модель Poll не подходит. Так же исходя из результатов теста Хаусмана можно сделать вывод о том, что оценки в модели RE смещённый и несостоятельные, что говорит о неправдоподобности результаов моделирования. На основании этого берём модь FE.

4. Построить прогноз по лучшей модели (выбор обосновать). Результаты моделирования и прогнозирования изобразить на графике. (10 баллов)

modeled = np.sum(RE.predict(effects=True), axis=1)
forecast = RE.predict(X_test[X_train.columns]) + RE.predict(effects=True)[RE.predict(effects=True).index.get_level_values('Год') == 2018].estimated_effects.values.reshape(-1, 1)
modeled_renamed = modeled.rename('predictions')
forecast = pd.concat([pd.DataFrame(modeled_renamed[modeled_renamed.index.get_level_values('Год') == 2018]), forecast], axis=0)
----------------

for region in data.index.get_level_values('Название региона').unique():
  plt.figure(figsize=(15, 7))
  years = np.array([2017, 2018, 2019])
  plt.plot(years,
           data[data.index.get_level_values('Название региона') == region]['КОЭФ РОЖД НА 1000 ЧЕЛ'],
           label='Фактические значения',
           marker='o')
  plt.plot(years[:-1],
           modeled[modeled.index.get_level_values('Название региона') == region],
           label='Смоделированные значения',
           linestyle = '--',
           marker='x')
  print(forecast[forecast.index.get_level_values('Название региона') == region])
  plt.plot(years[-2:],
           forecast[forecast.index.get_level_values('Название региона') == region],
           label='Предсказанные значения',
           linestyle = '--',
           marker='x')

  plt.grid()
  plt.title(region)
  plt.xticks(years)
  plt.xlabel('Год')
  plt.ylabel('КОЭФ РОЖД НА 1000 ЧЕЛ')
  plt.legend(loc='lower right')
  plt.show()


""",
13: """1. Запишите структурную форму модели в матричном виде и проведите проверку идентифицируемости системы правилами ранга и порядка (8 баллов)

sp.init_printing()
a_11, b_11, a_21, b_21, a_31, b_31 = sp.symbols("alpha_11, beta_11, alpha_21, beta_21, alpha_31, beta_31")
a_11, b_11, a_21, b_21, a_31, b_31

---------------

M = sp.Matrix([[1, -a_11, 0, 0, -b_11],
               [0, 1, -a_21, -b_21, 0],
               [-a_31, 0, 1, -b_31, 0]])
M
-------------

R1 = sp.Matrix([[0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0]])
(M * R1.T).rank()

---------------

R2 = sp.Matrix([[1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1]])
(M * R2.T).rank()

---------------

R3 = sp.Matrix([[0, 1, 0, 0, 0],
                [0, 0, 0, 0, 1]])
(M * R3.T).rank()

--------------

2. Какая оптимальная процедура оценивания системы, обоснуйте? Если система неидентифицируема, предложите способ для идентификации системы (5 баллов)

Методы оценивания параметров систем регрессионых уравнений

КМНК(Косвенный метод наименьших квадратов) - применяется для оценки параметров идентифицируемой системы. ДМНК(Двухшаговый метод наименьших квадратов) - применяется для оценки сверхидентифицируемых систем. ТМНК(Трёхшаговый метод наименьших квадратов) - подходит для всех видов систем, но работает хуже чем ДМНК и на параметры накладывааются ограничения

--------------

3. Оцените систему с помощью выбранной оптимальная процедуры, запишите оцененный вид спецификации. (10 баллов)

y1, y2, y3, x1, x2, x3, u1, u2, u3, b11, b12, a21, b21, a31, b31 = symbols('y_1 y_2 y_3 x_1 x_2 x_3 u_1 u_2 u_3 b_11 b_12 a_21 b_21 a_31 b_31')
eq1 = Eq(y1, b11*x1 + b12*x2)
eq2 = Eq(y2, a21*y1 + b21*x3)
eq3 = Eq(y3, a31*y2 + b31*x1)

Y = solve([eq1, eq2, eq3], [y1, y2, y3], dict=True)[0]
Y

---------

df = pd.read_excel("C:\\Users\\Mikhail\\Downloads\\Пересдача по эконометрике.xlsx", sheet_name='Вариант 5', usecols='A:E')
df.head()

---------

model1 = sm.OLS(df['y1'], df[['y2', 'x2']]).fit()
df['y1_pred'] = model1.predict()
print(model1.summary())

--------

model2 = sm.OLS(df['y2'], df[['y3', 'x1']]).fit()
df['y2_pred'] = model2.predict()
print(model2.summary())

--------

model3 = sm.OLS(df['y3'], df[['y1', 'x1']]).fit()
df['y3_pred'] = model3.predict()
print(model3.summary())

--------

model11 = sm.OLS(df['y1'], df[['y2_pred', 'x2']]).fit()
df['y11_pred'] = model11.predict()
print(model11.summary())

------

model21 = sm.OLS(df['y2'], df[['y3_pred', 'x1']]).fit()
df['y21_pred'] = model21.predict()
print(model21.summary())

-----

model31 = sm.OLS(df['y3'], df[['y1_pred', 'x1']]).fit()
df['y31_pred'] = model31.predict()
print(model31.summary())

----

4. Проиллюстрируйте графически результаты моделирования, сделайте выводы о качестве модели и о ее применимости. (7 баллов)

plt.plot(df['y1'])
plt.plot(df['y11_pred'])
plt.show()

-----

plt.plot(df['y2'])
plt.plot(df['y21_pred'])
plt.show()

------

plt.plot(df['y3'])
plt.plot(df['y31_pred'])
plt.show()""",

14: """df = pd.read_excel(r'Пересдача по эконометрике.xlsx', sheet_name='Вариант 3')
df.head()

from sklearn.model_selection import train_test_split
y, X = df['Class'], df.drop(['AREA','Class'],axis=1)
X = sm.add_constant(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7) 
logit = sm.Logit(y_train, X_train)
res1 = logit.fit()
print(res1.summary())
probit = sm.Probit(y_train, X_train)
res2 = probit.fit()
print(res2.summary())


y, X = df['Class'], df.drop(['AREA','Class'],axis=1)
X = sm.add_constant(X)
n = len(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)
X_train = X_train.drop(['SHAPEFACTOR_3', 'PERIMETER', 'SHAPEFACTOR_4', 'SHAPEFACTOR_2'], axis=1)
X_test = X_test.drop(['SHAPEFACTOR_3', 'PERIMETER', 'SHAPEFACTOR_4', 'SHAPEFACTOR_2'], axis=1)
logit = sm.Logit(y_train, X_train).fit()
print(logit.summary())

probit = sm.Probit(y_train, X_train).fit()
print(probit.summary())

print(logit.get_margeff().summary())
print(probit.get_margeff().summary())

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1score = f1_score(y_test, y_pred)

print(f"Precision = {precision}")
print(f"Recall = {recall}")
print(f"F1 Score = {f1score}")
print(f"Accuracy = {accuracy}")""",
15: """

1.  Предварительный анализ временных рядов. Построить график и провести
    визуальный анализ. Результаты описать. (5 баллов)

    import pandas as pd
    import scipy.stats as sts
    import numpy as np
    import sympy as sp
    import matplotlib.pyplot as plt
    import copy
    import math

    data = pd.read_excel('Пересдача по эконометрике.xlsx', sheet_name='Вариант 12', usecols='A, B')
    n = len(data)
    data

---------------------------------------------------------------------------------------------------------

    data = data.drop(index=0).reset_index(drop=True)
    data

  
2.Провести выявление аномальных наблюдений с помощью использования
распределения Стьюдента, Метода Ирвина. Написать выводы. Использовать
один метод на выбор. Выбор обосновать. (9 баллов)

Метод Ирвина: используется для выявления резких изменений между
соседними наблюдениями. Подходит, если вы подозреваете наличие
значительных скачков между последовательными точками временного ряда.
Распределение Стьюдента: используется для поиска выбросов в малых
выборках или если данные подчиняются нормальному распределению.
Позволяет выявить выбросы, которые сильно отклоняются от среднего
значения.

==============================================================================================

    # Вычисляем разности между соседними точками
    data['Difference'] = data['EX_NON-CIS_Y'].diff()

    # Определяем порог для аномалий (3 стандартных отклонения)
    threshold = data['Difference'].std() * 3

    # Определение аномалий
    data['Anomaly_Irwin'] = data['Difference'].abs() > threshold

    # Отображение аномалий
    anomalies_irwin = data[data['Anomaly_Irwin']]
    print(anomalies_irwin)

=============================================================================================

    # Вычисляем среднее и стандартное отклонение
    mean_val = data['EX_NON-CIS_Y'].mean()
    std_dev = data['EX_NON-CIS_Y'].std()

    # Выявляем выбросы по критерию Стьюдента (3 стандартных отклонения)
    data['Anomaly_Student'] = np.abs(data['EX_NON-CIS_Y'] - mean_val) > (3 * std_dev)

    # Отображение аномалий
    anomalies_student = data[data['Anomaly_Student']]
    print(anomalies_student)

1.  Провести проверку наличия тренда с помощью: Критерия серий,
    основанный на медиане, Метода проверки разности средних уровней,
    Метода Фостера-Стьюарта. Использовать один метод на выбор. Выбор
    обосновать. (9 баллов)

Выбор метода зависит от типа данных и структуры временного ряда:

Критерий серий, основанный на медиане: Подходит для данных, где важно
проверить случайное распределение значений относительно медианы.
Используется для общего анализа наличия тренда. Метод проверки разности
средних уровней: Применяется, когда необходимо проверить, различаются ли
средние значения двух половин временного ряда. Этот метод эффективен,
если вы ожидаете различия между ранними и более поздними наблюдениями.
Метод Фостера-Стьюарта: Подходит для данных, где важны изменения
максимумов и минимумов. Часто применяется, когда необходимо проверить
устойчивость тренда, связанного с экстремумами временного ряда. Выбор
метода зависит от конкретных свойств данных. Например, если вы
подозреваете, что изменения в тренде происходят неравномерно (например,
данные содержат чередующиеся максимумы и минимумы), можно выбрать Метод
Фостера-Стьюарта. Если же вы хотите проверить, отличаются ли два периода
наблюдений, подойдет Метод проверки разности средних уровней.

    #Критерий серий, основанный на медиане
    from statsmodels.sandbox.stats.runs import runstest_1samp

    # Рассчитываем медиану
    median_value = data['EX_NON-CIS_Y'].median()

    # Создаем бинарный ряд: 1 для значений выше медианы, 0 — для значений ниже медианы
    binary_series = np.where(data['EX_NON-CIS_Y'] > median_value, 1, 0)

    # Применяем критерий серий
    z_stat, p_value = runstest_1samp(binary_series, correction=True)

    # Выводим статистику теста
    print(f"Z-статистика: {z_stat}, p-значение: {p_value}")

    # Если p-значение меньше 0.05, мы отвергаем гипотезу о случайности (тренд присутствует)
    if p_value < 0.05:
        print("Тренд присутствует")
    else:
        print("Тренд отсутствует")

====================================================================================================

    # Метода проверки разности средних уровней
    half = len(data) // 2
    first_half = data['EX_NON-CIS_Y'][:half]
    second_half = data['EX_NON-CIS_Y'][half:]

    # Рассчитываем средние значения
    mean_first_half = first_half.mean()
    mean_second_half = second_half.mean()

    # Рассчитываем стандартные отклонения для обеих половин
    std_first_half = np.std(first_half, ddof=1)
    std_second_half = np.std(second_half, ddof=1)

    # Рассчитываем общий стандартный показатель (пул стандартных отклонений)
    pooled_std = np.sqrt(((len(first_half) - 1) * std_first_half**2 + (len(second_half) - 1) * std_second_half**2) / (len(data) - 2))

    # Рассчитываем t-статистику для разности средних уровней
    t_stat = np.abs(mean_first_half - mean_second_half) / (pooled_std * np.sqrt(1/len(first_half) + 1/len(second_half)))

    # Критическое значение t для уровня значимости 0.05
    t_critical = sts.t.ppf(1 - 0.05/2, df=len(data)-2)

    # Выводим результаты
    print(f"t-статистика: {t_stat}, критическое значение t: {t_critical}")

    # Если t-статистика больше критического значения, тренд присутствует
    if t_stat > t_critical:
        print("Тренд присутствует")
    else:
        print("Тренд отсутствует")

===================================================================================================

    #Метод Фостера-Стьюарта
    # Рассчитываем последовательность максимумов
    max_seq = [1 if data['EX_NON-CIS_Y'][i] > max(data['EX_NON-CIS_Y'][:i]) else 0 for i in range(1, len(data))]
    max_seq = np.array(max_seq)

    # Рассчитываем последовательность минимумов
    min_seq = [1 if data['EX_NON-CIS_Y'][i] < min(data['EX_NON-CIS_Y'][:i]) else 0 for i in range(1, len(data))]
    min_seq = np.array(min_seq)

    # Суммируем максимумы и минимумы
    s = np.sum(max_seq + min_seq)
    d = np.sum(max_seq - min_seq)

    # Рассчитываем статистику по методу Фостера-Стьюарта
    mu_s = (1.693872 * np.log(len(data)) - 0.299015) / (1 - 0.035092 * np.log(len(data)) + 0.002705 * np.log(len(data))**2)
    sigma_s = np.sqrt(2 * np.log(len(data)) - 3.4253)
    ts = np.abs(s - mu_s) / sigma_s

    # Рассчитываем статистику для d
    sigma_d = np.sqrt(2 * np.log(len(data)) - 0.8456)
    td = np.abs(d) / sigma_d

    # Критическое значение t для уровня значимости 0.05
    t_critical = sts.t.ppf(1 - 0.05/2, df=len(data)-2)

    # Выводим результаты
    print(f"ts-статистика: {ts}, td-статистика: {td}, критическое значение t: {t_critical}")

    # Если ts или td больше критического значения, тренд присутствует
    if ts > t_critical or td > t_critical:
        print("Присутствует значимый тренд")
    else:
        print("Тренд отсутствует")

========================================================================================================================

4.  Провести сглаживание временных рядов с помощью: Взвешенной
    (средневзвешенной) скользящей средней, а также провести
    Экспоненциальное сглаживание. Привести аналитические выводы. (7
    баллов)

    # Применяем взвешенное скользящее среднее с весами [0.1, 0.2, 0.3, 0.4]
    weights = [0.1, 0.2, 0.3, 0.4]
    data['Weighted_MA'] = data['EX_NON-CIS_Y'].rolling(window=4).apply(lambda x: np.dot(x, weights), raw=True)

=============================================================================================================================

    # Применяем экспоненциальное сглаживание с фактором сглаживания alpha
    alpha = 0.3
    data['Exponential_Smoothing'] = data['EX_NON-CIS_Y'].ewm(alpha=alpha).mean()

    # Построим графики для обоих методов
    plt.figure(figsize=(10, 6))
    plt.plot(data['T'], data['EX_NON-CIS_Y'], label='Оригинальные данные')
    plt.plot(data['T'], data['Weighted_MA'], label='Взвешенное скользящее среднее')
    plt.plot(data['T'], data['Exponential_Smoothing'], label='Экспоненциальное сглаживание')
    plt.legend()
    plt.show()

==============================================================================================================================

Пример выводов Взвешенное скользящее среднее:

Оранжевая линия сглаживания повторяет основные тренды оригинальных
данных, но с меньшими отклонениями. Она более плавная по сравнению с
оригинальными данными, особенно в периоде между 2005 и 2010 годами, где
резкие скачки заменяются более плавным переходом. Этот метод лучше
подходит для долгосрочного анализа, так как уменьшает влияние
краткосрочных колебаний и выделяет общие тренды. Экспоненциальное
сглаживание:

Зеленая линия сглаживания сильнее сглаживает данные в целом, особенно в
периодах с резкими скачками. Этот метод более "мягкий" по сравнению с
взвешенным скользящим средним. Он лучше подходит для прогнозирования,
если мы ожидаем, что недавние данные важнее старых наблюдений.
Экспоненциальное сглаживание особенно полезно при анализе последних лет,
так как реагирует на краткосрочные изменения более динамично (например,
на рост после 2020 года). Сравнение методов:

Оба метода эффективно сгладили резкие колебания, но взвешенное
скользящее среднее лучше показало моменты роста и падения в данные
2010–2015 годов, в то время как экспоненциальное сглаживание лучше
реагирует на последние наблюдения (особенно с 2020 года). Если нужно
выделить долгосрочные тенденции, то взвешенное скользящее среднее более
предпочтительно. Если же важны последние данные и краткосрочные
колебания, то экспоненциальное сглаживание даёт более "быстрый"
результат.
""",
16: """

1.    Скачать с любого сайта данные о дневных ценах закрытия выбранной
Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1)

    import pandas as pd
    import statsmodels.api as sm
    from statsmodels.tsa.arima.model import ARIMA
    import numpy as np
    from statsmodels.tsa.statespace.sarimax import SARIMAX

==========================================================================================


    # Загрузка данных - цены закрытия акций  "ВСТАВЬТЕНУЖНОЕ"  с 01.06.21 по 01.06.2022
    data = pd.read_excel('/content/Цена Сбер.xlsx')
    data


2.    Рассчитать доходность акции за выбранный период. (ряд 2) (3 балла)

    # Рассчитываем доходность
    profitability = data['CLOSE'].pct_change()
    data['PROFITABILITY'] = profitability

    data

1.  Ряды 1 и 2 проверить, соответствуют ли они определению стационарных
    рядов. (8 баллов)

Для проверки рядов на стационарность воспользуемся интеграционной
статистокой Дарбина-Уотсона(IDW)

    # первый ряд
    close_prices = data['CLOSE']

    # Рассчитываем квадрат разности текущего и предыдущего элемента
    difs_CLOSE = [(close_prices[i] - close_prices[i-1]) ** 2 for i in range(1, len(close_prices))]

    num_CLOSE = sum(difs_CLOSE)

    num_CLOSE

    mean_close = close_prices.mean()
    # Рассчитываем квадрат разности текущего и среднего значения
    difs_CLOSE2 = [(price - mean_close) ** 2 for price in close_prices]

    denum_CLOSE = sum(difs_CLOSE2)

    denum_CLOSE

    IDW_CLOSE = num_CLOSE/denum_CLOSE
    IDW_CLOSE

====================================================================================================================================

    Если значение интеграционной статистики Дарбина-Уотсона для первого ряда близко к 0, следовательно ряд - не стационарный

====================================================================================================================================

    #второй ряд
    profitability_prices = data['PROFITABILITY']

    # Рассчитываем квадрат разности текущего и предыдущего элемента
    difs_PROFITABILITY = [(profitability_prices[i + 1] - profitability_prices[i]) ** 2 for i in range(2, len(profitability_prices) - 1)]

    num_PROFITABILITY = sum(difs_PROFITABILITY)

    num_PROFITABILITY

    mean_profitability = profitability_prices.mean()
    # Рассчитываем квадрат разности текущего и среднего значения
    difs_PROFITABILITY2 = [(profitability_prices[i] - mean_profitability) ** 2 for i in range(2, len(profitability_prices))]

    denum_PROFITABILITY = sum(difs_PROFITABILITY2)

    denum_PROFITABILITY

========================================================================================================================================

    IDW_PROFITABILITY = num_PROFITABILITY/denum_PROFITABILITY
    IDW_PROFITABILITY


Значение интеграционной статистики Дарбина-Уотсона для второго ряда
близко к 2, следовательно ряд - стационарный

1.  Построить автокорреляционные функции. Построить их графики. Сделать
    аналитические выводы. Оценить порядок p и q в ARMA, где это
    возможно. (7 баллов)

    data['PROFITABILITY'] = profitability

    # Удаляем NaN значения из доходности
    profitability_non_nan = profitability.dropna()

    # Вычисление автокорреляционной функции (ACF) для доходности
    acf_profitability = sm.tsa.acf(profitability_non_nan, nlags=20, missing='drop')

    # Вывод значений автокорреляционной функции
    print("ACF for Profitability:")
    for lag, acf_value in enumerate(acf_profitability):
        print(f"Lag {lag}: {acf_value}")

========================================================================================================

Автокорреляционные функции для доходности

    fig = sm.graphics.tsa.plot_acf(profitability_non_nan, lags=20)

=========================================================================================================

Частичная автокорреляция

    fig = sm.graphics.tsa.plot_pacf(profitability_non_nan, lags=20)

=========================================================================================================

    Кол-во подряд вылезающих лагов у ACF - q, Кол-во подряд вылезующих лагов у PCF - p

    Как видно из графиков Автокорреляционных функций, первый же лаг не значим, следоватльно значимых лагов нет, значит лучше модель MA (скользящее среднее). p и q = 0, так как значимых лагов нет

 6. Для ряда 2 построить: Модель AR(1), AR(2), ARMA(1,1) и провести их
сравнение. Сделать аналитические выводы. Также в случае определения
параметров p и q с помощью коррелограммы, построить эту модели и
сравнить с AR(1), AR(2), ARMA(1,1) (12 баллов)

    AR1 = ARIMA(profitability_non_nan, order=(1, 0, 0)).fit()
    print(AR1.summary())

    # Выбираем лучшую модель, сделать для каждой
    # aic = np.log(sigma2) + 2*(цифры)/кол-во наблюдений
    print("AIC = ", np.log(0.0014) + 2*(3+0+0)/236)

=====================================================================

    AR2 = ARIMA(profitability_non_nan, order=(2, 0, 0)).fit()
    print(AR2.summary())

    # Выбираем лучшую модель, сделать для каждой
    # aic = np.log(sigma2) + 2*(цифры)/кол-во наблюдений
    print("AIC = ", np.log(0.0014) + 2*(3+0+0)/236)

=====================================================================

    ARMA11 = ARIMA(profitability_non_nan, order=(1, 0, 1)).fit()
    print(ARMA11.summary())

    # Выбираем лучшую модель, сделать для каждой
    # aic = np.log(sigma2) + 2*(цифры)/кол-во наблюдений
    print("AIC = ", np.log(0.0014) + 2*(3+0+0)/236)
""",
17: """

    1. Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна.  (10 баллов)

    import pandas as pd
    import statsmodels.api as sm
    import numpy as np
    import matplotlib.pyplot as plt
    from statsmodels.tsa.holtwinters import ExponentialSmoothing 
    from statsmodels.tsa.seasonal import seasonal_decompose

====================================================================================================

    data = pd.read_excel('Пересдача по эконометрике.xlsx', sheet_name='Вариант 14', usecols='A,B')
    data = data.drop(index=0).reset_index(drop=True)

    data['T'] = pd.period_range(start='1/1/2008', end='31/12/2021', freq='Q')
    df = data.set_index(['T'])
    df.index = df.index.to_timestamp()
    df

=====================================================================================================

    y = pd.to_numeric(df['INVFC_Q_DIRI'], errors='coerce')

=====================================================================================================

    y_a0_a1 = sm.OLS(y[:20], sm.add_constant(np.arange(1, 21))).fit()
    print(y_a0_a1.summary())

=====================================================================================================

    A0 = y_a0_a1.params['const']
    A1 = y_a0_a1.params['x1']
    beta = 0.9  # коэффициент сглаживания

    #  список для хранения коэффициентов
    coefs = [[A0, A1]]

=====================================================================================================

    for i in range(20, len(df)):
        y_pred = coefs[-1][0] + coefs[-1][1] * (i + 1)
        error = y.iloc[i] - y_pred  # вычисление ошибки
        
        # Обновление A0 и A1 на основе ошибки
        temp_A0 = coefs[-1][0] + coefs[-1][1] + (1 - beta) ** 2 * error
        temp_A1 = coefs[-1][1] + (1 - beta) ** 2 * error

        coefs.append([temp_A0, temp_A1])

=====================================================================================================

    # Преобразование коэффициентов в массив для последующих вычислений
    coefs = np.array(coefs)

    y_pred_brown = coefs[:, 0] + coefs[:, 1] * np.arange(1, len(coefs) + 1)

    # Построение графика оригинальных и прогнозных данных
    plt.figure(figsize=(10, 6))
    plt.plot(df.index[:len(y_pred_brown)], y[:len(y_pred_brown)], label="Исходные данные", marker='o')
    plt.plot(df.index[:len(y_pred_brown)], y_pred_brown, label="Прогноз по модели Брауна", linestyle='--', marker='x', color='orange')
    plt.xlabel("Период")
    plt.ylabel("Индекс реальных инвестиций в основной капитал (INVFC_Q_DIRI)")
    plt.title("Адаптивная модель прогнозирования Брауна")
    plt.legend()
    plt.grid(True)
    plt.show()

    2. Осуществить прогнозирование с применением адаптивной модели прогнозирования Хольта-Уинтерса.  (10 баллов)

    # Прогноз с использованием модели Хольта-Уинтерса 
    holt_winters_model = ExponentialSmoothing(y, seasonal='add', seasonal_periods=4, trend='add').fit()

    # Прогноз на 4 квартала вперед
    holt_winters_forecast = holt_winters_model.forecast(steps=4)

    # Построение графика с прогнозом по Хольта-Уинтерсу
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, y, label="Исходные данные", marker='o')
    plt.plot(df.index.append(pd.date_range(start='2022-01-01', periods=4, freq='Q')),
             np.append(holt_winters_model.fittedvalues, holt_winters_forecast),
             label="Прогноз по модели Хольта-Уинтерса", linestyle='--', marker='x', color='green')
    plt.xlabel("Период")
    plt.ylabel("Индекс реальных инвестиций в основной капитал (INVFC_Q_DIRI)")
    plt.title("Адаптивная модель прогнозирования Хольта-Уинтерса")
    plt.legend()
    plt.grid(True)
    plt.show()

    3. Выделение компонент тренд-сезонного временного ряда. Метод Четверикова: По заданным значениям временного ряда y_t выделить компоненты временного ряда: тренд f_t, сезонную компоненту S_t и остаточную последовательность ε_t.   (10 баллов)
    Построить следующие диаграммы: 
    1. Исходный ряд, тренды: предварительный, первый и второй. 
    2. Сезонную волну: первую и вторую. 
    3. Остаточную компоненту.

    # Шаг 1. Применение декомпозиции
    decomposition = seasonal_decompose(y, model='additive', period=4)

    # Шаг 2. Извлечение компонентов: тренд, сезонность, остаток
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # Шаг 3. Построение графиков для каждого компонента
    plt.figure(figsize=(10, 8))

    # Оригинальный ряд
    plt.subplot(4, 1, 1)
    plt.plot(df.index, y, label="Исходный ряд", marker='o')
    plt.title('Исходный ряд')
    plt.grid(True)

    # Тренд
    plt.subplot(4, 1, 2)
    plt.plot(df.index, trend, label="Тренд", color='orange', marker='o')
    plt.title('Тренд')
    plt.grid(True)

    # Сезонная компонента
    plt.subplot(4, 1, 3)
    plt.plot(df.index, seasonal, label="Сезонная компонента", color='green', marker='o')
    plt.title('Сезонная компонента')
    plt.grid(True)

    # Остаток
    plt.subplot(4, 1, 4)
    plt.plot(df.index, residual, label="Остаточная компонента", color='red', marker='o')
    plt.title('Остаточная компонента')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
"""
    }

    if option is None:
        return ("""1: (Предварительный анализ временных рядов...)'
                '2: (Pool, RE, FE)'
                '3: (Запишите структурную форму в матричном виде...)'
                '4: (Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна Хольта-уинтерса Четверикова)'
                '5: Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции',
                '6: Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции',
                '7: пул рс фс',
                '8: 9 вариант',
                '9: модель брауна',
                '10: что-то с методом фостера-стьюарта и кривой роста',
                '11: Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна.',
                '12: Pool, RE, FE (5 баллов)',
                '13: Запишите структурную форму модели в матричном виде и проведите проверку идентифицируемости системы правилами ранга и порядка (8 баллов)',
                '14: 3 вариант',
                '15: Предварительный анализ временных рядов. Построить график и провести визуальный анализ. Результаты описать. (5 баллов)',
                '16: Скачать с любого сайта данные о дневных ценах закрытия выбранной Вами акции в период с 01.06.2021 по 01.06.2022. (ряд 1)',
                '17: Осуществить прогнозирование с применением адаптивной модели прогнозирования Брауна. (10 баллов)"""
                )
    else:
        return task_map.get(option, "Некорректная опция. введи другую цифру такой нет.")


image_map = {
        1: [os.path.join(image_dir, "001_1.png"), os.path.join(image_dir, "001_2.png")],
        2: [os.path.join(image_dir, "002_1.png"), os.path.join(image_dir, "002_2.png")],
        3: [os.path.join(image_dir, "003_1.png"), os.path.join(image_dir, "003_2.png")],
        4: [os.path.join(image_dir, "004_1.png"), os.path.join(image_dir, "004_2.png")],
        5: [os.path.join(image_dir, "005_1.png"), os.path.join(image_dir, "005_2.png"), os.path.join(image_dir, "005_3.png")],
        6: [os.path.join(image_dir, "006_1.png"), os.path.join(image_dir, "006_2.png")],
        7: [os.path.join(image_dir, "007_1.png"), os.path.join(image_dir, "007_2.png")],
        8: [os.path.join(image_dir, "008_1.png"), os.path.join(image_dir, "008_2.png")],
        9: [os.path.join(image_dir, "009_1.png"), os.path.join(image_dir, "009_2.png")],
        10: [os.path.join(image_dir, "010_1.png"), os.path.join(image_dir, "010_2.png")],
        11: [os.path.join(image_dir, "011_1.png")],
        12: [os.path.join(image_dir, "012_1.png"), os.path.join(image_dir, "012_2.png")],
        13: [os.path.join(image_dir, "013_1.png"), os.path.join(image_dir, "013_2.png")],
        14: [os.path.join(image_dir, "014_1.png")],
        15: [os.path.join(image_dir, "015_1.png")],
        16: [os.path.join(image_dir, "016_1.png")],
        17: [os.path.join(image_dir, "017_1.png"), os.path.join(image_dir, "017_2.png")],
        18: [os.path.join(image_dir, "018_1.png")],
        19: [os.path.join(image_dir, "019_1.png"), os.path.join(image_dir, "019_2.png")],
        20: [os.path.join(image_dir, "020_1.png"), os.path.join(image_dir, "020_2.png"), os.path.join(image_dir, "020_3.png")],
        21: [os.path.join(image_dir, "021_1.png")],
        22: [os.path.join(image_dir, "022_1.png"), os.path.join(image_dir, "022_2.png"), os.path.join(image_dir, "022_3.png")],
        23: [os.path.join(image_dir, "023_1.png"), os.path.join(image_dir, "023_2.png")],
        24: [os.path.join(image_dir, "024_1.png"), os.path.join(image_dir, "024_2.png")],
        25: [os.path.join(image_dir, "025_1.png")],
        26: [os.path.join(image_dir, "026_1.png")],
        27: [os.path.join(image_dir, "027_1.png")],
        28: [os.path.join(image_dir, "028_1.png")],
        29: [os.path.join(image_dir, "029_1.png")],
        30: [os.path.join(image_dir, "030_1.png"), os.path.join(image_dir, "030_2.png")],
        31: [os.path.join(image_dir, "031_1.png"), os.path.join(image_dir, "031_2.png"), os.path.join(image_dir, "031_3.png")],
        32: [os.path.join(image_dir, "032_1.png"), os.path.join(image_dir, "032_2.png"), os.path.join(image_dir, "032_3.png")],
        33: [os.path.join(image_dir, "033_1.png")],
        34: [os.path.join(image_dir, "034_1.png"), os.path.join(image_dir, "034_2.png")],
        35: [os.path.join(image_dir, "035_1.png"), os.path.join(image_dir, "035_2.png")],
        36: [os.path.join(image_dir, "036_1.png"), os.path.join(image_dir, "036_2.png")],
        37: [os.path.join(image_dir, "037_1.png"), os.path.join(image_dir, "037_2.png"), os.path.join(image_dir, "037_3.png"), os.path.join(image_dir, "037_4.png")],
        38: [os.path.join(image_dir, "038_1.png")],
        39: [os.path.join(image_dir, "039_1.png"), os.path.join(image_dir, "039_2.png")],
        40: [os.path.join(image_dir, "040_1.png"), os.path.join(image_dir, "040_2.png"), os.path.join(image_dir, "040_3.png")],
        41: [os.path.join(image_dir, "041_1.png")],
        42: [os.path.join(image_dir, "042_1.png")],
        43: [os.path.join(image_dir, "043_1.png")],
        44: [os.path.join(image_dir, "044_1.png"), os.path.join(image_dir, "044_2.png")],
        45: [os.path.join(image_dir, "045_1.png")],
        46: [os.path.join(image_dir, "046_1.png"), os.path.join(image_dir, "046_2.png")],
        47: [os.path.join(image_dir, "047_1.png")],
        48: [os.path.join(image_dir, "048_1.png"), os.path.join(image_dir, "048_2.png")],
        49: [os.path.join(image_dir, "049_1.png"), os.path.join(image_dir, "049_2.png")],
        50: [os.path.join(image_dir, "050_1.png"), os.path.join(image_dir, "050_2.png")],
        51: [os.path.join(image_dir, "051_1.png"), os.path.join(image_dir, "051_2.png")],
        52: [os.path.join(image_dir, "052_1.png"), os.path.join(image_dir, "052_2.png"), os.path.join(image_dir, "052_3.png")],
        53: [os.path.join(image_dir, "053_1.png"), os.path.join(image_dir, "053_2.png")],
        54: [os.path.join(image_dir, "054_1.png"), os.path.join(image_dir, "054_2.png")],
        55: [os.path.join(image_dir, "055_1.png")],
        56: [os.path.join(image_dir, "056_1.png"), os.path.join(image_dir, "056_2.png"), os.path.join(image_dir, "056_3.png")],
        57: [os.path.join(image_dir, "057_1.png"), os.path.join(image_dir, "057_2.png"), os.path.join(image_dir, "057_3.png")],
        58: [os.path.join(image_dir, "058_1.png")],
        59: [os.path.join(image_dir, "059_1.png")],
        60: [os.path.join(image_dir, "060_1.png"), os.path.join(image_dir, "060_2.png")],
        61: [os.path.join(image_dir, "061_1.png")],
        62: [os.path.join(image_dir, "062_1.png"), os.path.join(image_dir, "062_2.png")],
        63: [os.path.join(image_dir, "063_1.png"), os.path.join(image_dir, "063_2.png"), os.path.join(image_dir, "063_3.png"), os.path.join(image_dir, "063_4.png")],
        64: [os.path.join(image_dir, "064_1.png"), os.path.join(image_dir, "064_2.png")],
        65: [os.path.join(image_dir, "065_1.png")],
        66: [os.path.join(image_dir, "066_1.png")],
        67: [os.path.join(image_dir, "067_1.png"), os.path.join(image_dir, "067_2.png")],
        68: [os.path.join(image_dir, "068_1.png"), os.path.join(image_dir, "068_2.png")],
        69: [os.path.join(image_dir, "069_1.png"), os.path.join(image_dir, "069_2.png"), os.path.join(image_dir, "069_3.png")],
        70: [os.path.join(image_dir, "070_1.png"), os.path.join(image_dir, "070_2.png"), os.path.join(image_dir, "070_3.png")],
        71: [os.path.join(image_dir, "071_1.png")],
        72: [os.path.join(image_dir, "072_1.png"), os.path.join(image_dir, "072_2.png")],
        73: [os.path.join(image_dir, "073_1.png"), os.path.join(image_dir, "073_2.png")],
        74: [os.path.join(image_dir, "074_1.png"), os.path.join(image_dir, "074_2.png")],
        75: [os.path.join(image_dir, "075_1.png"), os.path.join(image_dir, "075_2.png")],
        76: [os.path.join(image_dir, "076_1.png"), os.path.join(image_dir, "076_2.png")],
        77: [os.path.join(image_dir, "077_1.png"), os.path.join(image_dir, "077_2.png")],
        78: [os.path.join(image_dir, "078_1.png"), os.path.join(image_dir, "078_2.png")],
        79: [os.path.join(image_dir, "079_1.png")],
        80: [os.path.join(image_dir, "080_1.png"), os.path.join(image_dir, "080_2.png")],
        81: [os.path.join(image_dir, "081_1.png")],
        82: [os.path.join(image_dir, "082_1.png"), os.path.join(image_dir, "082_2.png")],
        83: [os.path.join(image_dir, "083_1.png"), os.path.join(image_dir, "083_2.png"), os.path.join(image_dir, "083_3.png"), os.path.join(image_dir, "083_4.png"), os.path.join(image_dir, "083_5.png")],
        84: [os.path.join(image_dir, "084_1.png"), os.path.join(image_dir, "084_2.png")],
        85: [os.path.join(image_dir, "085_1.png"), os.path.join(image_dir, "085_2.png")],
        86: [os.path.join(image_dir, "086_1.png"), os.path.join(image_dir, "086_2.png")],
        87: [os.path.join(image_dir, "087_1.png"), os.path.join(image_dir, "087_2.png"), os.path.join(image_dir, "087_3.png")],
        88: [os.path.join(image_dir, "088_1.png"), os.path.join(image_dir, "088_2.png")],
        89: [os.path.join(image_dir, "089_1.png"), os.path.join(image_dir, "089_2.png"), os.path.join(image_dir, "089_3.png")],
        90: [os.path.join(image_dir, "090_1.png"), os.path.join(image_dir, "090_2.png")],
        91: [os.path.join(image_dir, "091_1.png")],
        92: [os.path.join(image_dir, "092_1.png"), os.path.join(image_dir, "092_2.png")],
        93: [os.path.join(image_dir, "093_1.png"), os.path.join(image_dir, "093_2.png")],
        94: [os.path.join(image_dir, "094_1.png")],
        95: [os.path.join(image_dir, "095_1.png"), os.path.join(image_dir, "095_2.png")],
        96: [os.path.join(image_dir, "096_1.png"), os.path.join(image_dir, "096_2.png"), os.path.join(image_dir, "096_3.png")],
        97: [os.path.join(image_dir, "097_1.png"), os.path.join(image_dir, "097_2.png")],
        98: [os.path.join(image_dir, "098_1.png"), os.path.join(image_dir, "098_2.png")],
        99: [os.path.join(image_dir, "099_1.png"), os.path.join(image_dir, "099_2.png"), os.path.join(image_dir, "099_3.png")],
        100: [os.path.join(image_dir, "100_1.png")],
        101: [os.path.join(image_dir, "101_1.png")],
        102: [os.path.join(image_dir, "102_1.png")],
        103: [os.path.join(image_dir, "103_1.png"), os.path.join(image_dir, "103_2.png")],
        104: [os.path.join(image_dir, "104_1.png"), os.path.join(image_dir, "104_2.png"), os.path.join(image_dir, "104_3.png"), os.path.join(image_dir, "104_4.png")],
        105: [os.path.join(image_dir, "105_1.png"), os.path.join(image_dir, "105_2.png")],
        106: [os.path.join(image_dir, "106_1.png")],
        107: [os.path.join(image_dir, "107_1.png")],
        108: [os.path.join(image_dir, "108_1.png")],
        109: [os.path.join(image_dir, "109_1.png"), os.path.join(image_dir, "109_2.png")],
        110: [os.path.join(image_dir, "110_1.png")],
        111: [os.path.join(image_dir, "111_1.png")],
        112: [os.path.join(image_dir, "112_1.png"), os.path.join(image_dir, "112_2.png"), os.path.join(image_dir, "112_3.png")],
        113: [os.path.join(image_dir, "113_1.png"), os.path.join(image_dir, "113_2.png")],
        114: [os.path.join(image_dir, "114_1.png"), os.path.join(image_dir, "114_2.png"), os.path.join(image_dir, "114_3.png")],
        115: [os.path.join(image_dir, "115_1.png"), os.path.join(image_dir, "115_2.png"), os.path.join(image_dir, "115_3.png")],
        116: [os.path.join(image_dir, "116_1.png")],
        117: [os.path.join(image_dir, "117_1.png")],
        118: [os.path.join(image_dir, "118_1.png")],
        119: [os.path.join(image_dir, "119_1.png")],
        120: [os.path.join(image_dir, "120_1.png"), os.path.join(image_dir, "120_2.png"), os.path.join(image_dir, "120_3.png"), os.path.join(image_dir, "120_4.png")],
        121: [os.path.join(image_dir, "121_1.png"), os.path.join(image_dir, "121_2.png")]
    }


def t(option=None):
    if option is None:
        return ("""1. Линейная модель множественной регрессии. Основные предпосылки метода наименьших квадратов.
2. Нелинейные модели регрессии. Подходы к оцениванию. Примеры
3. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Тест Рамсея (тест RESET), условия применения теста.
4. Тестирование правильности выбора спецификации: типичные ошибки спецификации модели, Критерий Акаике, Критерий Шварца. условия применения критериев.
5. Гетероскедастичность: определение, причины, последствия. Тест Голдфеда-Квандта и особенности его применения.
6. Гетероскедастичность: определение, причины, последствия. Тест ранговой корреляции Спирмена и особенности его применения.
7. Гетероскедастичность: определение, причины, последствия. Тест Бреуша-Пагана и особенности его применения.
8. Гетероскедастичность: определение, причины, последствия. Тест Глейзера и особенности его применения.
9. Способы корректировки гетероскедастичности: взвешенный метод наименьших квадратов (ВМНК) и особенности его применения.
10. Автокорреляция: определение, причины, последствия. Тест Дарбина-Уотсона и особенности его применения.
11. Автокорреляция: определение, причины, последствия. Тест Бройша – Годфри и особенности его применения.
12.   Автокорреляция: определение, причины, последствия. H – тест и особенности его применения.
13. Автокорреляция: определение, причины, последствия. Метод рядов Сведа-Эйзенхарта и особенности его применения.
14. Модель с автокорреляцией случайного возмущения. Оценка моделей с авторегрессией.
15. Процедура Кохрейна-Оркатта.
16. Процедура Хилдрета – Лу.
17. Оценка влияния факторов, включенных в модель. Коэффициент эластичности, Бета-коэффициент, Дельта – коэффициент.
18. Мультиколлинеарность: понятие, причины и последствия.
19. Алгоритм пошаговой регрессии.
20. Метод главных компонент (PCA) как радикальный метод борьбы с мультиколлинеарностью
21. Выявление мультиколлинеарности: коэффициент увеличения дисперсии (VIF –тест).
22. Выявление мультиколлинеарности: Алгоритм Фаррара-Глобера.
23. Построение гребневой регрессии. Суть регуляризации.
24. Фиктивная переменная и правило её использования.
25. Модель дисперсионного анализа.
26. Модель ковариационного анализа.
27. Фиктивные переменные в сезонном анализе.
28.  Фиктивная переменная сдвига: спецификация регрессионной модели с фиктивной переменной сдвига; экономический смысл параметра при фиктивной переменной; смысл названия.
29. Фиктивная переменная наклона: спецификация регрессионной модели с фиктивной переменной наклона; экономический смысл параметра при фиктивной переменной; смысл названия.
30. Определение структурных изменений в экономике: использование фиктивных переменных, тест Чоу.
31. ​​Модели бинарного выбора. Недостатки линейной модели.
32. Модели множественного выбора: модели с неупорядоченными альтернативными вариантами.
33. Модели усеченных выборок.
34. Модели цензурированных выборок (tobit-модель).
35.   Модели множественного выбора: гнездовые logit-модели.
36.    Модели счетных данных (отрицательная биномиальная модель, hurdle-model)
37. Модели множественного выбора: модели с упорядоченными альтернативными вариантами.
38. Модели случайно усеченных выборок (selection model).
39. Логит-модель. Этапы оценки. Области применения.
40. Пробит-модель. Этапы оценки. Области применения.
41. Метод максимального правдоподобия
42. Свойства оценок метода максимального правдоподобия.
43. Информационная матрица и оценки стандартных ошибок для оценок параметров logit и probit моделей. Интерпретация коэффициентов в моделях бинарного выбора.
44. Мера качества аппроксимации и качества прогноза logit и probit моделей.
45. Временные ряды: определение, классификация, цель и задача моделирования временного ряда.
46.    Исследование структуры одномерного временного ряда.
47.   Процедура выявления аномальных наблюдений на основе метода Ирвина. Особенности применения метода. Анализ аномальных наблюдений.
48. Проверка наличия тренда. Критерий серий, основанный на медиане. Особенности применения метода.
49. Процедура выявления аномальных наблюдений. Причины аномальных значений. Блочные диаграммы по типу «ящика с усами».
50. Проверка наличия тренда. Метод проверки разности средних уровней. Особенности применения метода.
51. Проверка наличия тренда. Метод Фостера-Стьюарта. Особенности применения метода.
52.   Сглаживание временных рядов. Простая (среднеарифметическая) скользящая средняя. Взвешенная (средневзвешенная) скользящая средняя. Среднехронологическая. Экспоненциальное сглаживание.
53. Функциональные зависимости временного ряда. Предварительный анализ временных рядов.
54. Трендовые модели. Без предела роста. Примеры функций. Содержательная интерпретация параметров.
55. Процедура выявления аномальных наблюдений на основе распределения Стьюдента. Особенности применения метода. Анализ аномальных наблюдений.
56. Трендовые модели. С пределом роста без точки перегиба. Примеры функций. Содержательная интерпретация параметров.
57. Трендовые модели. С пределом роста и точкой перегиба или кривые насыщения. Примеры функций. Содержательная интерпретация параметров.
58.  Выбор кривой роста.
59. Прогнозирование с помощью кривой роста.
60.    Прогнозирование временного ряда на основе трендовой модели.
61. Модель Тейла-Вейджа (мультипликативная модель).
62. Метод Четверикова.
63. Моделирование тренд-сезонных процессов. Типы функциональных зависимостей.
64.Мультипликативная (аддитивная) модель ряда динамики при наличии тенденции: этапы построения.
65. Моделирование периодических колебаний (гармоники Фурье).
66. Прогнозирование одномерного временного ряда случайной компоненты (распределение Пуассона).
67. Функциональные преобразования переменных в линейной регрессионной модели. Метод Зарембки. Особенности применения.
68. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бокса-Кокса. Особенности применения.
69. Адаптивная модель прогнозирования Брауна.
70. Функциональные преобразования переменных в линейной регрессионной модели. Критерий Акаике  и Шварца. Особенности применения.
71. Модель Хольта-Уинтерса (адаптивная модель).
72. Функциональные преобразования переменных в линейной регрессионной модели. Тест Бера. Особенности применения.
73. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакАлера. Особенности применения.
74. Функциональные преобразования переменных в линейной регрессионной модели. Тест МакКиннона. Особенности применения.
75. Функциональные преобразования переменных в линейной регрессионной модели. Тест Уайта. Особенности применения.
76. Функциональные преобразования переменных в линейной регрессионной модели. Тест Дэвидсона. Особенности применения.
77. Модели с распределенными лаговыми переменными.
78. Оценка моделей с лагами в независимых переменных. Преобразование Койка
79. ​​Полиномиально распределенные лаги Алмон
80. Авторегрессионные модели.
81. Авторегрессионные модели с распределенными лагами.
82. Стационарные временные ряды. Определения стационарности, лаговой переменной, автоковариационной функции временного ряда, автокоррляционной функции, коррелограммы,  коэффициенты корреляции между разными элементами стационарного временного ряда с временным лагом.
83. Стационарные временные ряды. Определения частной автокорреляционной функции, белого шума, автоковариационная функция для белого шума, ACF для белого шума, частная автокорреляционная функция для белого шума.
84. Модели стационарных временных рядов: модель ARMA(p,q) (классический вид и через лаговый оператор). Авторегрессионный многочлен, авторегрессионная часть и часть скользящего среднего.
85. Модели стационарных временных рядов: модель ARMA(1, q). Доказательство утверждения: Модель ARMA(1, q) стационарна тогда и только тогда, когда |a|<1.
86. Модели стационарных временных рядов: Модель MA(q), Среднее, дисперсия и ACF для MA(q). Модель MA(∞).
87.  Модели стационарных временных рядов: Модель AR(p). Доказательство утверждения: Модель AR(p) определяет стационарный ряд ⇐⇒ выполнено условие стационарности: все корни многочлена a(z) по модулю больше единицы. Модель AR(1).
88. Прогнозирование для модели ARMA. Условия прогнозирования. Периоды прогнозирования. Информативность прогнозов.
89. Оценка и тестирование модели: Предварительное тестирование на белый шум.
90.  Оценка модели и тестирование гипотез временного ряда.
91. Информационные критерии для сравнения моделей и выбора порядка временного ряда: Акаике, Шварца, Хеннана-Куина. Условия их применения.
92. Проверка адекватности модели: тесты на автокорреляцию временного ряда Дарбина-Уотсона, Льюинга-Бокса.
93.    Линейная регрессия для стационарных рядов: Модель FDL.
94. Линейная регрессия для стационарных рядов. Модель ADL.
95. Понятие TS-ряда. Модель линейного тренда. Модель экспоненциального тренда.
96. Нестационарные временные ряды: случайное блуждание, стохастический тренд, случайное блуждание со сносом.
97. Дифференцирование ряда: определение, DS-ряды.
98. Подход Бокса-Дженкинса.
99. Модель ARIMA.
100.   Тест ADF на единичный корень.
101. Модель ARCH.
102. Модель GARCH.
103.  Область применения панельных данных. Преимущества использования панельных данных.
104. Модели панельных данных и основные обозначения.
105. Модель пула (Pool model).
106.  Модель регрессии с фиксированным эффектом (fixed effect model)
107. Модель регрессии со случайным эффектом (random effect model).
108. Тест Бройша-Пагана для панельных данных
109.    Тест Хаусмана для панельных данных.
110. Тест Лагранжа для панельных данных.
111. Вычисление значения оценок параметров β и а в модели с фиксированным эффектом.
112. Отражение пространственных эффектов. Бинарная матрица граничных соседей. Приведите пример.
113. Отражение пространственных эффектов. Бинарная матрица ближайших соседей. Приведите пример.
114. Отражение пространственных эффектов. Матрица расстояний. Приведите пример.
115. Отражение пространственных эффектов. Матрица расстояний с учетом размера объекта. Приведите пример.
117. Пространственная автокорреляция по методологии А. Гетиса и Дж. Орда. Недостатки методологии.
118. Пространственная автокорреляция по методологии Роберта Джири.
119. Пространственная автокорреляция по методологии Морана П.
120. Пространственная кластеризация территорий. Локальный индекс автокорреляции П. Морана (Ili)
121. Матрица взаимовлияния Л. Анселина (LISA).""")




    else:

            try:

                    # Получаем список путей к изображениям для задачи

                    image_paths = image_map.get(option)

                    if image_paths:

                            # Выводим каждое изображение в ячейке Jupyter Notebook

                            for image_path in image_paths:
                                    display(Image(filename=image_path))  # Отображаем изображение

                            return f"Показаны изображения для задачи {option}."

                    else:

                            return "Изображения для данной задачи не найдены."

            except ValueError:

                    return "Некорректная опция. Попробуйте снова."
