def get_file_content(file_name):
    with open(file_name) as f:
        content = f.read()
        return content.strip()
