from storages.backends.azure_storage  import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'gifpersonalizerstorage' # <storage_account_name>
    account_key = 'RoKTD57T2Nodutp2R6yrvk5v8qkUqCI4NeVxS/t3GU8wY/MCO5a8LUCrdgApzX6twRzV2xDAcR1n9FQ7T1FU2g==' # <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
