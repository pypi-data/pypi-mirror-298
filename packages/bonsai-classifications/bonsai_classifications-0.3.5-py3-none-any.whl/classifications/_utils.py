import pandas

from ._mapping_type import get_comment, get_skos_uri


# Lookup function for pandas DataFrame
def lookup(self, keyword):
    """Filter the DataFrame based on the keyword in the "name" column"""
    filtered_df = self[self["name"].str.contains(keyword)]
    return filtered_df


def get_children(self, parent_code):
    """Get all children of a certain parent_code"""
    try:
        filtered_df = self[self["parent_code"] == parent_code]
    except KeyError as e:
        raise KeyError("Data table has no column 'parent_code'") from e
    return filtered_df


def create_conc(df_A, df_B, source="", target="", intermediate=""):
    """Create new concordance based on two other tables.

    Argument
    --------
    df_A : pandas.DataFrame
        concordance table A
        with mapping from "x" to "y"
    df_B : pandas.DataFrame
        concordance table B
        with mapping from "y" to "z"
    target : str
        header name that specifies "x"
    source : str
        header name that specifies "z"
    intermediate : str
        header name that specifies "y"

    Returns
    -------
    pandas.DataFrame
        concordance table with mapping form "x" to "z"
    """
    new_mapping = pandas.merge(df_A, df_B, on=intermediate)

    # Drop duplicate pairs of source and target
    new_mapping = new_mapping.drop_duplicates(subset=[source, target])

    # Calculate the counts of each source and target in the merged DataFrame
    source_counts = new_mapping[source].value_counts().to_dict()
    target_counts = new_mapping[target].value_counts().to_dict()
    # Apply the get_comment function to each row
    new_mapping["comment"] = new_mapping.apply(
        lambda row: get_comment(
            source_counts[row[source]],
            target_counts[row[target]],
            s=row[source],
            t=row[target],
        ),
        axis=1,
    )
    new_mapping["skos_uri"] = new_mapping.apply(
        lambda row: get_skos_uri(
            source_counts[row[source]], target_counts[row[target]]
        ),
        axis=1,
    )

    new_mapping = new_mapping[[source, target, "comment", "skos_uri"]]
    new_mapping = new_mapping.reset_index(drop=True)
    return new_mapping


# Subclass pandas DataFrame
class CustomDataFrame(pandas.DataFrame):
    lookup = lookup
    get_children = get_children
