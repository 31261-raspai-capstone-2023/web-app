CREATE TABLE licence_plates (
    plate varchar(255) NOT NULL,
    first_seen DATETIME DEFAULT (datetime('now','localtime')),
    last_seen DATETIME DEFAULT (datetime('now','localtime')),
    PRIMARY KEY (plate)
);

CREATE TABLE parking_history (
    plate varchar(255) NOT NULL,
    entry_time DATETIME DEFAULT (datetime('now','localtime')),
    exit_time DATETIME DEFAULT NULL,
    PRIMARY KEY (plate, entry_time)
);

CREATE TABLE cameras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location varchar(255) NOT NULL
);

CREATE TABLE location_entries (
    plate varchar(255) NOT NULL,
    camera_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT (datetime('now','localtime')),

    FOREIGN KEY (plate) REFERENCES licence_plates(plate),
    FOREIGN KEY (camera_id) REFERENCES cameras(id)
);


-- -- Adding a camera
-- INSERT INTO cameras (location)
-- VALUES ("B1-G5") -- Basement 1, Green Level, Column 5

-- -- A Car enters the carpark
-- INSERT INTO licence_plates (plate) 
-- VALUES ('DEEZ-NUTS')
-- ON CONFLICT(plate) 
-- DO UPDATE SET last_seen = datetime('now','localtime');

-- INSERT INTO parking_history (plate) VALUES ('DEEZ-NUTS');

-- -- A Car exits the car park
-- UPDATE licence_plates SET last_seen = datetime('now','localtime') WHERE plate = 'DEEZ-NUTS';

-- UPDATE parking_history
-- SET exit_time = datetime('now', 'localtime')
-- WHERE 
--     plate = 'DEEZ-NUTS' AND
--     entry_time = (
--         SELECT MAX(entry_time)
--         FROM parking_history
--         WHERE plate = 'DEEZ-NUTS' AND exit_time IS NULL
--     );

-- -- A camera detects a car parked
-- INSERT INTO location_entries (plate, camera_id)
-- VALUES ('DEEZ-NUTS', 1)

-- -- A user want to get their car
-- SELECT le.plate, le.timestamp, c.location
-- FROM location_entries le
-- JOIN cameras c ON le.camera_id = c.id
-- WHERE le.plate = 'DEEZ-NUTS'
-- ORDER BY le.timestamp DESC
-- LIMIT 1;