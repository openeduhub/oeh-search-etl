import React, { useState } from 'react';

import { Rule } from './schema';

// A component that shows some text. When clicked, the text becomes editable.
// If you press enter or click outside, it accepts. If you press ESC, it cancels.
function Editable(props: { value: string, onChange: (value: string) => void }) {
  const [editing, setEditing] = useState(false);
  const [value, setValue] = useState(props.value);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      setEditing(false);
      props.onChange(value);
    } else if (e.key === 'Escape') {
      setEditing(false);
      setValue(props.value);
    }
  }

  function startEditing() {
    setEditing(true);
    setValue(props.value);
  }

  return <span onClick={startEditing} onFocus={startEditing} tabIndex={(!editing) ? 0 : undefined} >
    {props.value}
    {editing ? <input value={value} onChange={(e) => setValue(e.target.value)} onKeyDown={handleKeyDown} autoFocus onBlur={() => setEditing(false)} /> : ""}
  </span>
}

type RuleTableProps = {
  rules: Rule[],
  onDelete: (id: number) => void,
  onAdd: (id: number) => void,
  onMoveUp: (id: number) => void,
  onMoveDown: (id: number) => void,
  onShowDetails: (id: number) => void,
  onUpdateFields: (id: number, fields: { rule?: string, include?: boolean, page_type?: string }) => void,
}


export default function RuleTable(props: RuleTableProps) {
  return <table className="table">
    <thead>
      <tr>
        <th>URL Pattern</th>
        <th>Matches</th>
        <th>New Matches</th>
        <th>Include</th>
        <th>Type</th>
        <th>Position</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      {props.rules.map((rule: Rule) => {
        return <tr key={rule.id}>
          <EditableTD value={rule.rule} onChange={newValue => props.onUpdateFields(rule.id, {rule: newValue})} />
          <td>{rule.count}</td>
          <td>
            <div style={{display: "flex", alignItems: "center"}}>
              <div style={{flex: 1}}>{rule.cumulative_count}</div>
              <button className="mybutton mybutton-table" onClick={() => props.onShowDetails(rule.id)}>🔍</button>
            </div>
          </td>
          <td>
            <input type="checkbox" checked={rule.include} onChange={(e) => props.onUpdateFields(rule.id, {include: e.target.checked})} id={"include"+rule.id}/>&nbsp;
            <label htmlFor={"include"+rule.id}>{rule.include ? 'Yes' : 'No'}</label>
          </td>
          <EditableTD value={rule.page_type} onChange={newValue => props.onUpdateFields(rule.id, {page_type: newValue})} />
          <td>{rule.position}</td>
          <td>
            <button className="mybutton mybutton-table mybutton-delete" onClick={(e) => props.onDelete(rule.id)}>×</button>
            <button className="mybutton mybutton-table" onClick={(e) => props.onAdd(rule.id)}>+</button>
            <button className="mybutton mybutton-table" disabled={rule.position == 1} onClick={(e) => props.onMoveUp(rule.id)}>&uarr;</button>
            <button className="mybutton mybutton-table" disabled={rule.position == props.rules.length} onClick={(e) => props.onMoveDown(rule.id)}>&darr;</button>
          </td>
        </tr>
      })}
    </tbody>
  </table>
}

function EditableTD(props: { value: string, onChange: (value: string) => void }) {
  return <td className="editable-cell"><Editable value={props.value} onChange={props.onChange} /></td>
}