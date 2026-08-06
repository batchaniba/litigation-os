export const ServiceTracker = ({ serviceTracking }) => {
  if (!serviceTracking || serviceTracking.length === 0) return null;

  const servedCount = serviceTracking.filter((s) => s.served).length;
  const totalCount = serviceTracking.length;

  return (
    <section className="service-tracker" aria-label="Service tracker">
      <div className="detail-label">
        Service Tracker ({servedCount}/{totalCount})
      </div>
      <div className="service-tracker-list">
        {serviceTracking.map((defendant, idx) => (
          <div key={idx} className={`service-tracker-row${defendant.served ? " is-served" : ""}`}>
            <div className="service-tracker-check" aria-hidden="true">
              {defendant.served ? "✓" : ""}
            </div>
            <div className="service-tracker-body">
              <div className="service-tracker-name">{defendant.name}</div>
              <div className="service-tracker-meta">
                {defendant.title} · {defendant.location}
              </div>
              {defendant.dateServed && (
                <div className="service-tracker-date">Served: {defendant.dateServed}</div>
              )}
            </div>
            <div className="service-tracker-status">
              {defendant.served ? "Served" : "Pending"}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
