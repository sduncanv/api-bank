from pydantic import ValidationError
import json


def try_except(funct):
    def internal_function(*args, **kwargs):
        try:
            return funct(*args, **kwargs)

        except ValidationError as e:
            status = 404
            error = str(e)

        except KeyError as e:
            status = 404
            error = str(e)

        except AttributeError as e:
            status = 404
            error = str(e)

        except ValueError as e:
            status = 404
            error = str(e)

        except Exception as e:
            status = 404
            error = str(e)

        respon = {
            'statusCode': status,
            'body': json.dumps(error),
        }
        return respon

    return internal_function
