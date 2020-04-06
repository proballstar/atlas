from . import radiation_test as test_radiation

dev_mode = False

if __name__ == "__main__":
  try:
    test_radiation.test()
  except AssertionError as err:
    if dev_mode != False:
      raise AssertionErrror(err)
    else:
      raise AssertionError("The flight computer has radiation in it. Please reboot it and contact Mission Control.")
