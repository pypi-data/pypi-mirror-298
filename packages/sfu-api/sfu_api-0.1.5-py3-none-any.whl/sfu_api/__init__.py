from __future__ import annotations

import httpx

from sfu_api.models import (
    CourseNumber,
    CourseNumbers,
    CourseOutline,
    CourseSection,
    CourseSections,
    Department,
    Departments,
    LowerCaseStr,
    Term,
    Terms,
    Year,
    Years,
)

__all__ = ["Client"]

BASE_URL = "http://www.sfu.ca/bin/wcm/course-outlines?"


class Client:
    def __init__(self) -> None:
        self.client = httpx.Client()

    def get_years(self) -> Years:
        response = self.client.get(BASE_URL)
        if response.status_code != 200:
            raise Exception("Failed to fetch years from SFU API")
        years_json = response.json()
        return Years(years_json)

    def get_terms(self, year: Year | LowerCaseStr) -> Terms:
        if isinstance(year, Year):
            year = year.value

        terms_json = self.client.get(f"{BASE_URL}{year}").json()
        return Terms(terms_json)

    def get_departments(
        self, year: Year | LowerCaseStr, term: Term | LowerCaseStr
    ) -> Departments:
        if isinstance(year, Year):
            year = year.value
        if isinstance(term, Term):
            term = term.value

        departments_json = self.client.get(f"{BASE_URL}{year}/{term}").json()
        return Departments(departments_json)

    def get_course_numbers(
        self,
        year: Year | LowerCaseStr,
        term: Term | LowerCaseStr,
        department: Department | LowerCaseStr,
    ) -> CourseNumbers:
        if isinstance(year, Year):
            year = year.value
        if isinstance(term, Term):
            term = term.value
        if isinstance(department, Department):
            department = department.value

        course_numbers_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}"
        ).json()
        return CourseNumbers(course_numbers_json)

    def get_course_sections(
        self,
        year: Year | LowerCaseStr,
        term: Term | LowerCaseStr,
        department: Department | LowerCaseStr,
        course_number: CourseNumber | LowerCaseStr,
    ) -> CourseSections:
        if isinstance(year, Year):
            year = year.value
        if isinstance(term, Term):
            term = term.value
        if isinstance(department, Department):
            department = department.value
        if isinstance(course_number, CourseNumber):
            course_number = course_number.value

        course_section_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}/{course_number}"
        ).json()
        return CourseSections(course_section_json)

    def get_course_outline(
        self,
        year: Year | LowerCaseStr,
        term: Term | LowerCaseStr,
        department: Department | LowerCaseStr,
        course_number: CourseNumber | LowerCaseStr,
        course_section: CourseSection | LowerCaseStr,
    ) -> CourseOutline:
        if isinstance(year, Year):
            year = year.value
        if isinstance(term, Term):
            term = term.value
        if isinstance(department, Department):
            department = department.value
        if isinstance(course_number, CourseNumber):
            course_number = course_number.value
        if isinstance(course_section, CourseSection):
            course_section = course_section.value

        course_outline_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}/{course_number}/{course_section}"
        ).json()
        return CourseOutline(**course_outline_json)
