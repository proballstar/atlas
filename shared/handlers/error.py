def get_err(dev_mode, err):
    if dev_mode != False:
        if err == "EnvironmentError":
            status_code = 100
        elif err == "AssertionError":
            status_code = 200
        elif err == "SyntaxError":
            status_code = 300
        else:
            status_code = 400

    else:
        status_code = 900  # @TODO(aaronhma): UPDATE to resilient code

    return status_code