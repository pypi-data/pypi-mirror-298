from dataclasses import dataclass
from datetime import datetime
from typing import List

from ngohub.models.core import BaseDataclass
from ngohub.models.locations import City, County
from ngohub.models.nomenclatures import Domain


@dataclass
class OrganizationContact(BaseDataclass):
    email: str
    phone: str
    full_name: str


@dataclass
class OrganizationLegalReprezentative(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    full_name: str
    email: str
    phone: str
    role: str


@dataclass
class OrganizationDirector(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    full_name: str
    email: str
    phone: str
    role: str


@dataclass
class OrganizationReportFile(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    year: int
    status: str


@dataclass
class OrganizationReports(OrganizationReportFile):
    number_of_volunteers: int
    number_of_contractors: int
    report: str


@dataclass
class OrganizationPartners(OrganizationReportFile):
    number_of_partners: int
    path: str


@dataclass
class OrganizationInvestors(OrganizationReportFile):
    number_of_investors: int
    path: str


@dataclass
class OrganizationGeneral(BaseDataclass):
    id: str
    created_on: datetime
    updated_on: datetime
    name: str
    alias: str
    type: str
    email: str
    phone: str
    year_created: str
    cui: str
    association_registry_number: str
    association_registry_part: str
    association_registry_section: str
    association_registry_issuer_id: str
    national_registry_number: str
    raf_number: str
    short_description: str
    description: str
    address: str
    logo: str
    website: str
    facebook: str
    instagram: str
    twitter: str
    linkedin: str
    tiktok: str
    donation_website: str
    redirect_link: str
    donation_sms: str
    donation_keyword: str
    contact: OrganizationContact
    organization_address: str
    city: City
    county: County
    organization_city: str
    organization_county: str
    association_registry_issuer: str


@dataclass
class OrganizationActivity(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    area: str
    is_part_of_federation: bool
    is_part_of_coalition: bool
    is_part_of_international_organization: bool
    international_organization_name: str
    is_social_service_viable: bool
    offers_grants: bool
    is_public_interest_organization: bool
    has_branches: bool
    federations: List[str]
    coalitions: List[str]
    domains: List[Domain]
    cities: List[str]
    branches: List[str]
    regions: List[str]


@dataclass
class OrganizationLegal(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    others: str
    organization_statute: str
    non_political_affiliation_file: str
    balance_sheet_file: str
    legal_reprezentative: OrganizationLegalReprezentative
    directors: List[OrganizationDirector]


@dataclass
class OrganizationFinancial(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    type: str
    number_of_employees: int
    year: int
    total: int
    status: str
    report_status: str
    synced_anaf: bool
    data: str


@dataclass
class OrganizationReport(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    reports: List[OrganizationReports]
    partners: List[OrganizationPartners]
    investors: List[OrganizationInvestors]


@dataclass
class Organization(BaseDataclass):
    id: int
    created_on: datetime
    updated_on: datetime
    status: str
    general_data: OrganizationGeneral
    activity_data: OrganizationActivity
    legal_data: OrganizationLegal
    financial_data: List[OrganizationFinancial]
    report_data: OrganizationReport


@dataclass
class Application(BaseDataclass):
    id: int
    name: str


@dataclass
class OrganizationApplication(Application):
    logo: str
    short_description: str
    login_link: str
    website: str
    status: str
    ngo_status: str
    created_on: datetime
    type: str
    application_label: str
