// USER REACTED (LIKE/REACTION)
MATCH (u:User {user_id: $user_id}), (t {id: $target_id})
MERGE (u)-[:REACTED {type: $target_type, reaction: $reaction, created_at: $created_at}]->(t);

