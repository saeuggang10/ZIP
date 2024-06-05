def insert_row(idx, df, df_insert):
    return pd.concat([df.iloc[:idx, :], pd.DataFrame([df_insert], columns=df.columns), df.iloc[idx:, :]], axis=0).reset_index(drop = True)

num = df.shape[1]
insert_row(2, df, [np.nan]*num)
