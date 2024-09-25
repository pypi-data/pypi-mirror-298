
def get_annotation_with_name(taxonomy, cell_label, labelset, compare_func=None):
    """
    Get an annotation with a given cell label and labelset in the given taxonomy.
    :param taxonomy: taxonomy object
    :param cell_label: cell label
    :param labelset: labelset
    :param compare_func: optional function to compare cell labels (such as `lambda x, y: x.endswith(y)`)
    :return: annotation object. None if not found
    """
    cell_label = str(cell_label).strip()
    for annotation in taxonomy.annotations:
        if annotation.labelset == labelset:
            if compare_func:
                if compare_func(annotation.cell_label, cell_label):
                    return annotation
            else:
                if annotation.cell_label == cell_label:
                    return annotation
    return None
