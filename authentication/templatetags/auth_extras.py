from django import template

register = template.Library()


@register.filter(name='filterFiles')
def filterFiles(files, filter):
    new_downloads = []
    for download in files:
        if download.category == filter:
            new_downloads.append(download)
    return len(new_downloads)


@register.filter(name='getSize')
def getSize(files, filter):
    size = 0
    for download in files:
        if download.category == filter:
            size = size + download.file.size
            print(size)
    return size
 