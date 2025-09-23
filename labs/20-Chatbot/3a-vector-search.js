
require('dotenv').config();
const { MongoClient } = require('mongodb');
const {
    AzureCosmosDBVectorStore,
    AzureCosmosDBSimilarityType,
} = require("@langchain/community/vectorstores/azure_cosmosdb");
const { OpenAIEmbeddings } = require("@langchain/openai");

const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

async function main() {
    try {
        await dbClient.connect();
        console.log("Connected to MongoDB");

        // set up the Azure Cosmos DB vector store using the initialized MongoDB client


        // perform a vector search using the vector store


    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}

main().catch(console.error);