import os


class MorphConstant:
    # Directories
    INIT_DIR = os.path.expanduser("~/.morph")
    CANVAS_DIR = "canvases"
    PUBLIC_DIR = "_public"
    PRIVATE_DIR = "_private"
    TMP_MORPH_DIR = "/tmp/morph"
    # Files
    MORPH_CRED_PATH = os.path.expanduser("~/.morph/credentials")
    MORPH_PROJECT_YAML = "morph_project.yaml"
    MORPH_PROJECT_DB = "morph_project.sqlite3"
    MORPH_PROFILE_PATH = os.path.expanduser("~/.morph/profiles.yaml")
    # Others
    EXECUTABLE_EXTENSIONS = [".sql", ".py"]
