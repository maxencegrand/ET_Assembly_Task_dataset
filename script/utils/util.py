def get_code_timestamp(df, value):
    """
    """
    df = df[df["code"] == value]
    idx = df.index[0]
    return df.loc[idx]["timestamp"]

def get_coord(str):
    """
    """
    return [float(x) for x in str.strip("(')").split(", ")]
