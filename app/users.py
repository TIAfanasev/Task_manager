

class User:
    id: int
    login: str
    hash_pass: str
    name: str
    role: str

    def check_user_correct(login, password):
        print('Zaglushka')
        return True