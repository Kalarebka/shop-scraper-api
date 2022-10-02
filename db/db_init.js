db.createUser(
    {
        user: "fastapi",
        pwd: "password12345",
        roles: [
            {role: "readWrite",
            db: "shop_scraper"}
        ]
    }
)

db.createCollection("queries")
db.createCollection("offers")

// create index to speed up searches by query sorted by timestamp
db.offers.createIndex({"query": 1, "timestamp": -1})
