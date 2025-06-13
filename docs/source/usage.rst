Usage Examples
==============

Basic usage:

.. code-block:: bash

   python -m zipcli.main
   python -m zipcli.main myfolder --filter "*.txt"
   python -m zipcli.main logs --exclude "secret*" --date-format "%Y-%m-%d" --inventory --backup-location /backups

CLI Flags
---------

- `folder` – the source folder (defaults to current)
- `--filter` – include only matching patterns
- `--exclude` – exclude matching patterns
- `--include` – overrides filter
- `--inventory` – list included files
- `--date-format` – custom timestamp
- `--backup-location` – where to store .zip
