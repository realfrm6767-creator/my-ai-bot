from config import SETTINGS_FILE
import json
import os


class Permission:

    @staticmethod
    def load():

        if not os.path.exists(SETTINGS_FILE):

            return {

                "owner": 0,

                "admins": []

            }

        with open(

            SETTINGS_FILE,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    @staticmethod
    def is_owner(user_id):

        data = Permission.load()

        return user_id == data.get("owner", 0)

    @staticmethod
    def is_admin(user_id):

        data = Permission.load()

        return user_id in data.get("admins", [])

    @staticmethod
    def has_panel_access(user_id):

        return (

            Permission.is_owner(user_id)

            or

            Permission.is_admin(user_id)

        )

    @staticmethod
    def save(data):

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    @staticmethod
    def set_owner(user_id):

        data = Permission.load()

        data["owner"] = user_id

        Permission.save(data)

    @staticmethod
    def add_admin(user_id):

        data = Permission.load()

        if user_id not in data["admins"]:

            data["admins"].append(user_id)

            Permission.save(data)

    @staticmethod
    def remove_admin(user_id):

        data = Permission.load()

        if user_id in data["admins"]:

            data["admins"].remove(user_id)

            Permission.save(data)