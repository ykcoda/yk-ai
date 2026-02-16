from ipywidgets import FileUpload  # type: ignore
from IPython.display import display


uploader = FileUpload(accept=".png", multiple=False)
display(uploader)


print(uploader.value)
