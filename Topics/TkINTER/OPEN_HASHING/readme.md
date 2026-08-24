## Open Address Hashing

Open address hashing creates a table with specified capacity. The elements are inserted directly into cells in the table. If a collision occurs then it is resolved by using different resolution techniques:
- Linear resolution
- Quadratic resolution
- Random resolution

Lineare resolution probes the adjacent cells by using the formula $$(h(x) + 1) % table_size$$. So, it probes the table cell in the sequence $$h(x), h(x)+1, h(x)+2%% in cyclic order terminating at intial cell from where the probe began. Quadratic probe generates the probes in sequence $$h(x), h(x)+1, h(x)+2, h(x)+4, \ldots, h(x)+2^i$$ 
