"""Support functions to be used in multiple DAGS."""
import yaml


def read_yaml_file(file_address: str) -> dict:
    """Reads yaml file as dict.

    Parameters
    ----------
    file_address: str
        Path to the file we want to read

    Returns
    -------
    dict
        File's content as dict
    """
    with open(file_address, 'r', encoding='utf8') as stream:
        return yaml.safe_load(stream)
