from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


def make_thumbnail(img, thumb, max_width=370, max_height=220):
    if img:
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """

        image = Image.open(img)
        w, h = image.size
        if w > h:
            width = round(max_height/(h/w))
            thumb_size = (width, max_height)
        else:
            height = round(max_width/(w/h))
            thumb_size = (max_width, height)
        image.thumbnail(thumb_size, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(img.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        thumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

    return True