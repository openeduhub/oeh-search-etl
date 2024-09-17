// Add this at the beginning of your app entry.
import 'vite/modulepreload-polyfill';

import { useEffect, useState } from 'react';
import './App.css';
import RuleTable from './RuleTable';
import { FilterSet, Rule, UnmatchedResponse } from './schema';
import { MatchesDialog } from './MatchesDialog';


function App(props: { filterSetId: number, csrfToken: string }) {
  const [filterSet, setFilterSet] = useState<FilterSet | null>(null);
  const [rules, setRules] = useState<Rule[]>([]);
  const [detailsVisible, setDetailsVisible] = useState(false);
  // type is a json dict
  const [selectedRuleDetails, setSelectedRuleDetails] = useState({});
  const [unmatchedUrls, setUnmatchedUrls] = useState<UnmatchedResponse | null>(null);
  const apiBase = window.location.origin + "/api";
  const filterSetId = props.filterSetId;
  console.log("filterSetId", filterSetId);

  async function fetchData() {
    const url = apiBase + `/filter_sets/${filterSetId}/`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setFilterSet(data);
    setRules(data.rules);
  }
  useEffect(() => {
    fetchData();
    fetchUnmatchedUrls();
  }, []);

  async function fetchUnmatchedUrls() {
    const url = apiBase + `/filter_sets/${filterSetId}/unmatched`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setUnmatchedUrls(data);
  }

  async function deleteRow(id: number) {
    console.log("delete", id);

    const response = await fetch(`${apiBase}/filter_rules/${id}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': props.csrfToken,
      },
    });
    const data = await response.json();
    console.log(data);

    setRules(rules.filter((rule) => rule.id !== id));
  }

  async function addRowAfter(id: number) {
    console.log("add after", id);
    const filterSetUrl = apiBase + `/filter_sets/${filterSetId}/`;
    console.log("filterSetUrl", filterSetUrl);
    const newRule = {
      // TODO: how to make it so we can use an ID and not a URL?
      "filter_set": filterSetUrl,
      //"filter_set": "1",
      "rule": "https://www.weltderphysik.de/wir",
      "count": 123,
      "include": true,
      "page_type": "New row"
    }
    //setRules([...rules, newRule]);
    // insert after rule with the id
    const post_url = apiBase + "/filter_rules/";
    const response = await fetch(post_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      body: JSON.stringify(newRule),
    });
    const data = await response.json();
    console.log(data);
    // TODO: add ordering
    setRules([...rules, data]);


    //setRules(newRules);
  }

  async function updateFields(id: number, fields: { rule?: string, include?: boolean, page_type?: string}) {
    // Update the fields in the row right away
    const newRules1 = rules.map((rule) => (rule.id === id) ? { ...rule, ...fields } : rule);
    setRules(newRules1);

    // TODO: add a "pending" field to the row, so we can see that the update is in progress

    // // sleep 2 seconds to simulate a bad connection
    // await new Promise(r => setTimeout(r, 2000));

    // call the api
    const url = `${apiBase}/filter_rules/${id}/`;
    const response = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': props.csrfToken,
      },
      // The field names are the same as in the JSON schema,
      // so we can just pass this object here.
      // Typescript hopefully ensures that we don't pass any other fields.
      body: JSON.stringify(fields),
    });
    const updatedRule = await response.json();
    console.log(updatedRule);

    // console.log("update", id, newRuleString);
    // update the state
    const newRules = rules.map((rule) => (rule.id === id) ? updatedRule : rule);
    setRules(newRules);

    // actually we should refresh everything to get the new match counts
    await fetchData();
    await fetchUnmatchedUrls();
  }

  function moveDelta(delta: number) {
    return async (id: number) => {
      // construct the url
      const url = `${apiBase}/filter_rules/${id}/`;
      // call the api
      const old_position = rules.find((rule) => rule.id === id)?.position;
      if (old_position === undefined) {
        console.error("Could not find position of rule with id", id);
        return;
      }
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': props.csrfToken,
        },
        body: JSON.stringify({ position: old_position + delta }),
      });
      const updatedRule = await response.json();
      console.log(updatedRule);
      await fetchData();
    }
  }

  async function showDetails(id: number) {
    console.log("show details", id);
    setSelectedRuleDetails({});
    setDetailsVisible(true);
    // fetch the details
    const url = `${apiBase}/filter_rules/${id}/matches`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);
    setSelectedRuleDetails(data);

  }

  let detailUrls: string[];
  // selectedRuleDetails['new_matches'];
  if (selectedRuleDetails['new_matches'] !== undefined) {
    detailUrls = selectedRuleDetails['new_matches'];
  } else {
    detailUrls = [];
  }

  // iterate over all rules and pick the one with the last id
  let lastId = 0;
  for (let i = 0; i < rules.length; i++) {
    if (rules[i].id > lastId) {
      lastId = rules[i].id;
    }
  }

  return (
    <div>
      <p>{filterSet?.crawl_job.url_count} pages total, {filterSet?.remaining_urls} not handled yet</p>
      <h3>Rules</h3>
      <RuleTable rules={rules}
        onDelete={deleteRow}
        onAdd={addRowAfter}
        onUpdateFields={(id, fields) => { updateFields(id, fields); }}
        onMoveUp={moveDelta(-1)}
        onMoveDown={moveDelta(1)}
        onShowDetails={showDetails}
      />

      <div>
        <button className="mybutton" onClick={() => addRowAfter(lastId)}>Add rule</button>
        <button className="mybutton mybutton-fancy">Suggest rules</button>
      </div>

      {(detailsVisible && 
      <MatchesDialog onClose={() => setDetailsVisible(false)}
        detailUrls={detailUrls}/>)}

      <h3>Unmatched URLs</h3>
      {(unmatchedUrls &&
      <table className="table">
        <thead>
          <tr>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {unmatchedUrls.unmatched_urls.map((url) =>
          <tr key={url}>
            <td>{url}</td>
          </tr>)}
          {!unmatchedUrls.is_complete && <tr>
            <td><i>+ {unmatchedUrls.total_count - unmatchedUrls.unmatched_urls.length} URLs remaining</i></td>
          </tr>}
        </tbody>
      </table>
      )}
      </div>
  );
}

export default App
