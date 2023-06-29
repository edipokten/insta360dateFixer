import os
import re
import datetime
import piexif
import exiftool

filepath = input("Please enter file directory: ")
print("file path: ", filepath)

# Find files with `screenshot` in the name.
files = [f for f in os.listdir(filepath) if "screenshot" in f and f.endswith(".jpg") or f.endswith(".mp4")]
print(files)

for filename in files:
    print(filename)
    # Extract datetime
    date_rex = r"(20\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)"
    date_ranges = re.search(date_rex, filename)
    # Date
    year = date_ranges.group(1)
    month = date_ranges.group(2)
    day = date_ranges.group(3)
    # Time
    hour = date_ranges.group(4)
    minute = date_ranges.group(5)
    second = date_ranges.group(6)
    # date text
    dt_text = f"{year}:{month}:{day} {hour}:{month}:{second}"
    print(dt_text)
    # Image file path
    image_filepath = os.path.join(filepath, filename)
    print("image file path: ",image_filepath)
    if filename.endswith(".jpg"):
        exif_dict = piexif.load(image_filepath)
        print(exif_dict) # Before
        exif_dict["0th"][piexif.ImageIFD.DateTime] = dt_text
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = dt_text
        print(exif_dict) # After
        # Save new metadata
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_filepath)
    elif filename.endswith(".mp4"):
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata([image_filepath])
            print("meta: ",metadata)
            et.set_tags(
                [image_filepath],
                tags={"DateTimeOriginal": dt_text},
                params=["-P", "-overwrite_original"]
            )
            et.set_tags(
                [image_filepath],
                tags={"DateTime": dt_text},
                params=["-P", "-overwrite_original"]
            )






