"""Animal shelter adoption register backed by an in-memory SQLite database."""
import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT, "
             "species TEXT, age INTEGER, adopted INTEGER)")


def register_pet(name, species, age, tags=None):
    """Add a pet and return the tags list with its species appended."""
    if tags is None:
        tags = []
    conn.execute("INSERT INTO pets (name, species, age, adopted) "
                 "VALUES (?, ?, ?, 0)", (name, species, age))
    tags.append(species)
    return tags


def adopt(pet_id):
    """Mark the pet with the given id as adopted."""
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))


def adoption_code():
    """Return a random adoption code such as PET-1234."""
    return "PET-" + str(secrets.randbelow(9000) + 1000)


def oldest_available():
    """Return the oldest pet not yet adopted, or None if there is none."""
    row = conn.execute("SELECT name, age FROM pets WHERE adopted = 0 "
                       "ORDER BY age DESC").fetchone()
    if row is None:
        return None
    return row[0]


def clear_unadopted():
    """Delete every pet that has not been adopted."""
    conn.execute("DELETE FROM pets WHERE adopted = 0")


def shelter_status():
    """Return "active" if any pet has been adopted, otherwise "quiet"."""
    adopted = conn.execute(
        "SELECT COUNT(*) FROM pets WHERE adopted = 1").fetchone()[0]
    if adopted > 0:
        return "active"
    return "quiet"


def main():
    """Run a short demonstration of the register."""
    register_pet("Bruno", "dog", 7)
    register_pet("Mitzi", "cat", 3)
    register_pet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldest_available(), adoption_code(), shelter_status())
    clear_unadopted()


if __name__ == "__main__":
    main()
