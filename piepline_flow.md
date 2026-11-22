# How can the data flow
1. Firstly, we need playwright or some other sort of framework/tool to download the messages from CSGO-ID from sites, because of the cloudflare challenges.
2. Then, for each DISTINCT (need to keep a set of CSGO-IDS) steam id player, we look for all of the messages that tere are and do those things:
 - extract all of the messages (raw)
 - extract all of the CSGO ids or steam ids (which is the same at this point)
 - Deduplicate messages (see if the same message has been in the dataset before?)
 - Deduplicate CSGO ids.
 - Those deduplication mechanism can actually work concurently with downloading such as: downloading -> parsing the raw data and for each ID that isn't present in the database/files/hashmap file system (tobedecided) it will be saved to the steam IDS database. Also works for each message, Take the tuple that determines authenticity of one message and compare them with all of messages (it can be done optimally -> just make a hash of this tuple, when there is a match of hash -> look at contents).
 - Then the curated data will go to data/processed. It is important to keep track of the messages timeline, so that one message that came after the other is still in order - important for the transformer.

# Commands for data ingestation:
open -na "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/cs2tracker-chrome-profile"

# Running the main crawler for data ingestation:
uv run python -m src.crawler.crawler