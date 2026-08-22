"""
    1. Necessary queries to the database
    List of rooms and the number of students in each of them
    5 rooms with the smallest average age of students
    5 rooms with the largest difference in the age of students
    List of rooms where different-sex students live

    2. All the “math” should be done at the database level

"""
from database.base import Database


class ReportService:
    def __init__(self, db: Database):
        self._db = db

    def rooms_with_student_count(self) -> list[dict]:
        """List of rooms and the number of students in each of them."""
        query = """
        SELECT r.id AS room_id, r.name AS room_name, COUNT(s.id) AS student_count
        FROM rooms r
        LEFT JOIN students s ON s.room_id = r.id
        GROUP BY r.id, r.name
        ORDER BY r.id;
        """
        return self._db.fetchall(query)

    def top5_rooms_smallest_avg_age(self) -> list[dict]:
        """5 rooms with the smallest average age of students"""
        query = """
        SELECT r.id as room_id, r.name as room_name, AVG(
                DATE_PART(
                    'year',
                    AGE(CURRENT_DATE, st.birthday)
                )
            ) AS avg_age
        FROM rooms r
        JOIN students st ON st.room_id = r.id
        GROUP BY r.id, r.name
        ORDER BY avg_age ASC
        LIMIT 5;
        """
        return self._db.fetchall(query)

    def top5_rooms_largest_age_diff(self) -> list[dict]:
        """5 rooms with the largest difference between oldest and
        youngest student."""
        query = """
        SELECT r.id AS room_id, r.name AS room_name,
            MAX(
                DATE_PART(
                    'year',
                    AGE(CURRENT_DATE, st.birthday)
                )
            )
            -
            MIN(
                DATE_PART(
                    'year',
                    AGE(CURRENT_DATE, st.birthday)
                )
            ) AS age_diff
        FROM rooms r
        JOIN students st ON st.room_id = r.id
        GROUP BY r.id, r.name
        ORDER BY age_diff DESC
        LIMIT 5;
        """
        return self._db.fetchall(query)

    def rooms_with_mixed_sex(self) -> list[dict]:
        """List of rooms where different-sex students live"""
        query = """
            SELECT r.id AS room_id, r.name AS room_name
            FROM rooms r
            JOIN students st ON st.room_id = r.id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT st.sex) > 1
            ORDER BY r.id;
        """
        return self._db.fetchall(query)

    def build_all_reports(self) -> dict[str, list[dict]]:
        return {
            "rooms_with_student_count": self.rooms_with_student_count(),
            "top5_rooms_smallest_avg_age": self.top5_rooms_smallest_avg_age(),
            "top5_rooms_largest_age_diff": self.top5_rooms_largest_age_diff(),
            "rooms_with_mixed_sex": self.rooms_with_mixed_sex(),
        }
