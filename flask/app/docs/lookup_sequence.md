```mermaid    
    sequenceDiagram         
        participant Client
        participant Server
        participant SamKnows
        participant Database
        Client->>+Server:Postcode
        Server->>-Server:Validate Postcode
        Server->>+SamKnows:Postcode
        SamKnows->>-Server:Exchange
        Server->>+Database:Exchange Lookup
        Database->>-Server:FTTP
        Server->>Client:Decommission Date

