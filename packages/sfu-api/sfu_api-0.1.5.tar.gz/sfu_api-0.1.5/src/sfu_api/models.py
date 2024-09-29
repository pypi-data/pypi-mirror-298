from calendar import Day
from collections.abc import Iterator
from datetime import datetime, time
from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel as PydanticBaseModel
from pydantic import (
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
    field_serializer,
    field_validator,
)
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        frozen=True, alias_generator=to_camel, use_enum_values=True
    )


class SectionCode(StrEnum):
    """
    Enum class representing various section codes for university classes.

    Attributes:
        - CAP - Capstone
        - COP - Co-op
        - FLD - Fieldwork
        - INT - Internship
        - STD - Studio
        - IND - Independent Study
        - LAB - Laboratory
        - LEC - Lecture
        - OLC - Online Course
        - OPL - Open Lab
        - PHF - Physical Education
        - PRA - Practicum
        - SEM - Seminar
        - TUT - Tutorial
        - RQL - Research Qualifying
    """

    CAP = "CAP"
    """Capstone"""
    COP = "COP"
    """Co-op"""
    FLD = "FLD"
    """Fieldwork"""
    INT = "INT"
    """Internship"""
    STD = "STD"
    """Studio"""
    IND = "IND"
    """Independent Study"""
    LAB = "LAB"
    """Laboratory"""
    LEC = "LEC"
    """Lecture"""
    OLC = "OLC"
    """Online Course"""
    OPL = "OPL"
    """Open Lab"""
    PHF = "PHF"
    """Physical Education"""
    PRA = "PRA"
    """Practicum"""
    SEM = "SEM"
    """Seminar"""
    TUT = "TUT"
    """Tutorial"""
    RQL = "RQL"
    """Research Qualifying"""


class CourseSection(BaseModel):
    text: str
    value: str
    # title
    name: Annotated[str | None, Field(alias="title")] = None
    # classType (e=true, n=false)
    enrollment_section: Annotated[bool | None, Field(alias="classType")] = None

    @field_validator("enrollment_section", mode="plain")
    @classmethod
    def validate_enrollment_section(cls, v: str) -> bool:
        match v:
            case "e":
                return True
            case "n":
                return False
            case _:
                raise ValueError("classType must be 'e' or 'n'")

    @field_serializer("enrollment_section", mode="plain")
    @classmethod
    def serialize_enrollment_section(cls, v: bool) -> str:
        return "e" if v else "n"

    # sectionCode
    section_code: SectionCode | None = None
    # associatedClass
    associated_class: int

    def __str__(self) -> str:
        if self.section_code is None:
            return self.text
        return f"{self.text} ({self.section_code})"


class Info(BaseModel):
    notes: str | None = None
    # deliveryMethod
    delivery_method: str | None = None
    description: str | None = None
    section: str | None = None
    units: str | None = None
    title: str | None = None
    type: str | None = None
    # classNumber
    class_number: str | None = None
    # departmentalUgradNotes
    departmental_ugrad_notes: str | None = None
    prerequisites: str | None = None
    number: str | None = None
    # requiredReadingNotes
    required_reading_notes: str | None = None
    # registrarNotes
    registrar_notes: str | None = None
    # outlinePath
    outline_path: str | None = None
    term: str | None = None
    # gradingNotes
    grading_notes: str | None = None
    corequisites: str | None = None
    dept: str | None = None
    # degreeLevel
    degree_level: str | None = None
    # specialTopic
    special_topic: str | None = None
    # courseDetails
    course_details: str | None = None
    name: str | None = None
    designation: str | None = None


class Grade(BaseModel):
    description: str
    weight: float

    @field_validator("weight", mode="plain")
    @classmethod
    def validate_weight(cls, v: str) -> float:
        return float(v) / 100

    @field_serializer("weight", mode="plain")
    @classmethod
    def serialize_weight(cls, v: float) -> str:
        return str(int(v * 100))


class RoleCode(StrEnum):
    """
    Enum class representing either a primary or secondary instructor.

    Attributes:
        PI: Primary Instructor
        SI: Secondary Instructor
    """

    PI = "PI"
    """Primary Instructor"""
    SI = "SI"
    """Secondary Instructor"""


class Instructor(BaseModel):
    profile_url: str
    common_name: str
    first_name: str
    last_name: str
    phone: str | None = None
    role_code: str
    name: str
    office_hours: str | None = None
    office: str | None = None
    email: EmailStr | None = None

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> EmailStr | None:
        if v == "":
            return None

        return v


class Campus(StrEnum):
    """
    Enum class representing various campuses at Simon Fraser University.

    Attributes:
        - BURNABY: Burnaby
        - SURREY: Surrey
        - VANCOUVER: Vancouver
    """

    BURNABY = "Burnaby"
    """Burnaby"""
    SURREY = "Surrey"
    """Surrey"""
    VANCOUVER = "Vancouver"
    """Vancouver"""


