import json
import lcr


class Test:
    @classmethod
    def setup_class(cls):
        with open("profile.json") as f:
            profile = json.load(f)

        user = profile["username"]
        password = profile["password"]
        unit_number = profile["unit_number"]
        cls.cd = lcr.API(user, password, unit_number)

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
        birthdays = Test.cd.birthday_list(4, 1)

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
        moveins = Test.cd.members_moved_in(5)
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
        moveouts = Test.cd.members_moved_out(5)
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

    def test_ministering(self):
        ministering = Test.cd.ministering()
        assert isinstance(ministering, dict)

        eq = ministering["elders"]
        assert isinstance(eq, list)

        rs = ministering["reliefSociety"]
        assert isinstance(rs, list)

    def test_member_list(self):
        member_list = Test.cd.member_list()

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
        recommend_status = Test.cd.recommend_status()

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
