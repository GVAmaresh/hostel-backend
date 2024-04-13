import gdown

def list_files_in_google_drive_folder(folder_url):
    try:
        files = gdown.download_folder(url=folder_url, skip_download=True)
        if files is None:
            print("Failed to retrieve folder contents.")
            return []
        file_ids = []
        for file in files:
            file_ids.append(file.id)
        return file_ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return []