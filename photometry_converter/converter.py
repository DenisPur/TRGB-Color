import sys
import argparse
import pandas as pd


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Convert photometry data to CSV format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script.py -f data.txt -o output.csv
  python script.py --file observations.dat --output results.csv
        """
    )
    
    parser.add_argument(
        '--file', '-f', 
        required=True,
        help='Input file with raw photometry data'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True, 
        help='Output CSV filepath'
    )
    
    return parser.parse_args()


def read_data_file(file_path: str, skip_rows: int=0) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(
            file_path, 
            skiprows=skip_rows,
            sep=r'\s+',
            engine='python',
            header=None
        )
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def select_data_start(file_path: str, show_lines: int=5) -> int:
    """
    Shows first lines and ask how many to skip
    """
    with open(file_path, 'r') as f:
        lines = [f.readline() for _ in range(show_lines)]
    
    if show_lines:
        print(f"First {MAGENTA}{show_lines}{RESET} lines:")
        for i, line in enumerate(lines):
            print(f"{MAGENTA}{i}{RESET}: {line.strip()}")
    
    while True:
        try:
            skip = int(input("Number of header lines to skip: "))
            return skip
        except ValueError:
            print("Please enter a valid integer")


def select_columns_interactive(df: pd.DataFrame) -> dict[str, int]:
    def process_one_column_entrance(mandatory_column: bool) -> None:
        nonlocal column_mapping
        nonlocal index, col_name
        nonlocal total_number_of_columns

        try:
            del column_mapping[col_name]
        except:
            pass

        if mandatory_column:
            user_input = input(f"[{index+1}/{total_number_of_columns}] Select column number for {MAGENTA}'{col_name}'{RESET} (b - back): ").strip().lower()
            if user_input == 'n':
                print('This column is required and cannot be skipped!')
                return
        else:
            user_input = input(f"[{index+1}/{total_number_of_columns}] Select column number for {MAGENTA}'{col_name}'{RESET} (b - back, [n] - skip): ").strip().lower()
            if user_input == 'n' or user_input == '':
                print('Column skipped')
                index += 1
                return
        if user_input == 'b':
            if index == 0:
                print('Already at the first column')
                return
            print('Returning to previous column')
            index -= 1
            return
        try:
            col_idx = int(user_input) - 1
            if 0 <= col_idx < len(df.columns):
                preview = df.iloc[:5, col_idx].tolist()
                print(f"Preview: {preview} etc")
                confirm = input("Confirm? ([y]/n): ").strip().lower()
                if confirm == 'y' or confirm == '':
                    column_mapping[col_name] = col_idx
                    index += 1
                    return
                else:
                    print("Try again")
            else:
                print(f"Column number must be between 1 and {len(df.columns)}")
        except ValueError:
            print("Please enter a number, 'n' (skip), or 'b' (back)")
        return

    column_mapping = {} # new_name : old_idx

    required = ['x', 'y', 'mag_v', 'err_v', 'mag_i', 'err_i']
    optional = ['type', 'snr_v', 'snr_i', 'sharp_v', 'sharp_i', 
                'round_v', 'round_i', 'crowd_v', 'crowd_i', 
                'flag_v', 'flag_i']
    
    print(f"Total columns: {len(df.columns)}")

    index = 0
    total_number_of_columns = len(required + optional)
    while index < total_number_of_columns:
        col_name = (required + optional)[index]
        if col_name in required:
            process_one_column_entrance(True)
        else:
            process_one_column_entrance(False)

    return column_mapping


def create_output_csv(df: pd.DataFrame, column_mapping, output_path: str) -> None:
    output_data = {}
    for new_name, old_idx in column_mapping.items():
        output_data[new_name] = df.iloc[:, old_idx]
    
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_path, index=False)
    print(f"Successfully saved {len(output_df)} rows with {len(output_df.columns)} columns to {output_path}")


def main():
    args = parse_arguments()

    skip_rows = select_data_start(args.file)

    df = read_data_file(args.file, skip_rows)
    if df is None:
        return

    column_mapping = select_columns_interactive(df)

    create_output_csv(df, column_mapping, args.output)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nOperation cancelled by user.')
        sys.exit(1)
