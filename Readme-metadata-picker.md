# Install

You will need poetry and python3.9:
```shell script
sudo apt-get install python3.9     
python3.9 -m pip3 install poetry
```

# Launching the container

1. Start the container by executing `run.sh` from the main folder, not from `src`
2. The container can be reached on `http://0.0.0.0:5057`

# Accessing the Swagger UI

The Swagger UI of FastApi can be access by:
- `http://0.0.0.0:5057/redoc`
- or alternatively `http://0.0.0.0:5057/doc`

# Testing REST

1. Start the container
2. Execute:
    ```shell script
    curl --location --request POST '0.0.0.0:5057/extract_meta' \
    --header 'Content-Type: application/json' \
    --data-raw '{"url": "here", "html": "cool_content123", "headers": ""}'
    ```
3. You should get
    ```shell script
   {"url":"here","meta":{...}}     
    ```

# Pre commit

To see tracebacks of why the pre commit hook fails run in terminal:
``` shell script
pre-commit run --all-files 
```

# Adding new features for detection

To add a new feature, it must inherit from MetadataBase.
The class must be included in 
1. "src/features/metadata_manager.py:_create_extractors"
2. app.api.ExtractorTags
3. app.api.ListTags