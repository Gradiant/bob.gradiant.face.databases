
def get_filter_dataset_by_subset(subset, datasets):
    filter_datasets = []
    for dataset in datasets:
        filter_datasets.append({"name": dataset, "subsets": [subset]})
    return filter_datasets


def get_filter_dataset_all_subsets(datasets):
    filter_datasets = []
    for dataset in datasets:
        filter_datasets.append({"name": dataset, "subsets": ["Train", "Dev", "Test"]})
    return filter_datasets
