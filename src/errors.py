from flask import jsonify


class err:
    """
    Class for creating and formatting errors
    """

    @staticmethod
    def perm(action, db_specification):
        return jsonify(error=f"Permission denied, you have no access to {action} data({db_specification})"), 403

    @staticmethod
    def not_found(db_specification):
        return jsonify(error=f"Data not found in {db_specification}"), 404

    @staticmethod
    def db_add(db_specification):
        return jsonify(error=f"Data has not been added to {db_specification} table"), 500

    @staticmethod
    def db_update(db_specification):
        return jsonify(error=f"Data has not been updated in the {db_specification} table"), 500

    @staticmethod
    def create(error_message, http_code):
        return jsonify(error=error_message), http_code
