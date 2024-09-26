# Intro:
Provides APIs to collect/copy files to destination directory by file name pattern from given directories in script dir
## Methods:

### Method  `collect_files`
collect_files(patterns: str | list[str], src_dirs: str | list[str] = '.', dest: str | os.PathLike = 'static', exclude_dir: str | list[str] = [], maintain_hierarchy: bool = True, respect_git_ignore: bool = True) -> bool
 
Args:

    patterns (str | list[str]): Pattern to search files.
    src_dirs (list[str]): List of source directory relative path
    dest (str | os.PathLike): directory where files will be copied to
    exclude_dir (str | list[str]): directory/directories to exclude
    maintain_hierarchy (bool): If True then copied files will keep directory hierarchy relative to root dir
    respect_git_ignore (bool): If True then function will return False if given directory is ignored by git
    
Returns:

    newFiles (list[os.PathLike]): List of new copied file paths in destination directory.
### Method  `get_files`

get_files(patterns: str | list[str], src_dirs: str | list[str] = '.', exclude_dir: str | list[str] = 'static', respect_git_ignore: bool = True) -> list[str]
 
Args:

    patterns (str | list[str]): Pattern to search files.
    src_dirs (list[str]): List of source directory relative path
    exclude_dir (str | list[str]): directory/directories to exclude
    respect_git_ignore (bool): If True then function will return False if given directory is ignored by git

Returns:

    files (list[os.PathLike]): List of file paths.

### Method `get_src_dir_path`

get_src_dir_path(root_dir: os.PathLike, src_dir: str, respect_git_ignore: bool = True) -> bool | os.PathLike

Args:

    root_dir (os.PathLike): base absolute path
    src_dir (str): source directory relative path
    respect_git_ignore (bool): If True then function will return False if given directory is ignored by git

Returns:

    src_dir (bool | os.PathLike): False if path is ignored by git, Full `src_dir` path otherwise.

### Method `get_src_dirs`

get_src_dirs(root_dir: os.PathLike, src_dirs: list[str], respect_git_ignore: bool = True) -> list[None | os.PathLike]

Args:

    root_dir (os.PathLike): base absolute path
    src_dirs (list[str]): List of source directory relative path
    respect_git_ignore (bool): If True then function will return False if given directory is ignored by git

Returns:

    src_dirs (list[os.PathLike]): List of Full path from `src_dirs`.

### Method `is_ignored`

is_ignored(file_or_dir: str | os.PathLike) -> bool

Args:

    file_or_dir (str): Name or path string of the file/directory to check
 
Returns:

    is_ignored (bool): True if file/directory is ignore, false otherwise
    
:raises:

    CalledProcessError: If return code for command `git check-ignore -q <file_or_dir>` not 0 or 1

### Method `pop_all`

pop_all(li: list) -> list

Returns same emptied list
