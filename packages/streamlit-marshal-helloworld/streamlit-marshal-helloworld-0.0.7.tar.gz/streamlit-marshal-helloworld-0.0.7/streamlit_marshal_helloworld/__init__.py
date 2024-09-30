import os
import streamlit.components.v1 as components

# _RELEASE = False
_RELEASE = True

componet_name="streamlit_marshal_helloworld"

if not _RELEASE:
  _component_func = components.declare_component(
    componet_name,
    url="http://localhost:5173", # vite dev server port
  )
else:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend/dist")
  _component_func = components.declare_component(componet_name, path=build_dir)

def streamlit_marshal_helloworld(key=None):
  component_value = _component_func(key=key, default=0)
  return component_value

if not _RELEASE:
  import streamlit as st
  st.subheader("组件测试")
  num_clicks = streamlit_marshal_helloworld()
  st.markdown(f"点击了 {num_clicks} 次")