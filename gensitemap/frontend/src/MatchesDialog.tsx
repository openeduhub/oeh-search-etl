export function MatchesDialog(props: { onClose: () => void; detailUrls: string[]; }) {
  // () => setDetailsVisible(false)
  const { onClose, detailUrls } = props;

  function backdropClick(e: React.MouseEvent) {
    if (e.target == e.currentTarget) {
      e.preventDefault();
      onClose();
    }
  }

  return <div className="mydialog-backdrop" onClick={backdropClick}>
    <div className="mydialog-window">
      <div className="mydialog-titlebar">
        <h2>Details</h2>
        <div><button className='mybutton' onClick={onClose}>X</button></div>
      </div>
      <div className="mydialog-content">
        <p>New URLs matching this rule (and not previous rules):</p>
        <table className="table table-alternating">
          <thead>
            <tr>
              <th>URL</th>
            </tr>
          </thead>
          <tbody>
            {detailUrls.map((url: string) => <tr key={url}><td><a href={url}>{url}</a></td></tr>)}
          </tbody>
        </table>
      </div>
    </div>
  </div>;
}
