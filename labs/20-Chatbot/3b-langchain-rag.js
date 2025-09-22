require('dotenv').config();
const { MongoClient } = require('mongodb');
const { OpenAIEmbeddings, ChatOpenAI } = require("@langchain/openai");
// To support the LangChain LCEL RAG chain
const { PromptTemplate } = require("@langchain/core/prompts");
const {
    RunnableSequence,
    RunnablePassthrough,
} = require("@langchain/core/runnables");
const { StringOutputParser } = require("@langchain/core/output_parsers");

const { AzureCosmosDBVectorStore,
    AzureCosmosDBSimilarityType
} = require("@langchain/community/vectorstores/azure_cosmosdb")


// set up the MongoDB client
const dbClient = new MongoClient(process.env.MONGODB_CONNECTION_STRING);
var dbname = process.env.MONGODB_Name;

// set up the Azure Cosmos DB vector store using the initialized MongoDB client
const azureCosmosDBConfig = {
    client: dbClient,
    databaseName: dbname,
    collectionName: "products",
    indexName: "VectorSearchIndex",
    embeddingKey: "contentVector",
    textKey: "_id"
}
const vectorStore = new AzureCosmosDBVectorStore(new OpenAIEmbeddings(), azureCosmosDBConfig);
// set up the OpenAI chat model
const chatModel = new ChatOpenAI();

async function main() {
    try {
        await dbClient.connect();
        console.log("Connected to MongoDB");


    } catch (err) {
        console.error(err);
    } finally {
        await dbClient.close();
        console.log('Disconnected from MongoDB');
    }
}


main().catch(console.error);