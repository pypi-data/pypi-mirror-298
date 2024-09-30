import os
import streamlit.components.v1 as components

# _RELEASE = False
_RELEASE = True

if not _RELEASE:
  _component_func = components.declare_component(
    "vite_vanilla_component",
    url="http://localhost:5173", # vite dev server port
  )
else:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend/dist")
  _component_func = components.declare_component("vite_vanilla_component", path=build_dir)

def my_component(key=None):
  component_value = _component_func(key=key, default=0)
  return component_value

if not _RELEASE:
  import streamlit as st
  st.subheader("组件测试")
  num_clicks = my_component()
  st.markdown(f"点击了 {num_clicks} 次")