DATE_FORMAT = "%a %b %d %H:%M:%S %Z %Y"


class Schedule(BaseModel):
    start_time: time | None = None
    start_date: datetime | None = None
    end_time: time | None = None
    end_date: datetime | None = None
    section_code: SectionCode
    is_exam: bool
    days: list[Day] | None = None

    @field_validator("start_date", "end_date", mode="plain")
    @classmethod
    def parse_datetime(cls, v: str) -> datetime:
        v = v.replace("PDT", "Pacific Daylight Time").replace(
            "PST", "Pacific Standard Time"
        )
        return datetime.strptime(v, DATE_FORMAT)

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, v: str) -> str:
        if len(v) == 4:
            v = "0" + v
        return v

    @field_validator("days", mode="before")
    @classmethod
    def validate_days(cls, v: str) -> list[Day] | None:
        if v == "":
            return None

        def str_to_day(day: str) -> Day:
            match day:
                case "Mo":
                    return Day.MONDAY
                case "Tu":
                    return Day.TUESDAY
                case "We":
                    return Day.WEDNESDAY
                case "Th":
                    return Day.THURSDAY
                case "Fr":
                    return Day.FRIDAY
                case "Sa":
                    return Day.SATURDAY
                case "Su":
                    return Day.SUNDAY
                case _:
                    raise ValueError(f"Invalid day: {day}")

        return list(map(str_to_day, v.split(", ")))

    @field_serializer("days")
    @classmethod
    def serialize_days(cls, v: list[Day]) -> str:
        def day_to_str(day: Day) -> str:
            match day:
                case Day.MONDAY:
                    return "Mo"
                case Day.TUESDAY:
                    return "Tu"
                case Day.WEDNESDAY:
                    return "We"
                case Day.THURSDAY:
                    return "Th"
                case Day.FRIDAY:
                    return "Fr"
                case Day.SATURDAY:
                    return "Sa"
                case Day.SUNDAY:
                    return "Su"

        return ", ".join(map(day_to_str, v))

    campus: Campus | None = None


type HTMLStr = str


class Text(BaseModel):
    details: HTMLStr


def islower(v: str) -> str:
    if v.isalpha():
        assert v.islower(), "must be lower case (try '%s')" % v.lower()
    return v


type LowerCaseStr = Annotated[str, BeforeValidator(islower)]


class TextValue(BaseModel):
    text: str
    value: LowerCaseStr

    @classmethod
    def from_str(cls, value: str) -> Self:
        return cls(text=value, value=value)

    def __str__(self) -> LowerCaseStr:
        return self.value


class Year(TextValue): ...


class Term(TextValue):
    @classmethod
    def from_str(cls, value: str) -> Self:
        return cls(text=value.upper(), value=value.lower())


class NamedTextValue(BaseModel):
    text: str
    value: LowerCaseStr
    name: str

    def __str__(self) -> LowerCaseStr:
        return self.value


class Department(NamedTextValue): ...


class CourseNumber(NamedTextValue):  # name is title
    name: Annotated[str, Field(alias="title")]


class Years(RootModel[list[Year]]):
    root: list[Year]

    def __getitem__(self, index: int) -> Year:
        return self.root[index]

    def __iter__(self) -> Iterator[Year]:  # type: ignore
        return iter(self.root)


class Terms(RootModel[list[Term]]):
    root: list[Term]

    def __getitem__(self, index: int) -> Term:
        return self.root[index]

    def __iter__(self) -> Iterator[Term]:  # type: ignore
        return iter(self.root)


class Departments(RootModel[list[Department]]):
    root: list[Department]

    def __getitem__(self, index: int) -> Department:
        return self.root[index]

    def __iter__(self) -> Iterator[Department]:  # type: ignore
        return iter(self.root)


class CourseNumbers(RootModel[list[CourseNumber]]):
    root: list[CourseNumber]

    def __getitem__(self, index: int) -> CourseNumber:
        return self.root[index]

    def __iter__(self) -> Iterator[CourseNumber]:  # type: ignore
        return iter(self.root)


class CourseSections(RootModel[list[CourseSection]]):
    root: list[CourseSection]

    def __getitem__(self, index: int) -> CourseSection:
        return self.root[index]

    def __iter__(self) -> Iterator[CourseSection]:  # type: ignore
        return iter(self.root)


class CourseOutline(BaseModel):
    info: Info
    grades: list[Grade] | None = None
    instructor: list[Instructor] | None = None
    # courseSchedule
    course_schedule: list[Schedule] | None = None
    # examSchedule
    exam_schedule: list[Schedule] | None = None
    # requiredText
    required_text: list[Text] | None = None
    # recommendedText
    recommended_text: list[Text] | None = None
