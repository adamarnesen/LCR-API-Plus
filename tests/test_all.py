import json

import pytest

from lcr.api import API


class Test:
    @classmethod
    def setup_class(cls):
        with open("profile.json") as f:
            profile = json.load(f)

        user = profile["username"]
        password = profile["password"]
        unit_number = profile["unit_number"]
        cls.lcr_api = API(user, password, unit_number)

    def check_keys(self, expected, actual):
        if expected != actual:
            message = "Difference between expected and actual: {}\n".format(
                expected - actual
            )
            message += "Difference between actual and expected: {}\n".format(
                actual - expected
            )
            message += "Actual: {}\n".format(actual)
            assert False, message

    def test_birthday(self):
        birthdays = Test.lcr_api.birthday_list(4, 1)

        birthdays = birthdays[0]["birthdays"]
        assert isinstance(birthdays, list)

        birthday = birthdays[0]
        assert isinstance(birthday, dict)

        expected_keys = {
            "accountable",
            "actualAge",
            "actualAgeInMonths",
            "address",
            "age",
            "birthDate",
            "birthDateFormatted",
            "birthDateSort",
            "birthDayAge",
            "birthDayFormatted",
            "birthDaySort",
            "dayInteger",
            "displayBirthdate",
            "email",
            "formattedMrn",
            "gender",
            "genderCode",
            "genderLabelShort",
            "id",
            "monthInteger",
            "mrn",
            "name",
            "nameOrder",
            "nonMember",
            "notAccountable",
            "outOfUnitMember",
            "phone",
            "priesthood",
            "priesthoodCode",
            "priesthoodType",
            "setApart",
            "spokenName",
            "sustainedDate",
            "unitName",
            "unitNumber",
            "visible",
        }
        actual_keys = set(birthday.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveins(self):
        moveins = Test.lcr_api.members_moved_in(5)
        assert isinstance(moveins, list)

        movein = moveins[0]
        assert isinstance(movein, dict)

        expected_keys = {
            "gender",
            "phone",
            "moveDateCalc",
            "nameOrder",
            "genderLabelShort",
            "priesthood",
            "addressUnknown",
            "birthdate",
            "birthdateCalc",
            "moveDate",
            "unitName",
            "priorUnitNumber",
            "address",
            "id",
            "householdPositionEnum",
            "priorUnitName",
            "moveDateOrder",
            "textAddress",
            "locale",
            "householdUuid",
            "householdPosition",
            "name",
            "age",
        }

        actual_keys = set(movein.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_moveouts(self):
        moveouts = Test.lcr_api.members_moved_out(5)
        assert isinstance(moveouts, list)

        moveout = moveouts[0]
        assert isinstance(moveout, dict)

        expected_keys = {
            "deceased",
            "nextUnitNumber",
            "name",
            "nextUnitName",
            "addressUnknown",
            "moveDate",
            "priorUnit",
            "moveDateOrder",
            "birthDate",
            "nameOrder",
        }
        actual_keys = set(moveout.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_member_list(self):
        member_list = Test.lcr_api.member_list()

        assert isinstance(member_list, list)

        member = member_list[0]
        assert isinstance(member, dict)

        expected_keys = {
            "address",
            "age",
            "birth",
            "convert",
            "email",
            "emails",
            "formattedAddress",
            "householdAnchorPersonUuid",
            "householdMember",
            "houseHoldMemberNameForList",
            "householdNameDirectoryLocal",
            "householdNameFamilyLocal",
            "householdRole",
            "households",
            "householdUuid",
            "isAdult",
            "isHead",
            "isMember",
            "isOutOfUnitMember",
            "isProspectiveElder",
            "isSingleAdult",
            "isSpouse",
            "isYoungSingleAdult",
            "legacyCmisId",
            "member",
            "membershipUnit",
            "mrn",
            "nameFamilyPreferredLocal",
            "nameFormats",
            "nameGivenPreferredLocal",
            "nameListPreferredLocal",
            "nameOrder",
            "outOfUnitMember",
            "personStatusFlags",
            "personUuid",
            "phoneNumber",
            "phones",
            "positions",
            "priesthoodOffice",
            "priesthoodTeacherOrAbove",
            "sex",
            "unitName",
            "unitNumber",
            "unitOrgsCombined",
            "uuid",
            "wamPolicy",
            "youthBasedOnAge",
        }

        actual_keys = set(member.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_recommend_status(self):
        recommend_status = Test.lcr_api.recommend_status()

        assert isinstance(recommend_status, list)

        member = recommend_status[0]
        assert isinstance(member, dict)

        expected_keys = {
            "accountable",
            "actualAge",
            "actualAgeInMonths",
            "age",
            "birthDate",
            "birthDateFormatted",
            "birthDateSort",
            "birthDayFormatted",
            "birthDaySort",
            "email",
            "endowmentDate",
            "expirationDate",
            "formattedMrn",
            "gender",
            "genderCode",
            "genderLabelShort",
            "id",
            "marriageDate",
            "mrn",
            "name",
            "nameOrder",
            "nonMember",
            "notAccountable",
            "notBaptized",
            "outOfUnitMember",
            "phone",
            "priesthood",
            "priesthoodCode",
            "priesthoodType",
            "recommendEditable",
            "recommendStatus",
            "recommendStatusSimple",
            "setApart",
            "spokenName",
            "status",
            "sustainedDate",
            "type",
            "unitName",
            "unitNumber",
            "unordained",
            "visible",
        }

        actual_keys = set(member.keys())
        self.check_keys(expected_keys, actual_keys)

    def test_ministeringApi_RespondWithoutErrors(self):
        ministering = self.lcr_api.ministering()
        assert isinstance(ministering, dict)

    def test_ministeringApi_EldersQuorum_AccountHasAccess(self):
        ministering = self.lcr_api.ministering("EQ")
        access_key = "interviewViewAccess"
        access_expected_value = True
        assert (
            access_key in ministering
        ), f"{access_key} should be in the ministering response."
        assert (
            ministering[access_key] == access_expected_value
        ), f"{access_key} should be {access_expected_value} if your user has access to this resource."

    def test_ministeringApi_EldersQuorum_MatchesStructure(self):
        ministering = self.lcr_api.ministering("EQ")
        elders_key = "elders"
        assert (
            elders_key in ministering
        ), f"key: {elders_key} should be in the ministering response."
        eq = ministering["elders"]
        assert isinstance(eq, list)

    def test_ministeringApi_ReliefSociety_AccountHasAccess(self):
        ministering = self.lcr_api.ministering("RS")
        access_key = "interviewViewAccess"
        access_expected_value = True
        assert (
            access_key in ministering
        ), f"{access_key} should be in the ministering response."
        assert (
            ministering[access_key] == access_expected_value
        ), f"{access_key} should be {access_expected_value} if your user has access to this resource."

    def test_ministeringApi_ReliefSociety_MatchesStructure(self):
        ministering = self.lcr_api.ministering("RS")
        relief_society_key = "reliefSociety"
        assert (
            relief_society_key in ministering
        ), f"key: {relief_society_key} should be in the ministering response."
        eq = ministering["reliefSociety"]
        assert isinstance(eq, list)

    def test_InvalidOrganization_ThrowsValueError(self):
        with pytest.raises(ValueError) as e_info:
            ministering = self.lcr_api.ministering("BADID")
