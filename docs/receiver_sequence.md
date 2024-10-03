@startuml
actor Autosys
participant Receiver
participant ConfigLoader
participant ReceiverFactory
participant IStarCXReceiver
participant RenameTransformer
participant NoOpTransformer

Autosys -> Receiver: Start
Receiver -> ConfigLoader: Load receiver_config.yaml
ConfigLoader --> Receiver: Return Configuration

Receiver -> ReceiverFactory: Get Receiver Implementation
ReceiverFactory -> IStarCXReceiver: Instantiate IStarCXReceiver
ReceiverFactory --> Receiver: Return IStarCXReceiver

Receiver -> IStarCXReceiver: Call transfer()

IStarCXReceiver -> IStarCXReceiver: Iterate over files
alt should_process = 'None'
    IStarCXReceiver -> NoOpTransformer: Call NoOpTransformer
    NoOpTransformer --> IStarCXReceiver: Transfer without renaming
else should_process = 'Rename'
    IStarCXReceiver -> RenameTransformer: Call RenameTransformer
    RenameTransformer --> IStarCXReceiver: Rename and transfer files
end

IStarCXReceiver --> Receiver: Files transferred
Receiver --> Autosys: Return success

@enduml
