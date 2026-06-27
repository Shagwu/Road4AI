Schedule a Road4AI content post via Blotato.

Draft file: $ARGUMENTS

Steps:
1. Read the draft file at the path given above.
2. Extract the post text (everything after the visual/image prompt block, starting from the first content line).
3. Extract the Blotato image prompt (the paragraph after "**Blotato image prompt:**").
4. Determine the platform from the filename suffix: `-li` = LinkedIn (account 2383), `-x` = X (account 14446), `-ig` = Instagram (account 3879), `-fb` = Facebook (account 3672), `-threads` = Threads (account 1071), `-tt` = TikTok (account 4569).
5. Call `blotato_create_post` with:
   - `accountId`: the account ID for the platform
   - `text`: the extracted post text
   - `imagePrompt`: the extracted image prompt (if present)
6. Report the submission ID.
7. Ask user: "Move draft to archived and update queue?" — wait for yes/no before proceeding.
