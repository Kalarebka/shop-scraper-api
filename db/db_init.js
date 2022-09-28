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
