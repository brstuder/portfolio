# Engineering Flowchart

!!! info "Author's Note"

    The following is a humorous demonstration of Mermaid, a tool for generating flowcharts directly in documentation, by recreating a long-circulated "Engineering Flowchart" graphic for troubleshooting.

```mermaid
    graph TD
        A(Does it move?) -->|Yes| B(Is it supposed to?);
        A(Does it move?) -->|No| C(Is it supposed to?);
        B -->|Yes| D(No problem here!);
        B -->|No| E(Duct tape!);
        C -->|Yes| F(WD-40!);
        C -->|No| G(No problem here!);
```
