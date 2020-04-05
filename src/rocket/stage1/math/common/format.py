from . import format_helpers as format

def print_(format_str, dev_mode = False):
  """
  input:
    - format_str: string
      A string for formatting.
    - dev_mode: boolean
      Defines if a user is in developer mode or not. The default is false.
  
  returns:
    - format_: string
      The formatted string.
  """
  try:
    format_ = format.format_(format_str)
  except TypeError as err:
    if dev_mode != True:
      raise TypeError("Your input is anbigous. Is your type a string? More details:\n{}".format(err))
      format_ = "An error occured."
    else:
      raise TypeError("Your input is ambigous. Is your type a string?")
      format_ = "An error occured."
      
  return format_
