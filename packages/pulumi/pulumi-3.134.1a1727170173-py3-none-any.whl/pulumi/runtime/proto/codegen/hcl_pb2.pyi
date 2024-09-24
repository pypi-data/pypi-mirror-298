"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2016-2023, Pulumi Corporation.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _DiagnosticSeverity:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _DiagnosticSeverityEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_DiagnosticSeverity.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    DIAG_INVALID: _DiagnosticSeverity.ValueType  # 0
    """DIAG_INVALID is the invalid zero value of DiagnosticSeverity"""
    DIAG_ERROR: _DiagnosticSeverity.ValueType  # 1
    """DIAG_ERROR indicates that the problem reported by a diagnostic prevents
    further progress in parsing and/or evaluating the subject.
    """
    DIAG_WARNING: _DiagnosticSeverity.ValueType  # 2
    """DIAG_WARNING indicates that the problem reported by a diagnostic warrants
    user attention but does not prevent further progress. It is most
    commonly used for showing deprecation notices.
    """

class DiagnosticSeverity(_DiagnosticSeverity, metaclass=_DiagnosticSeverityEnumTypeWrapper):
    """DiagnosticSeverity is the severity level of a diagnostic message."""

DIAG_INVALID: DiagnosticSeverity.ValueType  # 0
"""DIAG_INVALID is the invalid zero value of DiagnosticSeverity"""
DIAG_ERROR: DiagnosticSeverity.ValueType  # 1
"""DIAG_ERROR indicates that the problem reported by a diagnostic prevents
further progress in parsing and/or evaluating the subject.
"""
DIAG_WARNING: DiagnosticSeverity.ValueType  # 2
"""DIAG_WARNING indicates that the problem reported by a diagnostic warrants
user attention but does not prevent further progress. It is most
commonly used for showing deprecation notices.
"""
global___DiagnosticSeverity = DiagnosticSeverity

@typing_extensions.final
class Pos(google.protobuf.message.Message):
    """Pos represents a single position in a source file, by addressing the start byte of a unicode character
    encoded in UTF-8.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LINE_FIELD_NUMBER: builtins.int
    COLUMN_FIELD_NUMBER: builtins.int
    BYTE_FIELD_NUMBER: builtins.int
    line: builtins.int
    """Line is the source code line where this position points. Lines are counted starting at 1 and
    incremented for each newline character encountered.
    """
    column: builtins.int
    """Column is the source code column where this position points, in unicode characters, with counting
    starting at 1.

    Column counts characters as they appear visually, so for example a latin letter with a combining
    diacritic mark counts as one character. This is intended for rendering visual markers against source
    code in contexts where these diacritics would be rendered in a single character cell. Technically
    speaking, Column is counting grapheme clusters as used in unicode normalization.
    """
    byte: builtins.int
    """Byte is the byte offset into the file where the indicated character begins. This is a zero-based offset
    to the first byte of the first UTF-8 codepoint sequence in the character, and thus gives a position
    that can be resolved _without_ awareness of Unicode characters.
    """
    def __init__(
        self,
        *,
        line: builtins.int = ...,
        column: builtins.int = ...,
        byte: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["byte", b"byte", "column", b"column", "line", b"line"]) -> None: ...

global___Pos = Pos

@typing_extensions.final
class Range(google.protobuf.message.Message):
    """Range represents a span of characters between two positions in a source file."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FILENAME_FIELD_NUMBER: builtins.int
    START_FIELD_NUMBER: builtins.int
    END_FIELD_NUMBER: builtins.int
    filename: builtins.str
    """Filename is the name of the file into which this range's positions point."""
    @property
    def start(self) -> global___Pos:
        """Start and End represent the bounds of this range. Start is inclusive and End is exclusive."""
    @property
    def end(self) -> global___Pos: ...
    def __init__(
        self,
        *,
        filename: builtins.str = ...,
        start: global___Pos | None = ...,
        end: global___Pos | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["end", b"end", "start", b"start"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["end", b"end", "filename", b"filename", "start", b"start"]) -> None: ...

global___Range = Range

@typing_extensions.final
class Diagnostic(google.protobuf.message.Message):
    """Diagnostic represents information to be presented to a user about an error or anomaly in parsing or evaluating configuration."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SEVERITY_FIELD_NUMBER: builtins.int
    SUMMARY_FIELD_NUMBER: builtins.int
    DETAIL_FIELD_NUMBER: builtins.int
    SUBJECT_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    severity: global___DiagnosticSeverity.ValueType
    summary: builtins.str
    """Summary and Detail contain the English-language description of the
    problem. Summary is a terse description of the general problem and
    detail is a more elaborate, often-multi-sentence description of
    the problem and what might be done to solve it.
    """
    detail: builtins.str
    @property
    def subject(self) -> global___Range:
        """Subject and Context are both source ranges relating to the diagnostic.

        Subject is a tight range referring to exactly the construct that
        is problematic, while Context is an optional broader range (which should
        fully contain Subject) that ought to be shown around Subject when
        generating isolated source-code snippets in diagnostic messages.
        If Context is nil, the Subject is also the Context.

        Some diagnostics have no source ranges at all. If Context is set then
        Subject should always also be set.
        """
    @property
    def context(self) -> global___Range: ...
    def __init__(
        self,
        *,
        severity: global___DiagnosticSeverity.ValueType = ...,
        summary: builtins.str = ...,
        detail: builtins.str = ...,
        subject: global___Range | None = ...,
        context: global___Range | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["context", b"context", "subject", b"subject"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context", b"context", "detail", b"detail", "severity", b"severity", "subject", b"subject", "summary", b"summary"]) -> None: ...

global___Diagnostic = Diagnostic
