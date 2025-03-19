# create file to hold data (add .txt extension)
file_name = "write_experiment"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# settings to write to file...
heading = "=== MMF TEST ===\n"
content = "Random Content"
more = "more content"


# list of strings
to_write = [heading, content, more]

# print the output
for item in to_write:
    print(item)

for item in to_write:
    text_file.write(item)
    text_file.write("\n")
