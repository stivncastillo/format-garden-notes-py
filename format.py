import os
import frontmatter
import shutil

from slugify import slugify
from datetime import date, datetime

root_folder = '/Users/stiven/Obsidian/Garden'
destination_folder = '/Users/stiven/Projects/Frontend/digital-garden/src/content/notes'

def rename_files_to_slug(source_folder, dest_folder):
    today = date.today()
    files_to_exclude = set(['Templates', 'Obsidian'])
    # get last updated date
    last_update_file = open("lastUpdate.txt", "a+")
    last_update_file.seek(0)
    saved_date = last_update_file.readline()
    last_update_date = datetime.strptime(saved_date, "%Y-%m-%d").date()

    print("Last update date:", last_update_date)

    for root, dirnames, filenames in os.walk(source_folder):
        dirnames[:] = [d for d in dirnames if d not in files_to_exclude]
        for filename in filenames:
            if filename.endswith('.md'):
                old_path = os.path.join(root, filename)
                print("Formating file:", old_path)
                with open(old_path) as reader:
                    content = reader.read()
                    # read frontmatter data
                    data = frontmatter.loads(content)
                    category = data["category"].lower()
                    updated_at = data["updatedAt"]
                    isPublished = data["published"]

                    # if (updated_at >= last_update_date):
                    if (isPublished):
                        title = filename.replace('.md', '')
                        # slugify the file name
                        new_filename = slugify(title) + '.md'
                        # create the new path (destination)
                        new_path_name = os.path.join(dest_folder, category)
                        # if the folder doesn't exists, create a new
                        is_folder_exist = os.path.exists(new_path_name)
                        if not is_folder_exist:
                            os.mkdir(new_path_name)

                        new_path = os.path.join(dest_folder, category, new_filename)
                        # copy the file to the new path
                        shutil.copy(old_path, new_path)
                        # print("Created => ", new_path)
    open('lastUpdate.txt', 'w').close()
    last_update_file.write(today.strftime('%Y-%m-%d'))
    print("Writing date of last update:", today)
    last_update_file.close()

# Rename files to slug style
rename_files_to_slug(root_folder, destination_folder)