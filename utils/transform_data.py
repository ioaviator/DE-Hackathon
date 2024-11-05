def transform_data(df):
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df.fillna('Unspecified', inplace=True)

    df_language = df[['country_name', 'languages']]
    df_language_expand = df_language.set_index('country_name')['languages'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='language')
    
    df.drop('languages', axis=1, inplace=True)
    
    return df, df_language_expand
