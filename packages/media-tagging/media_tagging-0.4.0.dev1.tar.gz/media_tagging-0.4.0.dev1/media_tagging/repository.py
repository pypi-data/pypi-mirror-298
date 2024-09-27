# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Repository for Tagging results."""

import abc
import os
import pickle
from collections.abc import Sequence

from typing_extensions import override

from media_tagging import utils
from media_tagging.taggers import base


class BaseTaggingResultsRepository(abc.ABC):
  """Interface for defining repositories."""

  @abc.abstractmethod
  def get(self, media_paths: str | Sequence[str]) -> list[base.TaggingResult]:
    """Specifies get operations."""

  @abc.abstractmethod
  def add(
    self, tagging_results: base.TaggingResult | Sequence[base.TaggingResult]
  ) -> None:
    """Specifies add operations."""

  def list(self) -> list[base.TaggingResult]:
    """Returns all tagging results from the repository."""
    return self.results


class PickleTaggingResultsRepository(BaseTaggingResultsRepository):
  """Uses pickle files for persisting tagging results."""

  def __init__(
    self, destination: str | os.PathLike = '/tmp/media_tagging.pickle'
  ) -> None:
    """Initializes PickleTaggingResultsRepository."""
    self.destination = destination
    try:
      with open(self.destination, 'rb') as f:
        self.results = pickle.load(f)
    except Exception:
      self.results = []

  @override
  def get(self, media_paths: Sequence[str]) -> list[base.TaggingResult]:
    converted_media_paths = [
      utils.convert_path_to_media_name(media_path) for media_path in media_paths
    ]
    return [
      result
      for result in self.results
      if result.identifier in converted_media_paths
    ]

  @override
  def add(self, tagging_results: Sequence[base.TaggingResult]) -> None:
    for result in tagging_results:
      self.results.append(result)
    with open(self.destination, 'wb') as f:
      pickle.dump(self.results, f)


class InMemoryTaggingResultsRepository(BaseTaggingResultsRepository):
  """Uses pickle files for persisting tagging results."""

  def __init__(self) -> None:
    """Initializes InMemoryTaggingResultsRepository."""
    self.results = []

  @override
  def get(self, media_paths: Sequence[str]) -> list[base.TaggingResult]:
    converted_media_paths = [
      utils.convert_path_to_media_name(media_path) for media_path in media_paths
    ]
    return [
      result
      for result in self.results
      if result.identifier in converted_media_paths
    ]

  @override
  def add(self, tagging_results: Sequence[base.TaggingResult]) -> None:
    for result in tagging_results:
      self.results.append(result)


class SqlAlchemyTaggingResultsRepository(BaseTaggingResultsRepository):
  """Uses SqlAlchemy engine for persisting tagging results."""

  def __init__(self, session) -> None:
    """Initializes SqlAlchemyTaggingResultsRepository."""
    self.session = session

  def get(self, media_paths: str | Sequence[str]) -> list[base.TaggingResult]:
    """Specifies get operations."""
    ...

  def add(
    self, tagging_results: base.TaggingResult | Sequence[base.TaggingResult]
  ) -> None:
    """Specifies add operations."""
    ...

  def list(self) -> list[base.TaggingResult]:
    """Returns all tagging results from the repository."""
    return self.results
