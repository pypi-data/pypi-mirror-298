class FileCategories:
    PlainText = (".txt", ".asc", ".lst", ".js", ".vbs", ".py", ".tcl", ".pl", ".groovy")                # Done
    StructuredText = (".json", ".sql")                                                                  # Done
    Document = (".doc", ".dot", ".docm", ".mht", ".docx")                                               # Done 
    PDF = (".pdf",)                                                                                     # Done
    Spreadsheet = (".xls", ".xlsx", ".xlsm", ".xlsb", ".csv", ".ods")                                   # Skipping for now 
    Presentation = (".pptx",)                                                                           # Done
    Email = (".msg",)                                                                                   # Need help decoding
    Image = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".avif", ".jfif")        # Skipping for PnG
    Video = (".mp4", ".avi", ".mov", ".wmv", ".mkv")                                                    # Skipping for PnG
    Archive = (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".dmg")                                    # Not Decided
    Certificate = (".cer", ".pem", ".der")                                                              # Done 
    