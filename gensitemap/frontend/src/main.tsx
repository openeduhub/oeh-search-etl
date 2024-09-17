// add the beginning of your app entry
import 'vite/modulepreload-polyfill'

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

const root = document.getElementById('root')!;
// convert all the "data-" attributes to a javascript object that we
// can pass as props to the component
const camelize = s => s.replace(/-./g, x=>x[1].toUpperCase())
const props = Object.fromEntries(
  Array.from(root.attributes)
    .filter(attr => attr.name.startsWith('data-'))
    .map(attr => [camelize(attr.name.slice(5)), attr.value])
)
console.log("props:", props);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App {...props} />
  </React.StrictMode>,
)
