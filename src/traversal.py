import os
import fnmatch

def traverse_dir(root_dir, include_patterns=None, exclude_patterns=None):
    """
    # Example usage:
      root_dir = '/path/to/directory'
      include_patterns = ['*.txt', '*.py']  # Include files matching these patterns
      exclude_patterns = ['exclude_dir1/*', 'exclude_dir2/*']  # Exclude directories matching these patterns

      for file_path in traverse_dir(root_dir, include_patterns=include_patterns, exclude_patterns=exclude_patterns):
          print(file_path)
    """
    for root, dirs, files in os.walk(root_dir):
        if exclude_patterns and any(fnmatch.fnmatch(root, pattern) for pattern in exclude_patterns):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if include_patterns and not any(fnmatch.fnmatch(file_path, pattern) for pattern in include_patterns):
                continue
            yield file_path


