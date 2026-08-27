CREATE INDEX IF NOT EXISTS idx_students_room_birthday
ON students (room_id, birthday);

CREATE INDEX IF NOT EXISTS idx_students_room_sex
ON students (room_id, sex);

CREATE INDEX IF NOT EXISTS idx_students_name
ON students (name);

CREATE INDEX IF NOT EXISTS idx_rooms_name
ON rooms (name);