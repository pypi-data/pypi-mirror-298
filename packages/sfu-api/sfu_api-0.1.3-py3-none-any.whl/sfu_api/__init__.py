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
        years_json = self.client.get(BASE_URL).json()
        return Years(years_json)

    def get_terms(self, year: Year | str) -> Terms:
        terms_json = self.client.get(f"{BASE_URL}{year}").json()
        return Terms(terms_json)

    def get_departments(self, year: Year | str, term: Term | str) -> Departments:
        departments_json = self.client.get(f"{BASE_URL}{year}/{term}").json()
        return Departments(departments_json)

    def get_course_numbers(
        self, year: Year | str, term: Term | str, department: Department | str
    ) -> CourseNumbers:
        course_numbers_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}"
        ).json()
        return CourseNumbers(course_numbers_json)

    def get_course_sections(
        self,
        year: Year | str,
        term: Term | str,
        department: Department | str,
        course_number: CourseNumber | str,
    ) -> CourseSections:
        course_section_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}/{course_number}"
        ).json()
        return CourseSections(course_section_json)

    def get_course_outline(
        self,
        year: Year | str,
        term: Term | str,
        department: Department | str,
        course_number: CourseNumber | str,
        course_section: CourseSection | str,
    ) -> CourseOutline:
        course_outline_json = self.client.get(
            f"{BASE_URL}{year}/{term}/{department}/{course_number}/{course_section}"
        ).json()
        return CourseOutline(**course_outline_json)
