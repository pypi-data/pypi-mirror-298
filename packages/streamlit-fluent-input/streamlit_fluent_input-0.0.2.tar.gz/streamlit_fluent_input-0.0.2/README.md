# streamlit-custom-component

Streamlit component that uses Fluent UI to create a Dropdown box.

## Installation instructions

```sh
pip install streamlit-fluent-input
```

## Usage instructions

```python
import streamlit as st
from fluent_input import fluent_input


test = fluent_input(name="fluid-input", label="Test Input")
st.write(test)
```

The returned value of this component is the index of the selected value. 