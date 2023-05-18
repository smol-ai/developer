import os

# Prompt the user for the description and app name
description = input("Enter the description: ")
app_name = input("Enter the app name: ")

# Read the input .md file
with open('plugins.md', 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('{{description}}', description)
filedata = filedata.replace('{{app_name}}', app_name)

# Write the file out again
with open(f'{app_name}.md', 'w') as file:
    file.write(filedata)

print(f"New .md file '{app_name}.md' has been created.")