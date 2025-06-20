import os
import json
from dotenv import load_dotenv

def list_image_files(directory):
    """List all image files in the given directory"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    image_files = []
    
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(file)
            
    return image_files

def main():
    # Load environment variables for API key
    load_dotenv()
    
    
    # Define the directory path
    project_root = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(project_root, "assets", "images")
    
    # Get all image files
    image_files = list_image_files(images_dir)
    
    # Create a dictionary to store image metadata
    image_metadata = {}
    
    # Process each image
    for idx, image_file in enumerate(image_files):
        print(f"Processing image {idx+1}/{len(image_files)}: {image_file}")
        
        # Get the name without extension to use as key
        name_without_ext = os.path.splitext(image_file)[0]
        
        # Get full path to the image
        image_path = os.path.join(images_dir, image_file)
        
        # Add to metadata dictionary
        image_metadata[name_without_ext] = {
            "filename": image_file,
        }
        
        print(f"Added description for {image_file}")
        
    # Write metadata to JSON file
    output_file = os.path.join(project_root, "data", "image_metadata.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"Image metadata saved to {output_file}")

if __name__ == "__main__":
    main()