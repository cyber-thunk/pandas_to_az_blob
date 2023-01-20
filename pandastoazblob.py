def write_to_az_blob(excel_data:pd.DataFrame,
                     config_data:dict,
                     JobId:str):
    """Write the pandas dataframe to a csv file in Azure Blob Storage.
    Args:
        excel_data (pd.DataFrame): This is the dataframe containg values pulled
            from the a sheet in the Excel file.
        config_data (dict): This is the dictionary containing the configuration
            data.
        JobId (str): This is the unique id for the job associated w/ the excel file
    """
    excel_data = excel_data.reset_index(drop=True)
    excel_data = excel_data.drop([0])
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(config_data.get('azure_blob').\
                                                                   get('connection_string'))
    # Create the container
    container_client = blob_service_client.get_container_client(config_data.get('azure_blob').\
                                                                get('container_name'))
    # Prep dataframe for upload
    output = excel_data.to_csv(index=False, encoding='utf-8')
    blob_client = container_client.get_blob_client(f"{JobId}.csv")
    blob_client.upload_blob(output, overwrite=True)

    print(f"File {JobId}.csv uploaded to Azure Blob Storage.")
