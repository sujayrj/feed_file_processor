# gloss-feed-file-processor

## Introduction
**gloss-feed-file-processor** is a file transfer mechanism designed to transfer `.dat` files from **ISTAR-CX** to the **Ops shared drive** and **Gloss Core server**. This project is developed in Python and will be deployed on a **Batch server**. The processor is divided into two main modules:
1. **Receiver**
2. **Dispatcher**

---

## 1. Receiver Module

The **Receiver** module is responsible for transferring files from the source location (**ISTAR export**) to a specific location on localhost. Within localhost, two directories are created that mirror:
- **Ops shared drive**
- **Gloss Core location**

### Workflow:
- **.dat files** are eligible for transfer only if their corresponding **.trg files** are available in the source.
- The **Receiver module** reads from the `receiver-config-{environment}.yaml` file, which contains:
  - **Source server details**
  - **File locations**
  - **Destination details** (where the files need to be transferred)
- **Ops-shared drive transfer**: The files must be renamed using a specified rename pattern provided in the config.
- **Gloss-Core transfer**: The `.dat` files are copied without renaming.
- **.trg files** are transferred to both the **Ops-shared drive** and **Gloss-Core** locations.
- After a successful transfer, the **.trg files** are deleted from the source directory.

### Example Configuration (receiver-config-{environment}.yaml):
```yaml
receivers:
  - name: 'i-star-cx-receiver-system'
    server_name : 'i-star-cx'
    source_path : '<source_path>'
    files:
      - file_name_pattern : 'OL_0360_nn_hhmm_CXI046.dat'
        destination:
          - path : "<destination_path1>"
            should_process : "Rename"
            process_config :
              rename_pattern : 'CXI046_YYMMDD_<nnnnn>_01(MMDD).csv'
          - path : "<destination_path2>"
            should_process : "None"
      - file_name_pattern : 'OL_0360_nn_hhmm_CXI249.dat'
        destination:
          - path : "<destination_path1>"
            should_process : "Rename"
            process_config :
              rename_pattern : 'CXI249_YYMMDD_<nnnnn>_01(MMDD).csv'
          - path : "<destination_path2>"
            should_process : "None"
      - file_name_pattern : 'OL_0360_nn_hhmm_CXI027.dat'
        destination:
          - path : "<destination_path1>"
            should_process : "Rename"
            process_config :
              rename_pattern : 'CXI027_YYMMDD_<nnnnn>_01(MMDD).csv'
          - path : "<destination_path2>"
            should_process : "None"
```

---

## 2. Dispatcher Module

The **Dispatcher** module is responsible for transferring files from the **Ops-shared drive** and **Gloss-Core directories** on localhost to the **actual Ops-shared drive** and **Gloss-Core server**.

### Workflow:
- The **Dispatcher** reads from the `dispatcher_config_{environment}.yaml` file.
- Based on the **destination type** (`shared_drive` or `external_server`), the dispatcher selects the appropriate file transfer mechanism:
  - **Shared Drive**: Files are copied directly using Python’s `shutil.copy()` method.
  - **External Server**: Files are transferred via **SFTP**, with server details retrieved using the `ServerConfigLoader.get_server_info(server_name)` method.
- **File Eligibility**: The `.dat` (or `.csv`) files are transferred only if a corresponding **.trg file** exists in the source.
- **.trg files** are deleted from the source directories after a successful transfer.

### Example Configuration (dispatcher_config_{environment}.yaml):
```yaml
directories:
  - source_directory : "<source_directory>"
    destination_type : "shared_drive"
    destination_details : 
      destination_path : "<destination_path>"
    file_extension : ".csv"
    trigger_extension : ".trg"
    enabled : True
  
  - source_directory : "<source_directory>"
    destination_type : "external_server"
    destination_details : 
      server_name : "gloss-web"
      destination_path : "<destination_path>"
    file_extension : ".dat"
    trigger_extension : ".trg"
    enabled : False
```

---

## Running the Modules

### 1. Receiver:
To run the **Receiver module**, invoke the `main.py` file from the command line and specify the environment (`dev`, `uat`, `prod`, etc.):

```bash
python -m receiver.main --env dev
```

### 2. Dispatcher:
To run the **Dispatcher module**, invoke the `main.py` file similarly, passing the appropriate environment:

```bash
python -m dispatcher.main --env dev
```

---

## Configuration Details

### Receiver Config:
- **Source server details**: Specifies the ISTAR-CX server and the source directory where files are located.
- **Destination details**: Specifies the Ops-shared drive and Gloss-Core directories where files need to be transferred.
- **Rename pattern**: If transferring to the Ops-shared drive, files are renamed based on the specified pattern.

### Dispatcher Config:
- **Source directory**: Specifies the local directories from which files are transferred.
- **Destination type**: Determines whether files are transferred to a shared drive or external server.
- **Trigger file requirement**: The `.dat` or `.csv` files are transferred only if the corresponding `.trg` file is present in the source directory.

---

## Technologies Used
- **Python**: Core programming language.
- **Paramiko**: Used for handling SFTP transfers in the **Dispatcher** module.
- **shutil**: Used for file copying in the **SharedDriveDispatcher** class.

---