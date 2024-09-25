# streamlit-custom-component

Streamlit component that uses Fluent UI to create a Dropdown box.

## Installation instructions

```sh
pip install streamlit-fluent-dropdown
```

## Usage instructions

```python
import streamlit as st

from fluent_dropdown import fluid_dropdown

keys = ["A", "B", "C", "D"]
labels = ["Item A", "Item B", "Item C", "Item D"]

selected_idx_ = fluid_dropdown(name="default", options=labels)

st.write(keys[selected_idx])
```

The returned value of this component is the index of the selected value. 