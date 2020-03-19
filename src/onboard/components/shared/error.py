
def get_err(dev_mode, err):
    if dev_mode != False:
        e = err
        if e == "EnvironmentError":
            status_code = 100
        elif e == "AssertionError":
            status_code = 200
        elif e == "SyntaxError":
            status_code = 300
        else:
            status_code = 400

    else:
        status_code = 900  # @TODO(aaronhma): UPDATE to resilient code

    return status_code


def status_code(err):
    get_err(True, err)
