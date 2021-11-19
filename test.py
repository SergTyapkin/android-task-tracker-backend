import requests

base_path = "android-task-tracker-backend.herokuapp.com:80"
session = requests.Session()

requests_total = 0


def respInfo(resp):
    global requests_total
    requests_total += 1
    print("#", requests_total, ": ", sep="")
    print(resp.status_code, resp.headers)
    print(resp.content.decode())
    print("---")


def post(path, data):
    respInfo(session.post(base_path + path, data=data))


def put(path, data):
    respInfo(session.put(base_path + path, data=data))


def get(path):
    respInfo(session.get(base_path + path))


def delete(path):
    respInfo(session.delete(base_path + path))


if __name__ == '__main__':
    # Auth user
    post("/user", {
        "name": "Serg",
        "password": "root",
        "university": "МГТУ",
        "educationGroup": "РК6-52Б",
        "groupRole": "student",
        "avatarUrl": "",
        "email": "Tyapki2002@mail.ru",
    })

    get("/user")

    delete("/user/session")

    post("/user/auth", {
        "username": "Sergey",
        "password": "root",
    })

    # Update user
    put("/user/Sergey/email", {"email": "ty@mail.ru"})

    put("/user/Sergey/password", {"oldPassword": "root",
                                  "newPassword": "rootable"})

    put("/user/Sergey/password", {"oldPassword": "rootable",
                                  "newPassword": "root"})



