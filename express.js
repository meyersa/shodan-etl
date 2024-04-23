const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();

// Get credentials from ENV
const { MONGO_URL, MONGO_DB } = process.env;

// MongoDB options
const options = {
  serverSelectionTimeoutMS: 10000,
};

let ipCollection;

// Attempt to connect before startup (build condition)
(async () => {
  try {
    // Connect to MongoDB
    const client = await MongoClient.connect(MONGO_URL, options);

    // Connect to specified DB
    const db = client.db(MONGO_DB);
    ipCollection = db.collection("ip-information");
    console.log("Connected to MongoDB");
  } catch (e) {
    console.error("Unable to connect to MongoDB, ignore if this was during initial build", e);
    process.exit(1);
  }
})();

app.get('/', async (req, res) => {
  try {
    if (!ipCollection) {
      throw new Error("MongoDB connection not established");
    }

    // Get open ports and their counts, sorted by count
    const openPortsCursor = ipCollection.aggregate([
      { $group: { _id: "$port", count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);
    const openPorts = await openPortsCursor.toArray();

    // Get unique cities and their counts
    const uniqueCitiesCursor = ipCollection.aggregate([
      { $group: { _id: "$city", count: { $sum: 1 } } }
    ]);
    const uniqueCities = await uniqueCitiesCursor.toArray();

    // Get most popular content and its count
    const mostPopularContentCursor = ipCollection.aggregate([
      { $group: { _id: "$data", count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $limit: 1 }
    ]);
    const mostPopularContent = await mostPopularContentCursor.toArray();
    const mostPopularData = mostPopularContent.length > 0 ? mostPopularContent[0] : null;

    // Get the last 3 records
    const lastThreeRecordsCursor = ipCollection.find().sort({ _id: -1 }).limit(3);
    const lastThreeRecords = await lastThreeRecordsCursor.toArray();

    // Prepare statistics
    const statistics = {
      open_ports: openPorts,
      unique_cities: uniqueCities,
      most_popular_content: mostPopularData,
      last_three_records: lastThreeRecords
    };

    // Get the number of bans and no bans
    const bansCursor = ipCollection.countDocuments({ 
      $or: [ 
        { banned: true }, // Check if the document has the "banned" field set to true
        { $or: statistics.last_three_records.map(record => ({ [`ban_${record.ban_id}`]: { $exists: true } })) } // Check for each ban_id property
      ]
    });
    const noBansCursor = ipCollection.countDocuments({ 
      $and: [ 
        { banned: { $ne: true } }, // Check if the document does not have the "banned" field set to true
        { $nor: [ // Ensure none of the ban properties exist
          ...statistics.last_three_records.map(record => ({ [`ban_${record.ban_id}`]: { $exists: true } }))
        ]}
      ]
    });
    const [bansCount, noBansCount] = await Promise.all([bansCursor, noBansCursor]);

    // Render the statistics as HTML on the home page
    res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>IP Information Dashboard</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
      <style>
        body {
          font-family: Arial, sans-serif;
          transition: background-color 0.5s, color 0.5s;
          margin: 0;
          padding: 0;
          background-color: #f5f5f5;
          color: #333;
        }
        .container {
          padding: 1vh 2rem;
        }
        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1vh;
        }
        .statistics h2 {
          margin-top: 2vh;
          margin-bottom: 1vh;
        }
        .statistics ul {
          list-style-type: none;
          padding-left: 0;
        }
        .footer {
          margin-top: 3vh;
          text-align: center;
          padding: 1vh 2rem;
        }
        .dark-mode {
          background-color: #333;
          color: #f5f5f5;
        }
        .dark-mode .theme-switch {
          color: #f5f5f5;
          font-size: 2.5vh;
        }
        a {
          text-decoration: none;
          color: inherit;
        }
        .bar {
          display: flex;
          align-items: center;
          margin-bottom: 1vh;
        }
        .bar span {
          display: inline-block;
          background-color: #ddd;
          color: #333;
          padding: 1vh;
          font-size: 1.2vh; /* Adjusted font size */
          text-align: center;
          vertical-align: middle;
        }
        .bar .bar-fill {
          height: 2vh;
          background-color: #999;
          border-radius: 2vh;
          min-width: 5%; /* Added minimum width */
          margin-left: 1rem;
          margin-right: 1rem;
        }
        .bar span:first-child {
          min-width: 10vh;
        }
        .bar span:last-child {
          margin-right: 2vw;
        }
        .fa-heart, .theme-switch {
          font-size: 2.5vh;
        }
        ul {
          text-overflow: ellipsis;
          max-width: 100dvw;
          overflow: hidden;
        }
        .footer .fa-heart {
          font-size: 2vh;
        }
        .footer a {
          text-decoration: underline;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>IP Information Dashboard</h1>
          <i class="fas fa-sun theme-switch" onclick="toggleDarkMode()"></i>
        </div>
        <div class="statistics">
          <h2>Open Ports and Their Counts:</h2>
          <div class="bars">
            ${statistics.open_ports.map(port => `
              <div class="bar">
                <span>${port._id}</span>
                <div class="bar-fill" style="width: ${(port.count / (statistics.open_ports[0] ? statistics.open_ports[0].count : 1)) * 100}%;"></div>
                <span>${port.count}</span>
              </div>`).join('')}
          </div>
          <h2>Unique Cities and Their Counts:</h2>
          <div class="bars">
            ${statistics.unique_cities.map(city => `
              <div class="bar">
                <span>${city._id}</span>
                <div class="bar-fill" style="width: ${(city.count / (statistics.unique_cities[0] ? statistics.unique_cities[0].count : 1)) * 100}%;"></div>
                <span>${city.count}</span>
              </div>`).join('')}
          </div>
          <h2>Most Popular Content:</h2>
          <div class="bars">
            ${statistics.most_popular_content ? `
              <div class="bar">
                <span>${statistics.most_popular_content._id}</span>
                <div class="bar-fill" style="width: ${(statistics.most_popular_content.count / (statistics.most_popular_content.count + 1)) * 100}%;"></div>
                <span>${statistics.most_popular_content.count}</span>
              </div>` : 'N/A'}
          </div>
          <h2>Bans:</h2>
          <div class="bars">
            ${bansCount !== undefined ? `
              <div class="bar">
                <span>Bans</span>
                <div class="bar-fill" style="width: ${(bansCount / (bansCount + noBansCount || 1)) * 100}%;"></div>
                <span>${bansCount}</span>
              </div>
              <div class="bar">
                <span>No Bans</span>
                <div class="bar-fill" style="width: ${(noBansCount / (bansCount + noBansCount || 1)) * 100}%;"></div>
                <span>${noBansCount}</span>
              </div>` : 'N/A'}
          </div>
          <h2>Last Three Records:</h2>
          <ul>
            ${statistics.last_three_records.map(record => `<li>${JSON.stringify(record)}</li>`).join('')}
          </ul>
        </div>
      </div>
      <div class="footer">
        <p>Source code <a href="https://github.com/meyersa/shodan-etl">GitHub</a> | Assisted with <i class="fas fa-heart" style="font-size: 1.5vh;"></i> by ChatGPT</p>
      </div>
      <script>
        function toggleDarkMode() {
          document.body.classList.toggle('dark-mode');
          const themeSwitch = document.querySelector('.theme-switch');
          themeSwitch.classList.toggle('fa-sun');
          themeSwitch.classList.toggle('fa-moon');
        }
      </script>
    </body>
    </html>
    `);
  } catch (err) {
    console.error("Error retrieving statistics:", err);
    res.status(500).send("<p>Internal Server Error</p>");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
