const express = require("express");
const path = require("path");
const NodeCache = require("node-cache");
const { MongoClient } = require("mongodb");
const { stat } = require("fs");

const app = express();
const cache = new NodeCache();

// Get credentials from ENV
const { MONGO_URL, MONGO_DB } = process.env;

// MongoDB options
const options = {
  serverSelectionTimeoutMS: 10000,
};

// Define our collection variable
let ipCollection;

// Attempt to connect before startup (build condition)
(async () => {
  try {
    // Connect to MongoDB
    console.log("Connecting to MongoDB...");
    const client = await MongoClient.connect(MONGO_URL, options);
    console.log("Connected to MongoDB");

    // Connect to specified DB
    console.log("Connecting to specified database");
    const db = client.db(MONGO_DB);

    console.log("Connecting to specified collection");
    ipCollection = db.collection("ips");

    console.log("Mongo is ready...");
  } catch (e) {
    console.error("Unable to connect to MongoDB, ignore if this was during initial build", e);
    process.exit(1);
  }

  console.log(`Startup finished \n\n\n`)

})();

// Serve the specific CSS file using a custom route
app.get("/express.css", (req, res) => {
  res.sendFile(path.join(__dirname, "express.css"));
});

async function getInfo() {
  console.log("--- Getting Shodan information ---");

  if (!ipCollection) {
    throw new Error("MongoDB connection not established");
  }

  console.log("Getting total document count");
  const totalCountCursor = ipCollection.countDocuments({});
  const totalcount = await totalCountCursor;

  console.log("Getting open ports and counts");
  const openPortsCursor = ipCollection.aggregate([
    {
      $project: {
        data: {
          $objectToArray: "$data",
        },
      },
    },
    {
      $unwind: "$data",
    },
    {
      $group: {
        _id: "$data.v.port",
        count: { $sum: 1 },
      },
    },
    {
      $sort: { count: -1 },
    },
    {
      $limit: 5,
    },
  ]);
  const openPorts = await openPortsCursor.toArray();

  console.log("Getting unique countries and their count");
  const uniqueCountriesCursor = ipCollection.aggregate([
    { $group: { _id: "$location.country", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
  ]);
  const uniqueCountries = await uniqueCountriesCursor.toArray();

  console.log("Getting most popular content and its count");
  const mostPopularContentCursor = ipCollection.aggregate([
    {
      $project: {
        data: {
          $objectToArray: "$data",
        },
      },
    },
    {
      $unwind: "$data",
    },
    {
      $group: {
        _id: "$data.v.data",
        count: { $sum: 1 },
      },
    },
    {
      $sort: { count: -1 },
    },
    {
      $limit: 3,
    },
  ]);
  const mostPopularContent = await mostPopularContentCursor.toArray();

  console.log("Getting last 3 records")
  const lastThreeRecordsCursor = ipCollection.find().sort({ _id: -1 }).limit(3);
  const lastThreeRecords = await lastThreeRecordsCursor.toArray();

  // Filter out null and empty string entries from mostPopularContent
  const validMostPopularContent = mostPopularContent.filter((content) => content._id !== null && content._id !== "");

  // Replace null and empty string with "Null"
  const formattedMostPopularContent = validMostPopularContent.map((content) => ({
    _id: content._id || "Null",
    count: content.count,
  }));

  console.log("Getting the number of bans")
  const bansCursor = ipCollection.countDocuments({
    $or: [
      { banned: true }, // Check if the document has the "banned" field set to true
    ],
  });
  const totalBans = await bansCursor;

  console.log("--- Returning Mongo Statistics ---")
  // Prepare statistics
  return (statistics = {
    total_count: totalcount,
    open_ports: openPorts,
    unique_countries: uniqueCountries,
    most_popular_content: formattedMostPopularContent,
    last_three_records: lastThreeRecords,
    ban_count: totalBans,
  });
}

app.get("/", async (req, res) => {
  try {
    console.log("Returning /")

    var statistics = undefined;

    statistics = cache.get("statistics");

    if (!statistics) {
      console.log("Cache miss")
      statistics = await getInfo();
      cache.set("statistics", statistics, 300);

    } else {
      console.log("Cache hit")

    }

    // Render the statistics as HTML on the home page
    res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Shodan ETL Dashboard</title>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
      <link rel="stylesheet" href="/express.css">
      <script defer data-domain="shodanetl.meyerstk.com" src="https://plausible.meyerstk.com/js/script.js"></script>
    </head>
    <body>
      <div class="header">
        <h1>Shodan ETL Dashboard</h1>
        <i class="fas fa-sun theme-switch" onclick="toggleDarkMode()"></i>
      </div>
      <div class="container">
        <div class="statistics">
          <h2>Top Open Ports:</h2>
          <div class="bars">
            ${statistics.open_ports
              .map(
                (port) => `
              <div class="bar">
                <span>${port._id}</span>
                <div class="bar-fill" style="width: ${
                  (port.count / (statistics.open_ports[0] ? statistics.open_ports[0].count : 1)) * 100
                }%;"></div>
                <span>${port.count}</span>
              </div>`
              )
              .join("")}
          </div>
          <h2>Most Popular Content:</h2>
          <div class="bars">
            ${
              statistics.most_popular_content && statistics.most_popular_content.length > 0
                ? statistics.most_popular_content
                    .slice(0, 3)
                    .map(
                      (content) => `
                    <div class="bar">
                      <span>${content._id === null || content._id === "" ? "Null" : content._id}</span>
                      <div class="bar-fill" style="width: ${
                        (content.count / (statistics.most_popular_content[0].count || 1)) * 100
                      }%;"></div>
                      <span>${content.count}</span>
                    </div>`
                    )
                    .join("")
                : "N/A"
            }
          </div>
          <h2>Top Countries:</h2>
          <div class="bars">
            ${statistics.unique_countries
              .sort((a, b) => b.count - a.count)
              .map(
                (city) => `
              <div class="bar">
                <span>${city._id}</span>
                <div class="bar-fill" style="width: ${
                  (city.count / (statistics.unique_countries[0] ? statistics.unique_countries[0].count : 1)) * 100
                }%;"></div>
                <span>${city.count}</span>
              </div>`
              )
              .join("")}
          </div>
          <h2>Crowdsec Bans:</h2>
          <div class="bars">
            ${
              statistics.ban_count !== undefined
                ? `
                <div class="bar">
                <span>No Bans</span>
                <div class="bar-fill" style="width: ${
                  ((statistics.total_count - statistics.ban_count) /
                    (statistics.ban_count + (statistics.total_count - statistics.ban_count) || 1)) *
                  100
                }%;"></div>
                <span>${statistics.total_count - statistics.ban_count}</span>
              </div>
              <div class="bar">
                <span>Bans</span>
                <div class="bar-fill" style="width: ${
                  (statistics.ban_count /
                    (statistics.ban_count + (statistics.total_count - statistics.ban_count) || 1)) *
                  100
                }%;"></div>
                <span>${statistics.ban_count}</span>
              </div>
                  `
                : "N/A"
            }
          </div>
          <h2>Total Records:</h2>
            <div class="bars">
              <div class="bar">
                <span>${statistics.total_count}</span>
              </div>
            </div>
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
