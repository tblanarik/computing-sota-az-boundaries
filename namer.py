import json
import argparse
import os

def find_all_geojson_files(directory):
    """
    Find all .geojson files in the given directory and its subdirectories.
    """
    import os
    geojson_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.geojson'):
                geojson_files.append(os.path.join(root, file))
    return geojson_files


def parse_geojson_filename(filename):
    """
    Parse a filename of the form W7W_XX_NNN.geojson and return W7W/XX-NNN.
    """
    base_name = os.path.basename(filename)
    if not base_name.endswith('.geojson'):
        raise ValueError("Filename must end with .geojson")
    
    # Remove .geojson and split by '_'
    parts = base_name[:-8].split('_')  
    if len(parts) != 3:
        raise ValueError("Filename must be in the format W7W_XX_NNN.geojson")
    
    return f"{parts[0]}/{parts[1]}-{parts[2]}"

def update_geojson_with_parsed_name(file_path):
    """
    Update the 'features.properties' field in a .geojson file with the parsed name from its filename.
    """
    try:
        # Parse the filename to get the name
        parsed_name = parse_geojson_filename(file_path)

        # Open the .geojson file and load its content
        with open(file_path, 'r') as f:
            geojson_data = json.load(f)

        # Update the 'features.properties' field with the parsed name
        for feature in geojson_data.get('features', []):
            if 'properties' in feature:
                feature['properties']['title'] = parsed_name

        # Save the updated .geojson file without spaces
        with open(file_path, 'w') as f:
            json.dump(geojson_data, f, separators=(',', ':'))

    except ValueError as e:
        print(f"Error parsing filename for {file_path}: {e}")
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find all .geojson files in a directory.")
    parser.add_argument('directory', type=str, help='The directory to search for .geojson files.')
    args = parser.parse_args()

    geojson_files = find_all_geojson_files(args.directory)
    
    for file in geojson_files:
        try:
            update_geojson_with_parsed_name(file)
        except ValueError as e:
            print(f"Error parsing file {file}: {e}")