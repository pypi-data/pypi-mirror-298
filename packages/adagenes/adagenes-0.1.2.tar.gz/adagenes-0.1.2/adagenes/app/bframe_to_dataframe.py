import pandas as pd


def bframe_to_app_dataframe(bframe, output_format="AVF"):
    """
    Converts a biomarker frame into a dataframe for the adagenes application

    :param bframe:
    :return:
    """
    data = {}

    if output_format == "AVF":
        pass
    elif output_format == "VCF":
        data = { "CHROM":[], "POS":[], "REF":[], "ALT":[] }
        for key in bframe.data.keys():
            var = bframe.data[key]
            data["CHROM"].append(var["variant_data"]["CHROM"])
            data["POS"].append(var["variant_data"]["POS"])
            data["REF"].append(var["variant_data"]["REF"])
            data["ALT"].append(var["variant_data"]["ALT"])

    df = pd.DataFrame(data=data)
    return df
