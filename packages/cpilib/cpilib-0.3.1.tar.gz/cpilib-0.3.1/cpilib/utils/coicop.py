import pandas as pd
import pkg_resources

abs_file_path = pkg_resources.resource_filename("cpilib", "data/hicp_labels.csv")
coicop_labels = pd.read_csv(abs_file_path, dtype={"code": str})
coicop_mapping = coicop_labels.assign(code="CP" + coicop_labels["code"]).set_index("code")["label"]
