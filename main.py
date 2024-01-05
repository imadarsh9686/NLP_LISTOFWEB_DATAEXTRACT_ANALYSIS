import os
import pandas as pd
from extractor import DataExtractor
from analyzer import DataAnalyzer

# Set the working directory
os.chdir("D:/nlp data scraping and extraction")

stop_words_folder = 'StopWords'
positive_words_path = 'MasterDictionary/positive-words.txt'
negative_words_path = 'MasterDictionary/negative-words.txt'

output_directory = "output_data"
os.makedirs(output_directory, exist_ok=True)

# Create instances of the extractor and analyzer classes
extractor = DataExtractor(output_directory="output_data")
analyzer = DataAnalyzer(stop_words_folder, positive_words_path, negative_words_path)

# Read input data from Excel file
df = pd.read_excel('Input.xlsx')

# Create DataFrame for output
output_columns = pd.read_excel('Output Data Structure.xlsx', header=None, names=['Variable'])['Variable'].tolist()
df_output = pd.DataFrame(columns=output_columns)

data_list = []

for index, row in df.iterrows():
    # Extract numeric part from 'URL_ID'
    numeric_part = ''.join(filter(str.isdigit, row['URL_ID']))
    
    if numeric_part:
        url_id = int(numeric_part)
        url = row['URL']
        
        # Construct the output file path
        output_filename = f"blackassign{url_id:04d}.txt"
        output_filepath = os.path.abspath(os.path.join(output_directory, output_filename))

        # Ensure the directory structure exists
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

        title, article_text = extractor.extract_article(url, output_filepath)
        
        if article_text is not None:
            analysis_results = analyzer.analyze_text(article_text)
            
            # Create a dictionary
            new_row = {
                'URL_ID': url_id,
                'Title': title,
                'Num_Sentences': analysis_results[4],  # Assuming avg_sentence_length is at index 4
                # Add other computed variables as needed
            }
            
            # Append the dictionary to the list
            data_list.append(new_row)

# Create the DataFrame from the list
df_output = pd.DataFrame(data_list)

output_file = 'output_results.xlsx'
df_output.to_excel(output_file, index=False)
print(f"Textual analysis results saved to {output_file}")
