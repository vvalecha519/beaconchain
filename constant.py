from dotenv import load_dotenv
import os

load_dotenv()

constants =  {
"BEACON_API_URL": "https://beacon.188xjjhfbd2h98yn4tt3wwb4w.blockchainnodeengine.com",
"BEACON_API_KEY": os.getenv("BEACON_NODE_API_KEY"),
"SUBGRAPH_API_KEY": os.getenv("SUBGRAPH_API_KEY")
}

