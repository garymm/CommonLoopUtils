# Copyright 2021 The CLU Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Small utilities by CLU libraries."""

import contextlib
import sys
import time

from absl import logging

import jax.numpy as jnp
import wrapt


@contextlib.contextmanager
def log_activity(activity_name: str):
  """Logs `activity_name` and timing information (or exception)."""
  t0 = time.time()
  logging.info("%s ...", activity_name)
  try:
    yield
  finally:
    dt = time.time() - t0
    exc, *_ = sys.exc_info()
    if exc is not None:
      logging.exception("%s FAILED after %.2fs with %s.", activity_name, dt,
                        exc.__name__)
    else:
      logging.info("%s finished after %.2fs.", activity_name, dt)



def logged_with(activity_name: str):
  """Returns a decorator wrapping a function with `log_activity()`."""
  @wrapt.decorator
  def decorator(wrapped, instance, args, kwargs):
    del instance  # not used
    with log_activity(activity_name):
      return wrapped(*args, **kwargs)
  return decorator


def check_param(value, *, ndim=None, dtype=jnp.float32):
  """Raises a `ValueError` if `value` does not match ndim/dtype.

  Args:
    value: Value to be tested.
    ndim: Expected dimensions.
    dtype: Expected dtype.

  Raises:
    A `ValueError` if `value` does not match `ndim` or `dtype`, or if `value`
    is not an instance of `jnp.ndarray`.
  """
  if not isinstance(value, jnp.ndarray):
    raise ValueError(f"Expected jnp.array, got type={type(value)}")
  if ndim is not None and value.ndim != ndim:
    raise ValueError(f"Expected ndim={ndim}, got ndim={value.ndim}")
  if dtype is not None and value.dtype != dtype:
    raise ValueError(f"Expected dtype={dtype}, got dtype={value.dtype}")
