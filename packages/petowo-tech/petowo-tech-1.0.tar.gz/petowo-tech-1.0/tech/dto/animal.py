import datetime
from typing import Optional

from core.animal.schema.animal import AnimalSchemaCreate, AnimalSchema
from core.utils.types import Sex, ID, AnimalName, Datetime, Weight, Height, Length

from tech.handlers.input import InputHandler
from tech.utils.exceptions import CancelInput, InvalidFloatInput, InvalidSexInput, InvalidBooleanInput
from tech.utils.lang.langmodel import LanguageModel


class AnimalDTO:
    id: int
    user_id: int
    breed_id: int
    name: str
    birth_dt: datetime.datetime
    sex: str
    weight: float
    height: float
    length: float
    has_defects: bool
    is_multicolor: bool
    input_handler: InputHandler
    lm: LanguageModel

    def __init__(self,
                 id: Optional[int] = None,
                 user_id: Optional[int] = None,
                 breed_id: Optional[int] = None,
                 name: Optional[str] = None,
                 birth_dt: Optional[datetime.datetime] = None,
                 sex: Optional[Sex] = None,
                 weight: Optional[float] = None,
                 height: Optional[float] = None,
                 length: Optional[float] = None,
                 has_defects: Optional[bool] = None,
                 is_multicolor: Optional[bool] = None,
                 input_handler: Optional[InputHandler] = None):
        if input_handler is not None:
            self.input_handler = input_handler
            self.lm = self.input_handler.lang_model
        if id is not None: self.id = id
        if user_id is not None: self.user_id = user_id
        if breed_id is not None: self.breed_id = breed_id
        if birth_dt is not None: self.birth_dt = birth_dt
        if sex is not None: self.sex = self.sex_from_enum(sex)
        if weight is not None: self.weight = weight
        if height is not None: self.height = height
        if length is not None: self.length = length
        if has_defects is not None: self.has_defects = has_defects
        if is_multicolor is not None: self.is_multicolor = is_multicolor
        if name is not None: self.name = name

    def sex_from_enum(self, sex: Sex):
        return self.lm.out_sex_female.lower() if sex == Sex.female else self.lm.out_sex_male.lower()

    def print(self):
        print("_______________________")
        print(f"{self.lm.out_id}:  {self.id}")
        print(f"{self.lm.out_name}: {self.name}")
        print(f"{self.lm.out_breed_id}: {self.breed_id}")
        print(f"{self.lm.out_user_id}: {self.user_id}")
        print(f"{self.lm.out_birth_dt}: {str(self.birth_dt)}")
        print(f"{self.lm.out_sex}: {self.sex}")
        print(f"{self.lm.out_weight}: {self.weight:5.3f} {self.lm.out_weight_unit}")
        print(f"{self.lm.out_height}: {self.height:5.1f} {self.lm.out_height_unit}")
        print(f"{self.lm.out_length}: {self.length:5.1f} {self.lm.out_length_unit}")
        print(f"{self.lm.out_has_defects}: {self.lm.yes if self.has_defects else self.lm.no}")
        print(f"{self.lm.out_is_multicolor}: {self.lm.yes if self.is_multicolor else self.lm.no}")

    def input_id(self):
        id = self.input_handler.wait_positive_int(
            self.lm.question_animal_id,
            self.lm.out_animal_id
        )
        if id is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal id input cancel')
        self.id = id

    def input_delete(self):
        self.input_id()
        return self

    def input_create(self, user_id: int):
        self.id = 0
        self.input_name()
        self.input_breed_id()
        self.input_sex()
        self.input_birth_dt()
        self.input_weight()
        self.input_height()
        self.input_length()
        self.input_has_defects()
        self.input_is_multicolor()
        self.with_user_id(user_id)
        return self

    def input_birth_dt(self):
        birth_dt = self.input_handler.date_input(
            self.lm.out_question_birth_dt
        )
        if birth_dt is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal birth_dt input cancel')
        self.birth_dt = birth_dt

    def with_user_id(self, user_id: int):
        self.user_id = user_id

    def input_breed_id(self):
        breed_id = self.input_handler.wait_positive_int(
            self.lm.question_breed_id,
            self.lm.out_breed_id
        )
        if breed_id is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal breed_id input cancel')
        self.breed_id = breed_id

    def input_name(self):
        name = self.input_handler.wait_input(
            self.lm.question_name,
            self.lm.out_name
        )
        if name is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal name input cancel')
        self.name = name

    def input_weight(self):
        weight = self.input_handler.wait_input(
            self.lm.question_weight,
            self.lm.out_weight
        )
        if weight is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal weight input cancel')
        try:
            self.weight = float(weight)
        except ValueError:
            print(self.lm.input_invalid + f'({self.lm.out_weight.lower()})')
            raise InvalidFloatInput('weight')

    def input_length(self):
        length = self.input_handler.wait_input(
            self.lm.question_length,
            self.lm.out_length
        )
        if length is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal length input cancel')
        try:
            self.length = float(length)
        except ValueError:
            print(self.lm.input_invalid + f'({self.lm.out_length.lower()})')
            raise InvalidFloatInput('length')

    def input_height(self):
        height = self.input_handler.wait_input(
            self.lm.question_height,
            self.lm.out_height
        )
        if height is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal height input cancel')
        try:
            self.height = float(height)
        except ValueError:
            print(self.lm.input_invalid + f'({self.lm.out_height.lower()})')
            raise InvalidFloatInput('height')

    def input_sex(self):
        sex = self.input_handler.wait_input(
            self.lm.question_sex,
            self.lm.out_sex
        )
        if sex is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal sex input cancel')
        if not self.sex_is_male(sex) and not self.sex_is_female(sex):
            print(self.lm.input_invalid + f'({self.lm.out_sex.lower()})')
            raise InvalidSexInput()
        self.sex = sex

    def sex_is_female(self, sex: str):
        return sex.upper() == self.lm.out_sex_female.upper() or sex.upper() == self.lm.out_sex_female_short.upper()

    def sex_is_male(self, sex: str):
        return sex.upper() == self.lm.out_sex_male.upper() or sex.upper() == self.lm.out_sex_male_short.upper()

    def input_has_defects(self):
        has_defects = self.input_handler.wait_input(self.lm.question_has_defects,
                                                    self.lm.out_question_has_defects)
        if has_defects is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal has_defects input cancel')
        if has_defects.upper() != self.lm.yes.upper() and has_defects.upper() != self.lm.no.upper():
            print(self.lm.input_invalid + f'({self.lm.out_has_defects.lower()})')
            raise InvalidBooleanInput('has_defects')
        self.has_defects = True if has_defects.upper() == self.lm.yes.upper() else False

    def input_is_multicolor(self):
        is_multicolor = self.input_handler.wait_input(self.lm.question_is_multicolor,
                                                      self.lm.out_question_is_multicolor)
        if is_multicolor is None:
            print(self.lm.cancel_input)
            raise CancelInput('animal is_multicolor input cancel')
        if is_multicolor.upper() != self.lm.yes.upper() and is_multicolor.upper() != self.lm.no.upper():
            print(self.lm.input_invalid + f'({self.lm.out_is_multicolor.lower()})')
            raise InvalidBooleanInput('is_multicolor')
        self.is_multicolor = True if is_multicolor.upper() == self.lm.yes.upper() else False

    def sex_to_enum(self, sex: str):
        return Sex.female if self.sex_is_female(sex) else Sex.male

    def to_schema_create(self) -> AnimalSchemaCreate:
        return AnimalSchemaCreate(
            user_id=ID(self.user_id),
            breed_id=ID(self.breed_id),
            name=AnimalName(self.name),
            birth_dt=Datetime(self.birth_dt),
            sex=self.sex_to_enum(self.sex),
            weight=Weight(self.weight),
            height=Height(self.height),
            length=Length(self.length),
            has_defects=self.has_defects,
            is_multicolor=self.is_multicolor
        )

    @classmethod
    def from_schema(cls, other: AnimalSchema, input_handler: InputHandler):
        return cls(
            id=other.id.value,
            user_id=other.user_id.value,
            breed_id=other.breed_id.value,
            name=other.name.value,
            birth_dt=other.birth_dt.value,
            sex=other.sex,
            weight=other.weight.value,
            height=other.height.value,
            length=other.length.value,
            has_defects=other.has_defects,
            is_multicolor=other.is_multicolor,
            input_handler=input_handler
        )
