# ----- INSERTS -----
insertUser = \
    "INSERT INTO users (name, password, university, educationgroup, grouprole, avatarurl, email) " \
    "VALUES (%s, %s, %s, %s, %s, %s, %s) " \
    "RETURNING id, name, joineddate, university, educationgroup, grouprole, isconfirmed, avatarurl, email, isadmin"

insertPost = \
    "INSERT INTO posts (title, description, createddate, privacy, author) " \
    "VALUES (%s, %s, NOW(), %s, %s)"

insertEvent = \
    "INSERT INTO events (title, description, date, type, createddate, privacy, author, calendar) " \
    "VALUES (%s, %s, %s, %s, NOW(), %s, %s, %s)"

insertLesson = \
    "INSERT INTO lessons (title, teachername, type, start, \"end\") " \
    "VALUES (%s, %s, %s, %s, %s)"

insertCalendar = \
    "INSERT INTO calendars (title, description, createddate, privacy, author) " \
    "VALUES (%s, %s, NOW(), %s, %s)"

insertSession = \
    "INSERT INTO sessions (userid, token, expires) " \
    "VALUES (%s, %s, %s)"

# ----- SELECTS -----
selectUserByNamePassword = \
    "SELECT id, name, joineddate, university, educationgroup, grouprole, isconfirmed, avatarurl, email, isadmin FROM users " \
    "WHERE name = %s AND password = %s"

selectUserById = \
    "SELECT id, name, joineddate, university, educationgroup, grouprole, isconfirmed, avatarurl, email, isadmin FROM users " \
    "WHERE id = %s"

selectUserPostsById = \
    "SELECT posts.id, title, description, createddate, privacy  FROM posts " \
    "JOIN users ON users.id = posts.author " \
    "WHERE users.id = %s"

selectUserIdBySessionToken = \
    "SELECT userid FROM sessions " \
    "WHERE token = %s"

selectSessionById = \
    "SELECT token, expires FROM sessions " \
    "WHERE userid = %s"

selectUserDataBySessionToken = \
    "SELECT id, name, joineddate, university, educationgroup, grouprole, isconfirmed, avatarurl, email, isadmin FROM sessions " \
    "JOIN users ON sessions.userid = users.id " \
    "WHERE token = %s"

# ----- UPDATES -----
updateUserConfirmationByName = \
    "UPDATE users SET " \
    "university = %s," \
    "educationgroup = %s," \
    "grouprole = %s," \
    "isconfirmed = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserNameByName = \
    "UPDATE users SET " \
    "name = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserAvatarByName = \
    "UPDATE users SET " \
    "avatarurl = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserEmailByName = \
    "UPDATE users SET " \
    "email = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserPasswordByNamePassword = \
    "UPDATE users SET " \
    "password = %s " \
    "WHERE name = %s AND password = %s " \
    "RETURNING id"

updateUserGroupRoleById = \
    "UPDATE users SET " \
    "grouprole = %s " \
    "WHERE id = %s " \
    "RETURNING id"


# ----- DELETES -----
deleteSessionByToken = \
    "DELETE FROM sessions " \
    "WHERE token = %s"
