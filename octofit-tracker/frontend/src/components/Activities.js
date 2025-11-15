const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

function Activities() {
  const [activities, setActivities] = useState([]);

  useEffect(() => {
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Activities endpoint:', API_URL);
        console.log('Fetched activities:', results);
      });
  }, []);

  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title mb-4">Activities</h2>
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-dark">
              <tr>
                <th>#</th>
                <th>Type</th>
                <th>Duration (min)</th>
                <th>Distance (km)</th>
                <th>Timestamp</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((a, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{a.activity_type}</td>
                  <td>{a.duration_minutes}</td>
                  <td>{a.distance_km}</td>
                  <td>{a.timestamp}</td>
                  <td>{a.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Activities;
