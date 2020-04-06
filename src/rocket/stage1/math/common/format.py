#
# MIT License
#
# Copyright (c) 2017 - 2020 Firebolt Space Agency,
# Copyright (c) 2017 - 2020 Firebolt, Inc,
# Copyright (C) 2020 - Present Aaron Ma,
# Copyright (c) 2020 - Present Rohan Fernandes.
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
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
