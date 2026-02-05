// Initialize MongoDB with elkeid user in elkeid database
// This script runs when the container is first started

db = db.getSiblingDB('elkeid');

// Create the elkeid user with readWrite role on elkeid database
// Note: This runs after MONGO_INITDB_ROOT_USERNAME creates the root user
// but before authentication is enforced on connections
db.createUser({
    user: 'elkeid',
    pwd: 'c596988d134go1qran',
    roles: [
        { role: 'readWrite', db: 'elkeid' },
        { role: 'dbAdmin', db: 'elkeid' }
    ]
});

print('Created elkeid user in elkeid database');