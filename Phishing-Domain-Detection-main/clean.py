import pandas as pd


def cleanDataframe(df):
    for col in df:
        temp = []
        for cell in df[col]:
            temp.append(int(cell))
        df[col] = temp
    
    # Drop columns for unused features
    df.drop("SSLfinal_State", inplace=True, axis=1)
    df.drop("Favicon", inplace=True, axis=1)
    df.drop("port", inplace=True, axis=1)
    df.drop("Request_URL", inplace=True, axis=1)
    df.drop("URL_of_Anchor", inplace=True, axis=1)
    df.drop("Links_in_tags", inplace=True, axis=1)
    df.drop("SFH", inplace=True, axis=1)
    df.drop("Submitting_to_email", inplace=True, axis=1)
    df.drop("Abnormal_URL", inplace=True, axis=1)
    df.drop("popUpWidnow", inplace=True, axis=1)
    df.drop("Page_Rank", inplace=True, axis=1)
    df.drop("Links_pointing_to_page", inplace=True, axis=1)
    df.drop("Statistical_report", inplace=True, axis=1)
    return df
