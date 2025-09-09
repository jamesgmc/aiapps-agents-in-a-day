require('dotenv').config();
const { MongoClient } = require('mongodb');

// set up the MongoDB client
const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

async function main() {
    try {
        await dbClient.connect();
        console.log("Connected to MongoDB");

        // TODO: Set up Azure Cosmos DB vector store for LangChain RAG
        // This will be added during the lab exercise

    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}

main().catch(console.error);