# Functions used all the generators

import os

# Check if file and path exist, if not, create them. Then rewrite file or add content at the 
# beginning, commenting the existing part.
def create_write_file(file_path, new_content, rewrite = False, comment_start = '<!--', comment_end = '-->'):
    file_param = 'r+'
    if not os.path.exists(file_path):
        file_param = 'w+'
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc: 
            if exc.errno != errno.EEXIST:
                raise Exception('Path cannot be created, please try again.')

    with open(file_path, file_param) as output_file:
        if not rewrite:
            output_file.seek(0)
            content = output_file.read()
            content = comment_start + content
            content += comment_end
            content = new_content + content
        else:
            content = new_content
        output_file.seek(0)
        output_file.truncate()
        output_file.write(content)
        output_file.close()
    