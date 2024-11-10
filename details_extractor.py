import re
import sys

def extract_data(input_file, output_file):
    # Open the input file and read its contents
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = infile.read()

    # Regular expressions to match the required fields
    nickname_pattern = r'"nickname":"([^"]+)"'
    user_id_pattern = r'"user_id":(\d+)'
    nationality_pattern = r'"nationality":"([^"]+)"'
    head_url_pattern = r'"head_url":"([^"]+)"'

    # Find all matches for each field
    nicknames = re.findall(nickname_pattern, data)
    user_ids = re.findall(user_id_pattern, data)
    nationalities = re.findall(nationality_pattern, data)
    head_urls = re.findall(head_url_pattern, data)

    # Check if all fields have the same number of matches (i.e., they correspond to the same user)
    num_entries = len(nicknames)

    if num_entries == len(user_ids) == len(nationalities) == len(head_urls):
        # Open the output file in append mode and write the data
        with open(output_file, 'a', encoding='utf-8') as outfile:
            for i in range(num_entries):
                # Write each user's data in the desired format
                outfile.write(f"Nickname: {nicknames[i]}\n")
                outfile.write(f"User ID: {user_ids[i]}\n")
                outfile.write(f"Nationality: {nationalities[i]}\n")
                outfile.write(f"Head URL: {head_urls[i]}\n")
                outfile.write('-' * 40 + '\n')  # Separate entries with a line of dashes
        print(f"Data successfully extracted and saved to {output_file}")
    else:
        print("Error: Data mismatch detected. Please check the file format.")

if __name__ == "__main__":
    # Ensure the user provided exactly two arguments: input file and output file
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file_name output_file_name")
        sys.exit(1)

    # Get the input file and output file from command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Call the function to extract and save the data
    extract_data(input_file, output_file)
