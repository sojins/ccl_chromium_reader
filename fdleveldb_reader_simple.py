import sys
from ccl_chromium_reader import ccl_chromium_indexeddb

def run(db_dir, blob_dir=None):
    # assuming command line arguments are paths to the .leveldb and .blob folders
    leveldb_folder_path = db_dir #sys.argv[1]
    blob_folder_path = blob_dir #sys.argv[2]

    # open the indexedDB:
    wrapper = ccl_chromium_indexeddb.WrappedIndexDB(leveldb_folder_path, blob_folder_path)

    # You can check the databases present using `wrapper.database_ids`

    # Databases can be accessed from the wrapper in a number of ways:
    # db = wrapper[2]  # accessing database using id number
    # db = wrapper["MyTestDatabase"]  # accessing database using name (only valid for single origin indexedDB instances)
    # db = wrapper["MyTestDatabase", "file__0@1"]  # accessing the database using name and origin

    # find table name
    db_name = ''
    for name in wrapper._db_name_lookup:
        if 'Teams:conversation-manager:react-web-client' in name[0]:
            print(name)
            db_name = name[0]
            break
    
    # db = wrapper['teams-service-worker-v2']
    # db = wrapper['teams-service-worker-v2', 'https_teams.live.com_0@1']
    db_idx = 0x13
    # db_name = 'Teams:conversation-manager:react-web-client:9188040d-6c67-4c5b-b112-36a304b66dad:00000000-0000-0000-f5d0-875f54c2be1e:ko-kr'
    if db_name:
        db_idx = db_name
    db = wrapper[db_idx]

    # NB using name and origin is likely the preferred option in most cases

    # The wrapper object also supports checking for databases using `in`

    # You can check for object store names using `db.object_store_names`

    # Object stores can be accessed from the database in a number of ways:
    obj_store = db[1]  # accessing object store using id number
    obj_store = db["conversations"]  # accessing object store using name
    

    # Records can then be accessed by iterating the object store in a for-loop
    for record in obj_store.iterate_records():
        try: print(record.user_key)
        except: pass
        print(record.value)

        # if this record contained a FileInfo object somewhere linking
        # to data stored in the blob dir, we could access that data like
        # so (assume the "file" key in the record value is our FileInfo):
        try:
            with record.get_blob_stream(record.value["file"]) as f:
                file_data = f.read()
        except Exception as e:
            # print(e)
            file_data = None

    # By default, any errors in decoding records will bubble an exception 
    # which might be painful when iterating records in a for-loop, so either
    # passing True into the errors_to_stdout argument and/or by passing in an 
    # error handler function to bad_deserialization_data_handler, you can 
    # perform logging rather than crashing:

    for record in obj_store.iterate_records(
            errors_to_stdout=True, 
            bad_deserializer_data_handler= lambda k,v: print(f"error: {k}, {v}")):
        try: print(record.user_key) 
        except: pass
        print(record.value)

if __name__ == "__main__":
    # db_dir=r'G:\Examples\~MSTeams\Lee'
    # blob_dir=r'G:\Examples\~MSTeams\Lee'
    db_dir=r'G:\Examples\~MSTeams\김지민\https_teams.live.com_0.indexeddb.leveldb'
    run(db_dir=db_dir)
