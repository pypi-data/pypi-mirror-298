import pandas as pd
from sklearn.utils import resample
def balanced_downsampling(df, label_col, second_col=None):
    """
    Perform balanced downsampling to ensure that each combination of label_col and second_col
    (if provided) has the same number of samples, based on the smallest group size.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    label_col (str): The primary column for balancing.
    second_col (str, optional): The secondary column for balancing. Defaults to None.

    Returns:
    pd.DataFrame: Dataframe with balanced downsampling.
    """
    # Determine the grouping columns
    group_cols = [label_col] if second_col is None else [label_col, second_col]

    # Find the smallest group size across all combinations of group_cols
    min_count = df.groupby(group_cols).size().min()

    # Downsample each group to the smallest group size
    balanced_dfs = []
    for _, group in df.groupby(group_cols):
        balanced_group = group.sample(min_count, random_state=42)
        balanced_dfs.append(balanced_group)

    return pd.concat(balanced_dfs).reset_index(drop=True)

def balanced_upsampling(df, label_col, second_col=None):
    """
    Perform balanced upsampling to ensure that each combination of label_col and second_col
    (if provided) has the same number of samples, based on the largest group size.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    label_col (str): The primary column for balancing.
    second_col (str, optional): The secondary column for balancing. Defaults to None.

    Returns:
    pd.DataFrame: Dataframe with balanced upsampling.
    """
    # Determine the grouping columns
    group_cols = [label_col] if second_col is None else [label_col, second_col]

    # Find the largest group size across all combinations of group_cols
    max_count = df.groupby(group_cols).size().max()

    # Upsample each group to the largest group size
    upsampled_dfs = []
    for _, group in df.groupby(group_cols):
        upsampled_group = resample(group, replace=True, n_samples=max_count, random_state=42)
        upsampled_dfs.append(upsampled_group)

    return pd.concat(upsampled_dfs).reset_index(drop=True)

def balanced_fixedcount(df, total_count, label_col, second_col=None):
    """
    Perform balanced sampling to ensure each combination of label_col and second_col (if provided) has
    approximately total_count / number_of_combinations samples. Adjust the final count to
    match the total_count exactly.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    label_col (str): The primary column for balancing.
    second_col (str, optional): The secondary column for balancing. Defaults to None.
    total_count (int): The total number of samples desired in the output dataframe.

    Returns:
    pd.DataFrame: Dataframe with balanced sampling.
    """
    # Determine the grouping columns
    group_cols = [label_col] if second_col is None else [label_col, second_col]

    # Number of unique combinations of label_col and second_col
    num_combinations = df.groupby(group_cols).ngroups

    # Determine the target number of samples per group
    target_per_group = total_count // num_combinations
    # Calculate the remainder to adjust the total sample count
    remainder = total_count % num_combinations

    # Collect the sampled data
    sampled_dfs = []
    for _, group in df.groupby(group_cols):
        if len(group) > target_per_group:
            # Downsample to target_per_group
            sampled_group = group.sample(target_per_group, random_state=42)
        else:
            # Upsample to target_per_group
            sampled_group = resample(group, replace=True, n_samples=target_per_group, random_state=42)
        sampled_dfs.append(sampled_group)

    # If there is a remainder, adjust the final count
    if remainder > 0:
        # Identify groups to add one more sample
        additional_dfs = []
        for _, group in df.groupby(group_cols):
            if len(group) >= target_per_group + 1:
                additional_group = group.sample(target_per_group + 1, random_state=42)
                additional_dfs.append(additional_group)
                remainder -= 1
                if remainder == 0:
                    break

        # Combine all sampled dataframes
        sampled_dfs.extend(additional_dfs)

    # Combine all sampled dataframes
    final_df = pd.concat(sampled_dfs)

    # Ensure the final count matches total_count
    if len(final_df) < total_count:
        # If the final dataframe is smaller than the desired total count, upsample with replacement
        final_df = resample(final_df, replace=True, n_samples=total_count, random_state=42)
    else:
        # Otherwise, downsample without replacement
        final_df = final_df.sample(total_count, random_state=42).reset_index(drop=True)

    return final_df

if __name__ == "__main__":
    # Example
    data = {
        'label': ['A', 'A', 'A', 'B', 'B', 'C', 'C', 'C', 'C', 'A', 'B', 'C'],
        'second_col': ['X', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'Y', 'Z', 'Z', 'Z', 'Z']
    }
    df = pd.DataFrame(data)

    upsampled_on_label = balanced_upsampling(df, label_col='label')
    print(upsampled_on_label)
    downsampled_on_label = balanced_downsampling(df, label_col='label')
    print(downsampled_on_label)
    fixed_on_label = balanced_fixedcount(df, 12, label_col='label')
    print(fixed_on_label)
    upsampled_df = balanced_upsampling(df, label_col='label', second_col='second_col')
    print(upsampled_df)
    downsampled_df = balanced_downsampling(df, label_col='label', second_col='second_col')
    print(downsampled_df)
    fixed_df = balanced_fixedcount(df, 12, 'label', 'second_col')
    print(fixed_df)
