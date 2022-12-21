import pandas as pd

def merge_input_list(file_path1, file_path2):
    patient_df = pd.read_csv(file_path1)
    physician_df = pd.read_csv(file_path2)
    result = pd.concat([patient_df, physician_df])
    result_no_dup = result.drop_duplicates()
    result_no_dup['Words'].to_csv('./input/input_list.csv', index=False)

if __name__ == '__main__':
    file_path1 = "./input/input_list_patient.csv"
    file_path2 = "./input/input_list_physician.csv"
    merge_input_list(file_path1, file_path2)