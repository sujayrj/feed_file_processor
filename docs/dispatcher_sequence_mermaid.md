sequenceDiagram
    participant Autosys
    participant Dispatcher
    participant ConfigLoader
    participant DispatcherFactory
    participant SharedDriveDispatcher
    participant SFTPDispatcher
    participant ServerConfigLoader
    participant SFTPHelper

    Autosys ->> Dispatcher: Trigger main method
    Dispatcher ->> ConfigLoader: Load dispatcher_config.yaml
    ConfigLoader -->> Dispatcher: Return configuration

    loop For each directory in config
        Dispatcher ->> DispatcherFactory: Get Dispatcher based on destination_type
        alt destination_type = shared_drive
            DispatcherFactory ->> SharedDriveDispatcher: Instantiate
            DispatcherFactory -->> Dispatcher: Return SharedDriveDispatcher
            Dispatcher ->> SharedDriveDispatcher: Call transfer()
            SharedDriveDispatcher ->> SharedDriveDispatcher: Copy files with shutil2.copy()
            SharedDriveDispatcher ->> Dispatcher: Files copied, delete .trg files
        else destination_type = external_server
            DispatcherFactory ->> ServerConfigLoader: Get server_info(server_name)
            ServerConfigLoader -->> DispatcherFactory: Return server_info
            DispatcherFactory ->> SFTPDispatcher: Instantiate with server_info
            DispatcherFactory -->> Dispatcher: Return SFTPDispatcher
            Dispatcher ->> SFTPDispatcher: Call transfer()
            SFTPDispatcher ->> SFTPHelper: Use upload_file() to transfer files
            SFTPHelper -->> SFTPDispatcher: Files transferred
            SFTPDispatcher ->> Dispatcher: Files copied, delete .trg files
        end
    end

    Dispatcher -->> Autosys: Return success
