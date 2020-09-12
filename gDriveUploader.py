def gDriveUploader(filename):
    '''
    IN: Binary file (Excel)
    OUT: Uploads the file to the specified Google Drive folder 
    Folder location can be changed by changing the ID key in 'parents'
    '''
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    import os

    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)

    # Open the file, 'rb' since it's a binary file
    with open(filename, mode="rb") as file:
        # Create the file in the specified folder
        file_drive = drive.CreateFile({
            'title':os.path.basename(file.name),
            'parents': [{'id': ['1HqQ1mNDYtPwsRRuLKgLGX5JQTRMvTWNr']}]
                })
        # set the contents to that file
        file_drive.SetContentFile(filename) 
        file_drive.Upload()
