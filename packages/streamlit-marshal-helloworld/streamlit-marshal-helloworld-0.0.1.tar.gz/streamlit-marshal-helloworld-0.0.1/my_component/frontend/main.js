import { Streamlit } from "streamlit-component-lib"

const span = document.body.appendChild(document.createElement("span"))
const button = span.appendChild(document.createElement("button"))
button.textContent = "按这里"

let numClicks = 0
button.onclick = function () {
  numClicks += 1
  Streamlit.setComponentValue(numClicks)
}

function onRender(event) {
  Streamlit.setFrameHeight(button.offsetHeight + 10)
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()