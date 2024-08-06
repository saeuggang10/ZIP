## 수치형 변수에 대한 단변령 분석 함수
def eda_1_n(data, var, bins = 30) :
    # 기초 통계량
    display(data[[var]].describe().T)

    # 시각화
    plt.figure(figsize = (12,8))
    plt.subplot(2,1,1)
    sns.histplot(data[var], bins = bins, kde = True)
    plt.grid()

    plt.subplot(2,1,2)
    sns.boxplot(x = data[var])
    plt.grid()
    plt.show()

## 범주형 변수에 대한 단변량 분석 함수
def eda_1_c(data, var) :
    # 기초 통계량
    print(f' <<<  {var}   >>')
    cnt = data[var].value_counts()
    prop = data[var].value_counts()/data.shape[0]
    temp = pd.DataFrame({'Class':cnt.index, 'Count':cnt.values, 'Prop':prop.values})
    display(temp)
    # 시각화
    sns.countplot(x = var, data = data)
    plt.grid()
    plt.show()

## 산점도
def eda_2_nn(data, feature, target) :
    temp = data.loc[data[feature].notnull()]
    sns.scatterplot( x= feature, y = target, data = temp)
    plt.grid()
    plt.show()
    result = spst.pearsonr(temp[feature], temp[target])
    print(f'상관계수 : {result[0]}, P-value : {result[1]}')

## 연속->범주
def eda_2_nc(data, feature, target) :

    plt.figure(figsize = (6, 10))
    plt.subplot(3,1,1)
    sns.kdeplot(x = feature, data = data, hue = target, common_norm = False)
    plt.xlim(data[feature].min(), data[feature].max())
    plt.grid()

    plt.subplot(3,1,2)
    sns.kdeplot(x = feature, data = data, hue = target, multiple = 'fill')
    plt.axhline(data[target].mean(), color = 'r')
    plt.xlim(data[feature].min(), data[feature].max())
    plt.grid()

    plt.subplot(3,1,3)
    sns.histplot(x = feature, data = data, bins = 30, hue = target, multiple = 'fill')
    plt.axhline(data[target].mean(), color = 'r')
    plt.xlim(data[feature].min(), data[feature].max())
    plt.grid()

plt.show()

## 범주->범주
def eda_2_cc(data, target, var) :

    print(data[target].mean())

    temp1 = pd.crosstab(data[target], data[var])
    display(temp1)
    temp2 = pd.crosstab(data[target], data[var], normalize = 'columns')
    display(temp2)

    mosaic(data, [ var,target], gap = 0.01)
    plt.axhline(data[target].mean(), color = 'r')
    plt.show()

    # 카이제곱검정
    print(spst.chi2_contingency(temp1))

## 시계열 분해
def decomp_plot(decomp) :
    # 시계열 분해 결과를 받아서 데이터프레임으로 저장
    result = pd.DataFrame({'observed':decomp.observed, 'trend':decomp.trend, 'seasonal':decomp.seasonal, 'residual':decomp.resid})

    # 4개의 그래프로 나눠서 그리기
    plt.subplot(4,1,1)
    plt.plot(result['observed'])
    plt.ylabel('observed')

    plt.subplot(4,1,2)
    plt.plot(result['trend'])
    plt.ylabel('trend')

    plt.subplot(4,1,3)
    plt.plot(result['seasonal'])
    plt.ylabel('seasonal')

    plt.subplot(4,1,4)
    plt.plot(result['residual'])
    plt.ylabel('residual')
    plt.show()

    return result
# 시계열 데이터 분해
decomp = sm.tsa.seasonal_decompose(bike['Count'], model = 'additive', period = 24)

# 그래프 그리기
plt.figure(figsize=(12, 8))
result = decomp_plot(decomp)

##
